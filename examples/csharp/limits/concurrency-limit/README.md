# Concurrency Limit

Demonstrates KubeMQ's per-agent concurrency limit enforcement.

## What It Shows

- Agent has a 2-second delay to hold connections open
- Client fires 101 concurrent requests (default limit is 100)
- At least 1 request receives error code `-32603` (concurrency limit exceeded)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project ConcurrencyLimit.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ConcurrencyLimit.csproj
```

## Expected Output

```
Sending 101 concurrent requests (limit is 100)...

Results:
  Successes:            100
  Concurrency errors:   1 (code -32603)
  Other errors:         0
  Exceptions:           0
  Total:                101

Concurrency limit enforced — 1 request(s) rejected!
```
