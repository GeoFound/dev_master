from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from runtime_engine.verifier import verify_runner_facts

ARTIFACT_FAMILY = "semantic_verifier_benchmark"
SCHEMA_VERSION = "1.0.0"
POLICY_VERSION = "phase1-gate-v1"
RULESET_VERSION = "semantic-verifier-benchmark-v1"


@dataclass(frozen=True)
class FixtureResult:
    fixture_id: str
    fixture_type: str
    expected_decision: str
    actual_decision: str
    expected_codes: tuple[str, ...]
    actual_codes: tuple[str, ...]
    matched: bool
    critical_false_allow: bool
    actionable: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "fixture_type": self.fixture_type,
            "expected_decision": self.expected_decision,
            "actual_decision": self.actual_decision,
            "expected_codes": list(self.expected_codes),
            "actual_codes": list(self.actual_codes),
            "matched": self.matched,
            "critical_false_allow": self.critical_false_allow,
            "actionable": self.actionable,
        }


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def run_benchmark(
    *,
    fixture_set: dict[str, Any],
    base_runner_facts: dict[str, Any],
    created_at: str | None = None,
) -> dict[str, Any]:
    results = [
        _run_fixture(fixture=fixture, base_runner_facts=base_runner_facts)
        for fixture in _fixtures(fixture_set)
    ]
    fixture_count = len(results)
    critical_false_allow_count = sum(1 for result in results if result.critical_false_allow)
    mismatch_count = sum(1 for result in results if not result.matched)
    missing_actionable_reason_count = sum(
        1
        for result in results
        if result.actual_decision in {"block", "escalate"} and not result.actionable
    )
    misclassification_rate = mismatch_count / fixture_count if fixture_count else 1.0
    fixture_types = sorted({result.fixture_type for result in results})
    pass_conditions_met = (
        fixture_count >= 20
        and {"forced_ok", "forced_bad", "risk_boundary"}.issubset(set(fixture_types))
        and critical_false_allow_count == 0
        and misclassification_rate < 0.05
        and missing_actionable_reason_count == 0
    )

    return {
        "artifact_family": ARTIFACT_FAMILY,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "ruleset_version": RULESET_VERSION,
        "created_at": created_at or utc_now_iso(),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set["schema_version"],
        "fixture_count": fixture_count,
        "fixture_types": fixture_types,
        "critical_false_allow_count": critical_false_allow_count,
        "risk_misclassification_count": mismatch_count,
        "total_risk_misclassification_rate": misclassification_rate,
        "missing_actionable_reason_count": missing_actionable_reason_count,
        "pass": pass_conditions_met,
        "results": [result.as_dict() for result in results],
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _fixtures(fixture_set: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = fixture_set.get("fixtures")
    if not isinstance(fixtures, list):
        raise ValueError("fixture_set.fixtures must be a list")
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def _run_fixture(fixture: dict[str, Any], base_runner_facts: dict[str, Any]) -> FixtureResult:
    payload = deepcopy(base_runner_facts)
    for mutation in _mutations(fixture):
        _apply_mutation(payload, mutation)

    verifier_decision = verify_runner_facts(payload).as_dict()
    actual_decision = str(verifier_decision["decision"])
    actual_codes = tuple(finding["code"] for finding in verifier_decision["findings"])
    expected_decision = str(fixture["expected_decision"])
    expected_codes = tuple(cast(list[str], fixture.get("expected_codes", [])))
    matched = actual_decision == expected_decision and set(expected_codes).issubset(actual_codes)
    actionable = actual_decision == "allow" or bool(verifier_decision["reasons"])

    return FixtureResult(
        fixture_id=str(fixture["fixture_id"]),
        fixture_type=str(fixture["fixture_type"]),
        expected_decision=expected_decision,
        actual_decision=actual_decision,
        expected_codes=expected_codes,
        actual_codes=actual_codes,
        matched=matched,
        critical_false_allow=expected_decision != "allow" and actual_decision == "allow",
        actionable=actionable,
    )


def _mutations(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    mutations = fixture.get("mutations", [])
    if not isinstance(mutations, list):
        raise ValueError("fixture.mutations must be a list")
    return [mutation for mutation in mutations if isinstance(mutation, dict)]


def _apply_mutation(payload: dict[str, Any], mutation: dict[str, Any]) -> None:
    operation = mutation.get("op")
    path = mutation.get("path")
    if not isinstance(path, list) or not all(isinstance(part, str) for part in path):
        raise ValueError("mutation.path must be a list of strings")
    if not path:
        raise ValueError("mutation.path must not be empty")

    if operation == "set":
        _set_path(payload, path, mutation.get("value"))
        return
    if operation == "delete":
        _delete_path(payload, path)
        return
    raise ValueError(f"unsupported mutation operation: {operation}")


def _set_path(payload: dict[str, Any], path: list[str], value: Any) -> None:
    current = payload
    for part in path[:-1]:
        next_value = current.setdefault(part, {})
        if not isinstance(next_value, dict):
            raise ValueError(f"cannot traverse non-object mutation path: {'.'.join(path)}")
        current = next_value
    current[path[-1]] = value


def _delete_path(payload: dict[str, Any], path: list[str]) -> None:
    current = payload
    for part in path[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            return
        current = next_value
    current.pop(path[-1], None)
