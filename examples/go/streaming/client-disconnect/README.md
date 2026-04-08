# Client Disconnect

Disconnects from an SSE stream after receiving 2 events.

## What It Shows

- Client intentionally disconnecting mid-stream
- KubeMQ detecting the disconnection and cleaning up
- Agent detecting the broken connection

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
