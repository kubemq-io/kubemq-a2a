# Invalid Request

Demonstrates error responses for various malformed JSON-RPC payloads.

## What It Shows

- Invalid JSON body triggers `-32700` (Parse Error)
- Missing `method` field triggers `-32600` (Invalid Request)
- Wrong `jsonrpc` version triggers `-32600` (Invalid Request)
- No agent server is needed for this example (KubeMQ validates before forwarding)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Python 3.10+ with dependencies installed (`uv sync`)

## Run

```bash
uv run python client.py
```

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
  Message: invalid request: invalid jsonrpc version

All invalid request errors demonstrated!
```
