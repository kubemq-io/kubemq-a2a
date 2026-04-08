# Response Size Limit

Demonstrates the response size limit (10MB) enforcement by KubeMQ.

## What It Shows

- Agent returns a >10MB response body
- KubeMQ rejects it with JSON-RPC error code `-32603` containing "too large"
- Client handles the size limit error

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
Sending request to oversize agent (expects >10MB response)...
Error code:    -32603
Error message: internal error: response too large
Size limit enforced: true
```
