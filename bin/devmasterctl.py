#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime_engine.devmasterd_client import (
    DEFAULT_BASE_URL,
    DEFAULT_CLI_SMOKE_PATH,
    DEFAULT_CLI_STATE_DIR,
    DevmasterClient,
    load_task_proposal,
    run_cli_smoke,
    run_cli_smoke_with_test_daemon,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Control a local devmasterd daemon.")
    parser.add_argument("--base-url", default=os.environ.get("DEVMASTERD_URL", DEFAULT_BASE_URL))
    parser.add_argument("--token-env", default="DEVMASTERD_TOKEN")
    parser.add_argument("--test-token", help="Explicit local test token for smoke tests only.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Read devmasterd state.")
    subparsers.add_parser("evidence", help="Read devmasterd evidence records.")

    intake = subparsers.add_parser("intake", help="Submit a local task proposal JSON.")
    intake.add_argument("--proposal", type=Path, required=True)

    smoke = subparsers.add_parser("smoke", help="Run CLI smoke against localhost devmasterd.")
    smoke.add_argument("--output", type=Path, default=DEFAULT_CLI_SMOKE_PATH)
    smoke.add_argument("--proposal", type=Path)
    smoke.add_argument("--provider-fixture", type=Path)
    smoke.add_argument("--start-test-daemon", action="store_true")
    smoke.add_argument("--state-dir", type=Path, default=DEFAULT_CLI_STATE_DIR)

    args = parser.parse_args()
    token = args.test_token or os.environ.get(args.token_env)
    if not token:
        print(f"{args.token_env} is required", file=sys.stderr)
        return 2

    if args.command == "smoke":
        report = _run_smoke_command(args, token)
        print(_summary_json({"output": args.output.as_posix(), "pass": report["pass"]}))
        return 0 if report["pass"] else 1

    client = DevmasterClient(base_url=args.base_url, token=token)
    if args.command == "status":
        print(_summary_json(client.status()))
        return 0
    if args.command == "evidence":
        print(_summary_json(client.evidence()))
        return 0
    if args.command == "intake":
        task_proposal = load_task_proposal(args.proposal)
        print(_summary_json(client.intake(task_proposal)))
        return 0

    print(f"unknown command: {args.command}", file=sys.stderr)
    return 2


def _run_smoke_command(args: argparse.Namespace, token: str) -> dict[str, Any]:
    provider_fixture = args.provider_fixture if args.provider_fixture else None
    common = {
        "token": token,
        "output_path": args.output.resolve(),
        "task_proposal_path": args.proposal,
    }
    if provider_fixture is not None:
        common["provider_fixture"] = provider_fixture
    if args.start_test_daemon:
        return run_cli_smoke_with_test_daemon(
            **common,
            state_dir=args.state_dir.resolve(),
        )
    return run_cli_smoke(
        **common,
        base_url=args.base_url,
    )


def _summary_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=True)


if __name__ == "__main__":
    raise SystemExit(main())
