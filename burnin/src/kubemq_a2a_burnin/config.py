from __future__ import annotations

import os
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ServerConfig:
    address: str = "http://localhost:9090"
    metrics_address: str = "http://localhost:8080"


@dataclass
class EchoAgentConfig:
    count: int = 2


@dataclass
class SlowAgentConfig:
    count: int = 1
    delay_ms: int = 2000


@dataclass
class ErrorAgentConfig:
    count: int = 1
    error_rate: float = 1.0


@dataclass
class StreamingAgentConfig:
    count: int = 2
    events_per_stream: int = 10
    event_delay_ms: int = 100


@dataclass
class OversizeAgentConfig:
    count: int = 1
    response_size_bytes: int = 20_971_520


@dataclass
class AgentsConfig:
    base_port: int = 18080
    echo: EchoAgentConfig = field(default_factory=EchoAgentConfig)
    slow: SlowAgentConfig = field(default_factory=SlowAgentConfig)
    error: ErrorAgentConfig = field(default_factory=ErrorAgentConfig)
    streaming: StreamingAgentConfig = field(default_factory=StreamingAgentConfig)
    oversize: OversizeAgentConfig = field(default_factory=OversizeAgentConfig)


@dataclass
class SuitesConfig:
    a2a_registry: bool = True
    a2a_sync: bool = True
    a2a_streaming: bool = True
    a2a_errors: bool = True
    a2a_limits: bool = True
    a2a_soak: bool = True


@dataclass
class SoakConfig:
    rate: int = 50
    snapshot_interval: str = "30s"


@dataclass
class ThresholdsConfig:
    max_error_rate_pct: float = 1.0
    max_p99_latency_ms: float = 5000
    max_p999_latency_ms: float = 10000
    min_throughput_pct: float = 90
    max_memory_growth_pct: float = 50


@dataclass
class OutputConfig:
    report_file: str = ""
    log_level: str = "info"
    log_format: str = "text"


@dataclass
class BurninConfig:
    version: str = "1"
    server: ServerConfig = field(default_factory=ServerConfig)
    mode: str = "functional"
    duration: str = "15m"
    run_id: str = ""
    agents: AgentsConfig = field(default_factory=AgentsConfig)
    suites: SuitesConfig = field(default_factory=SuitesConfig)
    soak: SoakConfig = field(default_factory=SoakConfig)
    thresholds: ThresholdsConfig = field(default_factory=ThresholdsConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def __post_init__(self) -> None:
        if self.version != "1":
            raise ValueError("Only config version '1' is supported")
        if self.mode not in ("smoke", "functional", "soak"):
            raise ValueError(f"Invalid mode '{self.mode}': must be smoke|functional|soak")
        if not re.match(r"^\d+[smhd]$", self.duration):
            raise ValueError("Duration must match format: <number>[s|m|h|d]")
        if not self.run_id:
            self.run_id = uuid.uuid4().hex[:12]

    def duration_seconds(self) -> int:
        unit_map = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        return int(self.duration[:-1]) * unit_map[self.duration[-1]]


def _apply_nested(data: dict[str, Any], dc_cls: type, defaults: Any | None = None) -> Any:
    """Build a dataclass instance from a dict, handling nested dataclass fields."""
    if defaults is None:
        defaults = dc_cls()
    kwargs: dict[str, Any] = {}
    for f_name in {f.name for f in dc_cls.__dataclass_fields__.values()}:
        if f_name in data:
            child_type = dc_cls.__dataclass_fields__[f_name].type
            child_default = getattr(defaults, f_name)
            if isinstance(data[f_name], dict) and hasattr(child_default, "__dataclass_fields__"):
                kwargs[f_name] = _apply_nested(data[f_name], type(child_default), child_default)
            else:
                kwargs[f_name] = data[f_name]
        else:
            kwargs[f_name] = getattr(defaults, f_name)
    return dc_cls(**kwargs)


def load_config(path: str | None = None) -> BurninConfig:
    """Load config from YAML file, then apply environment variable overrides."""
    data: dict[str, Any] = {}
    if path and Path(path).exists():
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
            if raw is None:
                data = {}
            elif not isinstance(raw, dict):
                raise ValueError(
                    f"Config file must contain a YAML mapping, got {type(raw).__name__}"
                )
            else:
                data = raw

    config = _apply_nested(data, BurninConfig)

    if addr := os.environ.get("KUBEMQ_A2A_BURNIN_SERVER_ADDRESS"):
        config.server.address = addr
    if addr := os.environ.get("KUBEMQ_A2A_BURNIN_METRICS_ADDRESS"):
        config.server.metrics_address = addr
    if mode := os.environ.get("KUBEMQ_A2A_BURNIN_MODE"):
        config.mode = mode
    if dur := os.environ.get("KUBEMQ_A2A_BURNIN_DURATION"):
        config.duration = dur
    if level := os.environ.get("KUBEMQ_A2A_BURNIN_LOG_LEVEL"):
        config.output.log_level = level
    if fmt := os.environ.get("KUBEMQ_A2A_BURNIN_LOG_FORMAT"):
        config.output.log_format = fmt
    if report := os.environ.get("KUBEMQ_A2A_BURNIN_REPORT_FILE"):
        config.output.report_file = report

    config.__post_init__()

    return config
