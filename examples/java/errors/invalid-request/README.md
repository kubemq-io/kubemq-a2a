# Invalid Request

Demonstrates various malformed JSON-RPC request errors.

## What It Shows

- Sending invalid JSON (parse error `-32700`)
- Sending a request without a `method` field (invalid request `-32600`)
- Sending a request with wrong `jsonrpc` version (invalid request `-32600`)
- No agent server needed — errors come from KubeMQ validation

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
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
  Message: invalid request: ...

All invalid request errors demonstrated!
```
