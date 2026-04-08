# Basic Stream

Reads SSE events from a streaming agent via POST `message/stream`.

## What It Shows

- POST-based SSE streaming through KubeMQ A2A gateway
- `message/stream` method triggering server-sent events
- Reading `task.status` progress events and terminal `task.done` event
- Using `bufio.Scanner` for line-by-line SSE parsing

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
go run agent.go
```

Terminal 2 (run the client):
```bash
go run client.go
```

## Expected Output

Client:
```
Connecting to SSE stream...
[task.status] {"type":"status_update","payload":{"progress":1,"status":"working","total":5}}
[task.status] {"type":"status_update","payload":{"progress":2,"status":"working","total":5}}
[task.status] {"type":"status_update","payload":{"progress":3,"status":"working","total":5}}
[task.status] {"type":"status_update","payload":{"progress":4,"status":"working","total":5}}
[task.status] {"type":"status_update","payload":{"progress":5,"status":"working","total":5}}
[task.done] {"type":"done","payload":{"event_count":5,"final_result":"completed"}}

Received 6 events
Stream completed!
```
