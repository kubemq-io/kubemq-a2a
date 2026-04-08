# Basic Send

Demonstrates a basic `message/send` JSON-RPC round-trip through KubeMQ.

## What It Shows

- Sending a `message/send` JSON-RPC 2.0 request via `POST /a2a/{agent_id}`
- Echo agent returning the received message in the result
- Verifying the response contains a `result` field

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
Status: 200
{
  "jsonrpc" : "2.0",
  "id" : 1,
  "result" : {
    "echo" : { ... }
  }
}

Basic send completed successfully!
```
