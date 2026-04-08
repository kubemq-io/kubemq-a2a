# SSE Behavior

Detailed protocol behavior for Server-Sent Event (SSE) streams through the KubeMQ A2A gateway.

## SSE Format

Each SSE event consists of an `event:` line and a `data:` line, followed by a blank line:

```
event: {event_type}
data: {json_payload}

```

The `Content-Type` for SSE responses is `text/event-stream`.

## Event Types

| Event Type | Type Field | Description | Terminal |
|-----------|-----------|-------------|----------|
| `task.status` | `status_update` | Progress updates with status, progress, total | No |
| `task.artifact` | `artifact` | Intermediate artifact delivery | No |
| `task.done` | `done` | Successful completion | Yes |
| `task.error` | `error` | Failure | Yes |

### Status Update Payload

```json
{"type": "status_update", "payload": {"status": "working", "progress": 3, "total": 10}}
```

### Artifact Payload

```json
{"type": "artifact", "payload": {"name": "result.json", "data": {"key": "value"}}}
```

### Done Payload

```json
{"type": "done", "payload": {"final_result": "completed", "event_count": 10}}
```

### Error Payload

```json
{"type": "error", "payload": {"code": -32001, "message": "agent timeout"}}
```

## Terminal Events

`task.done` and `task.error` are terminal events. After receiving either:

1. The client should stop reading from the stream
2. KubeMQ closes the proxy connection
3. The `kubemq_a2a_sse_streams_active` metric decreases

## Keepalive Comments

KubeMQ sends keepalive comments every ~30 seconds to prevent proxy/load-balancer connection timeouts:

```
: keepalive

```

Keepalive lines start with `:` (the SSE comment prefix). They are not events and contain no `data:` line. SSE client libraries typically ignore comment lines automatically.

## Client-Side Reconnection

KubeMQ A2A streams are not resumable — there is no event ID or `Last-Event-ID` support. If a client disconnects:

- The stream cannot be resumed from where it left off
- The client must send a new request to start a fresh stream
- Any undelivered events are lost

### Reconnection Strategy

For long-running tasks, consider:

1. Using `contextId` to correlate the new stream with the original request
2. Implementing idempotent processing on the agent side
3. Using `tasks/get` to check task status before re-streaming

## Concurrent Streams

Multiple SSE streams can be open simultaneously:

- Multiple streams to the **same agent** are allowed (each counts against the concurrency limit)
- Multiple streams to **different agents** are independent
- The `kubemq_a2a_sse_streams_active` metric tracks all active streams per agent

## Large Payloads

SSE events can carry large payloads (10 KB+ message parts). Each event's `data:` field contains a single JSON line. Multi-line JSON must be serialized to a single line.

## Agent Implementation Notes

When implementing SSE on the agent side:

1. Set `Content-Type: text/event-stream` on the response
2. Disable response buffering (flush after each event)
3. Use the SSE format: `event: {type}\ndata: {json}\n\n`
4. Send a terminal event (`task.done` or `task.error`) to signal completion
5. For long-running tasks, send periodic `task.status` events to prevent idle timeout

## See Also

- [Streaming Pattern](../patterns/streaming.md) — streaming usage patterns
- [Building Agents](building-agents.md) — implementing stream handlers
- [Concurrency Guide](concurrency.md) — concurrent stream limits
