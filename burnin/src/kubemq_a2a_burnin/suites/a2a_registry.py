from __future__ import annotations

from typing import Any

from kubemq_a2a_burnin.suites.base import BaseSuite


class A2ARegistrySuite(BaseSuite):
    suite_name = "a2a_registry"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("R01", "Register valid agent", self.test_r01),
            ("R02", "Register with invalid agent_id (uppercase)", self.test_r02),
            ("R03", "Register with invalid agent_id (too short)", self.test_r03),
            ("R04", "Register with invalid agent_id (special chars)", self.test_r04),
            ("R05", "Register without URL", self.test_r05),
            ("R06", "Register with relative URL", self.test_r06),
            ("R07", "Register without name", self.test_r07),
            ("R08", "Re-register same agent", self.test_r08),
            ("R09", "List agents (no filter)", self.test_r09),
            ("R10", "List agents with skill_tags filter", self.test_r10),
            ("R11", "List agents with limit", self.test_r11),
            ("R12", "Get single agent", self.test_r12),
            ("R13", "Get non-existent agent", self.test_r13),
            ("R14", "Heartbeat valid agent", self.test_r14),
            ("R15", "Heartbeat non-existent agent", self.test_r15),
            ("R16", "Deregister via POST", self.test_r16),
            ("R17", "Deregister via DELETE", self.test_r17),
            ("R18", "Deregister non-existent", self.test_r18),
            ("R19", "Platform agent card", self.test_r19),
            ("R20", "Individual agent card", self.test_r20),
            ("R21", "Agent card for non-existent", self.test_r21),
            ("R22", "GET on A2A endpoint", self.test_r22),
        ]

    async def test_r01(self) -> int:
        card = {
            "agent_id": "test-r01-agent",
            "name": "Test R01 Agent",
            "description": "Test agent for R01",
            "version": "1.0.0",
            "url": "http://localhost:19999/",
            "skills": [
                {
                    "id": "test",
                    "name": "Test",
                    "description": "Test skill",
                    "tags": ["test"],
                }
            ],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        resp = await self.registry.register(card)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert "registered_at" in data or "registered_at" in str(data), (
            "Missing registered_at"
        )
        assert "last_seen" in data or "last_seen" in str(data), "Missing last_seen"
        await self.registry.deregister_post("test-r01-agent")
        return 3

    async def test_r02(self) -> int:
        card = {
            "agent_id": "INVALID_UPPERCASE",
            "name": "Bad",
            "url": "http://localhost:1/",
        }
        resp = await self.registry.register(card)
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        return 1

    async def test_r03(self) -> int:
        card = {"agent_id": "x", "name": "Bad", "url": "http://localhost:1/"}
        resp = await self.registry.register(card)
        assert resp.status_code == 400
        return 1

    async def test_r04(self) -> int:
        card = {
            "agent_id": "agent@invalid!",
            "name": "Bad",
            "url": "http://localhost:1/",
        }
        resp = await self.registry.register(card)
        assert resp.status_code == 400
        return 1

    async def test_r05(self) -> int:
        card = {"agent_id": "test-r05", "name": "Bad"}
        resp = await self.registry.register(card)
        assert resp.status_code == 400
        return 1

    async def test_r06(self) -> int:
        card = {"agent_id": "test-r06", "name": "Bad", "url": "/relative/path"}
        resp = await self.registry.register(card)
        assert resp.status_code == 400
        return 1

    async def test_r07(self) -> int:
        card = {"agent_id": "test-r07", "url": "http://localhost:1/"}
        resp = await self.registry.register(card)
        assert resp.status_code == 400
        return 1

    async def test_r08(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents available")
        agent = agents[0]
        resp1 = await self.registry.get_agent(agent.agent_id)
        data1 = resp1.json()
        resp2 = await self.registry.register(agent.registration_card())
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["registered_at"] == data1["registered_at"], (
            "registered_at must be preserved on re-registration"
        )
        assert data2["last_seen"] >= data1["last_seen"], (
            "last_seen must be updated on re-registration"
        )
        return 4

    async def test_r09(self) -> int:
        resp = await self.registry.list_agents()
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        return 2

    async def test_r10(self) -> int:
        resp = await self.registry.list_agents(skill_tags="test,echo")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list) and len(data) > 0, (
            "Expected at least one agent with matching tags"
        )
        for agent in data:
            agent_tags = {
                tag
                for skill in agent.get("skills", [])
                for tag in skill.get("tags", [])
            }
            assert agent_tags & {"test", "echo"}, (
                f"Agent {agent['agent_id']} has no matching skill tags"
            )
        return 3

    async def test_r11(self) -> int:
        resp = await self.registry.list_agents(limit=2)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) <= 2
        return 2

    async def test_r12(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        resp = await self.registry.get_agent(agents[0].agent_id)
        assert resp.status_code == 200
        return 1

    async def test_r13(self) -> int:
        resp = await self.registry.get_agent("nonexistent-agent-xyz")
        assert resp.status_code == 404
        return 1

    async def test_r14(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        resp = await self.registry.heartbeat(agents[0].agent_id)
        assert resp.status_code == 200
        return 1

    async def test_r15(self) -> int:
        resp = await self.registry.heartbeat("nonexistent-agent-xyz")
        assert resp.status_code == 400
        return 1

    async def test_r16(self) -> int:
        card = {
            "agent_id": "test-r16",
            "name": "Temp",
            "url": "http://localhost:19998/",
            "skills": [],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        await self.registry.register(card)
        resp = await self.registry.deregister_post("test-r16")
        assert resp.status_code == 200
        return 1

    async def test_r17(self) -> int:
        card = {
            "agent_id": "test-r17",
            "name": "Temp",
            "url": "http://localhost:19997/",
            "skills": [],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        await self.registry.register(card)
        resp = await self.registry.deregister_delete("test-r17")
        assert resp.status_code == 200
        return 1

    async def test_r18(self) -> int:
        resp = await self.registry.deregister_post("nonexistent-agent-xyz")
        assert resp.status_code == 404
        return 1

    async def test_r19(self) -> int:
        resp = await self.registry.get_platform_card()
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("name") == "kubemq"
        return 2

    async def test_r20(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        resp = await self.registry.get_agent_card(agents[0].agent_id)
        assert resp.status_code == 200
        return 1

    async def test_r21(self) -> int:
        resp = await self.registry.get_agent_card("nonexistent-agent-xyz")
        assert resp.status_code == 404
        return 1

    async def test_r22(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        resp = await self.a2a.get(f"/a2a/{agents[0].agent_id}")
        assert resp.status_code == 405
        return 1
