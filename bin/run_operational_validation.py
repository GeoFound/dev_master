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

from runtime_engine.operational_validation import write_operational_validation_report

DEFAULT_OUTPUT = REPO_ROOT / "runtime/operational-validation/current-kernel-report.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run repo-local operational validation for the current dev_master kernel."
    )
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = write_operational_validation_report(
        output_path=args.output.resolve(),
        iterations=args.iterations,
    )
    print(
        json.dumps(
            {
                "output": args.output.as_posix(),
                "pass": report["aggregate"]["pass"],
                "iteration_count": report["iteration_count"],
                "recommendation": report["recommendation"],
                "failed_checks": report["aggregate"]["failed_checks"],
            },
            indent=2,
            ensure_ascii=True,
        )
    )
    return 0 if report["aggregate"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
