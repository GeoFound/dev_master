from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.provider_adapter import adapt_provider_fixture, validate_provider_output

REPO_ROOT = Path(__file__).resolve().parent.parent
OK_FIXTURE = REPO_ROOT / "runtime/fixtures/provider-output.ok.json"
DRIFT_FIXTURE = REPO_ROOT / "runtime/fixtures/provider-output.drift.json"


class ProviderAdapterTests(unittest.TestCase):
    def test_ok_fixture_normalizes_to_non_drift_provider_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "provider-output.json"
            raw_store_dir = Path(temp_dir) / "raw"
            result = adapt_provider_fixture(
                fixture_path=OK_FIXTURE,
                output_path=output_path,
                raw_store_dir=raw_store_dir,
            )

            payload = result.provider_output
            self.assertEqual(validate_provider_output(payload), [])
            self.assertFalse(payload["drift_detected"])
            self.assertTrue(payload["authorization_sensitive_use_allowed"])
            self.assertEqual(payload["provider_kind"], "api")
            self.assertEqual(payload["provider_name"], "api_compatible_worker_stub")
            self.assertTrue(payload["provider_raw_output_digest"].startswith("sha256:"))
            self.assertEqual(payload["provider_raw_output_size_bytes"], OK_FIXTURE.stat().st_size)
            self.assertTrue(result.raw_output_path.exists())
            self.assertEqual(
                result.raw_output_path.read_text(encoding="utf-8"),
                OK_FIXTURE.read_text(encoding="utf-8"),
            )

    def test_forced_drift_fixture_sets_drift_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "provider-output.json"
            raw_store_dir = Path(temp_dir) / "raw"
            result = adapt_provider_fixture(
                fixture_path=DRIFT_FIXTURE,
                output_path=output_path,
                raw_store_dir=raw_store_dir,
            )

            payload = result.provider_output
            self.assertEqual(validate_provider_output(payload), [])
            self.assertTrue(payload["drift_detected"])
            self.assertFalse(payload["authorization_sensitive_use_allowed"])
            self.assertIn("missing_or_invalid_result_object", payload["drift_reasons"])
            self.assertIn("provider_name_not_allowed", payload["drift_reasons"])
            self.assertIn("provider_warnings_present", payload["drift_reasons"])

    def test_cli_writes_required_provider_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "provider-output.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_provider_adapter_stub.py",
                    "--provider-fixture",
                    "runtime/fixtures/provider-output.ok.json",
                    "--output",
                    str(output_path),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertFalse(summary["drift_detected"])
            self.assertEqual(summary["validation_errors"], [])
            self.assertFalse(payload["drift_detected"])
            self.assertEqual(payload["cost_facts"]["estimated_usd"], 0.0)
            self.assertEqual(payload["cost_facts"]["actual_usd"], 0.0)


if __name__ == "__main__":
    unittest.main()
