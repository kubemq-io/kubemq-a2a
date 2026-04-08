"""List-Agents example — registers 3 agents with different skills."""

import asyncio
import json
import signal

import httpx
from aiohttp import web

KUBEMQ_URL = "http://localhost:9090"
BASE_PORT = 18080

AGENTS = [
    {
        "agent_id": "echo-agent-01",
        "name": "Echo Agent",
        "description": "Echoes back messages",
        "version": "1.0.0",
        "url": f"http://localhost:{BASE_PORT}/",
        "skills": [{"id": "echo", "name": "Echo", "description": "Echo skill", "tags": ["echo", "test"]}],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "protocolVersions": ["1.0"],
    },
    {
        "agent_id": "translate-agent-01",
        "name": "Translate Agent",
        "description": "Translates text",
        "version": "1.0.0",
        "url": f"http://localhost:{BASE_PORT + 1}/",
        "skills": [{"id": "translate", "name": "Translate", "description": "Translation skill", "tags": ["translate", "nlp"]}],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "protocolVersions": ["1.0"],
    },
    {
        "agent_id": "summarize-agent-01",
        "name": "Summarize Agent",
        "description": "Summarizes text",
        "version": "1.0.0",
        "url": f"http://localhost:{BASE_PORT + 2}/",
        "skills": [{"id": "summarize", "name": "Summarize", "description": "Summarization skill", "tags": ["summarize", "nlp"]}],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "protocolVersions": ["1.0"],
    },
]


async def handle_request(request: web.Request) -> web.Response:
    body = await request.json()
    return web.json_response({"jsonrpc": "2.0", "id": body.get("id"), "result": {"echo": body}})


async def main() -> None:
    runners: list[web.AppRunner] = []
    try:
        for i, agent_card in enumerate(AGENTS):
            app = web.Application()
            app.router.add_post("/", handle_request)
            runner = web.AppRunner(app)
            await runner.setup()
            port = BASE_PORT + i
            site = web.TCPSite(runner, "0.0.0.0", port)
            await site.start()
            runners.append(runner)
            print(f"Agent '{agent_card['agent_id']}' listening on port {port}")

        async with httpx.AsyncClient() as client:
            for agent_card in AGENTS:
                resp = await client.post(f"{KUBEMQ_URL}/agents/register", json=agent_card)
                print(f"Registered '{agent_card['agent_id']}': {resp.status_code}")

        stop = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop.set)

        await stop.wait()
    finally:
        for runner in runners:
            await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
