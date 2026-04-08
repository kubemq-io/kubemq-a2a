from __future__ import annotations

import asyncio
from typing import Any

from kubemq_a2a_burnin.suites.base import BaseSuite


class A2ASyncSuite(BaseSuite):
    suite_name = "a2a_sync"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("S01", "Basic message/send", self.test_s01),
            ("S02", "message/send with custom timeout", self.test_s02),
            ("S03", "message/send to slow agent", self.test_s03),
            ("S04", "message/send preserves headers", self.test_s04),
            ("S05", "X-KubeMQ-Caller-ID header", self.test_s05),
            ("S06", "Hop-by-hop headers stripped", self.test_s06),
            ("S07", "message/send with context_id", self.test_s07),
            ("S08", "tasks/get method", self.test_s08),
            ("S09", "tasks/cancel method", self.test_s09),
            ("S10", "Custom JSON-RPC method", self.test_s10),
            ("S11", "Multiple sequential requests", self.test_s11),
            ("S12", "Concurrent requests to same agent", self.test_s12),
            ("S13", "tasks/send method metric label", self.test_s13),
            ("S14", "Unknown method metric label", self.test_s14),
        ]

    async def test_s01(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "hello from s01"}]},
            },
        )
        assert "result" in result, f"Expected result key, got {list(result.keys())}"
        assert "echo" in result["result"], "Echo agent should return echo field"
        return 2

    async def test_s02(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {"message": {"parts": [{"text": "s02"}]}, "configuration": {"timeout": 5}},
            timeout=5,
        )
        assert "result" in result, f"Expected result, got {list(result.keys())}"
        return 1

    async def test_s03(self) -> int:
        agents = self.agent_manager.get_agents_by_type("slow")
        if not agents:
            raise RuntimeError("No slow agents available")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {"message": {"parts": [{"text": "s03"}]}},
            timeout=30,
        )
        assert "result" in result, (
            f"Expected result from slow agent, got {list(result.keys())}"
        )
        assert result["result"].get("delayed_ms") == agent.delay_ms
        return 2

    async def test_s04(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        agent.request_log.clear()
        await self.a2a.send(
            agent.agent_id,
            "message/send",
            {"message": {"parts": [{"text": "s04"}]}},
            headers={"X-Custom-Header": "test-value-s04"},
        )
        assert len(agent.request_log) > 0, "Agent should have received request"
        last_req = agent.request_log[-1]
        received_headers = last_req["headers"]
        has_custom = any("custom-header" in k.lower() for k in received_headers)
        assert has_custom, (
            f"Custom header not forwarded. Received headers: {list(received_headers.keys())}"
        )
        return 2

    async def test_s05(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        agent.request_log.clear()
        await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "s05"}]},
            },
        )
        assert len(agent.request_log) > 0, "Agent should have received request"
        last_req = agent.request_log[-1]
        received_headers = last_req["headers"]
        has_caller_id = any("kubemq-caller-id" in k.lower() for k in received_headers)
        assert has_caller_id, (
            f"X-KubeMQ-Caller-ID not present. Headers: {list(received_headers.keys())}"
        )
        return 1

    async def test_s06(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        agent.request_log.clear()
        await self.a2a.send(
            agent.agent_id,
            "message/send",
            {"message": {"parts": [{"text": "s06"}]}},
            headers={
                "Authorization": "Bearer secret-token",
                "Cookie": "session=abc123",
                "X-Custom-Allowed": "should-pass",
            },
        )
        assert len(agent.request_log) > 0
        last_req = agent.request_log[-1]
        received_headers = {k.lower(): v for k, v in last_req["headers"].items()}
        stripped_headers = [
            "authorization",
            "cookie",
            "proxy-authorization",
            "x-forwarded-for",
        ]
        for h in stripped_headers:
            found = any(h in k for k in received_headers)
            assert not found, (
                f"Hop-by-hop header '{h}' should be stripped but was forwarded"
            )
        return 4

    async def test_s07(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "s07"}]},
                "contextId": "ctx-s07-test",
            },
        )
        assert "result" in result
        return 1

    async def test_s08(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "tasks/get",
            {
                "taskId": "task-s08",
            },
        )
        assert "result" in result, (
            f"Expected result for tasks/get, got {list(result.keys())}"
        )
        return 1

    async def test_s09(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "tasks/cancel",
            {
                "taskId": "task-s09",
            },
        )
        assert "result" in result, (
            f"Expected result for tasks/cancel, got {list(result.keys())}"
        )
        return 1

    async def test_s10(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "custom/action",
            {
                "data": "s10-custom",
            },
        )
        assert "result" in result, (
            f"Expected result for custom method, got {list(result.keys())}"
        )
        return 1

    async def test_s11(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        success_count = 0
        for i in range(100):
            result = await self.a2a.send(
                agent.agent_id,
                "message/send",
                {
                    "message": {"parts": [{"text": f"seq-{i}"}]},
                },
            )
            if "result" in result:
                success_count += 1
        assert success_count == 100, f"Expected 100 successes, got {success_count}"
        return 1

    async def test_s12(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]

        async def _send(idx: int) -> dict[str, Any]:
            return await self.a2a.send(
                agent.agent_id,
                "message/send",
                {
                    "message": {"parts": [{"text": f"concurrent-{idx}"}]},
                },
            )

        results = await asyncio.gather(*[_send(i) for i in range(20)])
        successes = [r for r in results if "result" in r]
        assert len(successes) == 20, f"Expected 20 successes, got {len(successes)}"
        return 1

    async def test_s13(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        before = await self.metrics.scrape()
        await self.a2a.send(
            agents[0].agent_id,
            "tasks/send",
            {
                "message": {"parts": [{"text": "s13"}]},
            },
        )
        after = await self.metrics.scrape()
        labels = {"agent_id": agents[0].agent_id, "method": "tasks/send"}
        delta = after.get("kubemq_a2a_requests_total", labels) - before.get(
            "kubemq_a2a_requests_total", labels
        )
        assert delta >= 1, f"Expected tasks/send label in metric, got delta={delta}"
        return 1

    async def test_s14(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        before = await self.metrics.scrape()
        await self.a2a.send(
            agents[0].agent_id,
            "nonexistent/method",
            {
                "message": {"parts": [{"text": "s14"}]},
            },
        )
        after = await self.metrics.scrape()
        labels = {"agent_id": agents[0].agent_id, "method": "unknown"}
        delta = after.get("kubemq_a2a_requests_total", labels) - before.get(
            "kubemq_a2a_requests_total", labels
        )
        assert delta >= 1, f"Expected 'unknown' method label, got delta={delta}"
        return 1
