# Basic Stream

Demonstrates basic SSE streaming via `message/stream` through KubeMQ.

## What It Shows

- Sending a `message/stream` JSON-RPC request via POST
- Reading SSE events using `httpx-sse`
- Handling `task.status` progress events and terminal `task.done` event

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

```
Connecting to SSE stream...
[task.status] {"type": "status_update", "payload": {"status": "working", "progress": 1, "total": 5}}
[task.status] {"type": "status_update", "payload": {"status": "working", "progress": 2, "total": 5}}
[task.status] {"type": "status_update", "payload": {"status": "working", "progress": 3, "total": 5}}
[task.status] {"type": "status_update", "payload": {"status": "working", "progress": 4, "total": 5}}
[task.status] {"type": "status_update", "payload": {"status": "working", "progress": 5, "total": 5}}
[task.done] {"type": "done", "payload": {"final_result": "completed", "event_count": 5}}

Received 6 events
Stream completed!
```
