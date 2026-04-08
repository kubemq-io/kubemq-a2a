# Deregister Agent

Demonstrates both methods of deregistering an agent from KubeMQ.

## What It Shows

- POST `/agents/deregister` with JSON body `{ "agent_id": "..." }`
- DELETE `/agents/{agent_id}` for REST-style deregistration
- 404 response when deregistering a non-existent agent

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
=== Deregister via POST /agents/deregister ===
POST deregister status: 200
Response: {}
Verify GET status: 404 (expect 404)

=== Deregister via DELETE /agents/{agent_id} ===
DELETE status: 200
Response: {}
Verify GET status: 404 (expect 404)

=== Deregister non-existent agent ===
Status: 404 (expect 404)
Error: agent not found
```
