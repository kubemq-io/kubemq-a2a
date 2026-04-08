# Header Forwarding

Demonstrates how KubeMQ forwards custom `X-*` headers to the agent.

## What It Shows

- Sending `X-Custom-Header` with a JSON-RPC request
- Agent receiving and returning forwarded headers
- KubeMQ injecting `X-KubeMQ-Caller-ID`

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
    "received_headers" : {
      "X-Custom-Header" : "my-custom-value",
      "X-Kubemq-Caller-Id" : "..."
    }
  }
}

Forwarded headers: {"X-Custom-Header":"my-custom-value","X-Kubemq-Caller-Id":"..."}
X-Custom-Header was forwarded successfully!
X-KubeMQ-Caller-ID injected by KubeMQ
```
