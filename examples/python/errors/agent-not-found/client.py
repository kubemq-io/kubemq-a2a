"""Agent-Not-Found example — sends a request to a nonexistent agent."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "nonexistent-agent"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": "Hello?"}]},
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
        data = resp.json()
        print(json.dumps(data, indent=2))

        error = data.get("error", {})
        print(f"\nError code:    {error.get('code')}")
        print(f"Error message: {error.get('message')}")

        assert error.get("code") == -32002, f"Expected -32002, got {error.get('code')}"
        print("\nAgent-not-found error (-32002) received as expected!")


if __name__ == "__main__":
    asyncio.run(main())
