from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.devmasterd import serve_in_thread
from runtime_engine.devmasterd_client import (
    DevmasterClient,
    load_task_proposal,
    run_cli_smoke_with_test_daemon,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class DevmasterClientTests(unittest.TestCase):
    def test_client_rejects_non_loopback_base_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "loopback"):
            DevmasterClient(base_url="http://example.com:8787", token="unit-test-token")

    def test_client_status_evidence_and_intake_use_daemon_api(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            serve_in_thread(token="unit-test-token", state_dir=Path(temp_dir)) as base_url,
        ):
            client = DevmasterClient(base_url=base_url, token="unit-test-token")
            intake = client.intake(
                {
                    "goal": "Submit through devmasterctl client.",
                    "slices": [
                        {
                            "slice_id": "slice_client_test",
                            "expected_cost_usd": 0.0,
                            "provider_kind": "local_tool",
                        }
                    ],
                }
            )
            status = client.status()
            evidence = client.evidence()

        self.assertEqual(intake["status"], "queued")
        self.assertEqual(status["items"][0]["item_id"], intake["item_id"])
        self.assertEqual(evidence["records"], [])

    def test_load_task_proposal_accepts_wrapped_contract_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            proposal_path = Path(temp_dir) / "proposal.json"
            proposal_path.write_text(
                json.dumps(
                    {
                        "task_proposal": {
                            "goal": "Wrapped proposal.",
                            "slices": [{"slice_id": "slice_wrapped"}],
                        }
                    }
                ),
                encoding="utf-8",
            )

            proposal = load_task_proposal(proposal_path)

        self.assertEqual(proposal["goal"], "Wrapped proposal.")

    def test_cli_smoke_with_test_daemon_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "devmasterctl-smoke.json"
            report = run_cli_smoke_with_test_daemon(
                token="unit-test-token",
                output_path=output_path,
                state_dir=Path(temp_dir) / "state",
            )
            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertTrue(report["pass"])
        self.assertTrue(written["pass"])
        self.assertEqual(written["unauthorized_status"], 401)
        self.assertEqual(written["provider_status"], "provider_completed")
        self.assertFalse(written["scope"]["external_repo_mutation"])

    def test_devmasterctl_smoke_command_uses_test_daemon(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "devmasterctl-smoke.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/devmasterctl.py",
                    "--test-token",
                    "unit-test-token",
                    "smoke",
                    "--start-test-daemon",
                    "--state-dir",
                    str(Path(temp_dir) / "state"),
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
            report = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertTrue(summary["pass"])
        self.assertTrue(report["pass"])


if __name__ == "__main__":
    unittest.main()
