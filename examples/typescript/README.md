# TypeScript examples

KubeMQ A2A examples using **Express** for the agent HTTP server and native **`fetch`** for registry and A2A calls. **`@a2a-js/sdk`** is included to match the official SDK; examples use hand-built JSON-RPC payloads per the spec.

## Requirements

- Node.js 18+ (native `fetch`)

## Install

From this directory:

```bash
npm install
```

Typecheck (optional):

```bash
npx tsc --noEmit
```

## Run an example

Replace `{category}` and `{name}` (for example `sync/basic-send`).

**Terminal 1 — agent** (skip for client-only examples):

```bash
cd examples/typescript
npx tsx {category}/{name}/agent.ts
```

**Terminal 2 — client:**

```bash
cd examples/typescript
npx tsx {category}/{name}/client.ts
```

## Environment

Default KubeMQ base URL is `http://localhost:9090` in each script unless edited.

## Stack (see spec §5.2)

| Role | Library |
|------|---------|
| A2A SDK (declared) | `@a2a-js/sdk` |
| Agent HTTP server | `express` |
| HTTP client | Node.js `fetch` |
| SSE client | `fetch` with `Accept: text/event-stream` + stream parsing |

See [package.json](package.json) and [tsconfig.json](tsconfig.json).
