# Invalid Request

Demonstrates various JSON-RPC validation errors returned by KubeMQ.

## What It Shows

- `-32700` Parse Error: invalid JSON body, wrong Content-Type
- `-32600` Invalid Request: missing method field, wrong JSON-RPC version, invalid agent_id
- No agent server needed — errors are caught by KubeMQ before forwarding

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

```bash
npx tsx client.ts
```

## Expected Output

```
=== Invalid JSON body (expect -32700) ===
Status: 200
Response: { "jsonrpc": "2.0", "id": null, "error": { "code": -32700, ... } }

=== Missing method field (expect -32600) ===
Status: 200
Response: { "jsonrpc": "2.0", "id": 1, "error": { "code": -32600, ... } }

=== Wrong JSON-RPC version (expect -32600) ===
Status: 200
Response: { "jsonrpc": "2.0", "id": 1, "error": { "code": -32600, ... } }

=== Wrong Content-Type (expect -32700) ===
Status: 200
Response: { "jsonrpc": "2.0", "id": null, "error": { "code": -32700, ... } }

=== Invalid agent_id format (expect -32600) ===
Status: 200
Response: { "jsonrpc": "2.0", "id": 1, "error": { "code": -32600, ... } }
```
