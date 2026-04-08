# Basic Send

Demonstrates a basic synchronous `message/send` JSON-RPC request through KubeMQ.

## What It Shows

- Sending a `message/send` JSON-RPC 2.0 request to an agent via `POST /a2a/{agent_id}`
- Receiving and parsing the JSON-RPC response
- The complete request/response round-trip through KubeMQ

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project BasicSend.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project BasicSend.csproj
```

## Expected Output

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
