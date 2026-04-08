# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_A2A_ENABLE` | `false` | Enable the A2A gateway |
| `KUBEMQ_A2A_PORT` | `9090` | HTTP port (shared with REST, MCP, CE connectors) |

## Server Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Address | `http://localhost:9090` | A2A endpoint base URL |
| Metrics address | `http://localhost:8080` | Prometheus metrics endpoint |
| TLS | Disabled | Enable via KubeMQ TLS configuration |

## Agent Configuration

### Timeout Settings

| Setting | Value | Description |
|---------|-------|-------------|
| Default timeout | Server default | Applied when no `timeout` is specified in `params.configuration` |
| Max timeout (MaxTimeoutSeconds) | 3600s | User-specified timeouts above this value are capped |
| Server-side gateway buffer | ~10s | KubeMQ adds ~10s to the user timeout before timing out the proxy request to the agent |
| Client-side HTTP timeout padding | 15s | The burn-in A2AClient adds 15s to the httpx client timeout to prevent the HTTP client from timing out before the gateway does |

The timeout chain works as follows:

```
User specifies: timeout = T seconds
  │
  ├─ Server caps at: min(T, 3600)
  │
  ├─ Server gateway timeout: T + ~10s
  │    (KubeMQ waits this long for the agent to respond)
  │
  └─ Client HTTP timeout: T + 15s
       (httpx/fetch waits this long for KubeMQ to respond)
```

### Concurrency Limits

| Setting | Value | Description |
|---------|-------|-------------|
| Per-agent concurrent requests | 100 | Maximum simultaneous requests to a single agent |
| Overflow behavior | JSON-RPC error `-32603` | Request 101+ receives an error response |

### Response Limits

| Setting | Value | Description |
|---------|-------|-------------|
| Max response size | 10 MB | Agent responses exceeding this size are rejected with error `-32603` |

## Metrics Configuration

KubeMQ exposes Prometheus metrics at the metrics endpoint (default `http://localhost:8080/metrics`).

### A2A-Specific Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `kubemq_a2a_requests_total` | Counter | `agent_id`, `method` | Total A2A requests |
| `kubemq_a2a_sse_streams_active` | Gauge | `agent_id` | Currently active SSE streams |
| `process_resident_memory_bytes` | Gauge | — | KubeMQ process memory (standard Go metric) |

### Method Label Values

The `method` label on `kubemq_a2a_requests_total` reflects the JSON-RPC method name:

| JSON-RPC Method | Metric Label |
|----------------|-------------|
| `message/send` | `method="message/send"` |
| `message/stream` | `method="message/stream"` |
| `tasks/get` | `method="tasks/get"` |
| `tasks/cancel` | `method="tasks/cancel"` |
| `tasks/send` | `method="tasks/send"` |
| Any other method | `method="unknown"` |
