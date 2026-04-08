# Client Disconnect

Demonstrates client-side SSE stream disconnection and server cleanup.

## What It Shows

- Client disconnects after receiving 2 of 10 events
- `AbortController` for clean connection teardown
- KubeMQ detects disconnection and cleans up (verified via `kubemq_a2a_sse_streams_active` metric)

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

Client:
```
Connecting to stream, will disconnect after 2 events...
[task.status] progress=1
[task.status] progress=2

Received 2 events, disconnecting...
Disconnected. KubeMQ will clean up the stream.
```

Agent:
```
Sent event 1/10
Sent event 2/10
Client disconnected at event 3
```
