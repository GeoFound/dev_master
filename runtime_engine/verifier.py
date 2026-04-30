from __future__ import annotations

import json
from dataclasses import dataclass
from fnmatch import fnmatchcase
from hashlib import sha256
from pathlib import PurePosixPath
from typing import Any, Literal

from runtime_engine.runner_contract import (
    POLICY_VERSION,
    RUNNER_CONTRACT_VERSION,
    validate_runner_facts,
)

VERIFIER_ARTIFACT_FAMILY = "verifier_decision"
VERIFIER_SCHEMA_VERSION = "1.0.0"
VERIFIER_POLICY_VERSION = POLICY_VERSION
VERIFIER_RULESET_VERSION = "verifier-core-v1"

PER_PROJECT_DAILY_USD = 5.0
GLOBAL_DAILY_USD = 30.0

Decision = Literal["allow", "block", "escalate"]
FindingSeverity = Literal["block", "escalate", "warn"]


@dataclass(frozen=True)
class Finding:
    code: str
    severity: FindingSeverity
    message: str
    path: str | None = None
    ruleset_version: str = VERIFIER_RULESET_VERSION

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "ruleset_version": self.ruleset_version,
        }
        if self.path is not None:
            payload["path"] = self.path
        return payload


@dataclass(frozen=True)
class VerifierDecision:
    decision: Decision
    reasons: tuple[str, ...]
    findings: tuple[Finding, ...]
    trace_id: str | None
    run_id: str | None
    step_id: str | None
    source_runner_digest: str
    required_evidence_persistence: bool = True
    artifact_family: str = VERIFIER_ARTIFACT_FAMILY
    schema_version: str = VERIFIER_SCHEMA_VERSION
    policy_version: str = VERIFIER_POLICY_VERSION
    ruleset_version: str = VERIFIER_RULESET_VERSION
    runner_contract_version: str = RUNNER_CONTRACT_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "artifact_family": self.artifact_family,
            "schema_version": self.schema_version,
            "policy_version": self.policy_version,
            "ruleset_version": self.ruleset_version,
            "runner_contract_version": self.runner_contract_version,
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "step_id": self.step_id,
            "source_runner_digest": self.source_runner_digest,
            "decision": self.decision,
            "reasons": list(self.reasons),
            "findings": [finding.as_dict() for finding in self.findings],
            "required_evidence_persistence": self.required_evidence_persistence,
        }


def verify_runner_facts(payload: dict[str, Any]) -> VerifierDecision:
    findings: list[Finding] = []

    for error in validate_runner_facts(payload):
        findings.append(
            Finding(
                code="runner_contract.invalid",
                severity="block",
                message=error,
            )
        )

    _check_scope(payload, findings)
    _check_explicit_checks(payload, findings)
    _check_risk_fit(payload, findings)
    _check_cost_facts(payload, findings)
    _check_boundary_fit(payload, findings)
    _check_provider_drift(payload, findings)
    _check_evidence_fit(payload, findings)

    decision = _decision_from_findings(findings)
    reasons = tuple(
        finding.message for finding in findings if finding.severity in {"block", "escalate"}
    )

    return VerifierDecision(
        decision=decision,
        reasons=reasons,
        findings=tuple(findings),
        trace_id=_optional_str(payload.get("trace_id")),
        run_id=_optional_str(payload.get("run_id")),
        step_id=_optional_str(payload.get("step_id")),
        source_runner_digest=_digest_payload(payload),
    )


def _decision_from_findings(findings: list[Finding]) -> Decision:
    if any(finding.severity == "block" for finding in findings):
        return "block"
    if any(finding.severity == "escalate" for finding in findings):
        return "escalate"
    return "allow"


