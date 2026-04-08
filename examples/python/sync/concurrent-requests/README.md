# Concurrent Requests

Demonstrates sending multiple concurrent requests to the same agent.

## What It Shows

- Using `asyncio.gather` to send 20 requests simultaneously
- All concurrent requests to the same agent succeed
- Collecting and summarizing results from concurrent operations

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
Sending 20 concurrent requests...

Results:
  Successes:  20
  Errors:     0
  Exceptions: 0
  Total:      20

All 20 concurrent requests completed successfully!
```
