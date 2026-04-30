from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.operational_validation import build_operational_validation_report

REPO_ROOT = Path(__file__).resolve().parent.parent


class OperationalValidationTests(unittest.TestCase):
    def test_report_collects_live_local_operational_signal(self) -> None:
        report = build_operational_validation_report(iterations=2)

        self.assertEqual(report["artifact_family"], "operational_validation_report")
        self.assertTrue(report["aggregate"]["pass"])
        self.assertEqual(report["iteration_count"], 2)
        self.assertEqual(report["aggregate"]["provider_drift_detected_count"], 0)
        self.assertEqual(report["recommendation"], "proceed_to_gate_e_operational_review")

        for iteration in report["iterations"]:
            self.assertTrue(iteration["pass"])
            self.assertTrue(iteration["live_http"]["ok"])
            self.assertEqual(iteration["live_http"]["status_code"], 200)
            self.assertTrue(iteration["prototype"]["visible_output"])
            self.assertTrue(iteration["provider"]["raw_digest_matches"])
            self.assertTrue(iteration["evidence"]["ok"])
            self.assertTrue(iteration["reliability"]["ok"])

    def test_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "operational-report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_operational_validation.py",
                    "--iterations",
                    "1",
                    "--output",
                    str(output_path),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            cli_summary = json.loads(result.stdout)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(cli_summary["pass"])
            self.assertTrue(report["aggregate"]["pass"])


if __name__ == "__main__":
    unittest.main()
