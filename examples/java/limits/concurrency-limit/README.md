# Concurrency Limit

Demonstrates the per-agent concurrency limit (100 concurrent requests).

## What It Shows

- Slow agent (2s delay) to hold connections open
- Client sending 101 concurrent requests to exceed the limit
- At least one request receiving error code `-32603` (internal error: concurrency limit exceeded)

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
Sending 101 concurrent requests (limit is 100)...

Results:
  Successes:            100
  Concurrency errors:   1 (code -32603)
  Other errors:         0
  Exceptions:           0
  Total:                101

Concurrency limit enforced — 1 request(s) rejected!
```
