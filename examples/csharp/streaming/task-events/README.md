# Task Events

Demonstrates reading and categorizing different SSE event types from a streaming agent.

## What It Shows

- Agent emits `task.status`, `task.artifact`, and `task.done` events
- Client categorizes and counts each event type
- Event summary with per-type counts

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project TaskEvents.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project TaskEvents.csproj
```

## Expected Output

```
Connecting to SSE stream...
  [STATUS]   progress=1/3
  [STATUS]   progress=2/3
  [ARTIFACT] name=result.json
  [DONE]     result=completed

--- Event Summary ---
  task.artifact: 1
  task.done: 1
  task.status: 2
  Total: 4
```
