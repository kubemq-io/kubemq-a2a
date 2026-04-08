# Response Size

Requests a response larger than the 10MB size limit.

## What It Shows

- KubeMQ enforcing response size limits (>10MB rejected)
- Agent generating an oversized response (11MB)
- Error response when the limit is exceeded

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
Requesting oversized response (>10MB)...

Error code:    -32603
Error message: internal error: response too large

Response size limit enforced!
```
