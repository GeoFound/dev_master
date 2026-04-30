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

from runtime_engine.task_progression import complete_current_task


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Complete the current task, persist a completion record, " "and derive the next task."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root. Defaults to the current dev_master repo.",
    )
    parser.add_argument(
        "--status",
        required=True,
        choices=["completed", "hold", "correct", "rollback", "blocked"],
    )
    parser.add_argument("--decision", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--recommendation-for-human", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--gate-verdict", choices=["pass", "fail", "pending"])
    parser.add_argument("--drift-found", action="store_true")
    args = parser.parse_args()

    payload = complete_current_task(
        root=args.root.resolve(),
        status=args.status,
        decision=args.decision,
        summary=args.summary,
        recommendation_for_human=args.recommendation_for_human,
        artifacts_changed=args.artifact,
        evidence_refs=args.evidence_ref,
        drift_found=args.drift_found,
        gate_verdict=args.gate_verdict,
        notes=args.note,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
