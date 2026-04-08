from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from kubemq_a2a_burnin.agents.manager import AgentManager
from kubemq_a2a_burnin.clients.a2a_client import A2AClient
from kubemq_a2a_burnin.clients.metrics_client import MetricsClient
from kubemq_a2a_burnin.clients.registry_client import RegistryClient
from kubemq_a2a_burnin.config import BurninConfig
from kubemq_a2a_burnin.metrics.tracker import TestResult, TestTracker

logger = logging.getLogger(__name__)


class BaseSuite:
    """Base class for all A2A burn-in test suites."""

    suite_name: str = "base"

    def __init__(
        self, config: BurninConfig, agent_manager: AgentManager, tracker: TestTracker
    ) -> None:
        self.config = config
        self.agent_manager = agent_manager
        self.tracker = tracker
        self.a2a = A2AClient(config.server.address)
        self.registry = RegistryClient(config.server.address)
        self.metrics = MetricsClient(config.server.metrics_address)

    async def run(self, filter_ids: set[str] | None = None) -> None:
        logger.info("Running suite: %s", self.suite_name)
        try:
            tests = self.get_tests()
            for test_id, test_name, test_fn in tests:
                if filter_ids is not None and test_id not in filter_ids:
                    continue
                await self._run_test(test_id, test_name, test_fn)
        finally:
            await self.a2a.close()
            await self.registry.close()
            await self.metrics.close()

    def get_tests(self) -> list[tuple[str, str, Any]]:
        raise NotImplementedError

    async def _run_test(
        self, test_id: str, test_name: str, test_fn: Callable[[], Awaitable[int]]
    ) -> None:
        start = time.time()
        try:
            assertions = await test_fn()
            elapsed_ms = (time.time() - start) * 1000
            self.tracker.record(
                TestResult(
                    id=test_id,
                    name=test_name,
                    suite=self.suite_name,
                    status="passed",
                    duration_ms=elapsed_ms,
                    assertions=assertions or 1,
                    error=None,
                )
            )
            logger.info("  PASS %s: %s (%.0fms)", test_id, test_name, elapsed_ms)
        except Exception as exc:
            elapsed_ms = (time.time() - start) * 1000
            self.tracker.record(
                TestResult(
                    id=test_id,
                    name=test_name,
                    suite=self.suite_name,
                    status="failed",
                    duration_ms=elapsed_ms,
                    assertions=0,
                    error=str(exc),
                )
            )
            logger.error(
                "  FAIL %s: %s - %s (%.0fms)", test_id, test_name, exc, elapsed_ms
            )
