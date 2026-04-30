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

from runtime_engine.prototype_pipeline import (
    DEFAULT_IDEA_PATH,
    DEFAULT_PROTOTYPE_ROOT,
    DEFAULT_VALIDATION_PATH,
    run_pipeline,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the local L1 idea-to-runnable-prototype pipeline."
    )
    parser.add_argument("--idea", type=Path, default=DEFAULT_IDEA_PATH)
    parser.add_argument("--prototype-root", type=Path, default=DEFAULT_PROTOTYPE_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_VALIDATION_PATH)
    args = parser.parse_args()

    report = run_pipeline(
        idea_path=args.idea.resolve(),
        prototype_root=args.prototype_root.resolve(),
        output_path=args.output.resolve(),
    )
    print(
        json.dumps(
            {
                "output": args.output.as_posix(),
                "pass": report["pass"],
                "prototype_id": report["prototype_id"],
                "prototype_dir": report["prototype_dir"],
                "localhost_http_status": report["localhost_http_status"],
            },
            indent=2,
            ensure_ascii=True,
        )
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
