# Building Agents

This guide covers how to build an A2A-compliant agent server that works with KubeMQ.

## Agent Server Requirements

An A2A agent is an HTTP server that:

1. Listens on a URL (e.g., `http://localhost:18080/`)
2. Accepts POST requests with JSON-RPC 2.0 bodies
3. Returns JSON-RPC 2.0 responses (or SSE streams for `message/stream`)

## message/send Handler

Parse the incoming JSON-RPC request, process it, and return a JSON-RPC response:

```
POST / HTTP/1.1
Content-Type: application/json

→ {"jsonrpc": "2.0", "id": 1, "method": "message/send", "params": {...}}
← {"jsonrpc": "2.0", "id": 1, "result": {...}}
```

The handler must:
- Parse the JSON body to extract `method`, `id`, and `params`
- Process the request based on the method
- Return a JSON response with the same `id`

## message/stream Handler

For streaming responses, return an SSE stream:

```
POST / HTTP/1.1
Content-Type: application/json
Accept: text/event-stream

→ {"jsonrpc": "2.0", "id": 1, "method": "message/stream", "params": {...}}

← HTTP/1.1 200 OK
← Content-Type: text/event-stream
←
← event: task.status
← data: {"type": "status_update", "payload": {"status": "working", "progress": 1, "total": 5}}
←
← event: task.done
← data: {"type": "done", "payload": {"result": "complete"}}
```

The handler must:
- Set `Content-Type: text/event-stream`
- Write SSE-formatted events (`event: {type}\ndata: {json}\n\n`)
- End with a terminal event (`task.done` or `task.error`)

## Registration Flow

The recommended startup sequence:

```
1. Start HTTP server on a port
2. Wait for server to be ready (accepting connections)
3. POST agent card to KubeMQ /agents/register
4. Begin handling requests
```

Always start the server before registering — KubeMQ may immediately route requests to the agent.

## Heartbeat Loop

Periodically send heartbeats to maintain registration and update `last_seen`:

```
POST /agents/heartbeat
{"agent_id": "my-agent"}
```

A typical heartbeat interval is 30–60 seconds. The heartbeat endpoint returns the updated `last_seen` timestamp.

## Graceful Shutdown

Before stopping the agent server:

1. Deregister from KubeMQ: `POST /agents/deregister` with `{"agent_id": "my-agent"}`
2. Wait for in-flight requests to complete
3. Stop the HTTP server

## Per-Language Patterns

### Python

- **HTTP server**: `aiohttp.web.Application` with `app.router.add_post("/", handler)`
- **Async**: All handlers are `async def`
- **Registration**: `httpx.AsyncClient` for HTTP calls to KubeMQ
- **SSE**: `aiohttp.web.StreamResponse` with `write()` for event streaming
- **Run**: `uv run python agent.py`

### TypeScript

- **HTTP server**: `express` with `app.post("/", handler)` and `express.json()` middleware
- **Registration**: Native `fetch()` for HTTP calls to KubeMQ
- **SSE**: Set response headers and `res.write()` for event streaming
- **Run**: `npx tsx agent.ts`

### Java

- **HTTP server**: `com.sun.net.httpserver.HttpServer` (JDK built-in) or Javalin
- **JSON**: `com.fasterxml.jackson.databind.ObjectMapper` for JSON parsing
- **Registration**: `java.net.http.HttpClient` (JDK 11+) for HTTP calls
- **SSE**: Write to `HttpExchange.getResponseBody()` for event streaming
- **Run**: `mvn exec:java -Dexec.mainClass="Agent"`

### Go

- **HTTP server**: `net/http` standard library with `http.HandleFunc("/", handler)`
- **JSON**: `encoding/json` for marshaling/unmarshaling
- **Registration**: `http.Post()` for HTTP calls to KubeMQ
- **SSE**: Set headers and `http.Flusher` for event streaming
- **Run**: `go run agent.go`

### C# / .NET

- **HTTP server**: ASP.NET Core minimal API with `app.MapPost("/", handler)`
- **JSON**: `System.Text.Json` for serialization
- **Registration**: `HttpClient` for HTTP calls to KubeMQ
- **SSE**: Write to `HttpContext.Response.Body` for event streaming
- **Run**: `dotnet run --project . -- agent`

## See Also

- [Registry Pattern](../patterns/registry.md) — registration API details
- [SSE Behavior](sse-behavior.md) — SSE protocol details for stream handlers
- [Getting Started](../getting-started.md) — complete echo agent walkthrough
