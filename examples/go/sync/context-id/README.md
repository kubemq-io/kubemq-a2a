# Context ID

Sends a request with a `contextId` and verifies it is echoed back for correlation.

## What It Shows

- `contextId` in `params` for request correlation
- Agent receiving and returning the contextId
- Verifying end-to-end correlation ID passthrough

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
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": { ... },
    "contextId": "ctx-001"
  }
}

Sent contextId:     ctx-001
Received contextId: ctx-001
Context ID correlation verified!
```
