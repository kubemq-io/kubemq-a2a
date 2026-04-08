"""Custom-Method example — sends a custom/action JSON-RPC method."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "custom-method-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "custom/action",
        "params": {"data": "custom-payload"},
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
        data = resp.json()
        print(json.dumps(data, indent=2))

        result = data.get("result", {})
        print(f"\nHandled method: {result.get('handled_method')}")
        assert result.get("handled_method") == "custom/action"
        print("Custom method forwarded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
