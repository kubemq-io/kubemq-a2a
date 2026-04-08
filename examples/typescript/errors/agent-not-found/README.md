# Agent Not Found

Demonstrates the error response when sending to a non-existent agent.

## What It Shows

- Sending to an unregistered `agent_id` returns JSON-RPC error code `-32002`
- No agent server needed — the agent is intentionally absent

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

```bash
npx tsx client.ts
```

## Expected Output

```
Sending to nonexistent agent...
Response: {
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32002,
    "message": "agent not found: nonexistent-agent"
  }
}

Error code:    -32002 (expect -32002)
Error message: agent not found: nonexistent-agent
Match:         true
```
