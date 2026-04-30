from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
YELLOW_PREP = REPO_ROOT / "runtime/yellow-prep"


class YellowPreparationTests(unittest.TestCase):
    def test_yellow_categories_do_not_enable_auto_approval(self) -> None:
        payload = _load("yellow-categories.json")

        self.assertFalse(payload["yellow_auto_approval_enabled"])
        self.assertEqual(payload["default_decision_after_timeout"], "hold")
        self.assertTrue(payload["human_approval_required"])
        for category in payload["categories"]:
            self.assertEqual(category["risk_label"], "yellow")
            self.assertIn("approve", category["forbidden_ai_work"])

    def test_review_payload_template_timeout_never_approves(self) -> None:
        payload = _load("review-payload-template.json")

        self.assertEqual(payload["default_review_mode"], "async_queue")
        self.assertEqual(payload["default_decision_after_timeout"], "hold")
        self.assertTrue(payload["timeout_must_not_auto_approve"])
        self.assertFalse(payload["auto_approval_enabled"])

    def test_deploy_preview_template_has_no_production_authority(self) -> None:
        payload = _load("deploy-preview-payload-template.json")

        self.assertTrue(payload["preview_only"])
        self.assertFalse(payload["production_authority"])
        self.assertFalse(payload["production_deploy_allowed"])
        self.assertFalse(payload["protected_branch_merge_allowed"])
        self.assertFalse(payload["auto_deploy_enabled"])
        self.assertTrue(payload["human_approval_required"])

    def test_example_review_pack_stays_pending_for_human(self) -> None:
        payload = _load("example-review-pack.json")

        self.assertEqual(payload["risk_label"], "yellow")
        self.assertEqual(payload["current_decision"], "pending_human")
        self.assertEqual(payload["default_decision_after_timeout"], "hold")
        self.assertFalse(payload["auto_approval_enabled"])
        self.assertTrue(payload["human_approval_required"])
        self.assertFalse(payload["deploy_preview_payload"]["production_authority"])

    def test_summary_is_gate_d_ready_without_autonomy_expansion(self) -> None:
        payload = _load("yellow-preparation-summary.json")

        self.assertEqual(payload["result"], "ready_for_gate_d_review")
        self.assertFalse(payload["yellow_auto_approval_enabled"])
        self.assertFalse(payload["production_authority"])
        self.assertEqual(payload["phase3_scope"], "yellow preparation only")


def _load(name: str) -> dict:
    return json.loads((YELLOW_PREP / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
