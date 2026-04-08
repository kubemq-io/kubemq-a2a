from __future__ import annotations

from typing import Any

from kubemq_a2a_burnin.agents.base import BaseMockAgent


class EchoAgent(BaseMockAgent):
    agent_type = "echo"

    async def handle_message_send(
        self, body: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        return {
            "echo": body,
            "received_headers": {
                k: v for k, v in headers.items() if k.lower().startswith("x-")
            },
        }
