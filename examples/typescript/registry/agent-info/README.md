# Agent Info

Demonstrates retrieving full agent card details from the registry.

## What It Shows

- Agent card with multiple skills
- GET `/agents/{agent_id}` to retrieve all fields
- Server-managed fields: `registered_at`, `last_seen`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
npx tsx agent.ts
```

Terminal 2 (run the client):
```bash
npx tsx client.ts
```

## Expected Output

```
=== Agent Card Details ===
  agent_id:          info-agent-01
  name:              Info Agent
  description:       Agent with full card details for inspection
  version:           2.1.0
  url:               http://localhost:18080/
  registered_at:     2026-...
  last_seen:         2026-...
  protocolVersions:  ["1.0"]
  defaultInputModes: ["text","data"]
  defaultOutputModes:["text"]

=== Skills ===
  - echo: Echo (tags: test, echo)
    Echoes back the received message
  - transform: Transform (tags: test, transform)
    Transforms message format
```
