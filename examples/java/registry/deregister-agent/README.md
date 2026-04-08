# Deregister Agent

Demonstrates both agent deregistration methods: POST and DELETE.

## What It Shows

- Deregistering via `POST /agents/deregister` with JSON body
- Deregistering via `DELETE /agents/{agent_id}`
- Verifying deregistration by checking agent no longer exists

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
=== Verify agent exists ===
GET /agents/deregister-agent-01: 200

=== Deregister via POST ===
POST /agents/deregister: 200
GET /agents/deregister-agent-01 after deregister: 404

=== Re-register for DELETE test ===
Re-registered: 200

=== Deregister via DELETE ===
DELETE /agents/deregister-agent-01: 200
GET /agents/deregister-agent-01 after delete: 404

Both deregistration methods demonstrated successfully!
```
