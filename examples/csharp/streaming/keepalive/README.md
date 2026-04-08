# Keepalive

Demonstrates KubeMQ's keepalive mechanism during long-lived SSE streams.

## What It Shows

- Agent emits events with 35-second pauses between them
- KubeMQ injects keepalive pings to prevent connection timeout
- Client handles both real events and keepalive pings
- Total stream duration ~70 seconds

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project Keepalive.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project Keepalive.csproj
```

## Expected Output

```
Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...
  [   0.1s] [task.status] {"type":"status_update",...}
  [  15.0s] [keepalive]
  [  30.0s] [keepalive]
  [  35.1s] [task.status] {"type":"status_update",...}
  ...
  [  70.2s] [task.done] {"type":"done",...}

Stream completed in 70.2s
Keepalive kept the connection alive during long pauses!
```
