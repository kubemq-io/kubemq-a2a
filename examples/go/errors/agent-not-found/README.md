# Agent Not Found

Sends a request to a nonexistent agent and receives error code `-32002`.

## What It Shows

- JSON-RPC error response for unregistered agents
- Error code `-32002` (Agent Not Found)
- No agent process needed — the error comes from KubeMQ

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

```bash
go run client.go
```

No agent is needed — this example demonstrates the error case.

## Expected Output

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32002,
    "message": "agent not found: nonexistent-agent"
  }
}

Error code:    -32002
Error message: agent not found: nonexistent-agent

Agent-not-found error (-32002) received as expected!
```
