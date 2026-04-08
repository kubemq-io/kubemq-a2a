# Concurrency Limit

Demonstrates the per-agent concurrency limit (100 concurrent requests).

## What It Shows

- Sending 101 concurrent requests to a slow agent (2s delay)
- KubeMQ enforces a limit of 100 concurrent requests per agent
- Overflow requests receive error code `-32603` (Internal Error)

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
Sending 101 concurrent requests (limit is 100)...

Results:
  Successes:            100
  Concurrency errors:   1 (code -32603)
  Other errors:         0
  Exceptions:           0
  Total:                101

Concurrency limit enforced — 1 request(s) rejected!
```
