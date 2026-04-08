# Custom Method

Sends a non-standard `custom/action` JSON-RPC method through KubeMQ.

## What It Shows

- KubeMQ forwards any JSON-RPC method name, not just standard A2A methods
- Agent handling arbitrary method names
- Verifying the method name is preserved end-to-end

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
    "handled_method": "custom/action",
    "echo": { ... }
  }
}

Handled method: custom/action
Custom method forwarded successfully!
```
