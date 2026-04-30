from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.devmasterd_validation import run_devmasterd_operational_validation

REPO_ROOT = Path(__file__).resolve().parent.parent


class DevmasterdValidationTests(unittest.TestCase):
    def test_operational_validation_runs_repeated_smoke_iterations(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "devmasterd-report.json"
            report = run_devmasterd_operational_validation(
                iterations=2,
                output_path=output_path,
                state_root=Path(temp_dir) / "validation-runs",
            )

            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertTrue(report["aggregate"]["pass"])
        self.assertTrue(written["aggregate"]["pass"])
        self.assertEqual(report["iteration_count"], 2)
        self.assertEqual(report["aggregate"]["unauthorized_401_count"], 2)
        self.assertEqual(report["aggregate"]["provider_completed_count"], 2)
        self.assertEqual(report["aggregate"]["external_side_effect_count"], 0)

    def test_validation_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "devmasterd-report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_devmasterd_validation.py",
                    "--iterations",
                    "1",
                    "--output",
                    str(output_path),
                    "--state-root",
                    str(Path(temp_dir) / "validation-runs"),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            report = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertTrue(summary["pass"])
        self.assertTrue(report["aggregate"]["pass"])


if __name__ == "__main__":
    unittest.main()
