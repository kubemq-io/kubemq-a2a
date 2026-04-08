# Response Size

Demonstrates the response size limit (10MB).

## What It Shows

- Agent returning a response larger than 10MB
- KubeMQ enforcing the response size limit
- Client receiving an error when the limit is exceeded

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the oversized agent):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Agent"
```

Terminal 2 (run the client):

```bash
mvn -f ../../pom.xml compile exec:java -Dexec.mainClass="Client"
```

## Expected Output

```
Requesting oversized response (>10MB)...

Error code:    -32603
Error message: internal error: response too large

Response size limit enforced!
```
