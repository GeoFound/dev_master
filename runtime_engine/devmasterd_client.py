from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from ipaddress import ip_address
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from runtime_engine.devmasterd import DEFAULT_FIXTURE_PATH, serve_in_thread, write_json

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "http://127.0.0.1:8787"
DEFAULT_CLI_SMOKE_PATH = REPO_ROOT / "runtime/cli-validation/devmasterctl-smoke.json"
DEFAULT_CLI_STATE_DIR = REPO_ROOT / "runtime/cli-validation/devmasterd-state"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class DevmasterClient:
    base_url: str
    token: str
    timeout_seconds: float = 3.0

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("token is required")
        _validate_loopback_base_url(self.base_url)

    def status(self) -> dict[str, Any]:
        return self._request_json("GET", "/v1/state")

    def evidence(self) -> dict[str, Any]:
        return self._request_json("GET", "/v1/evidence")

    def intake(self, task_proposal: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("POST", "/v1/intake", {"task_proposal": task_proposal})

    def authorize(self, item_id: str) -> dict[str, Any]:
        return self._request_json("POST", "/v1/authorize", {"item_id": item_id})

    def run_provider(
        self,
        item_id: str,
        provider_fixture: Path = DEFAULT_FIXTURE_PATH,
    ) -> dict[str, Any]:
        return self._request_json(
            "POST",
            "/v1/run-provider",
            {
                "item_id": item_id,
                "provider_fixture": _relative(provider_fixture),
            },
        )

    def unauthorized_status(self) -> int:
        request = Request(f"{self.base_url}/v1/state", method="GET")
        return _request_status(request, self.timeout_seconds)

    def _request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        data = None
        headers = {"Authorization": f"Bearer {self.token}"}
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        with urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310 - loopback only.
            return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))


def load_task_proposal(path: Path) -> dict[str, Any]:
    payload = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    task_proposal = payload.get("task_proposal", payload)
    if not isinstance(task_proposal, dict):
        raise ValueError("task proposal must be a JSON object")
    return task_proposal


def default_smoke_proposal() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "proposal_id": "prop_devmasterctl_smoke",
        "trace_id": "tr_devmasterctl_smoke",
        "proposer": "human",
        "goal": "Run the devmasterctl smoke path.",
        "slices": [
            {
                "slice_id": "slice_devmasterctl_smoke",
                "expected_cost_usd": 0.0,
                "provider_kind": "local_tool",
                "risk_label_estimate": "green",
            }
        ],
    }


def run_cli_smoke(
    *,
    base_url: str,
    token: str,
    output_path: Path,
    provider_fixture: Path = DEFAULT_FIXTURE_PATH,
    task_proposal_path: Path | None = None,
) -> dict[str, Any]:
    client = DevmasterClient(base_url=base_url, token=token)
    task_proposal = (
        load_task_proposal(task_proposal_path) if task_proposal_path else default_smoke_proposal()
    )

    unauthorized_status = client.unauthorized_status()
    intake = client.intake(task_proposal)
    authorize = client.authorize(_required_str(intake, "item_id"))
    provider_run = client.run_provider(_required_str(intake, "item_id"), provider_fixture)
    status = client.status()
    evidence = client.evidence()

    report = {
        "artifact_family": "devmasterctl_smoke_result",
        "schema_version": "1.0.0",
        "policy_version": "devmasterctl-local-client-v1",
        "created_at": utc_now_iso(),
        "base_url": base_url,
        "unauthorized_status": unauthorized_status,
        "intake_status": intake.get("status"),
        "authorize_status": authorize.get("status"),
        "provider_status": provider_run.get("status"),
        "drift_detected": provider_run.get("drift_detected"),
        "evidence_record_count": len(evidence.get("records", [])),
        "state_item_count": len(status.get("items", [])),
        "external_side_effects": False,
        "scope": {
            "client_only": True,
            "real_provider_calls": False,
            "subscription_cli_daemonization": False,
            "live_auto_router_calls": False,
            "external_repo_mutation": False,
            "deploy": False,
            "pr_creation": False,
            "production_side_effect": False,
        },
        "pass": (
            unauthorized_status == HTTPStatus.UNAUTHORIZED.value
            and intake.get("status") == "queued"
            and authorize.get("status") == "authorized"
            and provider_run.get("status") == "provider_completed"
            and provider_run.get("drift_detected") is False
            and len(evidence.get("records", [])) >= 1
        ),
    }
    write_json(output_path, report)
    return report


def run_cli_smoke_with_test_daemon(
    *,
    token: str,
    output_path: Path,
    state_dir: Path = DEFAULT_CLI_STATE_DIR,
    provider_fixture: Path = DEFAULT_FIXTURE_PATH,
    task_proposal_path: Path | None = None,
) -> dict[str, Any]:
    with serve_in_thread(token=token, state_dir=state_dir) as base_url:
        return run_cli_smoke(
            base_url=base_url,
            token=token,
            output_path=output_path,
            provider_fixture=provider_fixture,
            task_proposal_path=task_proposal_path,
        )


def run_cli_smoke_with_ephemeral_daemon(*, token: str, output_path: Path) -> dict[str, Any]:
    with TemporaryDirectory() as temp_dir:
        return run_cli_smoke_with_test_daemon(
            token=token,
            output_path=output_path,
            state_dir=Path(temp_dir) / "state",
        )


def _validate_loopback_base_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http":
        raise ValueError("devmasterd base URL must use http")
    if parsed.hostname is None:
        raise ValueError("devmasterd base URL must include a host")
    if parsed.hostname == "localhost":
        return
    try:
        if ip_address(parsed.hostname).is_loopback:
            return
    except ValueError as exc:
        raise ValueError("devmasterd base URL must target localhost or loopback") from exc
    raise ValueError("devmasterd base URL must target localhost or loopback")


def _required_str(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} is required")
    return value


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _request_status(request: Request, timeout_seconds: float) -> int:
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - loopback only.
            return int(response.status)
    except HTTPError as exc:
        status = int(exc.code)
        exc.close()
        return status
