# List Agents

Demonstrates listing registered agents and filtering by skill tags.

## What It Shows

- Registering 3 agents with different skill tags (echo, nlp)
- Listing all agents via `GET /agents`
- Filtering agents by `skill_tags` query parameter

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- .NET 8.0 SDK

## Run

Terminal 1 (start the agents):
```bash
dotnet run --project ListAgents.csproj -- agent
```

Terminal 2 (run the client):
```bash
dotnet run --project ListAgents.csproj
```

## Expected Output

```
=== All Agents ===
  echo-agent-01: skills=[echo]
  translate-agent-01: skills=[translate]
  summarize-agent-01: skills=[summarize]

Total agents: 3

=== Filter by skill_tags=echo ===
  echo-agent-01

Filtered count: 1

=== Filter by skill_tags=nlp ===
  translate-agent-01
  summarize-agent-01

Filtered count: 2
```
