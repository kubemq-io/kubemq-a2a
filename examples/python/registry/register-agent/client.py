"""Register-Agent example — verifies agent registration via the registry API."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "echo-agent-01"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2))

        assert data["agent_id"] == AGENT_ID
        assert "registered_at" in data
        print("\nAgent registration verified successfully!")


if __name__ == "__main__":
    asyncio.run(main())
