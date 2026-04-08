# Agent Registry

The KubeMQ agent registry is a REST API for managing A2A agent lifecycle — registration, discovery, heartbeat, and deregistration.

## Register Agent

Register an agent by posting its agent card to KubeMQ:

```
POST /agents/register
Content-Type: application/json
```

### Agent Card

```json
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  "description": "A simple echo agent for testing",
  "version": "1.0.0",
  "url": "http://localhost:18080/",
  "skills": [
    {
      "id": "echo",
      "name": "Echo",
      "description": "Echoes back the received message",
      "tags": ["test", "echo"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "protocolVersions": ["1.0"]
}
```

### Required Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `agent_id` | string | Lowercase, 2+ characters, alphanumeric + hyphens only |
| `name` | string | Non-empty |
| `url` | string | Absolute URL (e.g., `http://localhost:18080/`) |

### Optional Fields

| Field | Type | Default |
|-------|------|---------|
| `description` | string | `""` |
| `version` | string | `""` |
| `skills` | array | `[]` |
| `defaultInputModes` | array of strings | `["text"]` |
| `defaultOutputModes` | array of strings | `["text"]` |
| `protocolVersions` | array of strings | `["1.0"]` |

### Registration Response

```json
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  "description": "A simple echo agent for testing",
  "version": "1.0.0",
  "url": "http://localhost:18080/",
  "skills": [
    {
      "id": "echo",
      "name": "Echo",
      "description": "Echoes back the received message",
      "tags": ["test", "echo"]
    }
  ],
  "registered_at": "2026-04-06T10:00:00Z",
  "last_seen": "2026-04-06T10:00:00Z"
}
```

The response includes server-managed fields `registered_at` and `last_seen` (ISO 8601 timestamps).

### Agent ID Validation

Requests with invalid `agent_id` values return HTTP 400:

| Invalid ID | Reason |
|-----------|--------|
| `"A"` | Too short (min 2 chars) |
| `"MyAgent"` | Contains uppercase |
| `"agent@1"` | Contains special characters |

## Re-registration

Re-registering an existing `agent_id` is idempotent:
- `registered_at` is **preserved** (original registration time)
- `last_seen` is **updated** to current time

## List Agents

```
GET /agents
GET /agents?skill_tags=echo,test
GET /agents?limit=5
GET /agents?skill_tags=echo&limit=5
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `skill_tags` | string | Comma-separated tags to filter by |
| `limit` | integer | Maximum number of agents to return |

### Response

```json
[
  {
    "agent_id": "echo-agent-01",
    "name": "Echo Agent",
    "description": "A simple echo agent for testing",
    "version": "1.0.0",
    "url": "http://localhost:18080/",
    "skills": [
      {
        "id": "echo",
        "name": "Echo",
        "description": "Echoes back the received message",
        "tags": ["test", "echo"]
      }
    ],
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"],
    "protocolVersions": ["1.0"],
    "registered_at": "2026-04-06T10:00:00Z",
    "last_seen": "2026-04-06T10:05:00Z"
  }
]
```

When using `skill_tags`, only agents whose skills contain at least one matching tag are returned.

## Get Agent

```
GET /agents/{agent_id}
```

Returns the full agent card with server-managed fields. Returns HTTP 404 if the agent is not registered.

## Heartbeat

Heartbeats update the `last_seen` timestamp for a registered agent:

```
POST /agents/heartbeat
Content-Type: application/json

{
  "agent_id": "echo-agent-01"
}
```

### Success Response (200 OK)

```json
{
  "agent_id": "echo-agent-01",
  "last_seen": "2026-04-06T10:05:00Z"
}
```

### Error Response (400 Bad Request)

Returned when the agent is not registered:

```json
{
  "error": "agent not found"
}
```

## Deregister

Two methods are supported:

### POST Method

```
POST /agents/deregister
Content-Type: application/json

{
  "agent_id": "echo-agent-01"
}
```

### DELETE Method

```
DELETE /agents/echo-agent-01
```

Both return HTTP 200 on success and HTTP 404 if the agent is not registered:

```json
{
  "error": "agent not found"
}
```

## See Also

- [Agent Cards](agent-cards.md) — `.well-known` agent card endpoints
- [Building Agents](../guides/building-agents.md) — how to implement the registration flow
- [Endpoints Reference](../reference/endpoints.md) — complete endpoint table
