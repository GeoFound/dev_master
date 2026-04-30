from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

RUNNER_CONTRACT_VERSION = "software-change-runner-v2"
ARTIFACT_FAMILY = "software-change-runner"
SCHEMA_VERSION = "2.0.0"
POLICY_VERSION = "phase1-gate-v1"
RULESET_VERSION = "phase1-core-v1"
COST_POLICY_VERSION = "cost-ceilings-v1"
RATCHET_POLICY_VERSION = "autonomy-ratchet-v1"

CHECK_STATUSES = {"pass", "fail", "not_run"}
RISK_LABELS = {"green", "yellow", "red"}
COST_CEILING_STATUSES = {"within_limit", "soft_alert", "hard_block"}
BOUNDARY_TYPES = {
    "hard_red_line",
    "mature_library_only",
    "ratchetable_guardrail",
    "quality_floor",
}
RATCHET_BEHAVIORS = {
    "never_relax",
    "reduce_human_friction_only",
    "relax_by_metrics",
    "raise_only",
}
BOUNDARY_OWNERS = {"human", "verifier", "ratchet", "external_service"}
FORBIDDEN_APPROVAL_FIELDS = {
    "approval",
    "approval_decision",
    "approved",
    "final_approval",
    "self_approved",
    "verifier_decision",
}

REQUIRED_TOP_LEVEL_FIELDS = {
    "runner_contract_version",
    "artifact_family",
    "schema_version",
    "policy_version",
    "ruleset_version",
    "trace_id",
    "run_id",
    "step_id",
    "repo",
    "ref",
    "requested_change",
    "scope_in",
    "scope_out",
    "diff_digest",
    "files_changed",
    "checks",
    "risk_facts",
    "cost_facts",
    "ratchet_metrics_contribution",
    "engineering_boundary_classification",
    "artifact_digests",
    "evidence_refs",
    "worker",
    "timestamps",
}


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def null_ratchet_metrics(reason: str) -> dict[str, Any]:
    return {
        "contributes": False,
        "reason": reason,
        "metrics": None,
        "policy_version": RATCHET_POLICY_VERSION,
    }


def cost_facts(
    *,
    project_id: str,
    trace_id: str,
    run_id: str,
    estimated_usd: float = 0.0,
    actual_usd: float | None = None,
    per_project_daily_spend_usd: float = 0.0,
    global_daily_spend_usd: float = 0.0,
    ceiling_status: str = "within_limit",
) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "trace_id": trace_id,
        "run_id": run_id,
        "estimated_usd": estimated_usd,
        "actual_usd": actual_usd,
        "per_project_daily_spend_usd": per_project_daily_spend_usd,
        "global_daily_spend_usd": global_daily_spend_usd,
        "ceiling_status": ceiling_status,
        "policy_version": COST_POLICY_VERSION,
    }


def boundary_classification(
    *,
    boundary_id: str,
    boundary_type: str,
    ratchet_behavior: str,
    owner: str,
    allowed_ai_work: list[str],
    forbidden_ai_work: list[str],
    evidence_required: list[str],
) -> dict[str, Any]:
    return {
        "boundary_id": boundary_id,
        "boundary_type": boundary_type,
        "ratchet_behavior": ratchet_behavior,
        "owner": owner,
        "allowed_ai_work": list(allowed_ai_work),
        "forbidden_ai_work": list(forbidden_ai_work),
        "evidence_required": list(evidence_required),
    }


def build_runner_facts(
    *,
    trace_id: str,
    run_id: str,
    step_id: str,
    repo: str,
    ref: str,
    requested_change: str,
    scope_in: list[str],
    scope_out: list[str],
    diff_digest: str,
    files_changed: list[str],
    checks: dict[str, str],
    risk_facts: dict[str, Any],
    cost_facts_payload: dict[str, Any],
    ratchet_metrics_contribution: dict[str, Any],
    engineering_boundary_classification: list[dict[str, Any]],
    artifact_digests: list[str],
    evidence_refs: dict[str, Any],
    worker: dict[str, Any],
    timestamps: dict[str, str],
    entry_turn_id: str | None = None,
    gateway_request_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "runner_contract_version": RUNNER_CONTRACT_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "ruleset_version": RULESET_VERSION,
        "trace_id": trace_id,
        "run_id": run_id,
        "step_id": step_id,
        "repo": repo,
        "ref": ref,
        "requested_change": requested_change,
        "scope_in": list(scope_in),
        "scope_out": list(scope_out),
        "entry_turn_id": entry_turn_id,
        "gateway_request_id": gateway_request_id,
        "diff_digest": diff_digest,
        "files_changed": list(files_changed),
        "checks": deepcopy(checks),
        "risk_facts": deepcopy(risk_facts),
        "cost_facts": deepcopy(cost_facts_payload),
        "ratchet_metrics_contribution": deepcopy(ratchet_metrics_contribution),
        "engineering_boundary_classification": deepcopy(engineering_boundary_classification),
        "artifact_digests": list(artifact_digests),
        "evidence_refs": deepcopy(evidence_refs),
        "worker": deepcopy(worker),
        "timestamps": deepcopy(timestamps),
    }
    return payload


