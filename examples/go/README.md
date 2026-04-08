# Go examples

KubeMQ A2A examples using only the **Go standard library** (`net/http`, `encoding/json`, `bufio`, etc.). There is **no** `a2a-go` module dependency in this tree: agents and clients are minimal JSON-RPC over HTTP, matching the reference implementation style in the plan.

## Requirements

- Go 1.21+

## Module

The module path is `github.com/kubemq/kubemq-a2a/examples/go` (see [go.mod](go.mod)).

## Sync

From this directory:

```bash
go mod tidy
```

## Run an example

Replace `{category}` and `{name}` (for example `sync/basic-send`).

**Terminal 1 — agent** (skip for client-only examples):

```bash
cd examples/go
go run ./registry/register-agent/agent.go
# or: go run ./{category}/{name}/agent.go
```

**Terminal 2 — client:**

```bash
cd examples/go
go run ./{category}/{name}/client.go
```

Use the exact path once example files exist, for example:

```bash
go run ./sync/basic-send/client.go
```

## Environment

Examples use `http://localhost:9090` as the default KubeMQ base URL unless you change the constants in each program.

## Stack (see spec §5.4, plan Phase 2)

| Role | Library |
|------|---------|
| HTTP server / client | `net/http` |
| JSON | `encoding/json` |
| SSE line read | `bufio` |

Official `a2a-go` is documented in the spec for ecosystem reference; these examples stay stdlib-only by design.
