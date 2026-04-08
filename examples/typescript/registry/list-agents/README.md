# List Agents

Demonstrates listing registered agents and filtering by skill tags.

## What It Shows

- Registering multiple agents with different skills
- GET `/agents` to list all registered agents
- GET `/agents?skill_tags=echo` to filter by skill tag

## Prerequisites

- KubeMQ running with A2A enabled at `http://localhost:9090`

## Run

Terminal 1 (start the agents):
```bash
npx tsx agent.ts
```

Terminal 2 (run the client):
```bash
npx tsx client.ts
```

## Expected Output

```
=== List all agents ===
Found 3 agent(s):
  - list-echo-01 (skills: test, echo)
  - list-translate-01 (skills: nlp, translate)
  - list-summarize-01 (skills: nlp, summarize)

=== Filter by skill_tags=echo ===
Found 1 agent(s) with 'echo' tag:
  - list-echo-01

=== Filter by skill_tags=nlp ===
Found 2 agent(s) with 'nlp' tag:
  - list-translate-01
  - list-summarize-01
```
