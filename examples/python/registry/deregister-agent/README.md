# Deregister Agent

Demonstrates both methods for deregistering an agent from KubeMQ.

## What It Shows

- Deregistering via `POST /agents/deregister` with a JSON body
- Deregistering via `DELETE /agents/{agent_id}`
- Verifying deregistration by checking `GET /agents/{agent_id}` returns 404

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
