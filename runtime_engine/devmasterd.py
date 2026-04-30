from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

from runtime_engine.provider_adapter import adapt_provider_fixture

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_ARTIFACT_FAMILY = "devmasterd_state"
STATE_SCHEMA_VERSION = "1.0.0"
STATE_POLICY_VERSION = "devmasterd-local-kernel-v1"
DEFAULT_STATE_DIR = REPO_ROOT / "runtime/devmasterd"
DEFAULT_SMOKE_STATE_PATH = DEFAULT_STATE_DIR / "smoke-state.json"
DEFAULT_FIXTURE_PATH = REPO_ROOT / "runtime/fixtures/provider-output.ok.json"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True, ensure_ascii=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        records.append(cast(dict[str, Any], json.loads(line)))
    return records


def hash_file(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def initial_state() -> dict[str, Any]:
    return {
        "artifact_family": STATE_ARTIFACT_FAMILY,
        "schema_version": STATE_SCHEMA_VERSION,
        "policy_version": STATE_POLICY_VERSION,
        "updated_at": utc_now_iso(),
        "items": [],
        "decisions": [],
        "provider_runs": [],
        "external_side_effects": False,
        "provider_mode": "stub",
    }


@dataclass(frozen=True)
class IntakeResult:
    item_id: str
    status: str


@dataclass(frozen=True)
class AuthorizeResult:
    decision_id: str
    item_id: str
    status: str


@dataclass(frozen=True)
class ProviderRunResult:
    run_id: str
    item_id: str
    provider_output_ref: str
    evidence_ref: str
    drift_detected: bool
    status: str


class DevmasterStateStore:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.state_path = state_dir / "state.json"
        self.evidence_index_path = state_dir / "evidence-index.jsonl"
        self.provider_evidence_dir = state_dir / "provider-evidence"
        self._lock = threading.Lock()

    def load(self) -> dict[str, Any]:
        if not self.state_path.exists():
            state = initial_state()
            self.save(state)
            return state
        return load_json(self.state_path)

    def save(self, state: dict[str, Any]) -> None:
        state["updated_at"] = utc_now_iso()
        write_json(self.state_path, state)

    def evidence_records(self) -> list[dict[str, Any]]:
        return read_jsonl(self.evidence_index_path)

    def intake(self, proposal: dict[str, Any]) -> IntakeResult:
        _validate_proposal(proposal)
        with self._lock:
            state = self.load()
            item_id = new_id("item")
            item = {
                "item_id": item_id,
                "status": "queued",
                "created_at": utc_now_iso(),
                "proposal": proposal,
            }
            state.setdefault("items", []).append(item)
            self.save(state)
            return IntakeResult(item_id=item_id, status="queued")

    def authorize(self, item_id: str) -> AuthorizeResult:
        with self._lock:
            state = self.load()
            item = _find_item(state, item_id)
            if item["status"] != "queued":
                raise ValueError("item must be queued before authorization")
            decision_id = new_id("dec")
            item["status"] = "authorized"
            decision = {
                "decision_id": decision_id,
                "item_id": item_id,
                "decided_by": "dev_master",
                "decision": "authorize",
                "decided_at": utc_now_iso(),
                "provider_self_approval": False,
                "checks": {
                    "token_auth_passed": True,
                    "provider_mode_stub": True,
                    "external_side_effects": False,
                },
            }
            state.setdefault("decisions", []).append(decision)
            self.save(state)
            return AuthorizeResult(decision_id=decision_id, item_id=item_id, status="authorized")

    def run_provider(self, item_id: str, fixture_path: Path) -> ProviderRunResult:
        resolved_fixture = _resolve_fixture_path(fixture_path)
        with self._lock:
            state = self.load()
            item = _find_item(state, item_id)
            if item["status"] != "authorized":
                raise ValueError("item must be authorized before provider execution")

            run_id = new_id("run")
            output_path = self.provider_evidence_dir / f"{item_id}-{run_id}.json"
            adapter_result = adapt_provider_fixture(
                fixture_path=resolved_fixture,
                output_path=output_path,
                trace_id=f"tr_{item_id}",
                run_id=run_id,
                raw_store_dir=self.provider_evidence_dir / "raw",
            )
            provider_output = adapter_result.provider_output
            drift_detected = bool(provider_output["drift_detected"])
            status = "provider_drift" if drift_detected else "provider_completed"
            item["status"] = status

            evidence_record = self._build_evidence_record(
                item_id=item_id,
                run_id=run_id,
                provider_output_path=output_path,
                raw_output_path=adapter_result.raw_output_path,
            )
            append_jsonl(self.evidence_index_path, evidence_record)

            evidence_ref = f"{relative(self.evidence_index_path)}#{evidence_record['evidence_id']}"
            provider_run = {
                "run_id": run_id,
                "item_id": item_id,
                "status": status,
                "provider_output_ref": relative(output_path),
                "drift_detected": drift_detected,
                "evidence_ref": evidence_ref,
                "created_at": utc_now_iso(),
            }
            state.setdefault("provider_runs", []).append(provider_run)
            self.save(state)
            return ProviderRunResult(
                run_id=run_id,
                item_id=item_id,
                provider_output_ref=relative(output_path),
                evidence_ref=evidence_ref,
                drift_detected=drift_detected,
                status=status,
            )

    def _build_evidence_record(
        self,
        *,
        item_id: str,
        run_id: str,
        provider_output_path: Path,
        raw_output_path: Path,
    ) -> dict[str, Any]:
        seed = f"{item_id}:{run_id}:{relative(provider_output_path)}"
        evidence_id = "ev_" + sha256(seed.encode("utf-8")).hexdigest()[:16]
        return {
            "artifact_family": "devmasterd_local_evidence",
            "schema_version": "1.0.0",
            "policy_version": STATE_POLICY_VERSION,
            "evidence_id": evidence_id,
            "created_at": utc_now_iso(),
            "item_id": item_id,
            "run_id": run_id,
            "summary": "devmasterd local provider adapter run",
            "artifact_refs": [
                {
                    "path": relative(provider_output_path),
                    "digest": hash_file(provider_output_path),
                },
                {
                    "path": relative(raw_output_path),
                    "digest": hash_file(raw_output_path),
                },
            ],
            "writeback_status": "local_devmasterd",
            "external_side_effects": False,
        }


class DevmasterHTTPServer(ThreadingHTTPServer):
    state_store: DevmasterStateStore
    token: str

    def __init__(
        self,
        server_address: tuple[str, int],
        request_handler_class: type[BaseHTTPRequestHandler],
        *,
        state_store: DevmasterStateStore,
        token: str,
    ) -> None:
        super().__init__(server_address, request_handler_class)
        self.state_store = state_store
        self.token = token


class DevmasterRequestHandler(BaseHTTPRequestHandler):
    server: DevmasterHTTPServer

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:
        if not self._authorized():
            return
        if self.path == "/v1/state":
            self._send_json(HTTPStatus.OK, self.server.state_store.load())
            return
        if self.path == "/v1/evidence":
            self._send_json(
                HTTPStatus.OK,
                {"records": self.server.state_store.evidence_records()},
            )
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:
        if not self._authorized():
            return
        try:
            payload = self._read_json()
            if self.path == "/v1/intake":
                intake_result = self.server.state_store.intake(
                    cast(dict[str, Any], payload.get("task_proposal"))
                )
                self._send_json(HTTPStatus.CREATED, intake_result.__dict__)
                return
            if self.path == "/v1/authorize":
                authorize_result = self.server.state_store.authorize(
                    _required_str(payload, "item_id")
                )
                self._send_json(HTTPStatus.OK, authorize_result.__dict__)
                return
            if self.path == "/v1/run-provider":
                fixture = Path(payload.get("provider_fixture", DEFAULT_FIXTURE_PATH.as_posix()))
                provider_result = self.server.state_store.run_provider(
                    item_id=_required_str(payload, "item_id"),
                    fixture_path=fixture,
                )
                self._send_json(HTTPStatus.OK, provider_result.__dict__)
                return
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})

    def _authorized(self) -> bool:
        expected = f"Bearer {self.server.token}"
        if self.headers.get("Authorization") != expected:
            self._send_json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
            return False
        return True

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        return cast(dict[str, Any], json.loads(raw.decode("utf-8")))

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def create_server(*, host: str, port: int, token: str, state_dir: Path) -> DevmasterHTTPServer:
    if not token:
        raise ValueError("token is required")
    _validate_loopback_host(host)
    state_store = DevmasterStateStore(state_dir)
    state_store.load()
    return DevmasterHTTPServer(
        (host, port),
        DevmasterRequestHandler,
        state_store=state_store,
        token=token,
    )


