# Keepalive

Demonstrates SSE keepalive comments sent by KubeMQ during long-lived streams.

## What It Shows

- Agent emits events with 35-second pauses between them
- KubeMQ sends `: keepalive` comments (~every 30s) to prevent connection timeout
- Client identifies and counts keepalive comments vs real events

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
npx tsx agent.ts
```

Terminal 2 (run the client — takes ~70 seconds):
```bash
npx tsx client.ts
```

## Expected Output

```
Connecting to stream (expect ~70s total with keepalive comments)...
[EVENT]     #1 task.status at 2026-...
[KEEPALIVE] #1 at 2026-...
[EVENT]     #2 task.status at 2026-...
[KEEPALIVE] #2 at 2026-...
[EVENT]     #3 task.status at 2026-...
[EVENT]     #4 task.done at 2026-...

Stream complete.
  Events:     4
  Keepalives: 2
```
