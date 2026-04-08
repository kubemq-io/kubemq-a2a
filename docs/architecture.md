# Architecture

## Overview

KubeMQ acts as an A2A (Agent-to-Agent) gateway, providing a centralized JSON-RPC 2.0 proxy between A2A clients and agent servers. Clients never connect directly to agents — all traffic flows through KubeMQ, which handles routing, agent discovery, timeout enforcement, concurrency limiting, and SSE stream proxying.

## KubeMQ as A2A Gateway

```
Client ──[JSON-RPC 2.0]──▶ KubeMQ /a2a/{agent_id} ──[HTTP POST]──▶ Agent Server
                                                                        │
Client ◀──[JSON-RPC result]── KubeMQ ◀──[HTTP response]────────────────┘
```

KubeMQ provides:

- **Agent Registry** — REST API for registering, discovering, and managing agents
- **Request Proxying** — Forwards JSON-RPC 2.0 requests to the correct agent based on `agent_id`
- **SSE Stream Proxying** — Transparently proxies Server-Sent Event streams from agents to clients
- **Timeout Enforcement** — Caps and enforces request timeouts with server-side buffers
- **Concurrency Limiting** — Per-agent concurrency limits to prevent overload
- **Header Forwarding** — Selective forwarding of custom headers, stripping of sensitive ones

## Request Flow

### Sync Request (message/send)

```
1. Client POSTs JSON-RPC 2.0 to /a2a/{agent_id}
2. KubeMQ looks up agent_id in the registry
   → If not found: returns JSON-RPC error -32002
3. KubeMQ forwards the request body to the agent's registered URL
   → Forwards allowed headers (X-Custom-*, Content-Type)
   → Injects X-KubeMQ-Caller-ID header
   → Strips sensitive headers (Authorization, Cookie, etc.)
4. Agent processes the request and returns a JSON-RPC response
5. KubeMQ relays the response back to the client
```

### Streaming Request (message/stream)

```
1. Client POSTs JSON-RPC 2.0 with method "message/stream"
   (or GETs /a2a/{agent_id}/stream)
2. KubeMQ looks up agent_id, forwards to agent
3. Agent returns Content-Type: text/event-stream
4. KubeMQ proxies the SSE stream to the client
   → Forwards all event types (task.status, task.done, task.artifact, task.error)
   → Sends keepalive comments every ~30s
5. Stream ends when:
   → Agent sends terminal event (task.done or task.error)
   → Client disconnects
   → Idle timeout expires
```

## Agent Registry

The agent registry is a REST API that agents use to announce themselves to KubeMQ. The registry maintains:

| Field | Source | Description |
|-------|--------|-------------|
| agent_id | Agent | Unique identifier (lowercase, alphanumeric + hyphens, 2+ chars) |
| name | Agent | Human-readable name |
| description | Agent | Optional description |
| version | Agent | Optional version string |
| url | Agent | Agent's HTTP endpoint URL |
| skills | Agent | List of capabilities with tags |
| registered_at | Server | Timestamp of first registration |
| last_seen | Server | Timestamp of last heartbeat or re-registration |

Re-registering an existing agent preserves `registered_at` and updates `last_seen`.

## JSON-RPC 2.0 Transport

KubeMQ uses JSON-RPC 2.0 as the wire format for all A2A communication. The gateway is method-agnostic — it forwards any JSON-RPC method name to the agent, including:

- **Standard methods**: `message/send`, `message/stream`, `tasks/get`, `tasks/cancel`, `tasks/send`
- **Custom methods**: Any string (e.g., `custom/action`, `tools/invoke`)

The agent is responsible for handling or rejecting unknown methods.

## SSE Streaming Model

KubeMQ proxies SSE streams from agent servers to clients. Two streaming modes are supported:

| Mode | Request | Use Case |
|------|---------|----------|
| POST `/a2a/{agent_id}` | JSON-RPC body with `method: "message/stream"` | Client sends message, agent streams response |
| GET `/a2a/{agent_id}/stream` | No body, `Accept: text/event-stream` | Agent pushes events without client prompt |

### SSE Event Types

| Event | Type Field | Description | Terminal |
|-------|-----------|-------------|----------|
| `task.status` | `status_update` | Progress updates (status, progress, total) | No |
| `task.artifact` | `artifact` | Intermediate artifact delivery | No |
| `task.done` | `done` | Successful completion | Yes |
| `task.error` | `error` | Failure | Yes |

Keepalive comments (`: keepalive`) are sent every ~30 seconds to prevent connection timeouts.

## Header Forwarding

KubeMQ selectively forwards headers between clients and agents:

| Header Category | Direction | Behavior |
|----------------|-----------|----------|
| `X-Custom-*` | Client → Agent | **Forwarded** |
| `X-KubeMQ-Caller-ID` | KubeMQ → Agent | **Injected** by KubeMQ |
| `Authorization` | Client → Agent | **Stripped** |
| `Cookie` | Client → Agent | **Stripped** |
| `Proxy-Authorization` | Client → Agent | **Stripped** |
| `X-Forwarded-For` | Client → Agent | **Stripped** |
| `Content-Type` | Client → Agent | Forwarded (must be `application/json`) |
| `Accept` | Client → Agent | Forwarded (`text/event-stream` for SSE) |

## Agent Cards

KubeMQ exposes agent card endpoints following the A2A `.well-known` convention:

| Endpoint | Description |
|----------|-------------|
| `GET /.well-known/agent-card.json` | Platform-level card (name: `"kubemq"`) |
| `GET /a2a/{agent_id}/.well-known/agent-card.json` | Individual agent card (enriched with `registered_at`, `last_seen`) |

The individual agent card returns the same enriched representation as `GET /agents/{agent_id}`.

## Concurrency Model

| Limit | Value | Description |
|-------|-------|-------------|
| Per-agent concurrent requests | 100 | Request 101+ receives JSON-RPC error `-32603` |
| Max timeout | 3600s | User-specified timeouts are capped at this value |
| Server-side gateway buffer | ~10s | KubeMQ adds ~10s to the user timeout before timing out the proxy |
| Client-side timeout padding | 15s | Burn-in A2AClient adds 15s to httpx timeout to prevent premature client timeout |
| Response size limit | 10 MB | Responses exceeding this size are rejected |
