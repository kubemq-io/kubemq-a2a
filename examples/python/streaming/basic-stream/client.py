"""Basic-Stream example — reads SSE events from a streaming agent via POST."""

import asyncio
import json

import httpx
from httpx_sse import aconnect_sse

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "stream-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/stream",
        "params": {
            "message": {"parts": [{"text": "Stream me some updates"}]},
        },
    }

    async with httpx.AsyncClient(timeout=60) as client:
        print("Connecting to SSE stream...")
        async with aconnect_sse(
            client,
            "POST",
            f"{KUBEMQ_URL}/a2a/{AGENT_ID}",
            json=payload,
            headers={"Accept": "text/event-stream"},
        ) as event_source:
            event_count = 0
            async for event in event_source.aiter_sse():
                event_count += 1
                data = json.loads(event.data)
                print(f"[{event.event}] {json.dumps(data)}")
                if event.event in ("task.done", "task.error"):
                    break

    print(f"\nReceived {event_count} events")
    print("Stream completed!")


if __name__ == "__main__":
    asyncio.run(main())
