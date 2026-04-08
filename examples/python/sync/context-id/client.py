"""Context-ID example — sends a request with contextId and verifies correlation."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "context-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": "Track this request"}]},
            "contextId": "ctx-001",
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
        data = resp.json()
        print(json.dumps(data, indent=2))

        result = data.get("result", {})
        returned_ctx = result.get("contextId")
        print(f"\nSent contextId:     ctx-001")
        print(f"Received contextId: {returned_ctx}")

        if returned_ctx == "ctx-001":
            print("Context ID correlation verified!")
        else:
            print("Warning: contextId mismatch")


if __name__ == "__main__":
    asyncio.run(main())
