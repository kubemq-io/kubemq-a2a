# List Agents

Registers 3 agents with different skills and demonstrates listing and filtering.

## What It Shows

- Registering multiple agents with different skill tags
- GET `/agents` to list all registered agents
- GET `/agents?skill_tags=echo` to filter by skill tags

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agents):
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
=== All Agents ===
  echo-agent-01: skills=[echo]
  translate-agent-01: skills=[translate]
  summarize-agent-01: skills=[summarize]

Total: 3

=== Filter by skill_tags=echo ===
  echo-agent-01

Total: 1

=== Filter by skill_tags=nlp ===
  translate-agent-01
  summarize-agent-01

Total: 2
```
