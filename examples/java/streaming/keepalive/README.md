# Keepalive

Demonstrates long-lived SSE streams with keepalive handling.

## What It Shows

- Agent emitting events with 35-second pauses between them
- KubeMQ sending keepalive comments to maintain the connection
- Client handling keepalive comments alongside data events
- Stream surviving long idle periods (~70s total)

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
Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...
  [   0.1s] [task.status] {"type":"status_update","payload":{"status":"working","progress":1,"total":3}}
  [  30.0s] [keepalive]
  [  35.1s] [task.status] {"type":"status_update","payload":{"status":"working","progress":2,"total":3}}
  [  60.0s] [keepalive]
  [  70.1s] [task.done] {"type":"done","payload":{"final_result":"completed after keepalive pauses"}}

Stream completed in 70.1s
Keepalive kept the connection alive during long pauses!
```
