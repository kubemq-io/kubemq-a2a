# Concurrency Limit

Demonstrates the per-agent concurrency limit (100 concurrent requests).

## What It Shows

- Agent with 2-second delay to hold connections
- Client sends 101 concurrent requests
- Requests beyond the limit receive JSON-RPC error code `-32603`

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
Sending 101 concurrent requests (limit is 100)...

Results (2100ms):
  Total:          101
  Succeeded:      100 (expect <=100)
  Rejected -32603:1 (expect >=1)
  Other errors:   0

Concurrency limit enforced correctly.
```
