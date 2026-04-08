# Custom Method

Demonstrates sending a custom JSON-RPC method name through KubeMQ.

## What It Shows

- KubeMQ forwards any JSON-RPC method name to the agent (not just `message/send`)
- Agent receives and handles the `custom/action` method
- Custom methods enable domain-specific RPC patterns

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
    "handled_method": "custom/action",
    "echo": {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "custom/action",
      "params": {"data": "custom-payload"}
    }
  }
}

Handled method: custom/action
Custom method forwarded successfully!
```
