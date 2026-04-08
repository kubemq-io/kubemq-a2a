from __future__ import annotations

import json
import random
from typing import Any

from aiohttp import web

from kubemq_a2a_burnin.agents.base import BaseMockAgent


class ErrorAgent(BaseMockAgent):
    """Agent that returns HTTP error status codes based on error_rate probability.

    Overrides ``_handle_request`` (not ``handle_message_send``) per spec M-9 so that
    the error HTTP status code is set directly on the response.
    """

    agent_type = "error"

    def __init__(self, *args: Any, error_rate: float = 1.0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.error_rate = error_rate
        self._error_status_codes = [400, 500, 502, 503, 504]
        self._error_index = 0

    async def _handle_request(
        self, request: web.Request
    ) -> web.Response | web.StreamResponse:
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

        headers = dict(request.headers)
        self.request_log.append({"body": body, "headers": headers})

        method = body.get("method", "")

        if method == "message/stream":
            return await self.handle_message_stream(body, headers, request)
        if method == "stream_cancel":
            result = await self.handle_stream_cancel(body)
            return web.json_response(
                {"jsonrpc": "2.0", "id": body.get("id"), "result": result}
            )

        if random.random() < self.error_rate:
            status = self._error_status_codes[
                self._error_index % len(self._error_status_codes)
            ]
            self._error_index += 1
            return web.json_response(
                {"error": f"Simulated error with status {status}"},
                status=status,
            )
        result = await self.handle_message_send(body, headers)
        return web.json_response(
            {"jsonrpc": "2.0", "id": body.get("id"), "result": result}
        )
