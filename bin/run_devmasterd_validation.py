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

from runtime_engine.devmasterd_validation import (
    DEFAULT_REPORT_PATH,
    DEFAULT_VALIDATION_STATE_ROOT,
    run_devmasterd_operational_validation,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run repeated localhost devmasterd operational validation."
    )
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_VALIDATION_STATE_ROOT)
    args = parser.parse_args()

    report = run_devmasterd_operational_validation(
        iterations=args.iterations,
        output_path=args.output.resolve(),
        state_root=args.state_root.resolve(),
    )
    print(
        json.dumps(
            {
                "output": args.output.as_posix(),
                "pass": report["aggregate"]["pass"],
                "iteration_count": report["iteration_count"],
                "failed_iterations": report["aggregate"]["failed_iterations"],
                "recommendation": report["recommendation"],
            },
            indent=2,
            ensure_ascii=True,
        )
    )
    return 0 if report["aggregate"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
