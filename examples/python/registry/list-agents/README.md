# List Agents

Demonstrates listing registered agents and filtering by skill tags.

## What It Shows

- Registering multiple agents with different skills
- Listing all agents via `GET /agents`
- Filtering agents by skill tags via `GET /agents?skill_tags=echo`

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`
- Python 3.10+ with dependencies installed (`uv sync`)

## Run

Terminal 1 (start the agents):
```bash
uv run python agent.py
```

Terminal 2 (run the client):
```bash
uv run python client.py
```

## Expected Output

```
=== All Agents ===
  echo-agent-01: skills=['echo']
  translate-agent-01: skills=['translate']
  summarize-agent-01: skills=['summarize']

Total agents: 3

=== Filter by skill_tags=echo ===
  echo-agent-01

Filtered count: 1

=== Filter by skill_tags=nlp ===
  translate-agent-01
  summarize-agent-01

Filtered count: 2
```
