# Getting Started

Send your first A2A message through KubeMQ in 5 minutes.

## Step 1: Start KubeMQ

Start a KubeMQ server with A2A enabled:

```bash
docker run -d \
  --name kubemq \
  -p 9090:9090 \
  -p 8080:8080 \
  -e KUBEMQ_A2A_ENABLE=true \
  kubemq/kubemq:latest
```

Verify KubeMQ is running with A2A:

```bash
curl http://localhost:9090/.well-known/agent-card.json
```

Expected output:

```json
{
  "name": "kubemq",
  "description": "KubeMQ A2A Gateway",
  "version": "latest",
  "url": "http://localhost:9090/",
  "skills": [],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "protocolVersions": ["1.0"]
}
```

## Step 2: Start a Simple Echo Agent

Create a Python file `echo_agent.py`:

```python
import asyncio
import json
import httpx
from aiohttp import web

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "echo-agent-01"
AGENT_PORT = 18080

async def handle_request(request: web.Request) -> web.Response:
    body = await request.json()
    request_id = body.get("id")
    result = {"echo": body}
    return web.json_response({"jsonrpc": "2.0", "id": request_id, "result": result})

async def register_agent() -> None:
    card = {
        "agent_id": AGENT_ID,
        "name": "Echo Agent",
        "description": "A simple echo agent for testing",
        "version": "1.0.0",
        "url": f"http://localhost:{AGENT_PORT}/",
        "skills": [
            {"id": "echo", "name": "Echo", "description": "Echoes back the received message", "tags": ["test", "echo"]}
        ],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "protocolVersions": ["1.0"],
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{KUBEMQ_URL}/agents/register", json=card)
        print(f"Registered: {resp.status_code}")

async def main() -> None:
    app = web.Application()
    app.router.add_post("/", handle_request)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", AGENT_PORT)
    await site.start()
    print(f"Agent '{AGENT_ID}' listening on port {AGENT_PORT}")
    await register_agent()
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

Install dependencies and run:

```bash
pip install aiohttp httpx
python echo_agent.py
```

Expected output:

```
Agent 'echo-agent-01' listening on port 18080
Registered: 200
```

## Step 3: Verify Registration

In a new terminal, verify the agent is registered:

```bash
curl http://localhost:9090/agents/echo-agent-01
```

Expected output:

```json
{
  "agent_id": "echo-agent-01",
  "name": "Echo Agent",
  "description": "A simple echo agent for testing",
  "version": "1.0.0",
  "url": "http://localhost:18080/",
  "skills": [
    {"id": "echo", "name": "Echo", "description": "Echoes back the received message", "tags": ["test", "echo"]}
  ],
  "registered_at": "2026-04-06T10:00:00Z",
  "last_seen": "2026-04-06T10:00:00Z"
}
```

## Step 4: Send a Message

Send a JSON-RPC 2.0 `message/send` request through KubeMQ:

```bash
curl -X POST http://localhost:9090/a2a/echo-agent-01 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "parts": [{"text": "Hello, agent!"}]
      }
    }
  }'
```

## Step 5: Verify the Response

Expected response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "echo": {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "message/send",
      "params": {
        "message": {"parts": [{"text": "Hello, agent!"}]}
      }
    }
  }
}
```

The echo agent returned the full request body as the result, confirming the round-trip through KubeMQ.

## Next Steps

- Browse [examples/](../examples/) for all 19 scenarios in 5 languages
- Read [architecture.md](architecture.md) to understand the gateway model
- See [patterns/](patterns/) for registry, sync, streaming, and error handling patterns
- Run the [burn-in suite](../burnin/) to validate your deployment
