#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime_engine.verifier import verify_runner_facts


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify software-change-runner-v2 facts.")
    parser.add_argument("runner_facts", type=Path, help="Path to runner facts JSON.")
    args = parser.parse_args()

    payload = cast(
        dict[str, Any],
        json.loads(args.runner_facts.read_text(encoding="utf-8")),
    )
    decision = verify_runner_facts(payload).as_dict()
    print(json.dumps(decision, indent=2, ensure_ascii=True))

    exit_codes = {"allow": 0, "block": 2, "escalate": 3}
    return exit_codes[decision["decision"]]


if __name__ == "__main__":
    raise SystemExit(main())
