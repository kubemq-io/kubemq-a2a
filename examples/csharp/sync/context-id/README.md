# Context ID

Demonstrates sending a request with a `contextId` for correlation tracking.

## What It Shows

- Including a `contextId` field in the JSON-RPC params
- Verifying the agent receives and can return the same `contextId`
- Using context IDs for request correlation

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project ContextId.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ContextId.csproj
```

## Expected Output

```
Sent contextId:     ctx-001
Received contextId: ctx-001
Context ID correlation verified!
```
