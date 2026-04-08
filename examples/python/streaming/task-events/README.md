# Task Events

Demonstrates handling different SSE event types: status, artifact, and done.

## What It Shows

- Agent emits `task.status`, `task.artifact`, and `task.done` events
- Client categorizes and processes each event type differently
- Summary of event types received

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
  [STATUS]   progress=1/3
  [STATUS]   progress=2/3
  [ARTIFACT] name=result.json
  [DONE]     result=completed

--- Event Summary ---
  task.artifact: 1
  task.done: 1
  task.status: 2
  Total: 4
```
