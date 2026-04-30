from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

from runtime_engine.runner_contract import COST_POLICY_VERSION, cost_facts
from runtime_engine.task_progression import utc_now_iso

REPO_ROOT = Path(__file__).resolve().parent.parent

PROVIDER_ARTIFACT_FAMILY = "provider_output"
PROVIDER_SCHEMA_VERSION = "1.0.0"
PROVIDER_ADAPTER_VERSION = "provider-adapter-kernel-v0.1"
PROVIDER_PARSE_SCHEMA_VERSION = "1.0.0"
DEFAULT_PROVIDER_EVIDENCE_DIR = REPO_ROOT / "runtime/provider-evidence"
DEFAULT_RAW_STORE_DIR = DEFAULT_PROVIDER_EVIDENCE_DIR / "raw"

ALLOWED_PROVIDER_KINDS = {"api", "local_tool"}
ALLOWED_PROVIDER_NAMES = {
    "api_compatible_worker_stub",
    "openai_api_stub",
    "anthropic_api_stub",
    "auto_router_stub",
}
REQUIRED_PROVIDER_FIELDS = {
    "provider_adapter_version",
    "provider_kind",
    "provider_name",
    "provider_version",
    "provider_raw_output_digest",
    "provider_raw_output_ref",
    "provider_raw_output_size_bytes",
    "provider_raw_output_storage",
    "parsed_output",
    "parse_schema_version",
    "drift_detected",
    "drift_reasons",
}


@dataclass(frozen=True)
class ProviderAdapterResult:
    provider_output: dict[str, Any]
    raw_output_path: Path


