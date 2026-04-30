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

from runtime_engine.task_progression import derive_next_task


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Derive the next allowed task from the runtime task graph."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root. Defaults to the current dev_master repo.",
    )
    args = parser.parse_args()

    payload = derive_next_task(root=args.root.resolve(), write=True)
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