def _check_scope(payload: dict[str, Any], findings: list[Finding]) -> None:
    files_changed = _string_list(payload.get("files_changed"))
    scope_in = _path_constraints(payload.get("scope_in"))
    scope_out = _path_constraints(payload.get("scope_out"))

    for path in files_changed:
        if _unsafe_repo_path(path):
            findings.append(
                Finding(
                    code="scope.unsafe_path",
                    severity="block",
                    message=f"files_changed contains unsafe path: {path}",
                    path="files_changed",
                )
            )
            continue

        if scope_in and not any(_matches_scope(path, constraint) for constraint in scope_in):
            findings.append(
                Finding(
                    code="scope.out_of_bounds",
                    severity="block",
                    message=f"changed file is outside declared scope_in: {path}",
                    path="files_changed",
                )
            )

        if any(_matches_scope(path, constraint) for constraint in scope_out):
            findings.append(
                Finding(
                    code="scope.forbidden_path",
                    severity="block",
                    message=f"changed file matches declared scope_out: {path}",
                    path="files_changed",
                )
            )


def _check_explicit_checks(payload: dict[str, Any], findings: list[Finding]) -> None:
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        return

    statuses = [checks.get(name) for name in ("lint", "tests", "security")]
    for name, status in checks.items():
        if status == "fail":
            findings.append(
                Finding(
                    code="checks.failed",
                    severity="block",
                    message=f"check failed: {name}",
                    path=f"checks.{name}",
                )
            )

    if statuses and all(status == "not_run" for status in statuses):
        findings.append(
            Finding(
                code="checks.no_signal",
                severity="block",
                message="all required checks are not_run; verifier has no check signal",
                path="checks",
            )
        )


def _check_risk_fit(payload: dict[str, Any], findings: list[Finding]) -> None:
    risk_facts = payload.get("risk_facts")
    if not isinstance(risk_facts, dict):
        return

    label = risk_facts.get("risk_label")
    action_level = risk_facts.get("action_level")
    risky_green_facts = [
        name
        for name in (
            "dependency_changed",
            "secrets_or_permissions_changed",
            "infra_or_deploy_path_changed",
        )
        if risk_facts.get(name) is True
    ]

    if label == "green" and risky_green_facts:
        findings.append(
            Finding(
                code="risk.green_conflicts_with_facts",
                severity="block",
                message=(
                    "risk_label green conflicts with changed-file facts: "
                    + ", ".join(risky_green_facts)
                ),
                path="risk_facts.risk_label",
            )
        )

    if label == "green" and isinstance(action_level, int) and action_level > 2:
        findings.append(
            Finding(
                code="risk.green_conflicts_with_action_level",
                severity="block",
                message="risk_label green is incompatible with action_level > 2",
                path="risk_facts.action_level",
            )
        )

    if label == "yellow" or (isinstance(action_level, int) and action_level == 3):
        findings.append(
            Finding(
                code="risk.requires_human_review",
                severity="escalate",
                message="yellow risk requires human review in Phase 1",
                path="risk_facts.risk_label",
            )
        )

    if label == "red" or (isinstance(action_level, int) and action_level >= 4):
        findings.append(
            Finding(
                code="risk.red_line",
                severity="block",
                message="red risk is outside autonomous Phase 1 execution",
                path="risk_facts.risk_label",
            )
        )

    if risk_facts.get("docs_only") is True:
        non_docs = [
            path
            for path in _string_list(payload.get("files_changed"))
            if not path.endswith((".md", ".markdown", ".txt"))
        ]
        if non_docs:
            findings.append(
                Finding(
                    code="risk.docs_only_conflicts_with_files",
                    severity="block",
                    message="docs_only is true but non-document files changed: "
                    + ", ".join(non_docs),
                    path="risk_facts.docs_only",
                )
            )


def _check_cost_facts(payload: dict[str, Any], findings: list[Finding]) -> None:
    cost_facts = payload.get("cost_facts")
    if not isinstance(cost_facts, dict):
        return

    if cost_facts.get("ceiling_status") == "hard_block":
        findings.append(
            Finding(
                code="cost.hard_block",
                severity="block",
                message="cost ceiling status is hard_block",
                path="cost_facts.ceiling_status",
            )
        )

    per_project_spend = _number(cost_facts.get("per_project_daily_spend_usd"))
    if per_project_spend is not None and per_project_spend > PER_PROJECT_DAILY_USD:
        findings.append(
            Finding(
                code="cost.per_project_daily_exceeded",
                severity="block",
                message=f"per-project daily spend exceeds USD {PER_PROJECT_DAILY_USD}",
                path="cost_facts.per_project_daily_spend_usd",
            )
        )

    global_spend = _number(cost_facts.get("global_daily_spend_usd"))
    if global_spend is not None and global_spend > GLOBAL_DAILY_USD:
        findings.append(
            Finding(
                code="cost.global_daily_exceeded",
                severity="block",
                message=f"global daily spend exceeds USD {GLOBAL_DAILY_USD}",
                path="cost_facts.global_daily_spend_usd",
            )
        )


