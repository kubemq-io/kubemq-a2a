# Concurrent Requests

Sends 20 concurrent requests to an echo agent and collects results.

## What It Shows

- Sending multiple concurrent JSON-RPC requests using goroutines
- All requests completing successfully through KubeMQ
- Counting successes, errors, and exceptions

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
Sending 20 concurrent requests...

Results:
  Successes:  20
  Errors:     0
  Exceptions: 0
  Total:      20

All 20 concurrent requests completed successfully!
```
