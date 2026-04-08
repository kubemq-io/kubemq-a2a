from __future__ import annotations

import asyncio
from typing import Any

from kubemq_a2a_burnin.agents.base import BaseMockAgent


class SlowAgent(BaseMockAgent):
    agent_type = "slow"

    def __init__(self, *args: Any, delay_ms: int = 2000, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.delay_ms = delay_ms

    async def handle_message_send(
        self, body: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        await asyncio.sleep(self.delay_ms / 1000.0)
        return {"status": "ok", "delayed_ms": self.delay_ms}
