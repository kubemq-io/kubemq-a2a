# Concurrency

Concurrency limits, timeout behavior, and rate limiting for the KubeMQ A2A gateway.

## Per-Agent Concurrency Limit

Each agent has a maximum of **100 concurrent requests**. This includes both sync (`message/send`) and streaming (`message/stream`) requests.

| Request # | Behavior |
|-----------|----------|
| 1–100 | Processed normally |
| 101+ | Rejected with JSON-RPC error `-32603` |

### Overflow Error

```json
{
  "jsonrpc": "2.0",
  "id": 101,
  "error": {
    "code": -32603,
    "message": "internal error: concurrency limit exceeded"
  }
}
```

The concurrency limit is per-agent, not per-client. Multiple clients sending to the same agent share the same limit.

## Timeout Capping

User-specified timeouts in `params.configuration.timeout` are capped at `MaxTimeoutSeconds = 3600` (1 hour). Values above this threshold are silently reduced.

| User Timeout | Effective Timeout |
|-------------|-------------------|
| 30 | 30s |
| 3600 | 3600s |
| 99999 | 3600s (capped) |
| Not specified | Server default |

## Timeout Buffers

Two separate timeout buffers prevent false timeouts:

### Server-Side Gateway Buffer (~10s)

KubeMQ adds approximately 10 seconds to the user-specified timeout before timing out the proxy request to the agent. This accounts for network latency and agent startup overhead.

```
Agent proxy timeout = min(user_timeout, 3600) + ~10s
```

### Client-Side HTTP Timeout Padding (15s)

The burn-in A2AClient adds 15 seconds to the httpx client timeout to ensure the HTTP client does not time out before the gateway:

```
HTTP client timeout = user_timeout + 15s
```

### Combined Timeline

```
User timeout: T seconds
                     │
├────── T ──────────►│ Agent processing deadline
├────── T + ~10s ───►│ Gateway proxy timeout
├────── T + 15s ────►│ HTTP client timeout
```

## Default Timeout

When no `timeout` is specified in `params.configuration`, KubeMQ applies a server-configured default timeout. Requests succeed as long as the agent responds within this default window.

## High-Frequency Operations

The registry API supports high-frequency operations:

| Operation | Tested Rate | Description |
|-----------|-------------|-------------|
| Register/deregister cycles | 50+ rapid cycles | All cycles succeed without errors |
| Heartbeats | 100+ rapid heartbeats | All heartbeats succeed |

## Response Size Limit

Agent responses are limited to **10 MB**. Responses exceeding this size are rejected:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "internal error: response too large"
  }
}
```

## Monitoring

Use Prometheus metrics to monitor concurrency:

| Metric | Description |
|--------|-------------|
| `kubemq_a2a_requests_total` | Total requests per agent/method |
| `kubemq_a2a_sse_streams_active` | Currently active SSE streams per agent |

## See Also

- [Configuration](../configuration.md) — timeout and limit settings
- [Error Handling](../patterns/error-handling.md) — concurrency and timeout errors
- [Streaming](../patterns/streaming.md) — SSE stream concurrency
