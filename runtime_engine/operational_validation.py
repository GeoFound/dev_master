from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

from runtime_engine.task_progression import utc_now_iso

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTOTYPE_ROOT = REPO_ROOT / "runtime/prototypes/l1-local-prototype"
PROVIDER_OUTPUT_PATH = PROTOTYPE_ROOT / "provider-output.json"
PROVIDER_RAW_OUTPUT_PATH = PROTOTYPE_ROOT / "provider-raw-output.json"
PROGRAM_STATE_PATH = REPO_ROOT / "runtime/program-state.json"
CURRENT_TASK_PATH = REPO_ROOT / "runtime/current-task.json"
EVIDENCE_INDEX_PATH = REPO_ROOT / "runtime/evidence/index.jsonl"
GREEN_WINDOW_PATH = REPO_ROOT / "runtime/reliability/green-sample-window.json"
SEMANTIC_BENCHMARK_PATH = REPO_ROOT / "runtime/reliability/semantic-verifier-benchmark.json"

REPORT_ARTIFACT_FAMILY = "operational_validation_report"
REPORT_SCHEMA_VERSION = "1.0.0"
REPORT_POLICY_VERSION = "phase4-operational-validation-v1"


@dataclass(frozen=True)
class LiveHttpResult:
    ok: bool
    url: str
    status_code: int | None
    visible_output: bool
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "url": self.url,
            "status_code": self.status_code,
            "visible_output": self.visible_output,
            "error": self.error,
        }


class QuietPrototypeHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def hash_file(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


@contextmanager
def serve_local_prototype(root: Path = PROTOTYPE_ROOT) -> Iterator[str]:
    handler = partial(QuietPrototypeHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def check_live_http(url: str) -> LiveHttpResult:
    try:
        with urlopen(url, timeout=3) as response:  # noqa: S310 - local ephemeral URL only.
            body = response.read().decode("utf-8")
            status_code = response.status
    except Exception as exc:  # pragma: no cover - error path is data collection.
        return LiveHttpResult(
            ok=False,
            url=url,
            status_code=None,
            visible_output=False,
            error=type(exc).__name__ + ": " + str(exc),
        )

    visible_output = "<main" in body and "dev_master Factory Console" in body
    return LiveHttpResult(
        ok=status_code == 200 and visible_output,
        url=url,
        status_code=status_code,
        visible_output=visible_output,
    )


def prototype_contract() -> dict[str, Any]:
    index_path = PROTOTYPE_ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")
    provider_output = load_json(PROVIDER_OUTPUT_PATH)
    return {
        "prototype_root": relative(PROTOTYPE_ROOT),
        "entrypoint": relative(index_path),
        "visible_output": "<main" in html and "dev_master Factory Console" in html,
        "provider_kind": provider_output.get("provider_kind"),
        "provider_drift_detected": provider_output.get("drift_detected"),
        "run_command": "uv run python bin/run_l1_prototype.py --port 8765",
    }


def provider_contract() -> dict[str, Any]:
    provider_output = load_json(PROVIDER_OUTPUT_PATH)
    raw_ref = provider_output.get("provider_raw_output_ref")
    raw_path = REPO_ROOT / str(raw_ref)
    expected_digest = provider_output.get("provider_raw_output_digest")
    actual_digest = hash_file(raw_path)
    return {
        "provider_output_ref": relative(PROVIDER_OUTPUT_PATH),
        "provider_raw_output_ref": raw_ref,
        "provider_adapter_version": provider_output.get("provider_adapter_version"),
        "provider_kind": provider_output.get("provider_kind"),
        "parse_schema_version": provider_output.get("parse_schema_version"),
        "drift_detected": provider_output.get("drift_detected"),
        "raw_output_size_bytes": provider_output.get("provider_raw_output_size_bytes"),
        "raw_digest_matches": expected_digest == actual_digest,
        "expected_raw_digest": expected_digest,
        "actual_raw_digest": actual_digest,
        "ok": (
            provider_output.get("provider_kind") == "api"
            and provider_output.get("parse_schema_version") == "1.0.0"
            and provider_output.get("drift_detected") is False
            and expected_digest == actual_digest
        ),
    }


def gate_state_contract() -> dict[str, Any]:
    program_state = load_json(PROGRAM_STATE_PATH)
    current_task = load_json(CURRENT_TASK_PATH)
    gates = program_state.get("gates", {})
    required_gates = ("A", "B", "C", "D")
    return {
        "current_phase": program_state.get("current_phase"),
        "gates": gates,
        "required_gates_passed": all(gates.get(name) == "pass" for name in required_gates),
        "active_task_id": program_state.get("active_task_id"),
        "current_task_status": current_task.get("status"),
        "current_task_no_next_task": current_task.get("status") == "no-next-task",
    }


def evidence_contract() -> dict[str, Any]:
    lines = EVIDENCE_INDEX_PATH.read_text(encoding="utf-8").splitlines()
    malformed = 0
    records: list[dict[str, Any]] = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            malformed += 1

    evidence_ids = [record.get("evidence_id") for record in records]
    duplicate_ids = sorted(
        str(evidence_id) for evidence_id in set(evidence_ids) if evidence_ids.count(evidence_id) > 1
    )
    missing_artifacts = []
    for record in records:
        for artifact_ref in record.get("artifact_refs", []):
            artifact_path = artifact_ref.get("path")
            if artifact_path and not (REPO_ROOT / artifact_path).exists():
                missing_artifacts.append(artifact_path)

    return {
        "evidence_index_ref": relative(EVIDENCE_INDEX_PATH),
        "record_count": len(records),
        "malformed_record_count": malformed,
        "duplicate_evidence_ids": duplicate_ids,
        "missing_artifact_refs": sorted(set(missing_artifacts)),
        "local_fallback_record_count": sum(
            1 for record in records if record.get("local_fallback") is True
        ),
        "ok": malformed == 0 and not duplicate_ids and not missing_artifacts and len(records) > 0,
    }


def reliability_contract() -> dict[str, Any]:
    green_window = load_json(GREEN_WINDOW_PATH)
    benchmark = load_json(SEMANTIC_BENCHMARK_PATH)
    metrics = green_window.get("phase2_metrics", {})
    return {
        "green_window_ref": relative(GREEN_WINDOW_PATH),
        "semantic_benchmark_ref": relative(SEMANTIC_BENCHMARK_PATH),
        "full_loop_sample_count": len(green_window.get("full_loop_samples", [])),
        "risk_misclassifications": metrics.get("risk_misclassifications"),
        "local_evidence_integrity_failures": metrics.get("local_evidence_integrity_failures"),
        "optional_service_writeback_failures": metrics.get("optional_service_writeback_failures"),
        "semantic_fixture_count": benchmark.get("fixture_count"),
        "semantic_critical_false_allow_count": benchmark.get("critical_false_allow_count"),
        "semantic_risk_misclassification_rate": benchmark.get("total_risk_misclassification_rate"),
        "ok": (
            len(green_window.get("full_loop_samples", [])) >= 2
            and metrics.get("risk_misclassifications") == 0
            and metrics.get("local_evidence_integrity_failures") == 0
            and benchmark.get("pass") is True
            and benchmark.get("critical_false_allow_count") == 0
        ),
    }


def build_iteration(iteration: int, live_url: str) -> dict[str, Any]:
    prototype = prototype_contract()
    provider = provider_contract()
    gates = gate_state_contract()
    evidence = evidence_contract()
    reliability = reliability_contract()
    live_http = check_live_http(live_url)
    checks = {
        "prototype_contract": prototype["visible_output"] is True,
        "live_http": live_http.ok,
        "provider_contract": provider["ok"] is True,
        "provider_no_drift": provider["drift_detected"] is False,
        "gate_state": gates["required_gates_passed"] is True,
        "evidence_integrity": evidence["ok"] is True,
        "green_reliability": reliability["ok"] is True,
    }
    return {
        "iteration": iteration,
        "observed_at": utc_now_iso(),
        "checks": checks,
        "pass": all(checks.values()),
        "live_http": live_http.as_dict(),
        "prototype": prototype,
        "provider": provider,
        "gate_state": gates,
        "evidence": evidence,
        "reliability": reliability,
    }


def build_operational_validation_report(iterations: int = 3) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    with serve_local_prototype() as live_url:
        iteration_reports = [
            build_iteration(iteration=iteration, live_url=live_url)
            for iteration in range(1, iterations + 1)
        ]

    pass_count = sum(1 for item in iteration_reports if item["pass"])
    provider_drift_detected_count = sum(
        1 for item in iteration_reports if item["provider"]["drift_detected"] is True
    )
    failed_checks = sorted(
        {
            check_name
            for item in iteration_reports
            for check_name, passed in item["checks"].items()
            if not passed
        }
    )
    report_pass = pass_count == iterations and provider_drift_detected_count == 0

    return {
        "artifact_family": REPORT_ARTIFACT_FAMILY,
        "schema_version": REPORT_SCHEMA_VERSION,
        "policy_version": REPORT_POLICY_VERSION,
        "validation_id": "phase4-current-kernel-operational-validation",
        "generated_at": utc_now_iso(),
        "scope": {
            "mode": "repo-local operational validation",
            "phase": "Phase 4",
            "external_repo_mutation": False,
            "paid_provider_call": False,
            "production_side_effect": False,
            "live_surface": "local ephemeral HTTP prototype server",
        },
        "iteration_count": iterations,
        "iterations": iteration_reports,
        "aggregate": {
            "pass": report_pass,
            "pass_count": pass_count,
            "fail_count": iterations - pass_count,
            "provider_drift_detected_count": provider_drift_detected_count,
            "failed_checks": failed_checks,
        },
        "recommendation": (
            "proceed_to_gate_e_operational_review"
            if report_pass
            else "hold_and_fix_operational_validation_failures"
        ),
    }


def write_operational_validation_report(output_path: Path, iterations: int = 3) -> dict[str, Any]:
    report = build_operational_validation_report(iterations=iterations)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return report
