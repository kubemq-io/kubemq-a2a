# Register Agent

Demonstrates agent registration with KubeMQ using a full agent card.

## What It Shows

- Creating an HTTP agent server with `com.sun.net.httpserver`
- Registering the agent via `POST /agents/register`
- Verifying registration via `GET /agents/{agent_id}`

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

Agent:
```
Agent listening on port 18080
Registered: 200
{
  "agent_id" : "echo-agent-01",
  "name" : "Echo Agent",
  ...
}
```

Client:
```
Status: 200
{
  "agent_id" : "echo-agent-01",
  "registered_at" : "...",
  ...
}

Agent registration verified successfully!
```
