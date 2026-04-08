# Deregister Agent

Demonstrates both deregistration methods: POST and DELETE.

## What It Shows

- POST `/agents/deregister` with JSON body `{"agent_id": "..."}` to deregister
- DELETE `/agents/{agent_id}` as an alternative deregistration method
- Verifying the agent is gone after each deregistration

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
