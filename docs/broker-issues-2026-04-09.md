# KubeMQ A2A Gateway — Broker Issues Report

**Date:** 2026-04-09
**Reporter:** Client SDK Team
**Tested against:** KubeMQ server on `localhost:9090`
**Languages tested:** Go, Python, TypeScript, Java, C#
**Total examples run:** 95 (19 scenarios x 5 languages)

---

## Executive Summary

We ran the full A2A example suite (19 scenarios) across all 5 client languages. Two issues reproduce consistently in **every language**, which strongly indicates they originate on the broker/gateway side rather than in client code.

| Issue | Affected Example | Failure Rate | Severity |
|-------|-----------------|:------------:|:--------:|
| `/agents` response format mismatch | `registry/list-agents` | 5/5 languages | Medium |
| `configuration.timeout` not enforced | `errors/timeout` | 5/5 languages | High |

Everything else (82 of 95 runs) passes cleanly across all languages.

---

## Issue 1: `/agents` Endpoint Response Format

### Observed behavior

`GET /agents` returns a **wrapped object**:

```json
{
  "agents": [
    {
      "agent_id": "echo-agent-01",
      "name": "Echo Agent",
      "skills": [...],
      ...
    }
  ]
}
```

### Expected behavior (per A2A protocol convention)

All 5 client implementations were written to expect a **flat JSON array**:

```json
[
  {
    "agent_id": "echo-agent-01",
    "name": "Echo Agent",
    "skills": [...],
    ...
  }
]
```

### Reproduction

```bash
# Register a test agent
curl -s -X POST http://localhost:9090/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"test-01","name":"Test","description":"test","version":"1.0.0","url":"http://localhost:19999/","skills":[{"id":"s1","name":"S","description":"s","tags":["t"]}],"defaultInputModes":["text"],"defaultOutputModes":["text"],"protocolVersions":["1.0"]}'

# List agents — note the {"agents": [...]} wrapper
curl -s http://localhost:9090/agents
# Returns: {"agents":[{"agent_id":"test-01",...}]}
#                      ^^^^^^^^^^^^^^^^^^^^^^^
#          All clients expect this inner array as the top-level response

# Cleanup
curl -s -X POST http://localhost:9090/agents/deregister \
  -H "Content-Type: application/json" -d '{"agent_id":"test-01"}'
```

### Per-language error symptoms

| Language | Error |
|----------|-------|
| Go | `json.Unmarshal` into `[]map[string]interface{}` silently fails, returns empty slice |
| Python | `AttributeError: 'str' object has no attribute 'get'` |
| TypeScript | `TypeError: allAgents is not iterable` |
| Java | `NullPointerException` — `readTree()` returns object node, not array node |
| C# | `System.InvalidOperationException: The node must be of type 'JsonArray'` |

### Request to broker team

**One of these needs to happen:**

- **Option A (preferred):** Update the broker to return a flat JSON array from `GET /agents`, matching the A2A protocol convention and what all client examples expect.
- **Option B:** If the wrapped format `{"agents": [...]}` is intentional, confirm this is the contract so we can update all 5 client implementations accordingly. Please also update the A2A API documentation to reflect this.

**Additionally:** Does `GET /agents` support query parameters for filtering? The examples pass `?skill_tags=echo` — please confirm whether this is supported and document the query parameter schema.

---

## Issue 2: `configuration.timeout` Not Enforced

### Observed behavior

When a client sends a JSON-RPC request with a timeout configuration:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": { "parts": [{"text": "Hello"}] },
    "configuration": { "timeout": 1 }
  }
}
```

...and the target agent takes 5 seconds to respond, the gateway **waits the full 5 seconds** and returns the agent's successful response. No timeout error is returned.

### Expected behavior (per A2A protocol spec)

The gateway should enforce the `configuration.timeout` parameter (value in seconds). If the agent does not respond within the specified timeout, the gateway should return a JSON-RPC error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "agent timeout exceeded"
  }
}
```

