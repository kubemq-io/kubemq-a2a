# Concurrent Requests

Demonstrates sending 20 concurrent JSON-RPC requests to the same agent.

## What It Shows

- Sending multiple requests concurrently using `CompletableFuture`
- All requests completing successfully with no errors
- KubeMQ handling concurrent connections to the same agent

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
Sending 20 concurrent requests...

Results:
  Successes:  20
  Errors:     0
  Exceptions: 0
  Total:      20

All 20 concurrent requests completed successfully!
```
