"""Invalid-Request example — sends various malformed JSON-RPC payloads."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "echo-agent-01"


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print("=== Test 1: Invalid JSON ===")
        resp = await client.post(
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            content=b"{invalid json!!!}",
            headers={"Content-Type": "application/json"},
        )
        data = resp.json()
        error = data.get("error", {})
        print(f"  Code: {error.get('code')} (expected -32700)")
        print(f"  Message: {error.get('message')}")

        print("\n=== Test 2: Missing method field ===")
        resp = await client.post(
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            json={"jsonrpc": "2.0", "id": 1, "params": {}},
        )
        data = resp.json()
        error = data.get("error", {})
        print(f"  Code: {error.get('code')} (expected -32600)")
        print(f"  Message: {error.get('message')}")

        print("\n=== Test 3: Bad jsonrpc version ===")
        resp = await client.post(
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            json={"jsonrpc": "1.0", "id": 1, "method": "message/send", "params": {}},
        )
        data = resp.json()
        error = data.get("error", {})
        print(f"  Code: {error.get('code')} (expected -32600)")
        print(f"  Message: {error.get('message')}")

        print("\nAll invalid request errors demonstrated!")


if __name__ == "__main__":
    asyncio.run(main())
