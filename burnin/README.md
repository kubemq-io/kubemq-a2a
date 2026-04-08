# KubeMQ A2A Burn-In

Python test harness for soak-testing the KubeMQ A2A (Agent-to-Agent) endpoint. Adapted from the `kubemq-agents-fabric` A2A test suites, scoped to A2A functionality only.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A running KubeMQ instance with A2A gateway enabled

## Quick Start

```bash
# Install dependencies
uv sync

# Run with default config (functional mode)
uv run python -m kubemq_a2a_burnin

# Run with custom config
uv run python -m kubemq_a2a_burnin -c burnin-config.yaml
```

## Configuration

Edit `burnin-config.yaml` or use environment variables with `KUBEMQ_A2A_BURNIN_` prefix:

| Environment Variable | Config Path | Default |
|---------------------|-------------|---------|
| `KUBEMQ_A2A_BURNIN_SERVER_ADDRESS` | `server.address` | `http://localhost:9090` |
| `KUBEMQ_A2A_BURNIN_METRICS_ADDRESS` | `server.metrics_address` | `http://localhost:8080` |
| `KUBEMQ_A2A_BURNIN_MODE` | `mode` | `functional` |
| `KUBEMQ_A2A_BURNIN_DURATION` | `duration` | `15m` |
| `KUBEMQ_A2A_BURNIN_LOG_LEVEL` | `output.log_level` | `info` |

## Run Modes

| Mode | Suites | Duration | Purpose |
|------|--------|----------|---------|
| `smoke` | a2a_registry, a2a_sync (subset) | ~30s | Quick validation |
| `functional` | All 5 functional suites | ~2-5 min | Full functional coverage |
| `soak` | All 6 suites including a2a_soak | Configurable (default 15m) | Sustained load testing |

## Test Suites

| Suite | Tests | Description |
|-------|-------|-------------|
| `a2a_registry` | R01-R22 | Agent registration, listing, heartbeat, deregistration |
| `a2a_sync` | S01-S14 | Synchronous message/send, headers, concurrency |
| `a2a_streaming` | ST01-ST13 | SSE streaming via POST and GET |
| `a2a_errors` | E01-E14 | Error codes, timeouts, malformed payloads |
| `a2a_limits` | L01-L06 | Concurrency limits, response size, timeout caps |
| `a2a_soak` | SK01-SK05 | Sustained load, memory stability (soak mode only) |

## Mock Agents

| Agent | Behavior |
|-------|----------|
| Echo | Returns request body + X-* headers |
| Slow | Configurable delay (default 2000ms) |
| Error | Cycles through HTTP 400/500/502/503/504 |
| Stream | Emits N SSE events with configurable delay |
| Oversize | Returns >10MB response body |

## Project Structure

```
burnin/
├── burnin-config.yaml          # Default configuration
├── pyproject.toml               # Python project config
├── README.md                    # This file
├── src/kubemq_a2a_burnin/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── config.py                # YAML + env config loader
│   ├── runner.py                # Test suite runner
│   ├── agents/
│   │   ├── base.py              # BaseMockAgent (aiohttp server)
│   │   ├── echo_agent.py
│   │   ├── slow_agent.py
│   │   ├── error_agent.py
│   │   ├── stream_agent.py
│   │   ├── oversize_agent.py
│   │   └── manager.py           # Agent lifecycle manager
│   ├── clients/
│   │   ├── a2a_client.py        # JSON-RPC 2.0 transport client
│   │   ├── registry_client.py   # Agent registry REST client
│   │   └── metrics_client.py    # Prometheus metrics scraper
│   ├── metrics/
│   │   └── tracker.py           # Test result tracker
│   └── suites/
│       ├── base.py              # Base suite class
│       ├── a2a_registry.py      # R01-R22
│       ├── a2a_sync.py          # S01-S14
│       ├── a2a_streaming.py     # ST01-ST13
│       ├── a2a_errors.py        # E01-E14
│       ├── a2a_limits.py        # L01-L06
│       └── a2a_soak.py          # SK01-SK05
└── tests/
    └── test_config.py           # Config unit tests
```

## Success Criteria

| Metric | Threshold |
|--------|-----------|
| Error rate | < 1% |
| p99 latency | < 5000ms |
| p999 latency | < 10000ms |
| Throughput | >= 90% of target |
| Memory growth | < 50% over soak duration |
