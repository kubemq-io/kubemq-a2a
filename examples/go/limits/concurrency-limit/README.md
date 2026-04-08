# Concurrency Limit

Sends 101 concurrent requests to trigger the per-agent concurrency limit (100).

## What It Shows

- Per-agent concurrency limit of 100 concurrent requests
- Error code `-32603` (Internal Error) when the limit is exceeded
- Slow agent holding connections to fill the concurrency pool

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
Sending 101 concurrent requests (limit is 100)...

Results:
  Successes:            100
  Concurrency errors:   1 (code -32603)
  Other errors:         0
  Exceptions:           0
  Total:                101

Concurrency limit enforced — 1 request(s) rejected!
```
