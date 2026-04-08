# Python examples

KubeMQ A2A examples using **aiohttp** for the agent HTTP server and **httpx** / **httpx-sse** for registry and A2A clients. The **a2a-sdk** package is declared for alignment with the official SDK ecosystem; example code uses direct JSON-RPC over HTTP as in the project spec.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Install dependencies

From this directory:

```bash
uv sync
```

With pip (from a virtualenv):

```bash
pip install -e .
```

## Run an example

Use two terminals. Replace `{category}` and `{name}` (for example `sync/basic-send`).

**Terminal 1 — agent** (skip for client-only examples such as `errors/agent-not-found`):

```bash
cd examples/python
uv run python {category}/{name}/agent.py
```

**Terminal 2 — client:**

```bash
cd examples/python
uv run python {category}/{name}/client.py
```

## Environment

Examples assume KubeMQ at `http://localhost:9090` unless you change the constants in each script.

## Stack (see spec §5.1)

| Role | Library |
|------|---------|
| A2A SDK (declared) | `a2a-sdk` |
| Agent HTTP server | `aiohttp` |
| HTTP client | `httpx` |
| SSE client | `httpx-sse` |

Dependencies are pinned in [pyproject.toml](pyproject.toml).
