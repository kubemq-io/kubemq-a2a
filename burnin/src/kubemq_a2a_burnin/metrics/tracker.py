from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Literal


@dataclass
class TestResult:
    id: str
    name: str
    suite: str
    status: Literal["passed", "failed", "skipped"]
    duration_ms: float
    assertions: int
    error: str | None


class TestTracker:
    """Thread-safe test result accumulator."""

    def __init__(self) -> None:
        self._results: list[TestResult] = []
        self._lock = threading.Lock()

    def record(self, result: TestResult) -> None:
        with self._lock:
            self._results.append(result)

    @property
    def results(self) -> list[TestResult]:
        with self._lock:
            return list(self._results)

    @property
    def passed(self) -> int:
        with self._lock:
            return sum(1 for r in self._results if r.status == "passed")

    @property
    def failed(self) -> int:
        with self._lock:
            return sum(1 for r in self._results if r.status == "failed")

    @property
    def skipped(self) -> int:
        with self._lock:
            return sum(1 for r in self._results if r.status == "skipped")

    @property
    def total(self) -> int:
        with self._lock:
            return len(self._results)
