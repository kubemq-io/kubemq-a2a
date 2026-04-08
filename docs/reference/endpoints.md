# Endpoint Reference

Complete list of all KubeMQ A2A endpoints.

## Registry Endpoints

| Method | Path | Description | Request Body | Success | Error |
|--------|------|-------------|-------------|---------|-------|
| POST | `/agents/register` | Register an agent | Agent card JSON | 200 + enriched card | 400 (invalid card) |
| GET | `/agents` | List all agents | — | 200 + JSON array | — |
| GET | `/agents/{agent_id}` | Get agent details | — | 200 + agent card | 404 (not found) |
| POST | `/agents/deregister` | Deregister agent (JSON body) | `{"agent_id": "..."}` | 200 | 404 (not found) |
| DELETE | `/agents/{agent_id}` | Deregister agent (REST) | — | 200 | 404 (not found) |
| POST | `/agents/heartbeat` | Send heartbeat | `{"agent_id": "..."}` | 200 | 400 (not found) |

### Query Parameters for GET /agents

| Parameter | Type | Description |
|-----------|------|-------------|
| `skill_tags` | string | Comma-separated tags to filter agents by skill tags |
| `limit` | integer | Maximum number of agents to return |

## Agent Card Endpoints

| Method | Path | Description | Success | Error |
|--------|------|-------------|---------|-------|
| GET | `/.well-known/agent-card.json` | Platform agent card | 200 (name: `"kubemq"`) | — |
| GET | `/a2a/{agent_id}/.well-known/agent-card.json` | Individual agent card | 200 + enriched card | 404 (not found) |

## A2A Endpoints

| Method | Path | Description | Request Body | Success | Error |
|--------|------|-------------|-------------|---------|-------|
| POST | `/a2a/{agent_id}` | JSON-RPC 2.0 request (sync or stream) | JSON-RPC 2.0 payload | JSON-RPC result or SSE stream | JSON-RPC error |
| GET | `/a2a/{agent_id}` | Not supported | — | — | 405 Method Not Allowed |
| GET | `/a2a/{agent_id}/stream` | SSE stream via GET | — | SSE event stream | — |

## Endpoint Details

### POST /agents/register

Registers an agent with KubeMQ. The request body must be a valid agent card JSON object.

**Required fields:** `agent_id`, `name`, `url`

**Agent ID constraints:** Lowercase, 2+ characters, alphanumeric + hyphens only.

**Idempotent:** Re-registering the same `agent_id` preserves `registered_at` and updates `last_seen`.

**Response:** Returns the enriched agent card with server-managed fields (`registered_at`, `last_seen`).

### POST /a2a/{agent_id}

The primary A2A endpoint. Behavior depends on the JSON-RPC method:

| Method | Behavior | Response |
|--------|----------|----------|
| `message/send` | Synchronous proxy to agent | JSON-RPC response |
| `message/stream` | SSE stream proxy | `text/event-stream` |
| `tasks/get` | Forwarded to agent | JSON-RPC response |
| `tasks/cancel` | Forwarded to agent | JSON-RPC response |
| `tasks/send` | Forwarded to agent | JSON-RPC response |
| Any other method | Forwarded to agent | JSON-RPC response |

**Timeout:** Specified in `params.configuration.timeout`, capped at 3600s, with ~10s server-side gateway buffer.

**Concurrency:** Limited to 100 concurrent requests per agent.

### GET /a2a/{agent_id}/stream

Opens an SSE stream without sending a JSON-RPC request body. The agent determines what events to push.

**Headers:** `Accept: text/event-stream` recommended. Custom `X-*` headers are forwarded.

## See Also

- [JSON-RPC Reference](json-rpc-reference.md) — request/response format
- [Error Codes](error-codes.md) — error code table
- [Registry Pattern](../patterns/registry.md) — registration workflow
