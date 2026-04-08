# Task Events

Demonstrates reading and categorizing different SSE event types.

## What It Shows

- Agent emitting `task.status`, `task.artifact`, and `task.done` events
- Client categorizing events by type
- Event summary with counts per type

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
  [STATUS]   progress=1/3
  [STATUS]   progress=2/3
  [ARTIFACT] name=result.json
  [DONE]     result=completed

--- Event Summary ---
  task.status: 2
  task.artifact: 1
  task.done: 1
  Total: 4
```
