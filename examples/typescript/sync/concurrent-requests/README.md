# Concurrent Requests

Demonstrates sending multiple concurrent JSON-RPC requests to the same agent.

## What It Shows

- 20 concurrent `message/send` requests via `Promise.all`
- All requests succeed when within the concurrency limit (100)
- Response time and success/failure statistics

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
Sending 20 concurrent requests to concurrent-agent-01...

Results:
  Total:     20
  Succeeded: 20
  Failed:    0
  Avg time:  45ms
  Wall time: 52ms
```
