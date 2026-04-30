#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

ARTIFACT_FAMILY = "local_evidence_record"
SCHEMA_VERSION = "1.0.0"
POLICY_VERSION = "phase1-gate-v1"
RULESET_VERSION = "local-evidence-fallback-v1"
WRITEBACK_STATUSES = {"completed", "pending", "fallback_local", "not_required"}

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_PATH = REPO_ROOT / "runtime/evidence/index.jsonl"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def build_record(
    *,
    trace_id: str,
    run_id: str,
    stage: str,
    summary: str,
    artifact_refs: list[dict[str, str]],
    verifier_decision_ref: str | None,
    completion_ref: str | None,
    writeback_status: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    if writeback_status not in WRITEBACK_STATUSES:
        allowed = ", ".join(sorted(WRITEBACK_STATUSES))
        raise ValueError(f"writeback_status must be one of: {allowed}")

    timestamp = created_at or utc_now_iso()
    seed = {
        "trace_id": trace_id,
        "run_id": run_id,
        "stage": stage,
        "summary": summary,
        "artifact_refs": artifact_refs,
        "verifier_decision_ref": verifier_decision_ref,
        "completion_ref": completion_ref,
        "writeback_status": writeback_status,
        "created_at": timestamp,
    }
    evidence_id = (
        "ev_"
        + sha256(
            json.dumps(seed, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
                "utf-8"
            )
        ).hexdigest()[:16]
    )

    return {
        "artifact_family": ARTIFACT_FAMILY,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "ruleset_version": RULESET_VERSION,
        "evidence_id": evidence_id,
        "created_at": timestamp,
        "trace_id": trace_id,
        "run_id": run_id,
        "stage": stage,
        "summary": summary,
        "artifact_refs": artifact_refs,
        "verifier_decision_ref": verifier_decision_ref,
        "completion_ref": completion_ref,
        "writeback_status": writeback_status,
        "local_fallback": True,
        "canonical_truth": False,
    }


def append_record(index_path: Path, record: dict[str, Any]) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=True) + "\n")


def artifact_ref_from_path(repo_root: Path, path: Path) -> dict[str, str]:
    artifact_path = path if path.is_absolute() else repo_root / path
    digest = sha256(artifact_path.read_bytes()).hexdigest()
    try:
        display_path = artifact_path.relative_to(repo_root).as_posix()
    except ValueError:
        display_path = artifact_path.as_posix()
    return {"path": display_path, "digest": "sha256:" + digest}


def parse_artifact_ref(value: str) -> dict[str, str]:
    path, separator, digest = value.partition("=")
    if not separator or not path or not digest.startswith("sha256:"):
        raise ValueError("--artifact-ref must use path=sha256:<digest>")
    return {"path": path, "digest": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a local fallback evidence record.")
    parser.add_argument("--index-path", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--artifact-path", type=Path, action="append", default=[])
    parser.add_argument("--artifact-ref", action="append", default=[])
    parser.add_argument("--verifier-decision-ref")
    parser.add_argument("--completion-ref")
    parser.add_argument(
        "--writeback-status",
        default="fallback_local",
        choices=sorted(WRITEBACK_STATUSES),
    )
    args = parser.parse_args()

    artifact_refs = [
        artifact_ref_from_path(REPO_ROOT, artifact_path) for artifact_path in args.artifact_path
    ]
    artifact_refs.extend(parse_artifact_ref(value) for value in args.artifact_ref)

    record = build_record(
        trace_id=args.trace_id,
        run_id=args.run_id,
        stage=args.stage,
        summary=args.summary,
        artifact_refs=artifact_refs,
        verifier_decision_ref=args.verifier_decision_ref,
        completion_ref=args.completion_ref,
        writeback_status=args.writeback_status,
    )
    append_record(args.index_path, record)
    print(json.dumps(record, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
