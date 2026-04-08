# Context ID

Demonstrates using `contextId` for request correlation across A2A messages.

## What It Shows

- Sending a `contextId` field in `params` for request tracking
- Agent receives and echoes the `contextId` back
- Client-side correlation verification

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
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": {...},
    "contextId": "ctx-001"
  }
}

Sent contextId:     ctx-001
Received contextId: ctx-001
Context ID correlation verified!
```
