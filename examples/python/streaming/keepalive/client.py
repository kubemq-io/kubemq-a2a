"""Keepalive example — reads a long-lived stream with keepalive handling."""

import asyncio
import json
import time

import httpx
from httpx_sse import aconnect_sse

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "keepalive-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/stream",
        "params": {"message": {"parts": [{"text": "Long-running task"}]}},
    }

    start = time.monotonic()

    async with httpx.AsyncClient(timeout=120) as client:
        print("Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...")
        async with aconnect_sse(
            client, "POST", f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload
        ) as event_source:
            async for event in event_source.aiter_sse():
                elapsed = time.monotonic() - start
                if event.data:
                    data = json.loads(event.data)
                    print(f"  [{elapsed:6.1f}s] [{event.event}] {json.dumps(data)}")
                else:
                    print(f"  [{elapsed:6.1f}s] [keepalive]")

                if event.event in ("task.done", "task.error"):
                    break

    total = time.monotonic() - start
    print(f"\nStream completed in {total:.1f}s")
    print("Keepalive kept the connection alive during long pauses!")


if __name__ == "__main__":
    asyncio.run(main())
