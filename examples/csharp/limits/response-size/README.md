# Response Size

Demonstrates KubeMQ's response size limit enforcement.

## What It Shows

- Agent returns a response larger than 10MB (11MB payload)
- KubeMQ enforces the response size limit
- Client receives an error when the limit is exceeded

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project ResponseSize.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ResponseSize.csproj
```

## Expected Output

```
Requesting oversized response (>10MB)...

Error code:    -32603
Error message: response size exceeds limit

Response size limit enforced!
```
