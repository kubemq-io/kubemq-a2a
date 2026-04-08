from __future__ import annotations

import logging
from typing import Any, AsyncIterator

import httpx
from httpx_sse import aconnect_sse

logger = logging.getLogger(__name__)

_JSONRPC_VERSION = "2.0"


class A2AClient:
    """Raw httpx client for A2A JSON-RPC 2.0 endpoints."""

    def __init__(self, base_url: str, timeout: float = 60.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _jsonrpc_payload(
        self, method: str, params: dict[str, Any] | None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "jsonrpc": _JSONRPC_VERSION,
            "id": self._next_id(),
            "method": method,
        }
        if params:
            payload["params"] = params
        return payload

    async def send(
        self,
        agent_id: str,
        method: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Send a JSON-RPC 2.0 request to an A2A agent."""
        payload = self._jsonrpc_payload(method, params)

        kwargs: dict[str, Any] = {
            "json": payload,
            "headers": {**(headers or {})},
        }
        if timeout is not None:
            kwargs["timeout"] = timeout + 15.0

        resp = await self._client.post(f"/a2a/{agent_id}", **kwargs)
        resp.raise_for_status()
        try:
            data = resp.json()
        except Exception:
            return {"error": {"code": -1, "message": f"Non-JSON response: {resp.text[:200]}"}}
        if not isinstance(data, dict):
            return {"error": {"code": -1, "message": f"Expected JSON object, got {type(data).__name__}"}}
        return data

    async def send_raw(
        self,
        agent_id: str,
        body: bytes | str,
        content_type: str = "application/json",
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send raw bytes to A2A endpoint (for error testing)."""
        hdrs = {"Content-Type": content_type, **(headers or {})}
        return await self._client.post(f"/a2a/{agent_id}", content=body, headers=hdrs)

    async def stream(
        self,
        agent_id: str,
        method: str = "message/stream",
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Open an SSE stream to an A2A agent via POST."""
        payload = self._jsonrpc_payload(method, params)

        async with aconnect_sse(
            self._client,
            "POST",
            f"/a2a/{agent_id}",
            json=payload,
            headers=headers or {},
        ) as event_source:
            async for sse in event_source.aiter_sse():
                yield {"event": sse.event, "data": sse.data}

    async def stream_get(
        self,
        agent_id: str,
        headers: dict[str, str] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Open an SSE stream via GET /a2a/{agent_id}/stream."""
        async with aconnect_sse(
            self._client,
            "GET",
            f"/a2a/{agent_id}/stream",
            headers=headers or {},
        ) as event_source:
            async for sse in event_source.aiter_sse():
                yield {"event": sse.event, "data": sse.data}

    async def get(self, path: str) -> httpx.Response:
        """Send a GET request to an arbitrary path."""
        return await self._client.get(path)

    async def close(self) -> None:
        await self._client.aclose()
