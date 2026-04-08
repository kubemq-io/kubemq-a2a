# Custom Method

Demonstrates that KubeMQ forwards any JSON-RPC method name to the agent.

## What It Shows

- Sending a non-standard `custom/action` method
- KubeMQ forwarding the method without filtering
- Agent handling and echoing the custom method name

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
    "handled_method" : "custom/action",
    "echo" : { ... }
  }
}

Handled method: custom/action
Custom method forwarded successfully!
```
