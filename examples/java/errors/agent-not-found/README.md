# Agent Not Found

Demonstrates the error returned when sending to a nonexistent agent.

## What It Shows

- Sending a request to an unregistered `agent_id`
- Receiving JSON-RPC error code `-32002` (agent not found)
- No agent server needed — the error comes from KubeMQ itself

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
```

## Expected Output

```
{
  "jsonrpc" : "2.0",
  "id" : 1,
  "error" : {
    "code" : -32002,
    "message" : "agent not found: nonexistent-agent"
  }
}

Error code:    -32002
Error message: agent not found: nonexistent-agent

Agent-not-found error (-32002) received as expected!
```
