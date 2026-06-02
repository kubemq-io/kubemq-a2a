from __future__ import annotations

import asyncio
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

# Periodically re-heartbeat registered agents to keep them alive for the full
# duration of long soak runs. The server expires agent registrations on a TTL
# (observed: agents went missing < 11 min after registration when never
# heartbeated, which made SK03/SK04 fail with -32002 "agent not found"). Keep
# the interval well under that TTL.
_HEARTBEAT_INTERVAL_SECONDS = 30


class AgentManager:
    """Creates, starts, registers, and manages the lifecycle of all mock agents."""

    def __init__(self, config: BurninConfig) -> None:
        self._config = config
        self._agents: list[BaseMockAgent] = []
        self._registry = RegistryClient(config.server.address)
        self._heartbeat_task: asyncio.Task[None] | None = None

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

    async def start_heartbeats(self) -> None:
        """Start a background task that keeps every registered agent alive.

        Without this, agents registered once at startup expire on the server's
        registration TTL partway through a long soak, and later sends fail with
        JSON-RPC -32002 "agent not found".
        """
        if self._heartbeat_task is not None:
            return
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        logger.info(
            "Started agent heartbeat loop (every %ds for %d agents)",
            _HEARTBEAT_INTERVAL_SECONDS,
            len(self._agents),
        )

    async def _heartbeat_loop(self) -> None:
        while True:
            await asyncio.sleep(_HEARTBEAT_INTERVAL_SECONDS)
            for agent in self._agents:
                try:
                    resp = await self._registry.heartbeat(agent.agent_id)
                    if resp.status_code != 200:
                        logger.warning(
                            "Heartbeat for %s returned HTTP %d: %s",
                            agent.agent_id,
                            resp.status_code,
                            resp.text,
                        )
                except (OSError, httpx.HTTPError) as exc:
                    logger.warning("Heartbeat for %s failed: %s", agent.agent_id, exc)

    async def stop_heartbeats(self) -> None:
        if self._heartbeat_task is None:
            return
        self._heartbeat_task.cancel()
        try:
            await self._heartbeat_task
        except asyncio.CancelledError:
            pass
        self._heartbeat_task = None

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
        await self.stop_heartbeats()
        await self.deregister_all()
        await self.stop_all()
        await self._registry.close()
