# Sync Messaging

Synchronous A2A messaging follows a request/reply pattern using JSON-RPC 2.0 over HTTP POST.

## Basic message/send

Send a JSON-RPC 2.0 request to an agent through KubeMQ:

```
POST /a2a/{agent_id}
Content-Type: application/json
```

### Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": {
      "parts": [
        { "text": "Hello, agent!" }
      ]
    },
    "contextId": "ctx-001",
    "configuration": {
      "timeout": 30
    }
  }
}
```

### Response (Success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "message/send",
      "params": {
        "message": { "parts": [{ "text": "Hello, agent!" }] }
      }
    }
  }
}
```

## Timeout Handling

Timeouts are specified in `params.configuration.timeout` (in seconds). KubeMQ enforces a timeout chain:

| Layer | Timeout | Description |
|-------|---------|-------------|
| User-specified | `T` seconds | Value from `params.configuration.timeout` |
| Max cap | 3600s | Server caps the timeout at `MaxTimeoutSeconds` |
| Server gateway | `T + ~10s` | KubeMQ adds ~10s buffer before timing out the agent proxy |
| Client HTTP | `T + 15s` | A2AClient adds 15s to prevent premature client timeout |

When the timeout is exceeded, KubeMQ returns:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "agent timeout: echo-agent-01"
  }
}
```

## Context ID Tracking

Use `params.contextId` to correlate requests across multiple interactions with the same agent:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": { "parts": [{ "text": "Follow-up question" }] },
    "contextId": "ctx-001"
  }
}
```

The `contextId` is forwarded to the agent and can be used for conversation threading or session management.

## Standard Methods

KubeMQ forwards all JSON-RPC method names to the agent. Standard A2A methods include:

| Method | Description |
|--------|-------------|
| `message/send` | Send a message and receive a synchronous response |
| `message/stream` | Send a message and receive an SSE stream (see [Streaming](streaming.md)) |
| `tasks/get` | Query task status |
| `tasks/cancel` | Cancel a running task |
| `tasks/send` | Send a task-related message |

### tasks/get Example

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tasks/get",
  "params": {
    "taskId": "task-s08"
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "taskId": "task-s08",
    "status": "completed"
  }
}
```

### tasks/cancel Example

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tasks/cancel",
  "params": {
    "taskId": "task-s09"
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "taskId": "task-s09",
    "status": "cancelled"
  }
}
```

## Custom Methods

KubeMQ is method-agnostic — any JSON-RPC method name is forwarded to the agent. The agent decides how to handle it.

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "custom/action",
  "params": {
    "data": "s10-custom"
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "echo": {
      "jsonrpc": "2.0",
      "id": 4,
      "method": "custom/action",
      "params": { "data": "s10-custom" }
    }
  }
}
```

## Header Forwarding

Custom headers prefixed with `X-` are forwarded to the agent. Sensitive headers are stripped.

| Forwarded | Stripped |
|-----------|---------|
| `X-Custom-Header` | `Authorization` |
| `X-Request-ID` | `Cookie` |
| `Content-Type` | `Proxy-Authorization` |
| `Accept` | `X-Forwarded-For` |

KubeMQ injects `X-KubeMQ-Caller-ID` to identify the calling client.

## Concurrent Requests

Multiple simultaneous requests to the same agent are supported up to the per-agent concurrency limit (100). Requests beyond this limit receive JSON-RPC error `-32603`.

See [Concurrency Guide](../guides/concurrency.md) for details.

## See Also

- [Streaming](streaming.md) — SSE-based async messaging
- [Error Handling](error-handling.md) — timeout, not-found, and validation errors
- [JSON-RPC Reference](../reference/json-rpc-reference.md) — full request/response format
