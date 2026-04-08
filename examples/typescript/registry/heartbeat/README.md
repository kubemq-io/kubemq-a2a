# Heartbeat

Demonstrates the heartbeat keep-alive pattern for registered agents.

## What It Shows

- POST `/agents/heartbeat` with `{ "agent_id": "..." }`
- `last_seen` timestamp updates with each heartbeat
- 400 response when sending heartbeat for non-existent agent

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
Initial last_seen: 2026-04-06T10:00:00Z
Heartbeat #1: status=200, last_seen=2026-04-06T10:00:02Z
Heartbeat #2: status=200, last_seen=2026-04-06T10:00:04Z
Heartbeat #3: status=200, last_seen=2026-04-06T10:00:06Z

=== Heartbeat non-existent agent ===
Status: 400 (expect 400)
Error: agent not found
```
