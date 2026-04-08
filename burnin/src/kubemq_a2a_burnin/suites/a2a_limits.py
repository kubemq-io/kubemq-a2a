from __future__ import annotations

import asyncio
from typing import Any

from kubemq_a2a_burnin.suites.base import BaseSuite


class A2ALimitsSuite(BaseSuite):
    suite_name = "a2a_limits"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("L01", "Concurrency limit", self.test_l01),
            ("L02", "Response size limit", self.test_l02),
            ("L03", "Max timeout cap", self.test_l03),
            ("L04", "Default timeout applied", self.test_l04),
            ("L05", "Rapid registration cycles", self.test_l05),
            ("L06", "High-frequency heartbeats", self.test_l06),
        ]

    async def test_l01(self) -> int:
        slow_agents = self.agent_manager.get_agents_by_type("slow")
        if not slow_agents:
            raise RuntimeError("No slow agents available")
        agent = slow_agents[0]

        async def _send_one(idx: int) -> dict[str, Any]:
            return await self.a2a.send(
                agent.agent_id,
                "message/send",
                {"message": {"parts": [{"text": f"burst-{idx}"}]}},
                timeout=30,
            )

        tasks = [_send_one(i) for i in range(101)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        successes = [r for r in results if isinstance(r, dict) and "error" not in r]
        errors = [r for r in results if isinstance(r, dict) and "error" in r]

        assert len(successes) <= 100, f"Expected <=100 successes, got {len(successes)}"
        assert len(errors) >= 1, "Expected at least 1 concurrency-limit rejection"
        overflow = errors[0]
        assert overflow["error"]["code"] == -32603, (
            f"Expected code -32603, got {overflow['error']['code']}"
        )
        return 3

    async def test_l02(self) -> int:
        oversize_agents = self.agent_manager.get_agents_by_type("oversize")
        if not oversize_agents:
            raise RuntimeError("No oversize agents available")
        agent = oversize_agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {"message": {"parts": [{"text": "l02-oversize"}]}},
            timeout=30,
        )
        assert "error" in result, "Expected error for oversize response"
        error_msg = str(result["error"].get("message", "")).lower()
        assert "too large" in error_msg or "response" in error_msg, (
            f"Expected 'response too large' error, got: {result['error']}"
        )
        return 2

    async def test_l03(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "l03"}]},
                "configuration": {"timeout": 99999},
            },
            timeout=30,
        )
        assert "result" in result, (
            f"Expected result (timeout capped at MaxTimeoutSeconds=3600), got {list(result.keys())}"
        )
        return 1

    async def test_l04(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "l04-no-timeout"}]},
            },
        )
        assert "result" in result, (
            f"Expected result with default timeout, got {list(result.keys())}"
        )
        return 1

    async def test_l05(self) -> int:
        success_count = 0
        for i in range(50):
            card = {
                "agent_id": f"test-l05-{i:03d}",
                "name": f"Churn Agent {i}",
                "url": f"http://localhost:{19800 + i}/",
                "skills": [],
                "defaultInputModes": ["text"],
                "defaultOutputModes": ["text"],
                "protocolVersions": ["1.0"],
            }
            reg_resp = await self.registry.register(card)
            dereg_resp = await self.registry.deregister_post(f"test-l05-{i:03d}")
            if reg_resp.status_code == 200 and dereg_resp.status_code == 200:
                success_count += 1
        assert success_count == 50, (
            f"Expected 50 successful cycles, got {success_count}"
        )
        return 1

    async def test_l06(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        success_count = 0
        for _ in range(100):
            resp = await self.registry.heartbeat(agent.agent_id)
            if resp.status_code == 200:
                success_count += 1
        assert success_count == 100, (
            f"Expected 100 successful heartbeats, got {success_count}"
        )
        return 1
