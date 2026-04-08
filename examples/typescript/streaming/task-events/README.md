# Task Events

Demonstrates handling different SSE event types: status, artifact, and done.

## What It Shows

- `task.status` events with progress tracking
- `task.artifact` events delivering intermediate results
- `task.done` as the terminal event
- Categorizing and counting event types

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
[STATUS]   progress=1/3 status=working
[STATUS]   progress=2/3 status=working
[ARTIFACT] name=result.json data={"key":"value","items":[1,2,3]}
[STATUS]   progress=3/3 status=finishing
[DONE]     result=completed

=== Event Summary ===
  task.status: 3
  task.artifact: 1
  task.done: 1
```
