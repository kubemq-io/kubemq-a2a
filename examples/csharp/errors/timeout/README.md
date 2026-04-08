# Timeout

Demonstrates the timeout error when an agent responds too slowly.

## What It Shows

- Agent has a 5-second processing delay
- Client sends a request with `configuration.timeout = 1` (1 second)
- KubeMQ returns error code `-32001` (Timeout) before the agent responds

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project Timeout.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project Timeout.csproj
```

## Expected Output

```
Sending request with timeout=1 to slow agent (5s delay)...
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "timeout"
  }
}

Error code:    -32001
Error message: timeout

Timeout error (-32001) received as expected!
```
