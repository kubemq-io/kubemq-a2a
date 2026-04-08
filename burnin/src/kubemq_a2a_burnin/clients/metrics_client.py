from __future__ import annotations

import re

import httpx


class MetricsSnapshot:
    """Parsed Prometheus metrics snapshot for delta computation."""

    def __init__(self, raw: str) -> None:
        self._metrics: dict[str, list[tuple[dict[str, str], float]]] = {}
        self._parse(raw)

    def _parse(self, raw: str) -> None:
        for line in raw.strip().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            match = re.match(r"^(\w+)(\{([^}]*)\})?\s+([\d.eE+-]+)", line)
            if not match:
                continue
            name = match.group(1)
            labels_str = match.group(3) or ""
            value = float(match.group(4))
            labels = {}
            if labels_str:
                for pair in re.findall(r'(\w+)="([^"]*)"', labels_str):
                    labels[pair[0]] = pair[1]
            self._metrics.setdefault(name, []).append((labels, value))

    def get(self, name: str, labels: dict[str, str] | None = None) -> float:
        """Get metric value matching name and optional label filters."""
        for entry_labels, value in self._metrics.get(name, []):
            if labels is None or all(
                entry_labels.get(k) == v for k, v in labels.items()
            ):
                return value
        return 0.0


def compute_delta(
    before: MetricsSnapshot,
    after: MetricsSnapshot,
    metric_name: str,
    labels: dict[str, str] | None = None,
) -> float:
    return after.get(metric_name, labels) - before.get(metric_name, labels)


class MetricsClient:
    """Scrapes Prometheus /metrics endpoint from KubeMQ server."""

    def __init__(self, metrics_url: str) -> None:
        self._url = metrics_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=10.0)

    async def scrape(self) -> MetricsSnapshot:
        resp = await self._client.get(f"{self._url}/metrics")
        resp.raise_for_status()
        return MetricsSnapshot(resp.text)

    async def close(self) -> None:
        await self._client.aclose()
