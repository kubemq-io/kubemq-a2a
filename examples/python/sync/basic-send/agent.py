"""Basic-Send example — echo agent that returns the received message."""

import asyncio
import json
import signal

import httpx
from aiohttp import web

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "echo-agent-01"
AGENT_PORT = 18080


async def handle_request(request: web.Request) -> web.Response:
    body = await request.json()
    return web.json_response({
        "jsonrpc": "2.0",
        "id": body.get("id"),
        "result": {"echo": body},
    })


async def register_agent() -> None:
    card = {
        "agent_id": AGENT_ID,
        "name": "Echo Agent",
        "description": "Echoes back the received message",
        "version": "1.0.0",
        "url": f"http://localhost:{AGENT_PORT}/",
        "skills": [{"id": "echo", "name": "Echo", "description": "Echo skill", "tags": ["echo"]}],
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
    print(f"Agent listening on port {AGENT_PORT}")

    await register_agent()

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    await stop.wait()
    await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
