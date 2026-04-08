# Agent Info

Demonstrates retrieving and displaying all fields from an agent card.

## What It Shows

- Registering an agent with a complete card (multiple skills, all fields)
- Retrieving the full agent card via `GET /agents/{agent_id}`
- Displaying all card fields including server-managed `registered_at` and `last_seen`

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

--- Agent Card ---
  agent_id:           full-info-agent-01
  name:               Full Info Agent
  description:        An agent with all card fields populated for demonstration
  version:            2.1.0
  url:                http://localhost:18080/
  defaultInputModes:  ["text"]
  defaultOutputModes: ["text"]
  protocolVersions:   ["1.0"]
  registered_at:      2026-04-06T10:00:00Z
  last_seen:          2026-04-06T10:00:00Z

--- Skills (2) ---
  [echo] Echo: Echoes back the received message verbatim
    tags: ["echo","test","debug"]
  [greet] Greeting: Responds with a personalized greeting
    tags: ["greet","chat"]
```
