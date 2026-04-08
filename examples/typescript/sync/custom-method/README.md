# Custom Method

Demonstrates sending custom JSON-RPC methods through KubeMQ A2A.

## What It Shows

- KubeMQ forwards any JSON-RPC method name to the agent
- `custom/action` as a non-standard method
- Standard methods: `tasks/get`, `tasks/cancel`

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
=== custom/action ===
Response: {
  "jsonrpc": "2.0",
  "id": ...,
  "result": { "echo": { "method": "custom/action", ... } }
}

=== tasks/get ===
Response: {
  "jsonrpc": "2.0",
  "id": ...,
  "result": { "taskId": "task-001", "status": "completed" }
}

=== tasks/cancel ===
Response: {
  "jsonrpc": "2.0",
  "id": ...,
  "result": { "taskId": "task-002", "status": "cancelled" }
}
```
