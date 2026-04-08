# Keepalive

Demonstrates how KubeMQ keepalive comments maintain long-lived SSE connections.

## What It Shows

- Agent emits events with 35-second pauses between them
- KubeMQ sends keepalive comments (`": keepalive"`) every ~30s to prevent timeout
- Client maintains connection through long idle periods

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
Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...
  [   0.1s] [task.status] {"type": "status_update", "payload": {"status": "working", "progress": 1, "total": 3}}
  [  30.0s] [keepalive]
  [  35.1s] [task.status] {"type": "status_update", "payload": {"status": "working", "progress": 2, "total": 3}}
  [  65.0s] [keepalive]
  [  70.2s] [task.done] {"type": "done", "payload": {"final_result": "completed after keepalive pauses"}}

Stream completed in 70.2s
Keepalive kept the connection alive during long pauses!
```
