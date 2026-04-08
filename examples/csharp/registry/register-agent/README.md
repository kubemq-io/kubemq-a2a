# Register Agent

Demonstrates agent registration with KubeMQ's A2A registry.

## What It Shows

- Registering an agent with a full agent card (skills, versions, modes)
- Verifying registration via `GET /agents/{agent_id}`
- The agent card includes `registered_at` timestamp after registration

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project RegisterAgent.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project RegisterAgent.csproj
```

## Expected Output

```
Status: 200
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  ...
  "registered_at": "2025-..."
}

Agent registration verified successfully!
```