@contextmanager
def serve_in_thread(*, token: str, state_dir: Path) -> Iterator[str]:
    server = create_server(host="127.0.0.1", port=0, token=token, state_dir=state_dir)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def run_smoke(*, token: str, state_dir: Path, output_path: Path) -> dict[str, Any]:
    with serve_in_thread(token=token, state_dir=state_dir) as base_url:
        unauthorized_status = _request_status(
            Request(f"{base_url}/v1/state", method="GET"),
        )
        intake = _json_request(
            base_url,
            "/v1/intake",
            token,
            {
                "task_proposal": {
                    "schema_version": "1.0.0",
                    "proposal_id": "prop_devmasterd_smoke",
                    "trace_id": "tr_devmasterd_smoke",
                    "proposer": "human",
                    "goal": "Run the devmasterd smoke path.",
                    "slices": [
                        {
                            "slice_id": "slice_devmasterd_smoke",
                            "expected_cost_usd": 0.0,
                            "provider_kind": "api",
                            "risk_label_estimate": "green",
                        }
                    ],
                }
            },
        )
        authorize = _json_request(
            base_url,
            "/v1/authorize",
            token,
            {"item_id": intake["item_id"]},
        )
        provider_run = _json_request(
            base_url,
            "/v1/run-provider",
            token,
            {
                "item_id": intake["item_id"],
                "provider_fixture": "runtime/fixtures/provider-output.ok.json",
            },
        )
        state = _json_get(base_url, "/v1/state", token)
        evidence = _json_get(base_url, "/v1/evidence", token)

    smoke = {
        "artifact_family": "devmasterd_smoke_result",
        "schema_version": "1.0.0",
        "policy_version": STATE_POLICY_VERSION,
        "created_at": utc_now_iso(),
        "unauthorized_status": unauthorized_status,
        "intake": intake,
        "authorize": authorize,
        "provider_run": provider_run,
        "state": state,
        "evidence": evidence,
        "external_side_effects": False,
        "pass": (
            unauthorized_status == HTTPStatus.UNAUTHORIZED.value
            and intake.get("status") == "queued"
            and authorize.get("status") == "authorized"
            and provider_run.get("status") == "provider_completed"
            and bool(evidence.get("records"))
        ),
    }
    write_json(output_path, smoke)
    return smoke


