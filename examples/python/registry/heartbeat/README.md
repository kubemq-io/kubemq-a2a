# Heartbeat

Demonstrates the agent heartbeat mechanism for maintaining registration freshness.

## What It Shows

- Sending periodic heartbeats via `POST /agents/heartbeat`
- Observing `last_seen` timestamp updates after each heartbeat
- Maintaining agent liveness in the KubeMQ registry

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
Heartbeat 1: status=200 last_seen=2026-04-06T10:00:00Z
Heartbeat 2: status=200 last_seen=2026-04-06T10:00:02Z
Heartbeat 3: status=200 last_seen=2026-04-06T10:00:04Z

=== Final agent state ===
registered_at: 2026-04-06T09:59:55Z
last_seen:     2026-04-06T10:00:04Z

Heartbeat cycle completed!
```
