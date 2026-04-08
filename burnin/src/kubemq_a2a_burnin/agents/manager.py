from __future__ import annotations

import logging

import httpx

from kubemq_a2a_burnin.agents.base import BaseMockAgent
from kubemq_a2a_burnin.agents.echo_agent import EchoAgent
from kubemq_a2a_burnin.agents.slow_agent import SlowAgent
from kubemq_a2a_burnin.agents.error_agent import ErrorAgent
from kubemq_a2a_burnin.agents.stream_agent import StreamAgent
from kubemq_a2a_burnin.agents.oversize_agent import OversizeAgent
from kubemq_a2a_burnin.clients.registry_client import RegistryClient
from kubemq_a2a_burnin.config import BurninConfig

logger = logging.getLogger(__name__)


class AgentManager:
    """Creates, starts, registers, and manages the lifecycle of all mock agents."""

    def __init__(self, config: BurninConfig) -> None:
        self._config = config
        self._agents: list[BaseMockAgent] = []
        self._registry = RegistryClient(config.server.address)

    @property
    def agents(self) -> list[BaseMockAgent]:
        return list(self._agents)

    def get_agents_by_type(self, agent_type: str) -> list[BaseMockAgent]:
        return [a for a in self._agents if a.agent_type == agent_type]

    async def create_all(self) -> None:
        port = self._config.agents.base_port
        cfg = self._config.agents

        for i in range(cfg.echo.count):
            self._agents.append(
                EchoAgent(f"echo-{i + 1:02d}", f"Echo Agent {i + 1:02d}", port)
            )
            port += 1

        for i in range(cfg.slow.count):
            self._agents.append(
                SlowAgent(
                    f"slow-{i + 1:02d}",
                    f"Slow Agent {i + 1:02d}",
                    port,
                    delay_ms=cfg.slow.delay_ms,
                )
            )
            port += 1

        for i in range(cfg.error.count):
            self._agents.append(
                ErrorAgent(
                    f"error-{i + 1:02d}",
                    f"Error Agent {i + 1:02d}",
                    port,
                    error_rate=cfg.error.error_rate,
                )
            )
            port += 1

        for i in range(cfg.streaming.count):
            self._agents.append(
                StreamAgent(
                    f"stream-{i + 1:02d}",
                    f"Stream Agent {i + 1:02d}",
                    port,
                    events_per_stream=cfg.streaming.events_per_stream,
                    event_delay_ms=cfg.streaming.event_delay_ms,
                )
            )
            port += 1

        for i in range(cfg.oversize.count):
            self._agents.append(
                OversizeAgent(
                    f"oversize-{i + 1:02d}",
                    f"Oversize Agent {i + 1:02d}",
                    port,
                    response_size_bytes=cfg.oversize.response_size_bytes,
                )
            )
            port += 1

    async def start_all(self) -> None:
        for agent in self._agents:
            try:
                await agent.start()
            except OSError as exc:
                logger.error(
                    "Failed to start agent %s on port %d: %s",
                    agent.agent_id,
                    agent.port,
                    exc,
                )
                raise

    async def register_all(self) -> None:
        for agent in self._agents:
            resp = await self._registry.register(agent.registration_card())
            if resp.status_code != 200:
                logger.error("Failed to register %s: %s", agent.agent_id, resp.text)
                raise RuntimeError(
                    f"Agent registration failed for {agent.agent_id}: {resp.text}"
                )
            logger.info("Registered agent %s", agent.agent_id)

    async def deregister_all(self) -> None:
        for agent in self._agents:
            try:
                await self._registry.deregister_post(agent.agent_id)
            except (OSError, httpx.HTTPError) as exc:
                logger.warning("Failed to deregister %s: %s", agent.agent_id, exc)

    async def stop_all(self) -> None:
        for agent in self._agents:
            try:
                await agent.stop()
            except OSError as exc:
                logger.warning("Failed to stop %s: %s", agent.agent_id, exc)

    async def cleanup(self) -> None:
        await self.deregister_all()
        await self.stop_all()
        await self._registry.close()