def _validate_proposal(proposal: Any) -> None:
    if not isinstance(proposal, dict):
        raise ValueError("task_proposal must be an object")
    if not isinstance(proposal.get("goal"), str) or not proposal["goal"]:
        raise ValueError("task_proposal.goal is required")
    slices = proposal.get("slices")
    if not isinstance(slices, list) or not slices:
        raise ValueError("task_proposal.slices must be a non-empty list")


def _find_item(state: dict[str, Any], item_id: str) -> dict[str, Any]:
    for item in state.get("items", []):
        if isinstance(item, dict) and item.get("item_id") == item_id:
            return item
    raise ValueError("unknown item_id")


def _resolve_fixture_path(path: Path) -> Path:
    candidate = path if path.is_absolute() else REPO_ROOT / path
    resolved = candidate.resolve()
    fixtures_root = (REPO_ROOT / "runtime/fixtures").resolve()
    if not resolved.is_relative_to(fixtures_root):
        raise ValueError("provider_fixture must be under runtime/fixtures")
    if not resolved.exists():
        raise ValueError("provider_fixture does not exist")
    return resolved


def _validate_loopback_host(host: str) -> None:
    if host == "localhost":
        return
    try:
        if ip_address(host).is_loopback:
            return
    except ValueError as exc:
        raise ValueError("devmasterd host must be localhost or a loopback address") from exc
    raise ValueError("devmasterd host must be localhost or a loopback address")


def _required_str(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} is required")
    return value


def _json_request(
    base_url: str,
    path: str,
    token: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    request = Request(
        f"{base_url}{path}",
        data=json.dumps(payload, ensure_ascii=True).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=3) as response:  # noqa: S310 - localhost smoke only.
        return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))


def _json_get(base_url: str, path: str, token: str) -> dict[str, Any]:
    request = Request(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urlopen(request, timeout=3) as response:  # noqa: S310 - localhost smoke only.
        return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))


def _request_status(request: Request) -> int:
    try:
        with urlopen(request, timeout=3) as response:  # noqa: S310 - localhost smoke only.
            return int(response.status)
    except HTTPError as exc:
        status = int(exc.code)
        exc.close()
        return status