def validate_runner_facts(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(payload))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    _expect(payload, "runner_contract_version", RUNNER_CONTRACT_VERSION, errors)
    _expect(payload, "artifact_family", ARTIFACT_FAMILY, errors)
    _expect(payload, "schema_version", SCHEMA_VERSION, errors)
    _expect(payload, "policy_version", POLICY_VERSION, errors)
    _expect(payload, "ruleset_version", RULESET_VERSION, errors)

    if payload.get("artifact_family") == RUNNER_CONTRACT_VERSION:
        errors.append("artifact_family must not duplicate runner_contract_version")

    for field in ("scope_in", "scope_out", "files_changed", "artifact_digests"):
        if field in payload and not isinstance(payload[field], list):
            errors.append(f"{field} must be a list")

    if not _is_sha256_ref(payload.get("diff_digest")):
        errors.append("diff_digest must start with sha256:")

    for digest in payload.get("artifact_digests", []):
        if not _is_sha256_ref(digest):
            errors.append("artifact_digests entries must start with sha256:")

    _validate_checks(payload.get("checks"), errors)
    _validate_risk_facts(payload.get("risk_facts"), errors)
    _validate_cost_facts(payload.get("cost_facts"), payload, errors)
    _validate_ratchet_metrics(payload.get("ratchet_metrics_contribution"), errors)
    _validate_boundary_classification(payload.get("engineering_boundary_classification"), errors)
    _validate_evidence_refs(payload.get("evidence_refs"), errors)
    _validate_worker(payload.get("worker"), errors)
    _validate_timestamps(payload.get("timestamps"), errors)

    for field in FORBIDDEN_APPROVAL_FIELDS:
        if field in payload:
            errors.append(f"worker-owned runner facts must not include {field}")

    return errors


def _expect(payload: dict[str, Any], field: str, expected: str, errors: list[str]) -> None:
    if field in payload and payload[field] != expected:
        errors.append(f"{field} must be {expected}")


def _is_sha256_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) > 7


def _validate_checks(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("checks must be an object")
        return
    for check_name in ("lint", "tests", "security"):
        status = value.get(check_name)
        if status not in CHECK_STATUSES:
            errors.append(f"checks.{check_name} must be one of {sorted(CHECK_STATUSES)}")


def _validate_risk_facts(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("risk_facts must be an object")
        return
    for field in (
        "docs_only",
        "dependency_changed",
        "secrets_or_permissions_changed",
        "infra_or_deploy_path_changed",
    ):
        if not isinstance(value.get(field), bool):
            errors.append(f"risk_facts.{field} must be a boolean")
    if not isinstance(value.get("action_level"), int):
        errors.append("risk_facts.action_level must be an integer")
    if value.get("risk_label") not in RISK_LABELS:
        errors.append(f"risk_facts.risk_label must be one of {sorted(RISK_LABELS)}")


def _validate_cost_facts(value: Any, payload: dict[str, Any], errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("cost_facts must be an object")
        return
    if value.get("trace_id") != payload.get("trace_id"):
        errors.append("cost_facts.trace_id must match trace_id")
    if value.get("run_id") != payload.get("run_id"):
        errors.append("cost_facts.run_id must match run_id")
    if value.get("ceiling_status") not in COST_CEILING_STATUSES:
        errors.append(f"cost_facts.ceiling_status must be one of {sorted(COST_CEILING_STATUSES)}")
    if value.get("policy_version") != COST_POLICY_VERSION:
        errors.append(f"cost_facts.policy_version must be {COST_POLICY_VERSION}")
    for field in (
        "estimated_usd",
        "per_project_daily_spend_usd",
        "global_daily_spend_usd",
    ):
        if not isinstance(value.get(field), int | float):
            errors.append(f"cost_facts.{field} must be numeric")


def _validate_ratchet_metrics(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("ratchet_metrics_contribution must be an object")
        return
    if value.get("policy_version") != RATCHET_POLICY_VERSION:
        errors.append(
            f"ratchet_metrics_contribution.policy_version must be {RATCHET_POLICY_VERSION}"
        )
    contributes = value.get("contributes")
    if not isinstance(contributes, bool):
        errors.append("ratchet_metrics_contribution.contributes must be a boolean")
        return
    if contributes:
        if not isinstance(value.get("metrics"), dict):
            errors.append("ratchet_metrics_contribution.metrics must be present")
    else:
        if not value.get("reason"):
            errors.append("ratchet_metrics_contribution.reason is required when null")
        if value.get("metrics") is not None:
            errors.append("ratchet_metrics_contribution.metrics must be null")


def _validate_boundary_classification(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("engineering_boundary_classification must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"engineering_boundary_classification[{index}] must be an object")
            continue
        if item.get("boundary_type") not in BOUNDARY_TYPES:
            errors.append(f"engineering_boundary_classification[{index}].boundary_type is invalid")
        if item.get("ratchet_behavior") not in RATCHET_BEHAVIORS:
            errors.append(
                f"engineering_boundary_classification[{index}].ratchet_behavior is invalid"
            )
        if item.get("owner") not in BOUNDARY_OWNERS:
            errors.append(f"engineering_boundary_classification[{index}].owner is invalid")
        for field in ("allowed_ai_work", "forbidden_ai_work", "evidence_required"):
            if not isinstance(item.get(field), list):
                errors.append(
                    f"engineering_boundary_classification[{index}].{field} must be a list"
                )


def _validate_evidence_refs(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("evidence_refs must be an object")
        return
    if "local_evidence_id" not in value:
        errors.append("evidence_refs.local_evidence_id is required")


def _validate_worker(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("worker must be an object")
        return
    for field in FORBIDDEN_APPROVAL_FIELDS:
        if field in value:
            errors.append(f"worker must not include {field}")
    for field in ("implementation", "identity"):
        if not value.get(field):
            errors.append(f"worker.{field} is required")


def _validate_timestamps(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("timestamps must be an object")
        return
    for field in ("started_at", "completed_at"):
        if not value.get(field):
            errors.append(f"timestamps.{field} is required")
