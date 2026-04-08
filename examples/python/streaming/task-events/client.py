"""Task-Events example — reads and categorizes different SSE event types."""

import asyncio
import json
from collections import Counter

import httpx
from httpx_sse import aconnect_sse

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "task-events-agent-01"


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/stream",
        "params": {"message": {"parts": [{"text": "Show me all event types"}]}},
    }

    event_types: Counter[str] = Counter()

    async with httpx.AsyncClient(timeout=60) as client:
        print("Connecting to SSE stream...")
        async with aconnect_sse(
            client, "POST", f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload
        ) as event_source:
            async for event in event_source.aiter_sse():
                data = json.loads(event.data)
                event_types[event.event] += 1

                if event.event == "task.status":
                    payload_data = data["payload"]
                    print(f"  [STATUS]   progress={payload_data['progress']}/{payload_data['total']}")
                elif event.event == "task.artifact":
                    print(f"  [ARTIFACT] name={data['payload']['name']}")
                elif event.event == "task.done":
                    print(f"  [DONE]     result={data['payload']['final_result']}")
                elif event.event == "task.error":
                    print(f"  [ERROR]    {data['payload']}")

                if event.event in ("task.done", "task.error"):
                    break

    print(f"\n--- Event Summary ---")
    for event_type, count in sorted(event_types.items()):
        print(f"  {event_type}: {count}")
    print(f"  Total: {sum(event_types.values())}")


if __name__ == "__main__":
    asyncio.run(main())
