# Task Events

Reads and categorizes different SSE event types: status, artifact, and done.

## What It Shows

- Different SSE event types: `task.status`, `task.artifact`, `task.done`
- Parsing and categorizing each event type
- Event count summary by type

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