### Reproduction

```bash
# 1. Start a slow agent (any language — here using a simple nc-based mock)
#    Or use the Go timeout agent: go run ./errors/timeout/agent.go
#    (it delays 5 seconds before responding)

# 2. Send a request with timeout=1
curl -s -X POST http://localhost:9090/a2a/timeout-agent-01 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {"parts": [{"text": "test"}]},
      "configuration": {"timeout": 1}
    }
  }'

# ACTUAL: Returns {"jsonrpc":"2.0","id":1,"result":{"delayed_ms":5000,"status":"ok"}}
#         (successful response after 5 seconds — no timeout enforcement)
#
# EXPECTED: Returns {"jsonrpc":"2.0","id":1,"error":{"code":-32001,"message":"..."}}
#           (timeout error after 1 second)
```

### Impact

- Fails consistently across all 5 languages (Go, Python, TypeScript, Java, C#)
- Clients cannot set per-request timeouts, which is a core part of the A2A protocol
- Long-running or hung agents will block clients indefinitely

### Request to broker team

1. **Implement `configuration.timeout` enforcement** in the A2A gateway's request-forwarding layer. When the timeout expires, the gateway should:
   - Cancel/abort the upstream request to the agent
   - Return JSON-RPC error code `-32001` to the client
2. **Define default timeout behavior:** What happens if `configuration.timeout` is omitted? Is there a gateway-level default timeout? Please document this.
3. **Confirm the timeout unit:** The examples assume seconds. Please confirm whether the value is in seconds or milliseconds.

---

## Summary of Action Items

| # | Item | Owner | Priority |
|---|------|-------|----------|
| 1 | Clarify `/agents` response format (flat array vs wrapped object) | Broker team | Medium |
| 2 | Implement `configuration.timeout` enforcement in A2A gateway | Broker team | High |
| 3 | Document `GET /agents` query parameter support (`skill_tags`, etc.) | Broker team | Low |
| 4 | Document default timeout behavior when `configuration.timeout` is omitted | Broker team | Medium |
| 5 | Confirm timeout unit (seconds vs milliseconds) | Broker team | Low |

---

## Appendix: Full Test Results

| Example | Go | Python | TS | Java | C# |
|---------|:--:|:------:|:--:|:----:|:--:|
| registry/register-agent | PASS | PASS | PASS | PASS | PASS |
| registry/list-agents | FAIL | FAIL | FAIL | FAIL | FAIL |
| registry/agent-info | PASS | PASS | PASS | PASS | PASS |
| registry/deregister-agent | PASS | PASS | PASS | PASS | PASS |
| registry/heartbeat | PASS | PASS | PASS | PASS | PASS |
| sync/basic-send | PASS | PASS | PASS | PASS | PASS |
| sync/header-forwarding | PASS | PASS | PASS | PASS | PASS |
| sync/context-id | PASS | PASS | PASS | PASS | PASS |
| sync/custom-method | PASS | PASS | PASS | PASS | PASS |
| sync/concurrent-requests | PASS | PASS | PASS | PASS | PASS |
| streaming/basic-stream | PASS | PASS | PASS | PASS | PASS |
| streaming/task-events | PASS | FAIL | PASS | PASS | PASS |
| streaming/keepalive | PASS | PASS | PASS | PASS | PASS |
| streaming/client-disconnect | PASS | PASS | PASS | PASS | PASS |
| errors/agent-not-found | PASS | PASS | PASS | PASS | PASS |
| errors/invalid-request | PASS | PASS | PASS | PASS | PASS |
| errors/timeout | FAIL | FAIL | FAIL | FAIL | FAIL |
| limits/concurrency-limit | PASS | FAIL | PASS | PASS | PASS |
| limits/response-size | PASS | PASS | PASS | PASS | PASS |
| **Pass rate** | **89%** | **79%** | **89%** | **84%** | **89%** |
