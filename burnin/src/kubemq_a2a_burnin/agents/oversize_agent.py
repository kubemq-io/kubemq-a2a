from __future__ import annotations

import json
from typing import Any

from aiohttp import web

from kubemq_a2a_burnin.agents.base import BaseMockAgent


class OversizeAgent(BaseMockAgent):
    agent_type = "oversize"

    def __init__(
        self, *args: Any, response_size_bytes: int = 20_971_520, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.response_size_bytes = response_size_bytes
        self._payload = "X" * response_size_bytes

    async def _handle_request(self, request: web.Request) -> web.Response | web.StreamResponse:
        try:
            body = await request.json()
        except json.JSONDecodeError:
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None,
                },
                status=200,
            )

        if not isinstance(body, dict):
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {"code": -32600, "message": "Invalid request: body must be a JSON object"},
                    "id": None,
                },
                status=200,
            )

        self.request_log.append({"body": body, "headers": dict(request.headers)})

        method = body.get("method", "")
        if method == "message/stream":
            return await self.handle_message_stream(body, dict(request.headers), request)
        if method == "stream_cancel":
            result = await self.handle_stream_cancel(body)
            return web.json_response(
                {"jsonrpc": "2.0", "id": body.get("id"), "result": result}
            )

        return web.Response(
            text=self._payload,
            status=200,
            content_type="text/plain",
        )
