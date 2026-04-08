# Invalid Request

Demonstrates error responses for various malformed JSON-RPC payloads.

## What It Shows

- **Invalid JSON** — garbage payload returns error code `-32700` (Parse Error)
- **Missing method** — omitting the `method` field returns `-32600` (Invalid Request)
- **Bad jsonrpc version** — using `"1.0"` instead of `"2.0"` returns `-32600`
- No agent server is needed for this example (an existing registered agent is assumed)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

```bash
dotnet run --project InvalidRequest.csproj
```

## Expected Output

```
=== Test 1: Invalid JSON ===
  Code: -32700 (expected -32700)
  Message: Parse error

=== Test 2: Missing method field ===
  Code: -32600 (expected -32600)
  Message: Invalid Request

=== Test 3: Bad jsonrpc version ===
  Code: -32600 (expected -32600)
  Message: Invalid Request

All invalid request errors demonstrated!
```
