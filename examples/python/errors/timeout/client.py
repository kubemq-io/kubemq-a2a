"""Timeout example — sends a request with a 1-second timeout to a slow agent."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "slow-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": "This will timeout"}]},
            "configuration": {"timeout": 1},
        },
    }

    async with httpx.AsyncClient(timeout=30) as client:
        print("Sending request with timeout=1 to slow agent (5s delay)...")
        resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
        data = resp.json()
        print(json.dumps(data, indent=2))

        error = data.get("error", {})
        print(f"\nError code:    {error.get('code')}")
        print(f"Error message: {error.get('message')}")

        assert error.get("code") == -32001, f"Expected -32001, got {error.get('code')}"
        print("\nTimeout error (-32001) received as expected!")


if __name__ == "__main__":
    asyncio.run(main())
