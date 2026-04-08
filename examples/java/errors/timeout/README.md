# Timeout

Demonstrates the timeout error when an agent is too slow to respond.

## What It Shows

- Agent with a 5-second delay before responding
- Client sending a request with `timeout=1` in `params.configuration`
- Receiving JSON-RPC error code `-32001` (agent timeout)

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the slow agent):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Agent"
```

Terminal 2 (run the client):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
```

## Expected Output

```
Sending request with timeout=1 to slow agent (5s delay)...
{
  "jsonrpc" : "2.0",
  "id" : 1,
  "error" : {
    "code" : -32001,
    "message" : "agent timeout: slow-agent-01"
  }
}

Error code:    -32001
Error message: agent timeout: slow-agent-01

Timeout error (-32001) received as expected!
```
