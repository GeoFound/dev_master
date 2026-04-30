from __future__ import annotations

import json
import unittest
from pathlib import Path

from runtime_engine.runner_contract import (
    boundary_classification,
    build_runner_facts,
    cost_facts,
    null_ratchet_metrics,
    validate_runner_facts,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def build_valid_runner_facts() -> dict:
    trace_id = "tr_test"
    run_id = "run_test"
    return build_runner_facts(
        trace_id=trace_id,
        run_id=run_id,
        step_id="step_test",
        repo="dev_master",
        ref="working-tree",
        requested_change="Test runner contract builder.",
        scope_in=["runtime_engine/", "tests/"],
        scope_out=["external repo mutation"],
        diff_digest="sha256:test-diff",
        files_changed=["runtime_engine/runner_contract.py"],
        checks={"lint": "not_run", "tests": "pass", "security": "not_run"},
        risk_facts={
            "docs_only": False,
            "dependency_changed": False,
            "secrets_or_permissions_changed": False,
            "infra_or_deploy_path_changed": False,
            "action_level": 2,
            "risk_label": "green",
        },
        cost_facts_payload=cost_facts(
            project_id="dev_master",
            trace_id=trace_id,
            run_id=run_id,
        ),
        ratchet_metrics_contribution=null_ratchet_metrics(
            "Unit test builder sample; no metric window contribution."
        ),
        engineering_boundary_classification=[
            boundary_classification(
                boundary_id="runner_contract.test",
                boundary_type="quality_floor",
                ratchet_behavior="raise_only",
                owner="verifier",
                allowed_ai_work=["implementation", "tests"],
                forbidden_ai_work=["worker_self_approval"],
                evidence_required=["tests"],
            )
        ],
        artifact_digests=["sha256:test-artifact"],
        evidence_refs={"menmery_audit_id": None, "local_evidence_id": "ev_test"},
        worker={
            "implementation": "local-worktree-runner",
            "identity": "worker-local",
        },
        timestamps={
            "started_at": "2026-04-30T00:00:00Z",
            "completed_at": "2026-04-30T00:01:00Z",
        },
    )


class RunnerContractTests(unittest.TestCase):
    def test_builder_emits_valid_phase1_runner_facts(self) -> None:
        payload = build_valid_runner_facts()
        self.assertEqual(validate_runner_facts(payload), [])
        self.assertEqual(payload["runner_contract_version"], "software-change-runner-v2")
        self.assertEqual(payload["artifact_family"], "software-change-runner")

    def test_example_runner_facts_are_valid(self) -> None:
        path = REPO_ROOT / "runtime/examples/runner-facts.example.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(validate_runner_facts(payload), [])

    def test_schema_declares_required_contract_fields(self) -> None:
        path = REPO_ROOT / "runtime/schemas/software-change-runner-v2.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        required = set(schema["required"])
        self.assertIn("ratchet_metrics_contribution", required)
        self.assertIn("cost_facts", required)
        self.assertIn("engineering_boundary_classification", required)
        self.assertIn("diff_digest", required)

    def test_missing_ratchet_metric_reason_is_invalid(self) -> None:
        payload = build_valid_runner_facts()
        payload["ratchet_metrics_contribution"]["reason"] = ""
        errors = validate_runner_facts(payload)
        self.assertIn("ratchet_metrics_contribution.reason is required when null", errors)

    def test_worker_self_approval_is_invalid(self) -> None:
        payload = build_valid_runner_facts()
        payload["worker"]["self_approved"] = True
        errors = validate_runner_facts(payload)
        self.assertIn("worker must not include self_approved", errors)

    def test_cost_facts_must_match_trace_and_run(self) -> None:
        payload = build_valid_runner_facts()
        payload["cost_facts"]["run_id"] = "run_other"
        errors = validate_runner_facts(payload)
        self.assertIn("cost_facts.run_id must match run_id", errors)

    def test_boundary_classification_enforces_known_types(self) -> None:
        payload = build_valid_runner_facts()
        payload["engineering_boundary_classification"][0]["boundary_type"] = "unknown"
        errors = validate_runner_facts(payload)
        self.assertIn(
            "engineering_boundary_classification[0].boundary_type is invalid",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
