# Authentication

How KubeMQ handles authentication headers in A2A requests.

> **Scope note:** JWT integration is documented for awareness but is out of scope for examples and burn-in. This guide covers the header forwarding pattern only — specifically how KubeMQ handles authentication-related headers.

## Header Stripping

KubeMQ strips the following headers before forwarding requests to agents:

| Header | Reason |
|--------|--------|
| `Authorization` | Prevents credential leakage to agent servers |
| `Cookie` | Prevents session hijacking |
| `Proxy-Authorization` | Prevents proxy credential leakage |
| `X-Forwarded-For` | Prevents IP spoofing |

These headers are consumed by KubeMQ's auth middleware (if enabled) and are never visible to the agent.

## Custom Headers

Custom headers prefixed with `X-` are forwarded to agents:

```
POST /a2a/echo-agent-01 HTTP/1.1
Content-Type: application/json
Authorization: Bearer eyJhbG...     ← stripped by KubeMQ
X-Custom-Header: my-value           ← forwarded to agent
X-Request-ID: req-12345             ← forwarded to agent
```

The agent receives:

```
POST / HTTP/1.1
Content-Type: application/json
X-Custom-Header: my-value
X-Request-ID: req-12345
X-KubeMQ-Caller-ID: client-abc
```

## X-KubeMQ-Caller-ID

KubeMQ automatically injects the `X-KubeMQ-Caller-ID` header into every request forwarded to an agent. This header identifies the calling client and is always present regardless of whether authentication is enabled.

## JWT Integration

KubeMQ supports JWT-based authentication at the gateway level. When enabled:

1. Clients include `Authorization: Bearer <token>` in requests
2. KubeMQ validates the token against configured JWKS/signing keys
3. If valid, the request is forwarded (without the `Authorization` header)
4. If invalid, KubeMQ returns an HTTP 401 error before the request reaches any agent

### JWT Configuration

JWT configuration is part of the KubeMQ server configuration, not the A2A-specific configuration. Refer to the KubeMQ documentation for JWT setup details.

### What Agents See

With JWT enabled, agents never see the `Authorization` header. They can rely on `X-KubeMQ-Caller-ID` for caller identification. If additional claims need to reach the agent, use custom `X-` headers.

## See Also

- [Architecture](../architecture.md) — header forwarding overview
- [Sync Messaging](../patterns/sync-messaging.md) — header forwarding in practice
- [Configuration](../configuration.md) — server configuration
