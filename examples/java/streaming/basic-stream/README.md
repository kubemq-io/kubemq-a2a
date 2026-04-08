# Basic Stream

Demonstrates SSE streaming via `message/stream` through KubeMQ.

## What It Shows

- Sending a `message/stream` JSON-RPC request with SSE accept header
- Agent emitting 5 `task.status` events followed by a `task.done` event
- Client reading the SSE stream line-by-line using `BodyHandlers.ofLines()`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Agent"
```

Terminal 2 (run the client):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
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
