# Agent Cards

Agent cards describe an agent's capabilities and are accessible via `.well-known` endpoints following the A2A protocol convention.

## Platform Agent Card

The KubeMQ platform itself exposes an agent card:

```
GET /.well-known/agent-card.json
```

Response:

```json
{
  "name": "kubemq",
  "description": "KubeMQ A2A Gateway",
  "version": "latest",
  "url": "http://localhost:9090/",
  "skills": [],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "protocolVersions": ["1.0"]
}
```

The platform card represents the KubeMQ gateway itself (name is always `"kubemq"`), not any individual agent.

## Individual Agent Card

Each registered agent has a `.well-known` endpoint:

```
GET /a2a/{agent_id}/.well-known/agent-card.json
```

This returns the **enriched** agent card — the original registration fields plus server-managed fields (`registered_at`, `last_seen`) that KubeMQ adds upon registration. It is the same representation returned by `GET /agents/{agent_id}`.

Example response:

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
  "protocolVersions": ["1.0"],
  "registered_at": "2026-04-06T10:00:00Z",
  "last_seen": "2026-04-06T10:05:00Z"
}
```

## Agent Card Schema

Full schema with all required and optional fields:

```json
{
  "agent_id": "string (required, lowercase, 2+ chars, alphanumeric + hyphens)",
  "name": "string (required)",
  "description": "string (optional)",
  "version": "string (optional, e.g., '1.0.0')",
  "url": "string (required, absolute URL, e.g., 'http://localhost:18080/')",
  "skills": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "tags": ["string"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "protocolVersions": ["1.0"]
}
```

### Server-Managed Fields

These fields are added by KubeMQ and returned in responses but should not be sent during registration:

| Field | Type | Description |
|-------|------|-------------|
| `registered_at` | string (ISO 8601) | Timestamp of first registration |
| `last_seen` | string (ISO 8601) | Timestamp of last heartbeat or re-registration |

## Non-existent Agent Card

Requesting a `.well-known` card for a non-existent agent returns HTTP 404.

## See Also

- [Registry Pattern](registry.md) — agent registration and management
- [Building Agents](../guides/building-agents.md) — implementing the registration flow
- [Endpoints Reference](../reference/endpoints.md) — complete endpoint table
