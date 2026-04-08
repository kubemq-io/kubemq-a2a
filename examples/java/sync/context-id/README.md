# Context ID

Demonstrates request correlation using `contextId` in JSON-RPC params.

## What It Shows

- Sending `contextId` in `params` for request correlation
- Agent extracting and echoing the `contextId`
- Client verifying the returned `contextId` matches

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Agent"
```

Terminal 2 (run the client):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
```

## Expected Output

```
{
  "jsonrpc" : "2.0",
  "id" : 1,
  "result" : {
    "echo" : { ... },
    "contextId" : "ctx-001"
  }
}

Sent contextId:     ctx-001
Received contextId: ctx-001
Context ID correlation verified!
```
