from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.semantic_benchmark import load_json, run_benchmark

REPO_ROOT = Path(__file__).resolve().parent.parent


class SemanticBenchmarkTests(unittest.TestCase):
    def test_semantic_fixture_benchmark_passes_gate_c_baseline(self) -> None:
        report = run_benchmark(
            fixture_set=load_json(REPO_ROOT / "runtime/fixtures/semantic-verifier-v1.json"),
            base_runner_facts=load_json(
                REPO_ROOT / "runtime/runs/phase1-first-bounded-loop/runner-facts.json"
            ),
            created_at="2026-04-30T00:00:00Z",
        )

        self.assertTrue(report["pass"])
        self.assertGreaterEqual(report["fixture_count"], 20)
        self.assertEqual(report["critical_false_allow_count"], 0)
        self.assertLess(report["total_risk_misclassification_rate"], 0.05)
        self.assertEqual(report["missing_actionable_reason_count"], 0)
        self.assertTrue(
            {"forced_ok", "forced_bad", "risk_boundary"}.issubset(report["fixture_types"])
        )

    def test_committed_benchmark_report_matches_baseline_requirements(self) -> None:
        path = REPO_ROOT / "runtime/reliability/semantic-verifier-benchmark.json"
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(payload["pass"])
        self.assertEqual(payload["fixture_count"], 21)
        self.assertEqual(payload["critical_false_allow_count"], 0)
        self.assertEqual(payload["risk_misclassification_count"], 0)

    def test_green_sample_window_stays_inside_green_boundaries(self) -> None:
        path = REPO_ROOT / "runtime/reliability/green-sample-window.json"
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["result"], "candidate_green_window")
        self.assertEqual(payload["phase2_metrics"]["risk_misclassifications"], 0)
        self.assertEqual(
            payload["phase2_metrics"]["runner_boundary_violations_in_green_samples"],
            0,
        )
        for forbidden in ("dependencies", "infra", "deploy", "merge", "migrations"):
            self.assertIn(forbidden, payload["excluded_categories"])

    def test_cli_writes_benchmark_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "benchmark.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_semantic_verifier_benchmark.py",
                    "--output",
                    str(output_path),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(payload["pass"])


if __name__ == "__main__":
    unittest.main()
