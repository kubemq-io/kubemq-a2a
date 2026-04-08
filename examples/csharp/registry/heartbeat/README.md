# Heartbeat

Demonstrates sending periodic heartbeats to keep an agent's registration alive.

## What It Shows

- Sending heartbeat pings via `POST /agents/heartbeat`
- The `last_seen` timestamp updates with each heartbeat
- Verifying the agent's final state shows updated `last_seen`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project Heartbeat.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project Heartbeat.csproj
```

## Expected Output

```
Heartbeat 1: status=200 last_seen=2025-...
Heartbeat 2: status=200 last_seen=2025-...
Heartbeat 3: status=200 last_seen=2025-...

=== Final agent state ===
registered_at: 2025-...
last_seen:     2025-...

Heartbeat cycle completed!
```
