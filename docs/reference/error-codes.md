# Error Codes

JSON-RPC 2.0 error codes used by the KubeMQ A2A gateway.

## Error Code Table

| Code | Name | Description | Trigger |
|------|------|-------------|---------|
| `-32700` | Parse Error | Invalid JSON or wrong Content-Type | Malformed JSON body, `Content-Type` is not `application/json` |
| `-32600` | Invalid Request | Missing required fields or invalid format | Missing `method` field, `jsonrpc` != `"2.0"`, empty/invalid `agent_id` |
| `-32601` | Method Not Found | Unsupported method | Reserved; KubeMQ forwards all methods to agents |
| `-32602` | Invalid Params | Invalid parameters | Malformed `params` object |
| `-32001` | Agent Timeout | Agent did not respond within timeout | Slow agent + user-specified timeout exceeded |
| `-32002` | Agent Not Found | No agent registered with given ID | `agent_id` not in registry |
| `-32603` | Internal Error | Server-side failure | Concurrency limit (>100), response too large (>10 MB), agent HTTP 500 |

## Error Response Payloads

### Parse Error (-32700)

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "error": {
    "code": -32700,
    "message": "parse error: invalid JSON"
  }
}
```

**Triggers:**
- Invalid JSON body (e.g., `{invalid json!!!}`)
- Wrong `Content-Type` header (e.g., `text/plain` instead of `application/json`)

**Note:** The `id` field is `null` because the server cannot parse the request to extract the ID.

### Invalid Request (-32600)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "invalid request: missing method field"
  }
}
```

**Triggers:**
- Missing `method` field in the JSON-RPC request
- Invalid `jsonrpc` version (e.g., `"1.0"` instead of `"2.0"`)
- Empty `agent_id` in the URL path
- Invalid `agent_id` format (uppercase letters, special characters)

### Agent Timeout (-32001)

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

**Triggers:**
- Agent does not respond within `params.configuration.timeout` seconds
- Timeout is capped at MaxTimeoutSeconds=3600
- KubeMQ adds ~10s server-side gateway buffer before timing out
- The burn-in A2AClient separately adds 15s to the httpx client timeout

### Agent Not Found (-32002)

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

**Triggers:**
- The `agent_id` in the URL path (`/a2a/{agent_id}`) is not registered
- The agent was previously registered but has been deregistered

### Internal Error (-32603)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "internal error: concurrency limit exceeded"
  }
}
```

**Triggers:**
- Per-agent concurrency limit (100 concurrent requests) exceeded
- Agent response body exceeds 10 MB size limit
- Agent returns HTTP 500 Internal Server Error
- Agent connection refused (registered URL is unreachable)

## HTTP Status Code Mapping

When an agent returns an HTTP error, KubeMQ maps it to a JSON-RPC error:

| Agent HTTP Status | JSON-RPC Code | Error Message Contains |
|-------------------|--------------|----------------------|
| 400 | `-32603` | "400" or error details |
| 500 | `-32603` | "500" or error details |
| 502 | `-32603` | "unavailable" or "502" |
| 503 | `-32603` | "unavailable" or "503" |
| 504 | `-32001` | "timeout" or "504" |

## See Also

- [Error Handling Pattern](../patterns/error-handling.md) — transport vs application errors
- [Concurrency Guide](../guides/concurrency.md) — concurrency limit details
- [JSON-RPC Reference](json-rpc-reference.md) — request/response format
