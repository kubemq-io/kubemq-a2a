"""Client-Disconnect example — disconnects from SSE stream after 2 events."""

import asyncio
import json

import httpx
from httpx_sse import aconnect_sse

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "slow-stream-agent-01"
MAX_EVENTS = 2


async def main() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/stream",
        "params": {"message": {"parts": [{"text": "I will disconnect early"}]}},
    }

    async with httpx.AsyncClient(timeout=30) as client:
        print(f"Connecting to stream (will disconnect after {MAX_EVENTS} events)...")
        async with aconnect_sse(
            client, "POST", f"{KUBEMQ_URL}/a2a/{AGENT_ID}", json=payload
        ) as event_source:
            count = 0
            async for event in event_source.aiter_sse():
                count += 1
                data = json.loads(event.data)
                print(f"  Event {count}: [{event.event}] progress={data['payload'].get('progress')}")
                if count >= MAX_EVENTS:
                    print(f"\nDisconnecting after {MAX_EVENTS} events...")
                    break

    print("Client disconnected.")
    print("KubeMQ will detect the disconnect and clean up the stream.")


if __name__ == "__main__":
    asyncio.run(main())
