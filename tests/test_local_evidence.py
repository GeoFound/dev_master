from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class LocalEvidenceFallbackTests(unittest.TestCase):
    def test_cli_appends_without_rewriting_existing_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            index_path = Path(directory) / "index.jsonl"
            first = self._append(index_path, "first")
            first_line = index_path.read_text(encoding="utf-8").splitlines()[0]

            second = self._append(index_path, "second")
            lines = index_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], first_line)
        self.assertNotEqual(first["evidence_id"], second["evidence_id"])
        self.assertEqual(first["writeback_status"], "fallback_local")
        self.assertIs(first["local_fallback"], True)
        self.assertIs(first["canonical_truth"], False)

    def test_cli_rejects_bad_artifact_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            index_path = Path(directory) / "index.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/append_local_evidence.py",
                    "--index-path",
                    str(index_path),
                    "--trace-id",
                    "tr_bad",
                    "--run-id",
                    "run_bad",
                    "--stage",
                    "evidence",
                    "--summary",
                    "bad artifact ref",
                    "--artifact-ref",
                    "runtime_engine/verifier.py=not-a-sha",
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)

    def test_example_record_is_valid_json(self) -> None:
        path = REPO_ROOT / "runtime/examples/local-evidence-record.example.json"
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["artifact_family"], "local_evidence_record")
        self.assertEqual(payload["schema_version"], "1.0.0")
        self.assertIs(payload["canonical_truth"], False)

    def _append(self, index_path: Path, suffix: str) -> dict:
        result = subprocess.run(
            [
                sys.executable,
                "bin/append_local_evidence.py",
                "--index-path",
                str(index_path),
                "--trace-id",
                f"tr_{suffix}",
                "--run-id",
                f"run_{suffix}",
                "--stage",
                "verifier",
                "--summary",
                f"append {suffix}",
                "--artifact-path",
                "runtime_engine/verifier.py",
                "--verifier-decision-ref",
                "runtime/examples/verifier-decision.example.json",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
