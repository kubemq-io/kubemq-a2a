# Context ID

Demonstrates using `contextId` for request correlation across A2A calls.

## What It Shows

- Sending `contextId` in `params.contextId`
- Agent receives and echoes the context ID
- Client verifies round-trip correlation

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
Sending with contextId=ctx-ts-001
Echoed contextId: ctx-ts-001
Match: true
```
