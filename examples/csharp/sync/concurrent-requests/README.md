# Concurrent Requests

Demonstrates sending multiple concurrent JSON-RPC requests through KubeMQ.

## What It Shows

- Firing 20 parallel `message/send` requests using `Task.WhenAll`
- Verifying all responses arrive with correct results
- KubeMQ's ability to handle concurrent request routing

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project ConcurrentRequests.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ConcurrentRequests.csproj
```

## Expected Output

```
Sending 20 concurrent requests...

Results:
  Successes:  20
  Errors:     0
  Exceptions: 0
  Total:      20

All 20 concurrent requests completed successfully!
```
