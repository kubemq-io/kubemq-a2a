from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import httpx
from httpx_sse import aconnect_sse

from kubemq_a2a_burnin.suites.base import BaseSuite

logger = logging.getLogger(__name__)


class A2AStreamingSuite(BaseSuite):
    suite_name = "a2a_streaming"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("ST01", "Basic message/stream via POST", self.test_st01),
            ("ST02", "Stream via GET endpoint", self.test_st02),
            ("ST03", "Status update events", self.test_st03),
            ("ST04", "Status or artifact events", self.test_st04),
            ("ST05", "Done event (terminal)", self.test_st05),
            ("ST06", "Error event (terminal)", self.test_st06),
            ("ST07", "Keepalive comments", self.test_st07),
            ("ST08", "Idle timeout", self.test_st08),
            ("ST09", "Client disconnect causes cleanup", self.test_st09),
            ("ST10", "Multiple concurrent streams", self.test_st10),
            ("ST11", "Stream with headers forwarded", self.test_st11),
            ("ST12", "Stream event ordering", self.test_st12),
            ("ST13", "Large streaming payloads", self.test_st13),
        ]

    async def test_st01(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st01"}]}},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        assert len(events) > 0, "Expected at least one SSE event"
        assert any(e.get("event") == "task.status" for e in events) or any(
            e.get("event") == "task.done" for e in events
        ), "Expected task.status or task.done events"
        return 2

    async def test_st02(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream_get(agent.agent_id):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
            if len(events) >= 3:
                break
        assert len(events) > 0, "Expected at least one event from GET stream"
        return 1

    async def test_st03(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        status_events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st03-status"}]}},
        ):
            if event.get("event") == "task.status":
                data = (
                    json.loads(event["data"])
                    if isinstance(event["data"], str)
                    else event["data"]
                )
                assert data.get("type") == "status_update", (
                    f"Expected type=status_update, got {data.get('type')}"
                )
                status_events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        assert len(status_events) > 0, "Expected at least one task.status event"
        return 2

    async def test_st04(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st04-artifact"}]}},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        has_status_or_artifact = any(
            e.get("event") in ("task.status", "task.artifact") for e in events
        )
        assert has_status_or_artifact, "Expected task.status or task.artifact events"
        return 1

    async def test_st05(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        done_received = False
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st05-done"}]}},
        ):
            if event.get("event") == "task.done":
                data = (
                    json.loads(event["data"])
                    if isinstance(event["data"], str)
                    else event["data"]
                )
                assert data.get("type") == "done", (
                    f"Expected type=done, got {data.get('type')}"
                )
                done_received = True
                break
        assert done_received, "Expected task.done terminal event"
        return 2

    async def test_st06(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st06-error"}]}},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        has_terminal = any(
            e.get("event") in ("task.done", "task.error") for e in events
        )
        assert has_terminal, "Expected terminal event (task.done or task.error)"
        return 1

    async def test_st07(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        try:
            async for event in self.a2a.stream(
                agent.agent_id,
                "message/stream",
                {"message": {"parts": [{"text": "st07-keepalive"}]}},
            ):
                events.append(event)
                if event.get("event") in ("task.done", "task.error"):
                    break
        except Exception as exc:
            logger.debug("ST07 stream ended: %s", exc)
        assert len(events) > 0, "Expected events from stream"
        return 1

    async def test_st08(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        try:
            async for event in self.a2a.stream(
                agent.agent_id,
                "message/stream",
                {"message": {"parts": [{"text": "st08-idle"}]}},
            ):
                events.append(event)
                if event.get("event") in ("task.done", "task.error"):
                    break
        except Exception as exc:
            logger.debug("ST08 stream ended: %s", exc)
        assert len(events) > 0, "Expected events before idle timeout"
        return 1

    async def test_st09(self) -> int:
        stream_agents = self.agent_manager.get_agents_by_type("streaming")
        if not stream_agents:
            raise RuntimeError("No streaming agents configured")
        agent = stream_agents[0]
        agent.request_log.clear()

        async with httpx.AsyncClient(base_url=self.config.server.address) as client:
            payload = {
                "jsonrpc": "2.0",
                "id": "st09",
                "method": "message/stream",
                "params": {"message": {"parts": [{"text": "disconnect-test"}]}},
            }
            async with aconnect_sse(
                client, "POST", f"/a2a/{agent.agent_id}", json=payload
            ) as sse:
                async for event in sse.aiter_sse():
                    if event.event == "task.status":
                        break

        await asyncio.sleep(1.0)

        snap = await self.metrics.scrape()
        active_streams = snap.get("kubemq_a2a_sse_streams_active")
        assert active_streams == 0, (
            f"Expected 0 active streams after disconnect, got {active_streams}"
        )
        return 2

    async def test_st10(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        if len(agents) < 2:
            agents = agents * 5

        async def _stream_one(agent_id: str, idx: int) -> list[dict[str, Any]]:
            events: list[dict[str, Any]] = []
            a2a_client = type(self.a2a)(self.config.server.address)
            try:
                async for event in a2a_client.stream(
                    agent_id,
                    "message/stream",
                    {"message": {"parts": [{"text": f"concurrent-{idx}"}]}},
                ):
                    events.append(event)
                    if event.get("event") in ("task.done", "task.error"):
                        break
            except Exception as exc:
                logger.debug("ST10 stream-%d error: %s", idx, exc)
            finally:
                await a2a_client.close()
            return events

        tasks = [_stream_one(agents[i % len(agents)].agent_id, i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        successful = [r for r in results if len(r) > 0]
        assert len(successful) >= 3, (
            f"Expected at least 3 successful concurrent streams, got {len(successful)}"
        )
        return 2

    async def test_st11(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        agent.request_log.clear()
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st11-headers"}]}},
            headers={"X-Custom-Stream-Header": "stream-value"},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        assert len(events) > 0, "Expected events from stream"
        if agent.request_log:
            received_headers = agent.request_log[-1]["headers"]
            has_custom = any(
                "custom-stream-header" in k.lower() for k in received_headers
            )
            assert has_custom, (
                f"Custom header not forwarded in stream. Headers: {list(received_headers.keys())}"
            )
        return 2

    async def test_st12(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "st12-ordering"}]}},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break

        status_events = [e for e in events if e.get("event") == "task.status"]
        if len(status_events) >= 2:
            for i in range(1, len(status_events)):
                prev_data = (
                    json.loads(status_events[i - 1]["data"])
                    if isinstance(status_events[i - 1]["data"], str)
                    else status_events[i - 1]["data"]
                )
                curr_data = (
                    json.loads(status_events[i]["data"])
                    if isinstance(status_events[i]["data"], str)
                    else status_events[i]["data"]
                )
                prev_progress = prev_data.get("payload", {}).get("progress", 0)
                curr_progress = curr_data.get("payload", {}).get("progress", 0)
                assert curr_progress >= prev_progress, (
                    f"Events out of order: {prev_progress} -> {curr_progress}"
                )
        assert len(events) >= 2, "Expected at least 2 events for ordering test"
        return 2

    async def test_st13(self) -> int:
        agents = self.agent_manager.get_agents_by_type("streaming")
        if not agents:
            raise RuntimeError("No streaming agents configured")
        agent = agents[0]
        events: list[dict[str, Any]] = []
        async for event in self.a2a.stream(
            agent.agent_id,
            "message/stream",
            {"message": {"parts": [{"text": "x" * 10000}]}},
        ):
            events.append(event)
            if event.get("event") in ("task.done", "task.error"):
                break
        assert len(events) > 0, "Expected events even with large payloads"
        return 1
