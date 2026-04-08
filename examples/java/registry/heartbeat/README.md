# Heartbeat

Demonstrates the agent heartbeat keep-alive pattern.

## What It Shows

- Sending periodic heartbeats via `POST /agents/heartbeat`
- Observing `last_seen` timestamp updates
- Verifying the heartbeat cycle via `GET /agents/{agent_id}`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Agent"
```

Terminal 2 (run the client):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
```

## Expected Output

```
Heartbeat 1: status=200 last_seen=2026-04-06T10:00:00Z
Heartbeat 2: status=200 last_seen=2026-04-06T10:00:02Z
Heartbeat 3: status=200 last_seen=2026-04-06T10:00:04Z

=== Final agent state ===
registered_at: 2026-04-06T10:00:00Z
last_seen:     2026-04-06T10:00:04Z

Heartbeat cycle completed!
```
