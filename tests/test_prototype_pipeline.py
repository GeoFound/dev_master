from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime_engine.prototype_pipeline import build_prototype, run_pipeline, validate_idea

REPO_ROOT = Path(__file__).resolve().parent.parent


class PrototypePipelineTests(unittest.TestCase):
    def test_validate_idea_rejects_missing_actions(self) -> None:
        with self.assertRaisesRegex(ValueError, "primary_actions"):
            validate_idea(
                {
                    "idea_id": "bad",
                    "title": "Bad",
                    "audience": "Operator",
                    "problem": "No action list.",
                    "promise": "Rejected.",
                }
            )

    def test_build_prototype_writes_visible_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            idea_path = _write_idea(Path(temp_dir))
            result = build_prototype(
                idea_path=idea_path,
                prototype_root=Path(temp_dir) / "prototypes",
            )

            index = result.index_path.read_text(encoding="utf-8")
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))

        self.assertIn("Test Prototype", index)
        self.assertIn("Workflow", index)
        self.assertEqual(manifest["provider_kind"], "local_tool")
        self.assertFalse(manifest["scope"]["real_provider_calls"])

    def test_run_pipeline_validates_localhost_http(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            idea_path = _write_idea(Path(temp_dir))
            report_path = Path(temp_dir) / "report.json"
            report = run_pipeline(
                idea_path=idea_path,
                prototype_root=Path(temp_dir) / "prototypes",
                output_path=report_path,
            )
            written = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertTrue(report["pass"])
        self.assertTrue(written["pass"])
        self.assertEqual(written["localhost_http_status"], 200)
        self.assertEqual(len(written["artifact_refs"]), 3)
        self.assertFalse(written["scope"]["external_repo_mutation"])

    def test_cli_runs_pipeline_and_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            idea_path = _write_idea(Path(temp_dir))
            report_path = Path(temp_dir) / "report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "bin/run_l1_prototype_pipeline.py",
                    "--idea",
                    str(idea_path),
                    "--prototype-root",
                    str(Path(temp_dir) / "prototypes"),
                    "--output",
                    str(report_path),
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            summary = json.loads(result.stdout)
            report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(summary["pass"])
        self.assertTrue(report["pass"])


def _write_idea(directory: Path) -> Path:
    idea_path = directory / "idea.json"
    idea_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "idea_id": "test-prototype",
                "title": "Test Prototype",
                "audience": "Operator",
                "problem": "The operator needs a visible local artifact.",
                "promise": "Show a focused workflow without external services.",
                "primary_actions": [
                    "Open the local page",
                    "Review the workflow",
                    "Check the validation report",
                ],
                "success_signal": "The page loads over localhost.",
            }
        ),
        encoding="utf-8",
    )
    return idea_path


if __name__ == "__main__":
    unittest.main()
