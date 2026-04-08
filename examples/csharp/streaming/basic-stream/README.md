# Basic Stream

Demonstrates basic SSE streaming via `message/stream` through KubeMQ.

## What It Shows

- Sending a `message/stream` JSON-RPC request via POST
- Reading SSE events using `HttpClient` with `HttpCompletionOption.ResponseHeadersRead`
- Handling `task.status` progress events and terminal `task.done` event

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agent):
```bash
dotnet run --project BasicStream.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project BasicStream.csproj
```

## Expected Output

```
Connecting to SSE stream...
[task.status] {"type":"status_update","payload":{"status":"working","progress":1,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":2,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":3,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":4,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":5,"total":5}}
[task.done] {"type":"done","payload":{"final_result":"completed","event_count":5}}

Received 6 events
Stream completed!
```
