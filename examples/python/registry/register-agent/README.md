# Register Agent

Demonstrates how to register an A2A agent with KubeMQ and verify its registration.

## What It Shows

- Starting an aiohttp agent server that handles JSON-RPC 2.0 requests
- Registering the agent via `POST /agents/register` with a full agent card
- Verifying registration via `GET /agents/{agent_id}`

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

Agent terminal:
```
Agent listening on port 18080
Registered: 200
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  ...
  "registered_at": "2026-...",
  "last_seen": "2026-..."
}
```

Client terminal:
```
Status: 200
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  ...
}

Agent registration verified successfully!
```
