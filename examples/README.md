# Master example index — KubeMQ A2A

Copy-paste-ready examples for the KubeMQ A2A JSON-RPC gateway and agent registry, mirrored across five languages. Each scenario lives under the language folder in `registry/`, `sync/`, `streaming/`, `errors/`, or `limits/`.

**Prerequisites:** KubeMQ with A2A enabled (default `http://localhost:9090` for API, `http://localhost:8080` for metrics).

## Per-language setup

| Language | Guide |
|----------|--------|
| Python | [python/README.md](python/README.md) |
| TypeScript | [typescript/README.md](typescript/README.md) |
| Java | [java/README.md](java/README.md) |
| Go | [go/README.md](go/README.md) |
| C# | [csharp/README.md](csharp/README.md) |

## Example matrix (19 scenarios × 5 languages)

Rows are grouped by category: **5 registry**, **5 sync**, **4 streaming**, **3 errors**, **2 limits**. Each language column links to that scenario’s directory (sources added in Phases 3–7).

| # | Category | Scenario | Key concept | Python | TypeScript | Java | Go | C# |
|---|----------|----------|-------------|--------|------------|------|----|-----|
| 1 | Registry | register-agent | Register an agent card and verify with `GET /agents/{id}` | [dir](python/registry/register-agent/) | [dir](typescript/registry/register-agent/) | [dir](java/registry/register-agent/) | [dir](go/registry/register-agent/) | [dir](csharp/registry/register-agent/) |
| 2 | Registry | list-agents | `GET /agents` and optional `skill_tags` filtering | [dir](python/registry/list-agents/) | [dir](typescript/registry/list-agents/) | [dir](java/registry/list-agents/) | [dir](go/registry/list-agents/) | [dir](csharp/registry/list-agents/) |
| 3 | Registry | agent-info | Full agent card (optional fields) via registry | [dir](python/registry/agent-info/) | [dir](typescript/registry/agent-info/) | [dir](java/registry/agent-info/) | [dir](go/registry/agent-info/) | [dir](csharp/registry/agent-info/) |
| 4 | Registry | deregister-agent | `POST /agents/deregister` and `DELETE /agents/{id}` | [dir](python/registry/deregister-agent/) | [dir](typescript/registry/deregister-agent/) | [dir](java/registry/deregister-agent/) | [dir](go/registry/deregister-agent/) | [dir](csharp/registry/deregister-agent/) |
| 5 | Registry | heartbeat | `POST /agents/heartbeat` and `last_seen` updates | [dir](python/registry/heartbeat/) | [dir](typescript/registry/heartbeat/) | [dir](java/registry/heartbeat/) | [dir](go/registry/heartbeat/) | [dir](csharp/registry/heartbeat/) |
| 6 | Sync | basic-send | `message/send` JSON-RPC echo through `/a2a/{agent_id}` | [dir](python/sync/basic-send/) | [dir](typescript/sync/basic-send/) | [dir](java/sync/basic-send/) | [dir](go/sync/basic-send/) | [dir](csharp/sync/basic-send/) |
| 7 | Sync | header-forwarding | Custom `X-*` headers proxied to the agent | [dir](python/sync/header-forwarding/) | [dir](typescript/sync/header-forwarding/) | [dir](java/sync/header-forwarding/) | [dir](go/sync/header-forwarding/) | [dir](csharp/sync/header-forwarding/) |
| 8 | Sync | context-id | `contextId` in JSON-RPC params | [dir](python/sync/context-id/) | [dir](typescript/sync/context-id/) | [dir](java/sync/context-id/) | [dir](go/sync/context-id/) | [dir](csharp/sync/context-id/) |
| 9 | Sync | custom-method | Non-standard JSON-RPC method name | [dir](python/sync/custom-method/) | [dir](typescript/sync/custom-method/) | [dir](java/sync/custom-method/) | [dir](go/sync/custom-method/) | [dir](csharp/sync/custom-method/) |
| 10 | Sync | concurrent-requests | Many parallel `message/send` calls | [dir](python/sync/concurrent-requests/) | [dir](typescript/sync/concurrent-requests/) | [dir](java/sync/concurrent-requests/) | [dir](go/sync/concurrent-requests/) | [dir](csharp/sync/concurrent-requests/) |
| 11 | Streaming | basic-stream | SSE `message/stream` with `task.status` / `task.done` | [dir](python/streaming/basic-stream/) | [dir](typescript/streaming/basic-stream/) | [dir](java/streaming/basic-stream/) | [dir](go/streaming/basic-stream/) | [dir](csharp/streaming/basic-stream/) |
| 12 | Streaming | task-events | Stream task lifecycle and artifact events | [dir](python/streaming/task-events/) | [dir](typescript/streaming/task-events/) | [dir](java/streaming/task-events/) | [dir](go/streaming/task-events/) | [dir](csharp/streaming/task-events/) |
| 13 | Streaming | keepalive | Long idle periods and SSE keepalive comments | [dir](python/streaming/keepalive/) | [dir](typescript/streaming/keepalive/) | [dir](java/streaming/keepalive/) | [dir](go/streaming/keepalive/) | [dir](csharp/streaming/keepalive/) |
| 14 | Streaming | client-disconnect | Client closes stream while agent still emits | [dir](python/streaming/client-disconnect/) | [dir](typescript/streaming/client-disconnect/) | [dir](java/streaming/client-disconnect/) | [dir](go/streaming/client-disconnect/) | [dir](csharp/streaming/client-disconnect/) |
| 15 | Errors | agent-not-found | JSON-RPC error when the agent is not registered (`-32002`) | [dir](python/errors/agent-not-found/) | [dir](typescript/errors/agent-not-found/) | [dir](java/errors/agent-not-found/) | [dir](go/errors/agent-not-found/) | [dir](csharp/errors/agent-not-found/) |
| 16 | Errors | timeout | Agent slower than `params.configuration.timeout` (`-32001`) | [dir](python/errors/timeout/) | [dir](typescript/errors/timeout/) | [dir](java/errors/timeout/) | [dir](go/errors/timeout/) | [dir](csharp/errors/timeout/) |
| 17 | Errors | invalid-request | Malformed JSON-RPC (bad JSON, missing method, wrong `jsonrpc`) | [dir](python/errors/invalid-request/) | [dir](typescript/errors/invalid-request/) | [dir](java/errors/invalid-request/) | [dir](go/errors/invalid-request/) | [dir](csharp/errors/invalid-request/) |
| 18 | Limits | concurrency-limit | Per-agent concurrency cap exceeded (`-32603`) | [dir](python/limits/concurrency-limit/) | [dir](typescript/limits/concurrency-limit/) | [dir](java/limits/concurrency-limit/) | [dir](go/limits/concurrency-limit/) | [dir](csharp/limits/concurrency-limit/) |
| 19 | Limits | response-size | Agent response larger than gateway limit | [dir](python/limits/response-size/) | [dir](typescript/limits/response-size/) | [dir](java/limits/response-size/) | [dir](go/limits/response-size/) | [dir](csharp/limits/response-size/) |

### File layout per scenario

- **Python:** `agent.py`, `client.py`, `README.md` (except client-only scenarios: no `agent.py`).
- **TypeScript:** `agent.ts`, `client.ts`, `README.md` (same exceptions).
- **Java:** `Agent.java`, `Client.java`, `README.md` (same exceptions).
- **Go:** `agent.go`, `client.go`, `README.md` (same exceptions).
- **C#:** `Agent.cs`, `Client.cs`, example-local `.csproj`, `README.md` (same exceptions).

See the [specification](../../.work/tasks/kubemq-a2a/spec.md) for JSON-RPC payloads and registry shapes.
