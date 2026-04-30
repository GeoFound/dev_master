#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime_engine.semantic_benchmark import load_json, run_benchmark, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the semantic verifier fixture benchmark.")
    parser.add_argument(
        "--fixture-set",
        type=Path,
        default=REPO_ROOT / "runtime/fixtures/semantic-verifier-v1.json",
    )
    parser.add_argument(
        "--base-runner-facts",
        type=Path,
        default=REPO_ROOT / "runtime/runs/phase1-first-bounded-loop/runner-facts.json",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = run_benchmark(
        fixture_set=load_json(args.fixture_set),
        base_runner_facts=load_json(args.base_runner_facts),
    )
    if args.output is not None:
        write_report(args.output, report)
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
