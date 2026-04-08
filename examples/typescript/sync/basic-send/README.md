# Basic Send

Demonstrates a basic synchronous JSON-RPC `message/send` round-trip through KubeMQ.

## What It Shows

- JSON-RPC 2.0 `message/send` request with text parts
- POST to `/a2a/{agent_id}` through KubeMQ
- Agent echoes the full request body back

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
Sending message/send to sync-echo-01
Request: {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": {
      "parts": [{ "text": "Hello, agent!" }]
    }
  }
}

Response: {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": { ... }
  }
}

Round-trip verified: agent echoed the request
```
