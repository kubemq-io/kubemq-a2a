# Basic Stream

Demonstrates SSE streaming via POST `message/stream` through KubeMQ.

## What It Shows

- POST to `/a2a/{agent_id}` with `method: "message/stream"` and `Accept: text/event-stream`
- Agent emits 5 `task.status` events followed by a `task.done` event
- Client reads SSE stream using `ReadableStream` reader

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
npx tsx agent.ts
```

Terminal 2 (run the client):
```bash
npx tsx client.ts
```

## Expected Output

```
=== POST-based streaming ===
[task.status] {"type":"status_update","payload":{"status":"working","progress":1,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":2,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":3,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":4,"total":5}}
[task.status] {"type":"status_update","payload":{"status":"working","progress":5,"total":5}}
[task.done] {"type":"done","payload":{"final_result":"completed","event_count":5}}

Stream complete. Total events: 6
```
