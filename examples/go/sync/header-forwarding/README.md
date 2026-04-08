# Header Forwarding

Demonstrates how custom `X-*` headers are forwarded through KubeMQ to the agent.

## What It Shows

- Sending `X-Custom-Header` with a request
- Agent receiving and returning the forwarded headers
- `X-KubeMQ-Caller-ID` injected by KubeMQ
- Hop-by-hop headers (Authorization, Cookie) are stripped

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
    "received_headers": {
      "X-Custom-Header": "my-custom-value",
      "X-Kubemq-Caller-Id": "..."
    }
  }
}

Forwarded headers: map[...]
X-Custom-Header was forwarded successfully!
X-KubeMQ-Caller-ID injected: ...
```
