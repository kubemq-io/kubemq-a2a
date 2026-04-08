# JSON-RPC 2.0 Reference

The KubeMQ A2A gateway uses JSON-RPC 2.0 as the wire format for all client-to-agent communication.

## Request Format

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
    "contextId": "optional-correlation-id",
    "configuration": {
      "timeout": 30
    }
  }
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `jsonrpc` | string | Must be `"2.0"` |
| `id` | integer or string | Request identifier, echoed in the response |
| `method` | string | JSON-RPC method name |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `params` | object | Method parameters |
| `params.message` | object | Message payload with `parts` array |
| `params.contextId` | string | Correlation ID for request tracking |
| `params.configuration` | object | Request configuration |
| `params.configuration.timeout` | number | Timeout in seconds (capped at 3600) |

## Response Format (Success)

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

The `result` field contains whatever the agent returns. KubeMQ does not modify the result payload.

## Response Format (Error)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32002,
    "message": "agent not found: nonexistent-agent"
  }
}
```

### Error Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | integer | Error code (see [Error Codes](error-codes.md)) |
| `message` | string | Human-readable error description |

## Standard Methods

KubeMQ recognizes these standard A2A methods for metrics labeling:

| Method | Description | Metric Label |
|--------|-------------|-------------|
| `message/send` | Send a message, get synchronous response | `method="message/send"` |
| `message/stream` | Send a message, get SSE stream | `method="message/stream"` |
| `tasks/get` | Query task status | `method="tasks/get"` |
| `tasks/cancel` | Cancel a running task | `method="tasks/cancel"` |
| `tasks/send` | Send a task-related message | `method="tasks/send"` |

All other method names are forwarded to the agent but labeled as `method="unknown"` in Prometheus metrics.

## Custom Methods

KubeMQ is method-agnostic. Any JSON-RPC method name is forwarded to the agent:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "custom/action",
  "params": {
    "data": "example"
  }
}
```

The agent is responsible for handling or rejecting unknown methods. KubeMQ does not validate method names beyond checking that the `method` field is present.

## Notification Format

JSON-RPC 2.0 notifications (requests without an `id` field) are forwarded to the agent but receive no response. This is rarely used in A2A.

```json
{
  "jsonrpc": "2.0",
  "method": "notification/event",
  "params": {
    "data": "fire-and-forget"
  }
}
```

## Batch Requests

JSON-RPC 2.0 batch requests (an array of request objects) are not currently supported by the KubeMQ A2A gateway. Send individual requests instead.

## Message Parts

The `params.message.parts` array contains the message content. Each part has a `text` field:

```json
{
  "parts": [
    { "text": "First part of the message" },
    { "text": "Second part of the message" }
  ]
}
```

## Context ID

The `contextId` field enables request correlation across multiple interactions:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": { "parts": [{ "text": "Follow-up" }] },
    "contextId": "ctx-001"
  }
}
```

The `contextId` is passed through to the agent without modification. Agents can use it for conversation threading, session management, or request grouping.

## See Also

- [Error Codes](error-codes.md) — complete error code table
- [Endpoints](endpoints.md) — endpoint paths and methods
- [Sync Messaging](../patterns/sync-messaging.md) — usage patterns
