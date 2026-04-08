"""Task-Events example — agent that emits status, artifact, and done events."""

import asyncio
import json
import signal

import httpx
from aiohttp import web

KUBEMQ_URL = "http://localhost:9090"
AGENT_ID = "task-events-agent-01"
AGENT_PORT = 18080


async def handle_stream(request: web.Request) -> web.StreamResponse:
    resp = web.StreamResponse(
        status=200,
        headers={"Content-Type": "text/event-stream", "Cache-Control": "no-cache"},
    )
    await resp.prepare(request)

    status1 = json.dumps({"type": "status_update", "payload": {"status": "working", "progress": 1, "total": 3}})
    await resp.write(f"event: task.status\ndata: {status1}\n\n".encode())
    await asyncio.sleep(0.5)

    status2 = json.dumps({"type": "status_update", "payload": {"status": "working", "progress": 2, "total": 3}})
    await resp.write(f"event: task.status\ndata: {status2}\n\n".encode())
    await asyncio.sleep(0.5)

    artifact = json.dumps({"type": "artifact", "payload": {"name": "result.json", "data": {"key": "value"}}})
    await resp.write(f"event: task.artifact\ndata: {artifact}\n\n".encode())
    await asyncio.sleep(0.3)

    done = json.dumps({"type": "done", "payload": {"final_result": "completed"}})
    await resp.write(f"event: task.done\ndata: {done}\n\n".encode())
    await resp.write_eof()
    return resp


async def handle_request(request: web.Request) -> web.Response:
    body = await request.json()
    if body.get("method") == "message/stream":
        return await handle_stream(request)
    return web.json_response({"jsonrpc": "2.0", "id": body.get("id"), "result": {"echo": body}})


async def register_agent() -> None:
    card = {
        "agent_id": AGENT_ID,
        "name": "Task Events Agent",
        "description": "Emits various event types",
        "version": "1.0.0",
        "url": f"http://localhost:{AGENT_PORT}/",
        "skills": [],
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
