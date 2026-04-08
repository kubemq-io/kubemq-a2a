# KubeMQ A2A — Documentation

Documentation for the KubeMQ A2A (Agent-to-Agent) JSON-RPC 2.0 endpoint and agent registry.

## Contents

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | A2A gateway architecture, request flow, JSON-RPC 2.0 transport |
| [getting-started.md](getting-started.md) | Register an agent and send your first message in 5 minutes |
| [configuration.md](configuration.md) | Environment variables, timeouts, concurrency limits |
| **Patterns** | |
| [patterns/registry.md](patterns/registry.md) | Agent registration, listing, heartbeat, deregistration |
| [patterns/sync-messaging.md](patterns/sync-messaging.md) | message/send, tasks/get, tasks/cancel, custom methods |
| [patterns/streaming.md](patterns/streaming.md) | SSE via POST and GET, event types, keepalive |
| [patterns/error-handling.md](patterns/error-handling.md) | JSON-RPC error codes, transport vs application errors |
| [patterns/agent-cards.md](patterns/agent-cards.md) | Platform card, individual agent cards, .well-known |
| **Guides** | |
| [guides/building-agents.md](guides/building-agents.md) | How to build an A2A-compliant agent server |
| [guides/sse-behavior.md](guides/sse-behavior.md) | SSE protocol details, reconnection, keepalive |
| [guides/concurrency.md](guides/concurrency.md) | Concurrency limits, timeout behavior, rate limiting |
| [guides/authentication.md](guides/authentication.md) | Auth headers, JWT tokens, header forwarding |
| **Reference** | |
| [reference/endpoints.md](reference/endpoints.md) | Full endpoint reference (registry + A2A) |
| [reference/json-rpc-reference.md](reference/json-rpc-reference.md) | JSON-RPC 2.0 request/response format |
| [reference/error-codes.md](reference/error-codes.md) | JSON-RPC error codes with KubeMQ-specific codes |

## Examples

Working code examples in 5 languages are in [../examples/](../examples/README.md).

## Prerequisites

All examples and documentation assume:
- KubeMQ server running with A2A gateway enabled
- Default A2A endpoint: `http://localhost:9090/a2a/{agent_id}`
- Default registry endpoint: `http://localhost:9090/agents/*`
- Default metrics endpoint: `http://localhost:8080/metrics`
