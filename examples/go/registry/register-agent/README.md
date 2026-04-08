# Register Agent

Registers an echo agent with KubeMQ and verifies the registration via the registry API.

## What It Shows

- Agent card creation with skills, input/output modes, and protocol versions
- POST `/agents/register` to register the agent
- GET `/agents/{agent_id}` to verify registration and inspect server-managed fields (`registered_at`, `last_seen`)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
go run agent.go
```

Terminal 2 (run the client):
```bash
go run client.go
```

## Expected Output

Agent:
```
Agent listening on port 18080
Registered: 200
{
  "agent_id": "echo-agent-01",
  ...
}
```

Client:
```
Status: 200
{
  "agent_id": "echo-agent-01",
  "registered_at": "...",
  ...
}

Agent registration verified successfully!
```
