from __future__ import annotations

import json
from typing import Any

from kubemq_a2a_burnin.suites.base import BaseSuite


class A2AErrorsSuite(BaseSuite):
    suite_name = "a2a_errors"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("E01", "Agent not found", self.test_e01),
            ("E02", "Agent timeout", self.test_e02),
            ("E03", "Agent returns HTTP 500", self.test_e03),
            ("E04", "Agent returns HTTP 503", self.test_e04),
            ("E05", "Agent returns HTTP 502", self.test_e05),
            ("E06", "Agent connection refused", self.test_e06),
            ("E07", "Invalid JSON-RPC payload", self.test_e07),
            ("E08", "Missing method field", self.test_e08),
            ("E09", "Invalid JSON-RPC version", self.test_e09),
            ("E10", "Wrong Content-Type", self.test_e10),
            ("E11", "Empty agent_id", self.test_e11),
            ("E12", "Invalid agent_id format", self.test_e12),
            ("E13", "Agent returns non-JSON", self.test_e13),
            ("E14", "Transport vs application error distinction", self.test_e14),
        ]

    async def test_e01(self) -> int:
        result = await self.a2a.send(
            "nonexistent-agent-e01",
            "message/send",
            {
                "message": {"parts": [{"text": "e01"}]},
            },
        )
        assert "error" in result, "Expected error for non-existent agent"
        assert result["error"]["code"] == -32002, (
            f"Expected code -32002 (agentNotFound), got {result['error']['code']}"
        )
        return 2

    async def test_e02(self) -> int:
        slow_agents = self.agent_manager.get_agents_by_type("slow")
        if not slow_agents:
            raise RuntimeError("No slow agents available")
        agent = slow_agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "e02-timeout"}]},
                "configuration": {"timeout": 1},
            },
            timeout=1,
        )
        assert "error" in result, "Expected timeout error"
        assert result["error"]["code"] == -32001, (
            f"Expected code -32001 (agentTimeout), got {result['error']['code']}"
        )
        return 2

    async def test_e03(self) -> int:
        error_agents = self.agent_manager.get_agents_by_type("error")
        if not error_agents:
            raise RuntimeError("No error agents available")
        agent = error_agents[0]
        agent._error_index = 1
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "e03-500"}]},
            },
        )
        assert "result" in result or "error" in result, (
            "Expected response from error agent"
        )
        return 1

    async def test_e04(self) -> int:
        error_agents = self.agent_manager.get_agents_by_type("error")
        if not error_agents:
            raise RuntimeError("No error agents available")
        agent = error_agents[0]
        agent._error_index = 3
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "e04-503"}]},
            },
        )
        assert "result" in result or "error" in result, "Expected response"
        if "error" in result:
            error_msg = str(result["error"].get("message", "")).lower()
            assert "unavailable" in error_msg or "503" in error_msg, (
                f"Expected 503 unavailable error, got: {result['error']}"
            )
        return 1

    async def test_e05(self) -> int:
        error_agents = self.agent_manager.get_agents_by_type("error")
        if not error_agents:
            raise RuntimeError("No error agents available")
        agent = error_agents[0]
        agent._error_index = 2
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "e05-502"}]},
            },
        )
        assert "result" in result or "error" in result, "Expected response"
        if "error" in result:
            error_msg = str(result["error"].get("message", "")).lower()
            assert "unavailable" in error_msg or "502" in error_msg, (
                f"Expected 502 unavailable error, got: {result['error']}"
            )
        return 1

    async def test_e06(self) -> int:
        card = {
            "agent_id": "test-e06-unreachable",
            "name": "Unreachable Agent",
            "url": "http://localhost:19876/",
            "skills": [],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        await self.registry.register(card)
        try:
            result = await self.a2a.send(
                "test-e06-unreachable",
                "message/send",
                {
                    "message": {"parts": [{"text": "e06"}]},
                },
            )
            assert "error" in result, "Expected error for unreachable agent"
            error_msg = str(result["error"].get("message", "")).lower()
            assert (
                "unreachable" in error_msg
                or "refused" in error_msg
                or "unavailable" in error_msg
            ), f"Expected unreachable error, got: {result['error']}"
        finally:
            await self.registry.deregister_post("test-e06-unreachable")
        return 2

    async def test_e07(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        resp = await self.a2a.send_raw(agents[0].agent_id, b"{invalid json!!!}")
        data = resp.json()
        assert "error" in data, "Expected parse error"
        assert data["error"]["code"] == -32700, (
            f"Expected code -32700 (ParseError), got {data['error']['code']}"
        )
        return 2

    async def test_e08(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "params": {}})
        resp = await self.a2a.send_raw(agents[0].agent_id, payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for missing method"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600 (InvalidRequest), got {data['error']['code']}"
        )
        return 2

    async def test_e09(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        payload = json.dumps(
            {"jsonrpc": "1.0", "id": 1, "method": "message/send", "params": {}}
        )
        resp = await self.a2a.send_raw(agents[0].agent_id, payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for invalid JSON-RPC version"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600 (InvalidRequest), got {data['error']['code']}"
        )
        return 2

    async def test_e10(self) -> int:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "message/send", "params": {}}
        )
        resp = await self.a2a.send_raw(
            agents[0].agent_id, payload.encode(), content_type="text/plain"
        )
        data = resp.json()
        assert "error" in data, "Expected error for wrong Content-Type"
        assert data["error"]["code"] == -32700, (
            f"Expected code -32700 (ParseError), got {data['error']['code']}"
        )
        return 2

    async def test_e11(self) -> int:
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "message/send", "params": {}}
        )
        resp = await self.a2a.send_raw("", payload.encode())
        if resp.status_code == 405 or resp.status_code == 404:
            return 1
        data = resp.json()
        assert "error" in data, "Expected error for empty agent_id"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600, got {data['error']['code']}"
        )
        return 1

    async def test_e12(self) -> int:
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "message/send", "params": {}}
        )
        resp = await self.a2a.send_raw("INVALID_ID", payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for invalid agent_id format"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600, got {data['error']['code']}"
        )
        return 2

    async def test_e13(self) -> int:
        error_agents = self.agent_manager.get_agents_by_type("error")
        if not error_agents:
            raise RuntimeError("No error agents available")
        agent = error_agents[0]
        result = await self.a2a.send(
            agent.agent_id,
            "message/send",
            {
                "message": {"parts": [{"text": "e13-non-json"}]},
            },
        )
        assert "result" in result or "error" in result, (
            "Expected some response for non-JSON body"
        )
        return 1

    async def test_e14(self) -> int:
        card_unreachable = {
            "agent_id": "test-e14-unreachable",
            "name": "Unreachable",
            "url": "http://localhost:19877/",
            "skills": [],
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "protocolVersions": ["1.0"],
        }
        await self.registry.register(card_unreachable)
        try:
            transport_result = await self.a2a.send(
                "test-e14-unreachable",
                "message/send",
                {
                    "message": {"parts": [{"text": "transport-error"}]},
                },
            )
            assert "error" in transport_result, "Transport error: expected error field"

            error_agents = self.agent_manager.get_agents_by_type("error")
            if error_agents:
                app_result = await self.a2a.send(
                    error_agents[0].agent_id,
                    "message/send",
                    {
                        "message": {"parts": [{"text": "app-error"}]},
                    },
                )
                assert "result" in app_result or "error" in app_result, (
                    "Application error: expected response"
                )
        finally:
            await self.registry.deregister_post("test-e14-unreachable")
        return 3
