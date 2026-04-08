from __future__ import annotations

import asyncio
import logging
import random
import time
from typing import Any

from kubemq_a2a_burnin.clients.a2a_client import A2AClient
from kubemq_a2a_burnin.suites.base import BaseSuite

logger = logging.getLogger(__name__)

_UNIT_MAP = {"s": 1, "m": 60, "h": 3600, "d": 86400}

_LATENCY_RESERVOIR_CAP = 10_000


def _reservoir_append(reservoir: list[float], value: float, total_seen: int) -> None:
    """Reservoir sampling: keep at most _LATENCY_RESERVOIR_CAP items uniformly."""
    if len(reservoir) < _LATENCY_RESERVOIR_CAP:
        reservoir.append(value)
    else:
        idx = random.randint(0, total_seen - 1)
        if idx < _LATENCY_RESERVOIR_CAP:
            reservoir[idx] = value


class A2ASoakSuite(BaseSuite):
    """Sustained load / soak tests for A2A endpoints (SK01-SK05)."""

    suite_name = "a2a_soak"

    def _snapshot_seconds(self) -> int:
        si = self.config.soak.snapshot_interval
        return int(si[:-1]) * _UNIT_MAP[si[-1]]

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("SK01", "Sustained sync throughput", self.test_sk01),
            ("SK02", "Sustained streaming throughput", self.test_sk02),
            ("SK03", "Mixed sync + streaming load", self.test_sk03),
            ("SK04", "Registry churn under load", self.test_sk04),
            ("SK05", "Memory stability", self.test_sk05),
        ]

    async def test_sk01(self) -> int:
        """Send message/send at configured rate for duration, measure p50/p99/p999."""
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        rate = self.config.soak.rate
        duration_s = self.config.duration_seconds()
        interval = 1.0 / rate

        latencies: list[float] = []
        errors = 0
        total = 0
        first_error_logged = False
        start = time.time()

        while (time.time() - start) < duration_s:
            t0 = time.time()
            try:
                result = await self.a2a.send(
                    agent.agent_id,
                    "message/send",
                    {"message": {"parts": [{"text": "soak-sync"}]}},
                )
                if "error" in result:
                    errors += 1
                    if not first_error_logged:
                        logger.warning("SK01 first JSON-RPC error: %s", result["error"])
                        first_error_logged = True
                else:
                    total += 1
                    _reservoir_append(latencies, (time.time() - t0) * 1000, total)
            except Exception as exc:
                errors += 1
                if not first_error_logged:
                    logger.warning("SK01 first exception: %s", exc, exc_info=True)
                    first_error_logged = True
            total += 1

            elapsed = time.time() - t0
            if elapsed < interval:
                await asyncio.sleep(interval - elapsed)

        error_rate = (errors / total * 100) if total > 0 else 0
        assert error_rate <= self.config.thresholds.max_error_rate_pct, (
            f"Error rate {error_rate:.2f}% exceeds threshold "
            f"{self.config.thresholds.max_error_rate_pct}%"
        )

        if latencies:
            latencies.sort()
            p99_idx = int(len(latencies) * 0.99)
            p999_idx = int(len(latencies) * 0.999)
            p99 = latencies[min(p99_idx, len(latencies) - 1)]
            p999 = latencies[min(p999_idx, len(latencies) - 1)]
            logger.info(
                "SK01 stats: total=%d errors=%d p99=%.1fms p999=%.1fms",
                total, errors, p99, p999,
            )
            assert p99 <= self.config.thresholds.max_p99_latency_ms, (
                f"p99 latency {p99:.1f}ms exceeds {self.config.thresholds.max_p99_latency_ms}ms"
            )
            assert p999 <= self.config.thresholds.max_p999_latency_ms, (
                f"p999 latency {p999:.1f}ms exceeds {self.config.thresholds.max_p999_latency_ms}ms"
            )
        return 3

    async def test_sk02(self) -> int:
        """Open/close streams at configured rate for duration."""
        stream_agents = self.agent_manager.get_agents_by_type("streaming")
        if not stream_agents:
            raise RuntimeError("No streaming agents for soak")

        duration_s = self.config.duration_seconds()
        concurrent_streams = min(5, len(stream_agents) * 2)
        errors = 0
        total_completions = 0

        async def _stream_loop(agent_id: str, idx: int) -> tuple[int, int]:
            local_ok = 0
            local_err = 0
            first_err_logged = False
            a2a_client = A2AClient(self.config.server.address)
            try:
                end_time = time.time() + duration_s
                while time.time() < end_time:
                    try:
                        async for event in a2a_client.stream(
                            agent_id,
                            "message/stream",
                            {"message": {"parts": [{"text": f"soak-stream-{idx}"}]}},
                        ):
                            if event.get("event") in ("task.done", "task.error"):
                                break
                        local_ok += 1
                    except Exception as exc:
                        local_err += 1
                        if not first_err_logged:
                            logger.debug("SK02 worker-%d first error: %s", idx, exc)
                            first_err_logged = True
                    await asyncio.sleep(0.5)
            finally:
                await a2a_client.close()
            return local_ok, local_err

        tasks = [
            _stream_loop(stream_agents[i % len(stream_agents)].agent_id, i)
            for i in range(concurrent_streams)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for r in results:
            if isinstance(r, tuple):
                total_completions += r[0]
                errors += r[1]
            else:
                errors += 1

        total_ops = total_completions + errors
        error_rate = (errors / total_ops * 100) if total_ops > 0 else 0
        target_throughput = total_completions / total_ops * 100 if total_ops > 0 else 0
        logger.info(
            "SK02 stats: completions=%d errors=%d throughput=%.1f%%",
            total_completions, errors, target_throughput,
        )
        assert error_rate <= self.config.thresholds.max_error_rate_pct, (
            f"Stream error rate {error_rate:.2f}% exceeds threshold"
        )
        assert target_throughput >= self.config.thresholds.min_throughput_pct, (
            f"Throughput {target_throughput:.1f}% below {self.config.thresholds.min_throughput_pct}%"
        )
        return 2

    async def test_sk03(self) -> int:
        """Interleave sync and streaming requests at 50/50 ratio."""
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        stream_agents = self.agent_manager.get_agents_by_type("streaming")
        if not stream_agents:
            raise RuntimeError("No streaming agents for mixed soak")

        duration_s = self.config.duration_seconds()
        rate = max(1, self.config.soak.rate // 2)
        interval = 1.0 / rate

        sync_latencies: list[float] = []
        sync_successes = 0
        sync_errors = 0
        sync_total = 0
        stream_errors = 0
        stream_total = 0
        first_sync_err = False
        first_stream_err = False

        async def _sync_loop() -> None:
            nonlocal sync_errors, sync_total, sync_successes, first_sync_err
            end = time.time() + duration_s
            while time.time() < end:
                t0 = time.time()
                try:
                    result = await self.a2a.send(
                        agents[0].agent_id,
                        "message/send",
                        {"message": {"parts": [{"text": "mixed-sync"}]}},
                    )
                    if "error" in result:
                        sync_errors += 1
                        if not first_sync_err:
                            logger.warning("SK03 sync first error: %s", result["error"])
                            first_sync_err = True
                    else:
                        sync_successes += 1
                        _reservoir_append(sync_latencies, (time.time() - t0) * 1000, sync_successes)
                except Exception as exc:
                    sync_errors += 1
                    if not first_sync_err:
                        logger.warning("SK03 sync exception: %s", exc, exc_info=True)
                        first_sync_err = True
                sync_total += 1
                elapsed = time.time() - t0
                if elapsed < interval:
                    await asyncio.sleep(interval - elapsed)

        async def _stream_loop() -> None:
            nonlocal stream_errors, stream_total, first_stream_err
            a2a_client = A2AClient(self.config.server.address)
            try:
                end = time.time() + duration_s
                while time.time() < end:
                    try:
                        async for event in a2a_client.stream(
                            stream_agents[0].agent_id,
                            "message/stream",
                            {"message": {"parts": [{"text": "mixed-stream"}]}},
                        ):
                            if event.get("event") in ("task.done", "task.error"):
                                break
                    except Exception as exc:
                        stream_errors += 1
                        if not first_stream_err:
                            logger.debug("SK03 stream error: %s", exc)
                            first_stream_err = True
                    stream_total += 1
                    await asyncio.sleep(0.5)
            finally:
                await a2a_client.close()

        await asyncio.gather(_sync_loop(), _stream_loop())

        total_ops = sync_total + stream_total
        total_errors = sync_errors + stream_errors
        error_rate = (total_errors / total_ops * 100) if total_ops > 0 else 0
        logger.info(
            "SK03 stats: sync=%d/%d stream=%d/%d error_rate=%.2f%%",
            sync_total - sync_errors, sync_total,
            stream_total - stream_errors, stream_total,
            error_rate,
        )
        assert error_rate <= self.config.thresholds.max_error_rate_pct, (
            f"Mixed error rate {error_rate:.2f}% exceeds threshold"
        )

        if sync_latencies:
            sync_latencies.sort()
            p99_idx = int(len(sync_latencies) * 0.99)
            p99 = sync_latencies[min(p99_idx, len(sync_latencies) - 1)]
            assert p99 <= self.config.thresholds.max_p99_latency_ms, (
                f"Sync p99 {p99:.1f}ms exceeds threshold under mixed load"
            )

        throughput = ((total_ops - total_errors) / total_ops * 100) if total_ops > 0 else 0
        assert throughput >= self.config.thresholds.min_throughput_pct, (
            f"Throughput {throughput:.1f}% below {self.config.thresholds.min_throughput_pct}%"
        )
        return 3

    async def test_sk04(self) -> int:
        """Register/deregister agents while sync traffic flows."""
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        duration_s = self.config.duration_seconds()
        rate = max(1, self.config.soak.rate // 2)
        interval = 1.0 / rate

        traffic_errors = 0
        traffic_total = 0
        churn_errors = 0
        churn_total = 0
        first_traffic_err = False

        async def _traffic_loop() -> None:
            nonlocal traffic_errors, traffic_total, first_traffic_err
            end = time.time() + duration_s
            while time.time() < end:
                t0 = time.time()
                try:
                    result = await self.a2a.send(
                        agent.agent_id,
                        "message/send",
                        {"message": {"parts": [{"text": "churn-traffic"}]}},
                    )
                    if "error" in result:
                        traffic_errors += 1
                        if not first_traffic_err:
                            logger.warning("SK04 traffic first error: %s", result["error"])
                            first_traffic_err = True
                except Exception as exc:
                    traffic_errors += 1
                    if not first_traffic_err:
                        logger.warning("SK04 traffic exception: %s", exc, exc_info=True)
                        first_traffic_err = True
                traffic_total += 1
                elapsed = time.time() - t0
                if elapsed < interval:
                    await asyncio.sleep(interval - elapsed)

        async def _churn_loop() -> None:
            nonlocal churn_errors, churn_total
            end = time.time() + duration_s
            idx = 0
            while time.time() < end:
                agent_id = f"churn-sk04-{idx:04d}"
                try:
                    card = {
                        "agent_id": agent_id,
                        "name": f"Churn {idx}",
                        "url": f"http://localhost:{19600 + (idx % 100)}/",
                        "skills": [],
                        "defaultInputModes": ["text"],
                        "defaultOutputModes": ["text"],
                        "protocolVersions": ["1.0"],
                    }
                    await self.registry.register(card)
                    await self.registry.deregister_post(agent_id)
                except Exception as exc:
                    churn_errors += 1
                    if churn_errors == 1:
                        logger.warning("SK04 churn error: %s", exc)
                churn_total += 1
                idx += 1
                await asyncio.sleep(0.2)

        await asyncio.gather(_traffic_loop(), _churn_loop())

        logger.info(
            "SK04 stats: traffic=%d/%d churn=%d/%d",
            traffic_total - traffic_errors, traffic_total,
            churn_total - churn_errors, churn_total,
        )
        assert churn_errors == 0, (
            f"Registration churn had {churn_errors} failures"
        )
        traffic_error_rate = (
            (traffic_errors / traffic_total * 100) if traffic_total > 0 else 0
        )
        assert traffic_error_rate <= self.config.thresholds.max_error_rate_pct, (
            f"Traffic error rate during churn {traffic_error_rate:.2f}% exceeds threshold"
        )
        return 2

    async def test_sk05(self) -> int:
        """Monitor KubeMQ memory via Prometheus, assert <50% growth."""
        start_snap = await self.metrics.scrape()
        start_mem = start_snap.get("process_resident_memory_bytes")
        if start_mem == 0:
            logger.warning("process_resident_memory_bytes not found, skipping memory check")
            return 1

        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents configured")
        agent = agents[0]
        duration_s = self.config.duration_seconds()
        rate = max(1, self.config.soak.rate // 2)
        interval = 1.0 / rate
        start = time.time()
        send_errors = 0
        send_total = 0
        first_err_logged = False

        while (time.time() - start) < duration_s:
            t0 = time.time()
            try:
                await self.a2a.send(
                    agent.agent_id,
                    "message/send",
                    {"message": {"parts": [{"text": "mem-soak"}]}},
                )
            except Exception as exc:
                send_errors += 1
                if not first_err_logged:
                    logger.warning("SK05 send error: %s", exc, exc_info=True)
                    first_err_logged = True
            send_total += 1
            elapsed = time.time() - t0
            if elapsed < interval:
                await asyncio.sleep(interval - elapsed)

        max_acceptable_errors = max(1, int(send_total * 0.1))
        assert send_errors <= max_acceptable_errors, (
            f"SK05 had {send_errors}/{send_total} send errors (>{max_acceptable_errors} threshold)"
        )

        end_snap = await self.metrics.scrape()
        end_mem = end_snap.get("process_resident_memory_bytes")
        growth_pct = ((end_mem - start_mem) / start_mem * 100) if start_mem > 0 else 0
        logger.info(
            "SK05 stats: start_mem=%.1fMB end_mem=%.1fMB growth=%.1f%% send_errors=%d/%d",
            start_mem / 1024 / 1024, end_mem / 1024 / 1024, growth_pct,
            send_errors, send_total,
        )
        assert growth_pct <= self.config.thresholds.max_memory_growth_pct, (
            f"Memory growth {growth_pct:.1f}% exceeds {self.config.thresholds.max_memory_growth_pct}%"
        )
        return 1
