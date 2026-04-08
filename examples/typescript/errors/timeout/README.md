# Timeout

Demonstrates the timeout error when an agent takes longer than the specified timeout.

## What It Shows

- Agent with 5-second delay
- Client sends with `timeout: 1` in `params.configuration`
- KubeMQ returns JSON-RPC error code `-32001` (agent timeout)

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
Sending with timeout=1s to a 5s-delay agent...
Response: {
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "agent timeout: slow-timeout-agent-01"
  }
}

Error code:    -32001 (expect -32001)
Error message: agent timeout: slow-timeout-agent-01
Match:         true
```
