# Agent Info

Demonstrates retrieving and displaying all fields of an agent card.

## What It Shows

- Registering an agent with all card fields populated (multiple skills, tags)
- Retrieving the full agent card via `GET /agents/{agent_id}`
- Displaying all card fields including `registered_at` and `last_seen`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project AgentInfo.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project AgentInfo.csproj
```

## Expected Output

```
Status: 200

--- Agent Card ---
  agent_id:           full-info-agent-01
  name:               Full Info Agent
  description:        An agent with all card fields populated for demonstration
  version:            2.1.0
  ...

--- Skills (2) ---
  [echo] Echo: Echoes back the received message verbatim
    tags: ["echo","test","debug"]
  [greet] Greeting: Responds with a personalized greeting
    tags: ["greet","chat"]
```
