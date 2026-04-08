# Header Forwarding

Demonstrates which HTTP headers KubeMQ forwards to agents and which are stripped.

## What It Shows

- `X-Custom-*` headers are forwarded to the agent
- `Authorization`, `Cookie`, `Proxy-Authorization` headers are stripped
- `X-KubeMQ-Caller-ID` is automatically injected by KubeMQ

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
npx tsx agent.ts
```

Terminal 2 (run the client):
```bash
npx tsx client.ts
```

## Expected Output

```
=== Header Forwarding Results ===
X-Custom-Header:    my-custom-value
X-Request-ID:       req-12345
Authorization:      (stripped - correct)
X-KubeMQ-Caller-ID: ...
```
