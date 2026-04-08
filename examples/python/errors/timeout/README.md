# Timeout

Demonstrates the timeout error when an agent takes too long to respond.

## What It Shows

- Setting a short timeout (1 second) via `params.configuration.timeout`
- Agent has a 5-second delay, exceeding the timeout
- Receiving error code `-32001` (Agent Timeout)

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
Sending request with timeout=1 to slow agent (5s delay)...
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "agent timeout: slow-agent-01"
  }
}

Error code:    -32001
Error message: agent timeout: slow-agent-01

Timeout error (-32001) received as expected!
```
