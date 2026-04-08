from __future__ import annotations

from typing import Any

import httpx


class RegistryClient:
    """REST client for KubeMQ agent registry management."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(10.0, connect=5.0),
        )

    async def register(self, card: dict[str, Any]) -> httpx.Response:
        return await self._client.post("/agents/register", json=card)

    async def deregister_post(self, agent_id: str) -> httpx.Response:
        return await self._client.post(
            "/agents/deregister", json={"agent_id": agent_id}
        )

    async def deregister_delete(self, agent_id: str) -> httpx.Response:
        return await self._client.delete(f"/agents/{agent_id}")

    async def heartbeat(self, agent_id: str) -> httpx.Response:
        return await self._client.post("/agents/heartbeat", json={"agent_id": agent_id})

    async def list_agents(self, **params: Any) -> httpx.Response:
        return await self._client.get("/agents", params=params)

    async def get_agent(self, agent_id: str) -> httpx.Response:
        return await self._client.get(f"/agents/{agent_id}")

    async def get_platform_card(self) -> httpx.Response:
        return await self._client.get("/.well-known/agent-card.json")

    async def get_agent_card(self, agent_id: str) -> httpx.Response:
        return await self._client.get(f"/a2a/{agent_id}/.well-known/agent-card.json")

    async def close(self) -> None:
        await self._client.aclose()
