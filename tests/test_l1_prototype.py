from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class L1PrototypeTests(unittest.TestCase):
    def test_check_command_reports_visible_local_output(self) -> None:
        result = subprocess.run(
            [sys.executable, "bin/run_l1_prototype.py", "--check"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(payload["visible_output"])
        self.assertEqual(payload["provider_path"], "api")
        self.assertFalse(payload["provider_drift_detected"])

    def test_provider_output_preserves_raw_and_parsed_contract(self) -> None:
        path = REPO_ROOT / "runtime/prototypes/l1-local-prototype/provider-output.json"
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["provider_kind"], "api")
        self.assertTrue(payload["provider_raw_output_digest"].startswith("sha256:"))
        self.assertEqual(payload["parse_schema_version"], "1.0.0")
        self.assertFalse(payload["drift_detected"])

    def test_prototype_html_is_not_static_mock_report(self) -> None:
        path = REPO_ROOT / "runtime/prototypes/l1-local-prototype/index.html"
        html = path.read_text(encoding="utf-8")

        self.assertIn("<main", html)
        self.assertIn("dev_master Factory Console", html)
        self.assertIn("Run Timeline", html)


if __name__ == "__main__":
    unittest.main()
