# Keepalive

Reads a long-lived SSE stream with 35-second pauses between events.

## What It Shows

- Long-lived SSE connections with keepalive handling
- KubeMQ sending keepalive comments during idle periods
- Stream surviving pauses longer than typical HTTP timeouts

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

Client (takes ~70 seconds):
```
Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...
  [   0.1s] [task.status] {"type":"status_update",...}
  [  30.0s] [keepalive]
  [  35.1s] [task.status] {"type":"status_update",...}
  [  65.0s] [keepalive]
  [  70.1s] [task.done] {"type":"done",...}

Stream completed in 70.2s
Keepalive kept the connection alive during long pauses!
```
