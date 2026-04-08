# Agent Not Found

Demonstrates the error response when sending a request to a nonexistent agent.

## What It Shows

- Sending a JSON-RPC request to an agent ID that is not registered
- Receiving error code `-32002` (Agent Not Found)
- No agent server is needed for this example

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Python 3.10+ with dependencies installed (`uv sync`)

## Run

```bash
uv run python client.py
```

## Expected Output

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32002,
    "message": "agent not found: nonexistent-agent"
  }
}

Error code:    -32002
Error message: agent not found: nonexistent-agent

Agent-not-found error (-32002) received as expected!
```
