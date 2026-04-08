# SSE Streaming

KubeMQ proxies Server-Sent Event (SSE) streams from agent servers to clients, supporting both POST-based and GET-based streaming.

## POST Streaming

Send a JSON-RPC request with `method: "message/stream"`:

```
POST /a2a/{agent_id}
Content-Type: application/json
Accept: text/event-stream
```

### Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/stream",
  "params": {
    "message": {
      "parts": [
        { "text": "Stream me some updates" }
      ]
    }
  }
}
```

### SSE Response

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: task.status
data: {"type": "status_update", "payload": {"status": "working", "progress": 1, "total": 10}}

event: task.status
data: {"type": "status_update", "payload": {"status": "working", "progress": 2, "total": 10}}

event: task.done
data: {"type": "done", "payload": {"final_result": "completed", "event_count": 10}}

```

## GET Streaming

For server-push scenarios where the agent streams without a client-initiated JSON-RPC request:

```
GET /a2a/{agent_id}/stream
Accept: text/event-stream
```

No request body is sent. Optional custom headers (e.g., `X-Custom-Header`) are forwarded to the agent.

### POST vs GET Streaming

| Aspect | POST `/a2a/{agent_id}` | GET `/a2a/{agent_id}/stream` |
|--------|------------------------|------------------------------|
| Request body | JSON-RPC 2.0 payload | None |
| Content-Type | `application/json` | `Accept: text/event-stream` |
| Use case | Client sends message, agent streams response | Agent pushes events without client prompt |

## SSE Event Types

### task.status

Progress updates during processing:

```
event: task.status
data: {"type": "status_update", "payload": {"status": "working", "progress": 3, "total": 10}}

```

### task.artifact

Intermediate artifact delivery:

```
event: task.artifact
data: {"type": "artifact", "payload": {"name": "result.json", "data": {"key": "value"}}}

```

### task.done (Terminal)

Successful completion — the client should stop reading after this event:

```
event: task.done
data: {"type": "done", "payload": {"final_result": "completed", "event_count": 10}}

```

### task.error (Terminal)

Failure — the client should stop reading after this event:

```
event: task.error
data: {"type": "error", "payload": {"code": -32001, "message": "agent timeout"}}

```

## Keepalive

KubeMQ sends keepalive comments every ~30 seconds to prevent connection timeouts:

```
: keepalive

```

Keepalive lines start with `:` (SSE comment syntax) and are not events. SSE clients should ignore them.

## Idle Timeout

If no events are sent for a configurable idle period, KubeMQ closes the stream. Agents should send periodic status updates for long-running tasks to keep the stream alive.

## Client Disconnect

When a client disconnects from an SSE stream:

1. KubeMQ detects the disconnection
2. The proxy connection to the agent is cleaned up
3. The `kubemq_a2a_sse_streams_active` metric decreases

## Event Ordering

Progress events from an agent are delivered in order. When an agent sends sequential `task.status` events with increasing `progress` values, the client receives them in the same monotonically increasing order.

## Header Forwarding

Streaming requests follow the same header forwarding rules as sync requests — `X-Custom-*` headers are forwarded, sensitive headers are stripped.

## See Also

- [SSE Behavior Guide](../guides/sse-behavior.md) — protocol details, reconnection strategies
- [Sync Messaging](sync-messaging.md) — synchronous request/reply pattern
- [Building Agents](../guides/building-agents.md) — implementing SSE on the agent side
