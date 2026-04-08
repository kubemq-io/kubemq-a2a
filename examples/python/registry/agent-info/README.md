# Agent Info

Demonstrates retrieving and displaying all fields of an agent card.

## What It Shows

- Registering an agent with all optional fields (description, version, multiple skills)
- Retrieving the full agent card via `GET /agents/{agent_id}`
- Inspecting server-managed fields (`registered_at`, `last_seen`)

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
Status: 200

--- Agent Card ---
  agent_id:           full-info-agent-01
  name:               Full Info Agent
  description:        An agent with all card fields populated for demonstration
  version:            2.1.0
  url:                http://localhost:18080/
  defaultInputModes:  ['text']
  defaultOutputModes: ['text']
  protocolVersions:   ['1.0']
  registered_at:      2026-...
  last_seen:          2026-...

--- Skills (2) ---
  [echo] Echo: Echoes back the received message verbatim
    tags: ['echo', 'test', 'debug']
  [greet] Greeting: Responds with a personalized greeting
    tags: ['greet', 'chat']
```