def _check_boundary_fit(payload: dict[str, Any], findings: list[Finding]) -> None:
    classifications = payload.get("engineering_boundary_classification")
    if not isinstance(classifications, list):
        return

    for index, item in enumerate(classifications):
        if not isinstance(item, dict):
            continue
        boundary_type = item.get("boundary_type")
        if boundary_type == "hard_red_line":
            findings.append(
                Finding(
                    code="boundary.hard_red_line",
                    severity="block",
                    message="hard red-line boundary cannot be executed autonomously",
                    path=f"engineering_boundary_classification[{index}]",
                )
            )

        attempted_ai_work = _string_list(item.get("attempted_ai_work"))
        forbidden_ai_work = set(_string_list(item.get("forbidden_ai_work")))
        attempted_forbidden = sorted(set(attempted_ai_work) & forbidden_ai_work)
        if attempted_forbidden:
            findings.append(
                Finding(
                    code="boundary.forbidden_ai_work",
                    severity="block",
                    message="attempted AI work is forbidden: " + ", ".join(attempted_forbidden),
                    path=f"engineering_boundary_classification[{index}].attempted_ai_work",
                )
            )


def _check_provider_drift(payload: dict[str, Any], findings: list[Finding]) -> None:
    if payload.get("provider_drift_detected") is True:
        findings.append(
            Finding(
                code="provider.drift_detected",
                severity="block",
                message="provider drift detected; output fails closed",
                path="provider_drift_detected",
            )
        )

    provider_output = payload.get("provider_output")
    if isinstance(provider_output, dict) and provider_output.get("drift_detected") is True:
        findings.append(
            Finding(
                code="provider.output_drift_detected",
                severity="block",
                message="provider output drift detected; output fails closed",
                path="provider_output.drift_detected",
            )
        )


def _check_evidence_fit(payload: dict[str, Any], findings: list[Finding]) -> None:
    evidence_refs = payload.get("evidence_refs")
    if not isinstance(evidence_refs, dict):
        return

    if not _non_empty_str(evidence_refs.get("local_evidence_id")):
        findings.append(
            Finding(
                code="evidence.local_ref_missing",
                severity="block",
                message="evidence_refs.local_evidence_id must be a non-empty string",
                path="evidence_refs.local_evidence_id",
            )
        )

    entry_turn_id = payload.get("entry_turn_id")
    if _non_empty_str(entry_turn_id) and not _non_empty_str(evidence_refs.get("menmery_audit_id")):
        writeback_status = evidence_refs.get("writeback_status")
        if writeback_status not in {"pending", "fallback_local", "not_required"}:
            findings.append(
                Finding(
                    code="evidence.optional_writeback_unresolved",
                    severity="block",
                    message=(
                        "entry_turn_id is present but optional service writeback has "
                        "no audit ref or explicit fallback/pending status"
                    ),
                    path="evidence_refs",
                )
            )


def _digest_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return "sha256:" + sha256(encoded).hexdigest()


def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _path_constraints(value: Any) -> list[str]:
    return [
        item for item in _string_list(value) if item and not any(char.isspace() for char in item)
    ]


def _unsafe_repo_path(path: str) -> bool:
    pure = PurePosixPath(path)
    return path.startswith("/") or ".." in pure.parts


def _matches_scope(path: str, constraint: str) -> bool:
    normalized_path = path.strip("/")
    normalized_constraint = constraint.strip("/")

    if normalized_constraint in {"", ".", "*"}:
        return True
    if any(char in normalized_constraint for char in "*?[]"):
        return fnmatchcase(normalized_path, normalized_constraint) or PurePosixPath(
            normalized_path
        ).match(normalized_constraint)

    return normalized_path == normalized_constraint or normalized_path.startswith(
        normalized_constraint + "/"
    )
