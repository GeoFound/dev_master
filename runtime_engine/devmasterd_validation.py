from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime_engine.devmasterd import DEFAULT_STATE_DIR, run_smoke, write_json
from runtime_engine.task_progression import utc_now_iso

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT_PATH = REPO_ROOT / "runtime/operational-validation/devmasterd-report.json"
DEFAULT_VALIDATION_STATE_ROOT = DEFAULT_STATE_DIR / "validation-runs"


def run_devmasterd_operational_validation(
    *,
    iterations: int,
    output_path: Path,
    state_root: Path = DEFAULT_VALIDATION_STATE_ROOT,
) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    iteration_reports = []
    for index in range(1, iterations + 1):
        iteration_root = state_root / f"iteration-{index}"
        smoke_path = iteration_root / "smoke-state.json"
        smoke = run_smoke(
            token=f"validation-token-{index}",
            state_dir=iteration_root / "state",
            output_path=smoke_path,
        )
        evidence_records = smoke.get("evidence", {}).get("records", [])
        iteration_reports.append(
            {
                "iteration": index,
                "smoke_state_ref": _relative(smoke_path),
                "pass": smoke["pass"],
                "unauthorized_status": smoke["unauthorized_status"],
                "intake_status": smoke["intake"]["status"],
                "authorize_status": smoke["authorize"]["status"],
                "provider_status": smoke["provider_run"]["status"],
                "drift_detected": smoke["provider_run"]["drift_detected"],
                "evidence_record_count": len(evidence_records),
                "external_side_effects": smoke["external_side_effects"],
            }
        )

    pass_count = sum(1 for item in iteration_reports if item["pass"])
    failed_iterations = [
        item["iteration"] for item in iteration_reports if item["pass"] is not True
    ]
    report = {
        "artifact_family": "devmasterd_operational_validation_report",
        "schema_version": "1.0.0",
        "policy_version": "devmasterd-operational-validation-v1",
        "validation_id": "phase7-devmasterd-operational-validation",
        "generated_at": utc_now_iso(),
        "iteration_count": iterations,
        "iterations": iteration_reports,
        "aggregate": {
            "pass": pass_count == iterations,
            "pass_count": pass_count,
            "fail_count": iterations - pass_count,
            "failed_iterations": failed_iterations,
            "unauthorized_401_count": sum(
                1 for item in iteration_reports if item["unauthorized_status"] == 401
            ),
            "provider_completed_count": sum(
                1 for item in iteration_reports if item["provider_status"] == "provider_completed"
            ),
            "external_side_effect_count": sum(
                1 for item in iteration_reports if item["external_side_effects"] is not False
            ),
        },
        "scope": {
            "mode": "localhost-only devmasterd operational validation",
            "real_provider_calls": False,
            "subscription_cli_daemonization": False,
            "external_repo_mutation": False,
            "deploy": False,
            "production_side_effect": False,
        },
        "recommendation": (
            "proceed_to_gate_j_devmasterd_operational_review"
            if pass_count == iterations
            else "hold_and_fix_devmasterd_operational_failures"
        ),
    }
    write_json(output_path, report)
    return report


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
