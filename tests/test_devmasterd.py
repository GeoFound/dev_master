from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from runtime_engine.devmasterd import create_server, run_smoke, serve_in_thread

REPO_ROOT = Path(__file__).resolve().parent.parent


def json_request(
    base_url: str, path: str, token: str, payload: dict[str, object]
) -> dict[str, object]:
    request = Request(
        f"{base_url}{path}",
        data=json.dumps(payload, ensure_ascii=True).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


def json_get(base_url: str, path: str, token: str) -> dict[str, object]:
    request = Request(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urlopen(request, timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


class DevmasterdTests(unittest.TestCase):
    def test_server_rejects_non_loopback_host(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            self.assertRaisesRegex(ValueError, "loopback"),
        ):
            create_server(
                host="0.0.0.0",
                port=0,
                token="unit-test-token",
                state_dir=Path(temp_dir),
            )

    def test_unauthorized_request_is_rejected(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            serve_in_thread(token="unit-test-token", state_dir=Path(temp_dir)) as base_url,
        ):
            request = Request(f"{base_url}/v1/state", method="GET")
            with self.assertRaises(HTTPError) as context:
                urlopen(request, timeout=3)
            self.assertEqual(context.exception.code, 401)
            context.exception.close()

    def test_intake_authorize_run_provider_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir)
            with serve_in_thread(token="unit-test-token", state_dir=state_dir) as base_url:
                intake = json_request(
                    base_url,
                    "/v1/intake",
                    "unit-test-token",
                    {
                        "task_proposal": {
                            "goal": "Run provider adapter through devmasterd.",
                            "slices": [
                                {
                                    "slice_id": "slice_test",
                                    "expected_cost_usd": 0.0,
                                    "provider_kind": "api",
                                }
                            ],
                        }
                    },
                )
                authorize = json_request(
                    base_url,
                    "/v1/authorize",
                    "unit-test-token",
                    {"item_id": intake["item_id"]},
                )
                provider_run = json_request(
                    base_url,
                    "/v1/run-provider",
                    "unit-test-token",
                    {
                        "item_id": intake["item_id"],
                        "provider_fixture": "runtime/fixtures/provider-output.ok.json",
                    },
                )
                state = json_get(base_url, "/v1/state", "unit-test-token")
                evidence = json_get(base_url, "/v1/evidence", "unit-test-token")

            self.assertEqual(intake["status"], "queued")
            self.assertEqual(authorize["status"], "authorized")
            self.assertEqual(provider_run["status"], "provider_completed")
            self.assertFalse(provider_run["drift_detected"])
            self.assertEqual(state["external_side_effects"], False)
            self.assertEqual(state["provider_mode"], "stub")
            self.assertEqual(len(evidence["records"]), 1)
            self.assertTrue((state_dir / "provider-evidence").exists())

    def test_smoke_runner_writes_state_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            smoke_path = Path(temp_dir) / "smoke-state.json"
            result = run_smoke(
                token="unit-test-token",
                state_dir=Path(temp_dir) / "state",
                output_path=smoke_path,
            )

            written = json.loads(smoke_path.read_text(encoding="utf-8"))

        self.assertTrue(result["pass"])
        self.assertTrue(written["pass"])
        self.assertEqual(written["unauthorized_status"], 401)
        self.assertEqual(written["provider_run"]["status"], "provider_completed")

    def test_cli_smoke_uses_token_env(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            smoke_path = Path(temp_dir) / "smoke-state.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_devmasterd.py",
                    "--smoke",
                    "--test-token",
                    "unit-test-token",
                    "--state-dir",
                    str(Path(temp_dir) / "state"),
                    "--smoke-output",
                    str(smoke_path),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertTrue(summary["pass"])
            self.assertTrue(smoke_path.exists())


if __name__ == "__main__":
    unittest.main()
