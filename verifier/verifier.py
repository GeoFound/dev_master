#!/usr/bin/env python3
"""Verify software-change-runner-v1 facts.

The verifier gives an allow/block/escalate recommendation. It does not replace
menmery governance, final approval, or a human gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "software-change-runner-v1"
CHECK_VALUES = {"pass", "fail", "not_run"}
RISK_LABELS = {"green", "yellow", "red"}
WRITEBACK_METHODS = {"pending", "remember", "canonical_write", "fallback_local"}


REQUIRED_TOP_LEVEL = {
    "runner_contract_version",
    "trace_id",
    "menmery_context_ref",
    "requested_change",
    "repo_ref",
    "diff_digest",
    "files_changed",
    "checks",
    "risk_facts",
    "evidence_writeback",
}

REQUIRED_RISK_FACTS = {
    "docs_only",
    "repo_local_ai_scaffold",
    "dependency_changed",
    "secrets_or_permissions_changed",
    "infra_or_deploy_path_changed",
    "external_write",
    "action_level",
    "risk_label",
}


def load_facts(path: Path) -> dict[str, Any]:
    # Runner facts are JSON-compatible YAML, parsed with stdlib JSON to avoid
    # adding Phase 1 dependencies.
    return json.loads(path.read_text(encoding="utf-8"))


def as_bool(value: Any) -> bool:
    return isinstance(value, bool) and value


def verify(facts: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL - facts.keys())
    if missing:
        issues.append(f"missing top-level fields: {', '.join(missing)}")

    if facts.get("runner_contract_version") != CONTRACT_VERSION:
        issues.append("runner_contract_version mismatch")

    if not str(facts.get("diff_digest", "")).startswith("sha256:"):
        issues.append("diff_digest must start with sha256:")

    files_changed = facts.get("files_changed")
    if not isinstance(files_changed, list):
        issues.append("files_changed must be a list")

    checks = facts.get("checks", {})
    if not isinstance(checks, dict):
        issues.append("checks must be a mapping")
    else:
        for name in ("lint", "tests", "security"):
            value = checks.get(name)
            if value not in CHECK_VALUES:
                issues.append(f"checks.{name} must be one of pass|fail|not_run")
            elif value == "fail":
                issues.append(f"checks.{name} failed")

    risk = facts.get("risk_facts", {})
    if not isinstance(risk, dict):
        issues.append("risk_facts must be a mapping")
        risk = {}
    else:
        missing_risk = sorted(REQUIRED_RISK_FACTS - risk.keys())
        if missing_risk:
            issues.append(f"missing risk facts: {', '.join(missing_risk)}")

    action_level = risk.get("action_level")
    if action_level not in {0, 1, 2, 3, 4}:
        issues.append("risk_facts.action_level must be 0..4")

    risk_label = risk.get("risk_label")
    if risk_label not in RISK_LABELS:
        issues.append("risk_facts.risk_label must be green|yellow|red")

    if as_bool(risk.get("secrets_or_permissions_changed")) or as_bool(
        risk.get("infra_or_deploy_path_changed")
    ):
        if action_level != 4 or risk_label != "red":
            issues.append("red risk facts must map to action_level 4 and red label")

    if as_bool(risk.get("dependency_changed")) and risk_label == "green":
        issues.append("dependency changes cannot be green")

    if as_bool(risk.get("external_write")) and (not isinstance(action_level, int) or action_level < 3):
        issues.append("external writes require action_level >= 3")

    if risk_label == "green" and isinstance(action_level, int) and action_level > 2:
        issues.append("green risk cannot exceed action_level 2")

    writeback = facts.get("evidence_writeback", {})
    if not isinstance(writeback, dict):
        issues.append("evidence_writeback must be a mapping")
    else:
        method = writeback.get("method")
        evidence_id = writeback.get("id")
        if method not in WRITEBACK_METHODS:
            issues.append("evidence_writeback.method is invalid")
        if method in {"remember", "canonical_write"} and not evidence_id:
            issues.append("canonical/remember writeback requires evidence id")
        if method in {"pending", "fallback_local"}:
            warnings.append("evidence writeback is local or pending, not canonical")

    if issues:
        decision = "block"
    elif isinstance(action_level, int) and action_level >= 3:
        decision = "escalate"
    else:
        decision = "allow"

    return {
        "decision": decision,
        "reasons": issues or ["runner facts satisfy Phase 1 verifier checks"],
        "warnings": warnings,
        "required_writeback": True,
        "runner_contract_version": CONTRACT_VERSION,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify software-change-runner-v1 facts")
    parser.add_argument("--facts", required=True)
    parser.add_argument("--output")
    parser.add_argument("--expect-decision", choices=["allow", "block", "escalate"])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = verify(load_facts(Path(args.facts)))

    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    if args.expect_decision and report["decision"] != args.expect_decision:
        print(
            f"expected decision {args.expect_decision}, got {report['decision']}",
            file=sys.stderr,
        )
        return 1

    if not args.expect_decision and report["decision"] == "block":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
