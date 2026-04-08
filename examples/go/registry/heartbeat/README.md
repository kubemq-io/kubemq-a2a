# Heartbeat

Sends periodic heartbeats to keep an agent registration alive.

## What It Shows

- POST `/agents/heartbeat` with `{"agent_id": "..."}` to update `last_seen`
- Observing `last_seen` timestamp updates across heartbeats
- Keep-alive pattern for long-running agents

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

Client:
```
Heartbeat 1: status=200 last_seen=2026-04-07T10:00:00Z
Heartbeat 2: status=200 last_seen=2026-04-07T10:00:02Z
Heartbeat 3: status=200 last_seen=2026-04-07T10:00:04Z

=== Final agent state ===
registered_at: 2026-04-07T09:59:58Z
last_seen:     2026-04-07T10:00:04Z

Heartbeat cycle completed!
```
