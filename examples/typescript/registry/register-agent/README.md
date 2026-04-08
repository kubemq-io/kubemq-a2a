# Register Agent

Demonstrates registering an A2A agent with KubeMQ and verifying the registration.

## What It Shows

- Agent card structure with skills, input/output modes, and protocol versions
- POST `/agents/register` to register with KubeMQ
- GET `/agents/{agent_id}` to verify registration

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

Agent:
```
Agent listening on port 18080
Registered: {
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  ...
  "registered_at": "2026-...",
  "last_seen": "2026-..."
}
```

Client:
```
Agent info: {
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  ...
}

Verification:
  agent_id:      echo-agent-01
  name:          Echo Agent
  registered_at: 2026-...
  last_seen:     2026-...
```
