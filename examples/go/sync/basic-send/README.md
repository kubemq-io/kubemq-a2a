# Basic Send

Sends a `message/send` JSON-RPC request through KubeMQ to an echo agent.

## What It Shows

- Basic JSON-RPC 2.0 round-trip through KubeMQ A2A gateway
- `message/send` method with text parts
- Echo agent returning the full request body

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
Status: 200
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": { ... }
  }
}

Basic send completed successfully!
```
