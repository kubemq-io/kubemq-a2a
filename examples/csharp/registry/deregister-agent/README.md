# Deregister Agent

Demonstrates both methods of deregistering an agent from KubeMQ.

## What It Shows

- Deregistering via `POST /agents/deregister` with `{ "agent_id": "..." }`
- Deregistering via `DELETE /agents/{agent_id}`
- Verifying the agent is no longer found after deregistration

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project DeregisterAgent.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project DeregisterAgent.csproj
```

## Expected Output

```
=== Verify agent exists ===
GET /agents/deregister-agent-01: 200

=== Deregister via POST ===
POST /agents/deregister: 200
GET /agents/deregister-agent-01 after deregister: 404

=== Re-register for DELETE test ===
Re-registered: 200

=== Deregister via DELETE ===
DELETE /agents/deregister-agent-01: 200
GET /agents/deregister-agent-01 after delete: 404

Both deregistration methods demonstrated successfully!
```
