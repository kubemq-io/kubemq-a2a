from __future__ import annotations

import os
import tempfile
import textwrap

import pytest

from kubemq_a2a_burnin.config import BurninConfig, load_config


class TestBurninConfigDefaults:
    def test_default_values(self) -> None:
        cfg = BurninConfig()
        assert cfg.version == "1"
        assert cfg.mode == "functional"
        assert cfg.duration == "15m"
        assert cfg.server.address == "http://localhost:9090"
        assert cfg.server.metrics_address == "http://localhost:8080"
        assert cfg.agents.base_port == 18080
        assert cfg.soak.rate == 50
        assert cfg.thresholds.max_error_rate_pct == 1.0
        assert cfg.thresholds.max_p99_latency_ms == 5000
        assert cfg.thresholds.max_p999_latency_ms == 10000
        assert cfg.thresholds.min_throughput_pct == 90
        assert cfg.thresholds.max_memory_growth_pct == 50

    def test_duration_seconds(self) -> None:
        cfg = BurninConfig(duration="15m")
        assert cfg.duration_seconds() == 900

        cfg = BurninConfig(duration="30s")
        assert cfg.duration_seconds() == 30

        cfg = BurninConfig(duration="1h")
        assert cfg.duration_seconds() == 3600

        cfg = BurninConfig(duration="2d")
        assert cfg.duration_seconds() == 172800

    def test_auto_run_id(self) -> None:
        cfg = BurninConfig()
        assert len(cfg.run_id) == 12

    def test_explicit_run_id_preserved(self) -> None:
        cfg = BurninConfig(run_id="my-run-123")
        assert cfg.run_id == "my-run-123"


class TestBurninConfigValidation:
    def test_invalid_version(self) -> None:
        with pytest.raises(ValueError, match="Only config version"):
            BurninConfig(version="2")

    def test_invalid_mode(self) -> None:
        with pytest.raises(ValueError, match="Invalid mode"):
            BurninConfig(mode="turbo")

    def test_invalid_duration_format(self) -> None:
        with pytest.raises(ValueError, match="Duration must match"):
            BurninConfig(duration="fifteen")

    def test_valid_modes(self) -> None:
        for mode in ("smoke", "functional", "soak"):
            cfg = BurninConfig(mode=mode)
            assert cfg.mode == mode


class TestBurninConfigSuites:
    def test_all_suites_enabled_by_default(self) -> None:
        cfg = BurninConfig()
        assert cfg.suites.a2a_registry is True
        assert cfg.suites.a2a_sync is True
        assert cfg.suites.a2a_streaming is True
        assert cfg.suites.a2a_errors is True
        assert cfg.suites.a2a_limits is True
        assert cfg.suites.a2a_soak is True


class TestLoadConfig:
    def test_load_from_yaml(self, tmp_path: object) -> None:
        yaml_content = textwrap.dedent("""\
            version: "1"
            mode: smoke
            duration: 30s
            server:
              address: http://localhost:9999
        """)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write(yaml_content)
            path = f.name

        try:
            cfg = load_config(path)
            assert cfg.mode == "smoke"
            assert cfg.duration == "30s"
            assert cfg.server.address == "http://localhost:9999"
            assert cfg.server.metrics_address == "http://localhost:8080"
        finally:
            os.unlink(path)

    def test_load_nonexistent_file(self) -> None:
        cfg = load_config("/tmp/nonexistent-burnin-config.yaml")
        assert cfg.mode == "functional"

    def test_env_var_overrides(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("KUBEMQ_A2A_BURNIN_SERVER_ADDRESS", "http://env-host:9090")
        monkeypatch.setenv("KUBEMQ_A2A_BURNIN_MODE", "soak")
        monkeypatch.setenv("KUBEMQ_A2A_BURNIN_DURATION", "1h")
        monkeypatch.setenv("KUBEMQ_A2A_BURNIN_LOG_LEVEL", "debug")

        cfg = load_config(None)
        assert cfg.server.address == "http://env-host:9090"
        assert cfg.mode == "soak"
        assert cfg.duration == "1h"
        assert cfg.output.log_level == "debug"


class TestAgentsConfig:
    def test_default_agent_counts(self) -> None:
        cfg = BurninConfig()
        assert cfg.agents.echo.count == 2
        assert cfg.agents.slow.count == 1
        assert cfg.agents.error.count == 1
        assert cfg.agents.streaming.count == 2
        assert cfg.agents.oversize.count == 1

    def test_slow_agent_defaults(self) -> None:
        cfg = BurninConfig()
        assert cfg.agents.slow.delay_ms == 2000

    def test_error_agent_defaults(self) -> None:
        cfg = BurninConfig()
        assert cfg.agents.error.error_rate == 1.0

    def test_streaming_agent_defaults(self) -> None:
        cfg = BurninConfig()
        assert cfg.agents.streaming.events_per_stream == 10
        assert cfg.agents.streaming.event_delay_ms == 100

    def test_oversize_agent_defaults(self) -> None:
        cfg = BurninConfig()
        assert cfg.agents.oversize.response_size_bytes == 20_971_520
