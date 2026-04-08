"""Header-Forwarding example — sends custom X-* headers and verifies forwarding."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "header-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": "Check my headers"}]},
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            json=payload,
            headers={"X-Custom-Header": "my-custom-value"},
        )
        data = resp.json()
        print(json.dumps(data, indent=2))

        received = data.get("result", {}).get("received_headers", {})
        print(f"\nForwarded headers: {received}")

        x_custom = {k: v for k, v in received.items() if k.lower() == "x-custom-header"}
        if x_custom:
            print("X-Custom-Header was forwarded successfully!")
        else:
            print("Warning: X-Custom-Header not found in forwarded headers")

        x_caller = {k: v for k, v in received.items() if k.lower() == "x-kubemq-caller-id"}
        if x_caller:
            print(f"X-KubeMQ-Caller-ID injected: {x_caller}")


if __name__ == "__main__":
    asyncio.run(main())
