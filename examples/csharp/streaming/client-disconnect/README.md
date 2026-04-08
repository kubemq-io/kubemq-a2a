# Client Disconnect

Demonstrates client-side SSE stream disconnection and KubeMQ cleanup behavior.

## What It Shows

- Agent emits events slowly (2-second intervals, 10 total)
- Client intentionally disconnects after receiving 2 events
- KubeMQ detects the disconnect and cleans up the stream

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project ClientDisconnect.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ClientDisconnect.csproj
```

## Expected Output

```
Connecting to stream (will disconnect after 2 events)...
  Event 1: [task.status] progress=1
  Event 2: [task.status] progress=2

Disconnecting after 2 events...
Client disconnected.
KubeMQ will detect the disconnect and clean up the stream.
```
