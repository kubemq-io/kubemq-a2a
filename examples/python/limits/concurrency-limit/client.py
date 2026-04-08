"""Concurrency-Limit example — sends 101 concurrent requests to trigger limit."""

import asyncio
import json

import httpx

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "concurrency-agent-01"
NUM_REQUESTS = 101


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
    async with httpx.AsyncClient(timeout=30) as client:
        print(f"Sending {NUM_REQUESTS} concurrent requests (limit is 100)...")
        tasks = [send_request(client, i) for i in range(1, NUM_REQUESTS + 1)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = 0
    concurrency_errors = 0
    other_errors = 0
    exceptions = 0

    for r in results:
        if isinstance(r, Exception):
            exceptions += 1
        elif "result" in r:
            successes += 1
        elif "error" in r:
            if r["error"].get("code") == -32603:
                concurrency_errors += 1
            else:
                other_errors += 1

    print(f"\nResults:")
    print(f"  Successes:            {successes}")
    print(f"  Concurrency errors:   {concurrency_errors} (code -32603)")
    print(f"  Other errors:         {other_errors}")
    print(f"  Exceptions:           {exceptions}")
    print(f"  Total:                {len(results)}")

    assert concurrency_errors >= 1, "Expected at least 1 concurrency limit error"
    print(f"\nConcurrency limit enforced — {concurrency_errors} request(s) rejected!")


if __name__ == "__main__":
    asyncio.run(main())
