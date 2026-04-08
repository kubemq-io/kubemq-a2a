"""Deregister-Agent example — demonstrates both deregistration methods."""

import asyncio

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "deregister-agent-01"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print("=== Verify agent exists ===")
        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"GET /agents/{AGENT_ID}: {resp.status_code}")

        print("\n=== Deregister via POST ===")
        resp = await client.post(
            f"{KUBEMQ_URL}/agents/deregister",
            json={"agent_id": AGENT_ID},
        )
        print(f"POST /agents/deregister: {resp.status_code}")

        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"GET /agents/{AGENT_ID} after deregister: {resp.status_code}")

        print("\n=== Re-register for DELETE test ===")
        card = {
            "agent_id": AGENT_ID,
            "name": "Deregister Test Agent",
            "url": "http://localhost:18080/",
            "skills": [],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        resp = await client.post(f"{KUBEMQ_URL}/agents/register", json=card)
        print(f"Re-registered: {resp.status_code}")

        print("\n=== Deregister via DELETE ===")
        resp = await client.delete(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"DELETE /agents/{AGENT_ID}: {resp.status_code}")

        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        print(f"GET /agents/{AGENT_ID} after delete: {resp.status_code}")

        print("\nBoth deregistration methods demonstrated successfully!")


if __name__ == "__main__":
    asyncio.run(main())
