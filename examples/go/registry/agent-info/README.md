# Agent Info

Registers an agent with a complete agent card and retrieves all fields.

## What It Shows

- Full agent card with multiple skills, descriptions, and tags
- GET `/agents/{agent_id}` to retrieve all card fields including server-managed ones
- Displaying every field of the agent card

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agent):
```bash
go run agent.go
```

Terminal 2 (run the client):
```bash
go run client.go
```

## Expected Output

Client:
```
Status: 200

--- Agent Card ---
  agent_id:           full-info-agent-01
  name:               Full Info Agent
  description:        An agent with all card fields populated for demonstration
  version:            2.1.0
  url:                http://localhost:18080/
  ...
  registered_at:      ...
  last_seen:          ...

--- Skills (2) ---
  [echo] Echo: Echoes back the received message verbatim
    tags: [echo test debug]
  [greet] Greeting: Responds with a personalized greeting
    tags: [greet chat]
```
