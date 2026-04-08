# Client Disconnect

Demonstrates client-side SSE stream disconnection and cleanup.

## What It Shows

- Agent emitting events slowly (2-second intervals)
- Client disconnecting after receiving only 2 events
- KubeMQ detecting the disconnect and cleaning up

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

Client:
```
Connecting to stream (will disconnect after 2 events)...
  Event 1: [task.status] progress=1
  Event 2: [task.status] progress=2

Disconnecting after 2 events...
Client disconnected.
KubeMQ will detect the disconnect and clean up the stream.
```

Agent:
```
Sent event 1
Sent event 2
Client disconnected after event 2
```
