from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from kubemq_a2a_burnin.config import load_config

logger = logging.getLogger("kubemq_a2a_burnin")


def _configure_logging(level: str, fmt: str) -> None:
    numeric = getattr(logging, level.upper(), logging.INFO)
    if fmt == "json":
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '{"time":"%(asctime)s","level":"%(levelname)s",'
                '"logger":"%(name)s","message":"%(message)s"}'
            )
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-5s %(name)s  %(message)s")
        )
    logging.root.handlers.clear()
    logging.root.addHandler(handler)
    logging.root.setLevel(numeric)


async def _run(config_path: str | None, tests: str | None = None) -> int:
    config = load_config(config_path)
    _configure_logging(config.output.log_level, config.output.log_format)

    logger.info(
        "kubemq-a2a-burnin v%s  mode=%s  run_id=%s",
        "1.0.0",
        config.mode,
        config.run_id or "(auto)",
    )

    test_filter = (
        {t.strip() for t in tests.split(",") if t.strip()} if tests else None
    )

    try:
        from kubemq_a2a_burnin.runner import Runner  # noqa: F811

        runner = Runner(config, test_filter=test_filter)
        return await runner.run()
    except ImportError:
        logger.error("Runner not yet available (Phase 9)")
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="KubeMQ A2A Burn-In")
    parser.add_argument(
        "-c", "--config", default="burnin-config.yaml", help="Config file path"
    )
    parser.add_argument(
        "--tests",
        default=None,
        help="Comma-separated test IDs to run, e.g. SK03,SK04 (default: all)",
    )
    args = parser.parse_args()

    rc = asyncio.run(_run(args.config, args.tests))
    sys.exit(rc)


if __name__ == "__main__":
    main()
