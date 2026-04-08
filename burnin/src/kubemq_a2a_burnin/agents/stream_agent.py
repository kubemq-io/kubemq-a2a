from __future__ import annotations

import asyncio
import json
from typing import Any

from aiohttp import web

from kubemq_a2a_burnin.agents.base import BaseMockAgent


class StreamAgent(BaseMockAgent):
    agent_type = "streaming"

    def __init__(
        self,
        *args: Any,
        events_per_stream: int = 10,
        event_delay_ms: int = 100,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.events_per_stream = events_per_stream
        self.event_delay_ms = event_delay_ms

    async def handle_message_stream(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
        request: web.Request,
    ) -> web.StreamResponse:
        resp = web.StreamResponse(
            status=200,
            headers={"Content-Type": "text/event-stream", "Cache-Control": "no-cache"},
        )
        await resp.prepare(request)

        try:
            for i in range(self.events_per_stream):
                if i < self.events_per_stream - 1:
                    payload = json.dumps(
                        {
                            "type": "status_update",
                            "payload": {
                                "status": "working",
                                "progress": i,
                                "total": self.events_per_stream,
                            },
                        }
                    )
                    await resp.write(
                        f"event: task.status\ndata: {payload}\n\n".encode()
                    )
                else:
                    payload = json.dumps(
                        {
                            "type": "done",
                            "payload": {
                                "final_result": "completed",
                                "event_count": self.events_per_stream,
                            },
                        }
                    )
                    await resp.write(f"event: task.done\ndata: {payload}\n\n".encode())
                await asyncio.sleep(self.event_delay_ms / 1000.0)
        except (ConnectionResetError, ConnectionAbortedError):
            pass

        return resp
