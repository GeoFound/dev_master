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

from runtime_engine.provider_adapter import (
    DEFAULT_PROVIDER_EVIDENCE_DIR,
    adapt_provider_fixture,
    validate_provider_output,
)

DEFAULT_OUTPUT = DEFAULT_PROVIDER_EVIDENCE_DIR / "stub-provider-output.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize a local API-compatible provider fixture into provider evidence."
    )
    parser.add_argument("--provider-fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--provider-kind", default="api", choices=["api", "local_tool"])
    parser.add_argument("--project-id", default="dev_master")
    parser.add_argument("--trace-id", default="tr_provider_adapter_stub")
    parser.add_argument("--run-id", default="run_provider_adapter_stub")
    args = parser.parse_args()

    result = adapt_provider_fixture(
        fixture_path=args.provider_fixture.resolve(),
        output_path=args.output.resolve(),
        provider_kind=args.provider_kind,
        project_id=args.project_id,
        trace_id=args.trace_id,
        run_id=args.run_id,
    )
    validation_errors = validate_provider_output(result.provider_output)
    summary = {
        "output": args.output.as_posix(),
        "raw_output_ref": result.provider_output["provider_raw_output_ref"],
        "drift_detected": result.provider_output["drift_detected"],
        "drift_reasons": result.provider_output["drift_reasons"],
        "validation_errors": validation_errors,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 1 if validation_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
