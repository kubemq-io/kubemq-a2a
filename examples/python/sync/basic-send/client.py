"""Basic-Send example — sends a message/send JSON-RPC request through KubeMQ."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "echo-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "parts": [{"text": "Hello, agent!"}],
            },
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            json=payload,
        )
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2))

        assert "result" in data
        print("\nBasic send completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
