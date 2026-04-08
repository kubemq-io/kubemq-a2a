# Response Size

Demonstrates the response size limit (10MB) enforced by KubeMQ.

## What It Shows

- Agent attempts to return a response larger than 10MB
- KubeMQ rejects the oversized response
- Client receives an error indicating the response was too large

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
Requesting oversized response (>10MB)...

Error code:    -32603
Error message: internal error: response too large

Response size limit enforced!
```
