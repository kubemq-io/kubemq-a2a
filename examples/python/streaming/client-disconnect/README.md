# Client Disconnect

Demonstrates client-side disconnection from an SSE stream and server cleanup.

## What It Shows

- Agent emits events at 2-second intervals (10 total)
- Client intentionally disconnects after receiving only 2 events
- KubeMQ detects the disconnect and cleans up the stream

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Python 3.10+ with dependencies installed (`uv sync`)

## Run

Terminal 1 (start the agent):
```bash
uv run python agent.py
```

Terminal 2 (run the client):
```bash
uv run python client.py
```

## Expected Output

Client terminal:
```
Connecting to stream (will disconnect after 2 events)...
  Event 1: [task.status] progress=1
  Event 2: [task.status] progress=2

Disconnecting after 2 events...
Client disconnected.
KubeMQ will detect the disconnect and clean up the stream.
```

Agent terminal:
```
Sent event 1
Sent event 2
Client disconnected after event 2
```
