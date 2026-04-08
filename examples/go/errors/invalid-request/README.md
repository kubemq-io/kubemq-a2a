# Invalid Request

Sends various malformed JSON-RPC payloads to demonstrate validation errors.

## What It Shows

- Invalid JSON body triggers parse error `-32700`
- Missing `method` field triggers invalid request `-32600`
- Bad `jsonrpc` version triggers invalid request `-32600`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Any agent registered as `echo-agent-01` (or adjust the agent ID)

## Run

```bash
go run client.go
```

No agent is needed — these errors are caught by KubeMQ before forwarding.

## Expected Output

```
=== Test 1: Invalid JSON ===
  Code: -32700 (expected -32700)
  Message: parse error: invalid JSON

=== Test 2: Missing method field ===
  Code: -32600 (expected -32600)
  Message: invalid request: missing method field

=== Test 3: Bad jsonrpc version ===
  Code: -32600 (expected -32600)
  Message: invalid request: ...

All invalid request errors demonstrated!
```