def adapt_provider_fixture(
    *,
    fixture_path: Path,
    output_path: Path,
    provider_kind: str = "api",
    project_id: str = "dev_master",
    trace_id: str = "tr_provider_adapter_stub",
    run_id: str = "run_provider_adapter_stub",
    raw_store_dir: Path = DEFAULT_RAW_STORE_DIR,
) -> ProviderAdapterResult:
    raw_bytes = fixture_path.read_bytes()
    raw_digest = "sha256:" + sha256(raw_bytes).hexdigest()
    raw_output_path = _store_raw_output(raw_bytes, raw_digest, raw_store_dir)
    raw_output_size = len(raw_bytes)
    drift_reasons: list[str] = []
    raw_payload: dict[str, Any] = {}

    try:
        raw_payload = cast(dict[str, Any], json.loads(raw_bytes.decode("utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        drift_reasons.append(f"raw_output_unparseable:{type(exc).__name__}")

    provider_name = _string_or_unknown(raw_payload.get("provider"))
    provider_version = raw_payload.get("provider_version")
    parsed_output = _parsed_output(raw_payload, drift_reasons)
    _validate_provider_identity(provider_kind, provider_name, drift_reasons)
    _validate_provider_warning_shape(raw_payload, drift_reasons)

    output = {
        "artifact_family": PROVIDER_ARTIFACT_FAMILY,
        "schema_version": PROVIDER_SCHEMA_VERSION,
        "provider_adapter_version": PROVIDER_ADAPTER_VERSION,
        "provider_kind": provider_kind,
        "provider_name": provider_name,
        "provider_version": provider_version if isinstance(provider_version, str) else None,
        "provider_raw_output_digest": raw_digest,
        "provider_raw_output_ref": _relative(raw_output_path),
        "provider_raw_output_size_bytes": raw_output_size,
        "provider_raw_output_storage": "artifact_store",
        "parsed_output": parsed_output,
        "parse_schema_version": PROVIDER_PARSE_SCHEMA_VERSION,
        "drift_detected": bool(drift_reasons),
        "drift_reasons": drift_reasons,
        "cost_facts": cost_facts(
            project_id=project_id,
            trace_id=trace_id,
            run_id=run_id,
            estimated_usd=0.0,
            actual_usd=0.0,
            per_project_daily_spend_usd=0.0,
            global_daily_spend_usd=0.0,
            ceiling_status="within_limit",
        ),
        "authorization_sensitive_use_allowed": not drift_reasons,
        "source_fixture_ref": _relative(fixture_path),
        "captured_at": utc_now_iso(),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return ProviderAdapterResult(provider_output=output, raw_output_path=raw_output_path)


def validate_provider_output(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_PROVIDER_FIELDS - set(payload))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if payload.get("artifact_family") != PROVIDER_ARTIFACT_FAMILY:
        errors.append(f"artifact_family must be {PROVIDER_ARTIFACT_FAMILY}")
    if payload.get("schema_version") != PROVIDER_SCHEMA_VERSION:
        errors.append(f"schema_version must be {PROVIDER_SCHEMA_VERSION}")
    if payload.get("provider_adapter_version") != PROVIDER_ADAPTER_VERSION:
        errors.append(f"provider_adapter_version must be {PROVIDER_ADAPTER_VERSION}")
    if payload.get("provider_kind") not in ALLOWED_PROVIDER_KINDS:
        errors.append(f"provider_kind must be one of {sorted(ALLOWED_PROVIDER_KINDS)}")
    if (
        payload.get("provider_name") not in ALLOWED_PROVIDER_NAMES
        and payload.get("drift_detected") is not True
    ):
        errors.append("provider_name is not approved for the current local adapter slice")
    if not _is_sha256_ref(payload.get("provider_raw_output_digest")):
        errors.append("provider_raw_output_digest must start with sha256:")
    if not isinstance(payload.get("parsed_output"), dict):
        errors.append("parsed_output must be an object")
    if payload.get("parse_schema_version") != PROVIDER_PARSE_SCHEMA_VERSION:
        errors.append(f"parse_schema_version must be {PROVIDER_PARSE_SCHEMA_VERSION}")
    if not isinstance(payload.get("drift_detected"), bool):
        errors.append("drift_detected must be a boolean")
    if not isinstance(payload.get("drift_reasons"), list):
        errors.append("drift_reasons must be a list")
    if payload.get("drift_detected") is False and payload.get("drift_reasons"):
        errors.append("drift_reasons must be empty when drift_detected is false")
    if payload.get("drift_detected") is True and not payload.get("drift_reasons"):
        errors.append("drift_reasons must be non-empty when drift_detected is true")
    _validate_cost_facts(payload.get("cost_facts"), errors)

    return errors


def _store_raw_output(raw_bytes: bytes, digest: str, raw_store_dir: Path) -> Path:
    raw_store_dir.mkdir(parents=True, exist_ok=True)
    digest_suffix = digest.removeprefix("sha256:")
    raw_output_path = raw_store_dir / f"{digest_suffix}.json"
    raw_output_path.write_bytes(raw_bytes)
    return raw_output_path


def _parsed_output(raw_payload: dict[str, Any], drift_reasons: list[str]) -> dict[str, Any]:
    result = raw_payload.get("result")
    if not isinstance(result, dict):
        drift_reasons.append("missing_or_invalid_result_object")
        return {}
    return cast(dict[str, Any], result)


def _validate_provider_identity(
    provider_kind: str, provider_name: str, drift_reasons: list[str]
) -> None:
    if provider_kind not in ALLOWED_PROVIDER_KINDS:
        drift_reasons.append("provider_kind_not_allowed")
    if provider_name not in ALLOWED_PROVIDER_NAMES:
        drift_reasons.append("provider_name_not_allowed")


def _validate_provider_warning_shape(raw_payload: dict[str, Any], drift_reasons: list[str]) -> None:
    warnings = raw_payload.get("warnings", [])
    if warnings is None:
        return
    if not isinstance(warnings, list):
        drift_reasons.append("warnings_not_list")
        return
    if warnings:
        drift_reasons.append("provider_warnings_present")


def _validate_cost_facts(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("cost_facts must be an object")
        return
    if value.get("policy_version") != COST_POLICY_VERSION:
        errors.append(f"cost_facts.policy_version must be {COST_POLICY_VERSION}")
    if value.get("ceiling_status") != "within_limit":
        errors.append("cost_facts.ceiling_status must be within_limit")
    if value.get("estimated_usd") != 0.0:
        errors.append("cost_facts.estimated_usd must be 0.0 for this local slice")
    if value.get("actual_usd") != 0.0:
        errors.append("cost_facts.actual_usd must be 0.0 for this local slice")


def _string_or_unknown(value: Any) -> str:
    if isinstance(value, str) and value:
        return value
    return "unknown"


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _is_sha256_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) > 7
