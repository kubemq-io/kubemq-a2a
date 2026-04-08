"""Concurrent-Requests example — sends 20 concurrent requests via asyncio.gather."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "concurrent-agent-01"
NUM_REQUESTS = 20


async def send_request(client: httpx.AsyncClient, request_id: int) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "message/send",
        "params": {
            "message": {"parts": [{"text": f"Request #{request_id}"}]},
        },
    }
    resp = await client.post(f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload)
    return resp.json()


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print(f"Sending {NUM_REQUESTS} concurrent requests...")
        tasks = [send_request(client, i) for i in range(1, NUM_REQUESTS + 1)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = sum(1 for r in results if isinstance(r, dict) and "result" in r)
    errors = sum(1 for r in results if isinstance(r, dict) and "error" in r)
    exceptions = sum(1 for r in results if isinstance(r, Exception))

    print(f"\nResults:")
    print(f"  Successes:  {successes}")
    print(f"  Errors:     {errors}")
    print(f"  Exceptions: {exceptions}")
    print(f"  Total:      {len(results)}")

    assert successes == NUM_REQUESTS, f"Expected {NUM_REQUESTS} successes, got {successes}"
    print(f"\nAll {NUM_REQUESTS} concurrent requests completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
