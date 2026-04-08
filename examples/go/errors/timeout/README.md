# Timeout

Sends a request with a 1-second timeout to an agent that takes 5 seconds to respond.

## What It Shows

- `params.configuration.timeout` to set a request timeout
- Error code `-32001` (Agent Timeout) when the agent exceeds the timeout
- Slow agent pattern with configurable delay

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
Sending request with timeout=1 to slow agent (5s delay)...
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "agent timeout: slow-agent-01"
  }
}

Error code:    -32001
Error message: agent timeout: slow-agent-01

Timeout error (-32001) received as expected!
```
