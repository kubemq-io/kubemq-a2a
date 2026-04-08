"""Heartbeat example — sends periodic heartbeats and shows last_seen updates."""

import asyncio

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "heartbeat-agent-01"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        for i in range(1, 4):
            resp = await client.post(
                f"{KUBEMQ_URL}/agents/heartbeat",
                json={"agent_id": AGENT_ID},
            )
            data = resp.json()
            print(f"Heartbeat {i}: status={resp.status_code} last_seen={data.get('last_seen')}")
            if i < 3:
                await asyncio.sleep(2)

        print("\n=== Final agent state ===")
        resp = await client.get(f"{KUBEMQ_URL}/agents/{AGENT_ID}")
        data = resp.json()
        print(f"registered_at: {data.get('registered_at')}")
        print(f"last_seen:     {data.get('last_seen')}")
        print("\nHeartbeat cycle completed!")


if __name__ == "__main__":
    asyncio.run(main())
