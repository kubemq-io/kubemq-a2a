from __future__ import annotations

import json
import logging
from collections import deque
from typing import Any

from aiohttp import web

logger = logging.getLogger(__name__)

_REQUEST_LOG_MAX = 1000


class BaseMockAgent:
    """Base class for all mock agents. Each agent is an in-process aiohttp HTTP server
    implementing JSON-RPC 2.0 that KubeMQ's virtual subscriber will POST to.
    """

    agent_type: str = "base"

    def __init__(
        self,
        agent_id: str,
        name: str,
        port: int,
        skills: list[dict[str, Any]] | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.name = name
        self.port = port
        self.url = f"http://localhost:{port}/"
        self.skills = skills or [
            {
                "id": self.agent_type,
                "name": self.agent_type.title(),
                "description": f"{self.agent_type} agent",
                "tags": ["test", self.agent_type],
            }
        ]
        self.request_log: deque[dict[str, Any]] = deque(maxlen=_REQUEST_LOG_MAX)
        self._app: web.Application | None = None
        self._runner: web.AppRunner | None = None

    async def start(self) -> None:
        self._app = web.Application()
        self._app.router.add_post("/", self._handle_request)
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "0.0.0.0", self.port)
        await site.start()
        logger.info("Mock agent %s started on port %d", self.agent_id, self.port)

    async def stop(self) -> None:
        if self._runner:
            await self._runner.cleanup()
            logger.info("Mock agent %s stopped", self.agent_id)

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
        request_id = body.get("id")

        if method == "message/stream":
            return await self.handle_message_stream(body, headers, request)
        elif method == "stream_cancel":
            result = await self.handle_stream_cancel(body)
            return web.json_response(
                {"jsonrpc": "2.0", "id": request_id, "result": result}
            )
        else:
            result = await self.handle_message_send(body, headers)
            return web.json_response(
                {"jsonrpc": "2.0", "id": request_id, "result": result}
            )

    async def handle_message_send(
        self, body: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        return {"status": "ok"}

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
        await resp.write(b'event: task.done\ndata: {"type": "done", "payload": {}}\n\n')
        return resp

    async def handle_stream_cancel(self, body: dict[str, Any]) -> dict[str, Any]:
        return {"status": "cancelled"}

    def registration_card(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": f"{self.agent_type} agent for burn-in testing",
            "version": "1.0.0",
            "url": self.url,
            "skills": self.skills,
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
