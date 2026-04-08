"""Response-Size example — requests a response larger than the 10MB limit."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "oversize-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": "Give me a large response"}]},
        },
    }

    async with httpx.AsyncClient(timeout=30) as client:
        print("Requesting oversized response (>10MB)...")
        resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
        data = resp.json()

        if "error" in data:
            error = data["error"]
            print(f"\nError code:    {error.get('code')}")
            print(f"Error message: {error.get('message')}")
            print("\nResponse size limit enforced!")
        else:
            print(f"\nStatus: {resp.status_code}")
            print("Note: Response was accepted (check KubeMQ size limit configuration)")


if __name__ == "__main__":
    asyncio.run(main())
