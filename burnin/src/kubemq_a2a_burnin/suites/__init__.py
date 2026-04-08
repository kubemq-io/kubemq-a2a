from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kubemq_a2a_burnin.agents.manager import AgentManager
    from kubemq_a2a_burnin.config import BurninConfig
    from kubemq_a2a_burnin.metrics.tracker import TestTracker
    from kubemq_a2a_burnin.suites.base import BaseSuite


def get_suite_runner(
    name: str,
    config: "BurninConfig",
    agent_manager: "AgentManager",
    tracker: "TestTracker",
) -> "BaseSuite":
    from kubemq_a2a_burnin.suites.a2a_registry import A2ARegistrySuite
    from kubemq_a2a_burnin.suites.a2a_sync import A2ASyncSuite
    from kubemq_a2a_burnin.suites.a2a_streaming import A2AStreamingSuite
    from kubemq_a2a_burnin.suites.a2a_errors import A2AErrorsSuite
    from kubemq_a2a_burnin.suites.a2a_limits import A2ALimitsSuite
    from kubemq_a2a_burnin.suites.a2a_soak import A2ASoakSuite

    registry = {
        "a2a_registry": A2ARegistrySuite,
        "a2a_sync": A2ASyncSuite,
        "a2a_streaming": A2AStreamingSuite,
        "a2a_errors": A2AErrorsSuite,
        "a2a_limits": A2ALimitsSuite,
        "a2a_soak": A2ASoakSuite,
    }

    cls = registry.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown suite '{name}'. Valid: {', '.join(sorted(registry))}"
        )
    return cls(config, agent_manager, tracker)
