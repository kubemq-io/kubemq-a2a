from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from kubemq_a2a_burnin.agents.manager import AgentManager
from kubemq_a2a_burnin.config import BurninConfig
from kubemq_a2a_burnin.metrics.tracker import TestTracker
from kubemq_a2a_burnin.suites import get_suite_runner

logger = logging.getLogger(__name__)

_SMOKE_SUITES = ["a2a_registry", "a2a_sync"]
_SMOKE_SYNC_TESTS = {"S01", "S04", "S07"}

_FUNCTIONAL_SUITES = [
    "a2a_registry",
    "a2a_sync",
    "a2a_streaming",
    "a2a_errors",
    "a2a_limits",
]

_SOAK_SUITES = _FUNCTIONAL_SUITES + ["a2a_soak"]


class Runner:
    """Orchestrates suite execution based on run mode."""

    def __init__(self, config: BurninConfig) -> None:
        self.config = config
        self.tracker = TestTracker()
        self.agent_manager = AgentManager(config)
        self._fatal = False

    def _get_suites_for_mode(self) -> list[str]:
        if self.config.mode == "smoke":
            candidates = _SMOKE_SUITES
        elif self.config.mode == "functional":
            candidates = _FUNCTIONAL_SUITES
        else:
            candidates = _SOAK_SUITES
        return [
            s for s in candidates
            if getattr(self.config.suites, s, True)
        ]

    async def run(self) -> int:
        start_time = time.time()
        suite_names = self._get_suites_for_mode()
        logger.info(
            "Starting burn-in  mode=%s  suites=%s  run_id=%s",
            self.config.mode,
            suite_names,
            self.config.run_id,
        )

        try:
            await self.agent_manager.create_all()
            await self.agent_manager.start_all()
            await self.agent_manager.register_all()

            for name in suite_names:
                suite = get_suite_runner(
                    name, self.config, self.agent_manager, self.tracker
                )
                if self.config.mode == "smoke" and name == "a2a_sync":
                    await suite.run(filter_ids=_SMOKE_SYNC_TESTS)
                else:
                    await suite.run()

        except Exception as exc:
            logger.error("Fatal error during burn-in: %s", exc, exc_info=True)
            self._fatal = True
        finally:
            await self.agent_manager.cleanup()

        elapsed = time.time() - start_time
        self._print_summary(elapsed)

        if self.config.output.report_file:
            await asyncio.to_thread(self._write_report, elapsed)

        if self._fatal:
            return 1
        return 0 if self.tracker.failed == 0 else 1

    def _print_summary(self, elapsed_s: float) -> None:
        total = self.tracker.total
        passed = self.tracker.passed
        failed = self.tracker.failed
        verdict = "PASSED" if failed == 0 and not self._fatal else "FAILED"
        logger.info(
            "Burn-in complete: %s  total=%d passed=%d failed=%d  elapsed=%.1fs",
            verdict,
            total,
            passed,
            failed,
            elapsed_s,
        )
        if failed > 0:
            for r in self.tracker.results:
                if r.status == "failed":
                    logger.error("  FAILED: %s %s — %s", r.id, r.name, r.error)

    def _write_report(self, elapsed_s: float) -> None:
        report: dict[str, Any] = {
            "run_id": self.config.run_id,
            "mode": self.config.mode,
            "elapsed_seconds": round(elapsed_s, 1),
            "total": self.tracker.total,
            "passed": self.tracker.passed,
            "failed": self.tracker.failed,
            "verdict": "PASSED" if self.tracker.failed == 0 and not self._fatal else "FAILED",
            "results": [
                {
                    "id": r.id,
                    "name": r.name,
                    "suite": r.suite,
                    "status": r.status,
                    "duration_ms": round(r.duration_ms, 1),
                    "assertions": r.assertions,
                    "error": r.error,
                }
                for r in self.tracker.results
            ],
        }
        try:
            with open(self.config.output.report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            logger.info("Report written to %s", self.config.output.report_file)
        except OSError as exc:
            logger.error("Failed to write report: %s", exc)
