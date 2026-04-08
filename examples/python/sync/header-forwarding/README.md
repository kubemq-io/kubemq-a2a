# Header Forwarding

Demonstrates how custom `X-*` headers are forwarded through KubeMQ to agents.

## What It Shows

- Sending custom `X-Custom-Header` with a JSON-RPC request
- Verifying the header is forwarded to the agent
- Observing `X-KubeMQ-Caller-ID` injected by KubeMQ

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Python 3.10+ with dependencies installed (`uv sync`)

## Run

Terminal 1 (start the agent):
```bash
uv run python agent.py
```

Terminal 2 (run the client):
```bash
uv run python client.py
```

## Expected Output

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": {...},
    "received_headers": {
      "X-Custom-Header": "my-custom-value",
      "X-Kubemq-Caller-Id": "..."
    }
  }
}

Forwarded headers: {'X-Custom-Header': 'my-custom-value', 'X-Kubemq-Caller-Id': '...'}
X-Custom-Header was forwarded successfully!
X-KubeMQ-Caller-ID injected: {'X-Kubemq-Caller-Id': '...'}
```
