from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from runtime_engine.verifier import verify_runner_facts
from tests.test_runner_contract import build_valid_runner_facts

REPO_ROOT = Path(__file__).resolve().parent.parent


class VerifierKernelTests(unittest.TestCase):
    def test_valid_runner_facts_are_allowed(self) -> None:
        decision = verify_runner_facts(build_valid_runner_facts()).as_dict()
        self.assertEqual(decision["decision"], "allow")
        self.assertEqual(decision["reasons"], [])
        self.assertEqual(decision["artifact_family"], "verifier_decision")
        self.assertEqual(decision["ruleset_version"], "verifier-core-v1")
        self.assertTrue(decision["source_runner_digest"].startswith("sha256:"))

    def test_forced_bad_fixture_blocks(self) -> None:
        path = REPO_ROOT / "tests/fixtures/runner-facts.forced-bad.json"
        payload = json.loads(path.read_text(encoding="utf-8"))

        decision = verify_runner_facts(payload).as_dict()
        finding_codes = {finding["code"] for finding in decision["findings"]}

        self.assertEqual(decision["decision"], "block")
        self.assertIn("scope.out_of_bounds", finding_codes)
        self.assertIn("scope.forbidden_path", finding_codes)

    def test_failed_check_blocks(self) -> None:
        payload = build_valid_runner_facts()
        payload["checks"]["tests"] = "fail"

        decision = verify_runner_facts(payload).as_dict()

        self.assertEqual(decision["decision"], "block")
        self.assertIn("check failed: tests", decision["reasons"])

    def test_green_dependency_risk_blocks(self) -> None:
        payload = build_valid_runner_facts()
        payload["risk_facts"]["dependency_changed"] = True

        decision = verify_runner_facts(payload).as_dict()
        finding_codes = {finding["code"] for finding in decision["findings"]}

        self.assertEqual(decision["decision"], "block")
        self.assertIn("risk.green_conflicts_with_facts", finding_codes)

    def test_yellow_risk_escalates(self) -> None:
        payload = build_valid_runner_facts()
        payload["risk_facts"]["risk_label"] = "yellow"
        payload["risk_facts"]["action_level"] = 3

        decision = verify_runner_facts(payload).as_dict()

        self.assertEqual(decision["decision"], "escalate")
        self.assertEqual(decision["findings"][0]["severity"], "escalate")

    def test_hard_cost_ceiling_blocks(self) -> None:
        payload = build_valid_runner_facts()
        payload["cost_facts"]["ceiling_status"] = "hard_block"

        decision = verify_runner_facts(payload).as_dict()

        self.assertEqual(decision["decision"], "block")
        self.assertIn("cost ceiling status is hard_block", decision["reasons"])

    def test_cli_blocks_forced_bad_fixture(self) -> None:
        runner_facts = REPO_ROOT / "tests/fixtures/runner-facts.forced-bad.json"

        result = subprocess.run(
            [sys.executable, "bin/verify_runner_facts.py", str(runner_facts)],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        decision = json.loads(result.stdout)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(decision["decision"], "block")


if __name__ == "__main__":
    unittest.main()
