from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = REPO_ROOT / "runtime"
DOC_REGISTRY_PATH = RUNTIME_DIR / "doc-registry.json"
TASK_GRAPH_PATH = RUNTIME_DIR / "task-graph.json"
PROGRAM_STATE_PATH = RUNTIME_DIR / "program-state.json"
CURRENT_TASK_PATH = RUNTIME_DIR / "current-task.json"
SESSION_LOG_PATH = RUNTIME_DIR / "session-log.jsonl"
COMPLETIONS_DIR = RUNTIME_DIR / "completions"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def load_doc_registry(root: Path = REPO_ROOT) -> dict[str, Any]:
    return load_json(root / DOC_REGISTRY_PATH.relative_to(REPO_ROOT))


def load_task_graph(root: Path = REPO_ROOT) -> dict[str, Any]:
    return load_json(root / TASK_GRAPH_PATH.relative_to(REPO_ROOT))


def load_program_state(root: Path = REPO_ROOT) -> dict[str, Any]:
    return load_json(root / PROGRAM_STATE_PATH.relative_to(REPO_ROOT))


def load_current_task(root: Path = REPO_ROOT) -> dict[str, Any]:
    path = root / CURRENT_TASK_PATH.relative_to(REPO_ROOT)
    if not path.exists():
        return {}
    return load_json(path)


def registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["path"]: item for item in registry["documents"]}


def sorted_tasks(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(graph["tasks"], key=lambda item: item["order"])


def prerequisites_met(task: dict[str, Any], state: dict[str, Any]) -> bool:
    completed = set(state.get("completed_tasks", []))
    prereq = task.get("prerequisites", {})

    for task_id in prereq.get("tasks", []):
        if task_id not in completed:
            return False

    gates = state.get("gates", {})
    for gate_name, expected in prereq.get("gates", {}).items():
        if gates.get(gate_name) != expected:
            return False

    return True


def next_available_task(graph: dict[str, Any], state: dict[str, Any]) -> dict[str, Any] | None:
    completed = set(state.get("completed_tasks", []))
    for task in sorted_tasks(graph):
        if task["id"] in completed:
            continue
        if prerequisites_met(task, state):
            return task
    return None


def build_current_task_payload(
    task: dict[str, Any] | None,
    graph: dict[str, Any],
    state: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    if task is None:
        return {
            "generated_at": utc_now_iso(),
            "graph_version": graph["version"],
            "state_version": state["version"],
            "status": "no-next-task",
            "reason": "No available task matched the current phase/gate state.",
        }

    index = registry_index(registry)
    source_docs = []
    for path in task.get("source_docs", []):
        record = deepcopy(index.get(path, {"path": path, "role": "unknown"}))
        source_docs.append(record)

    return {
        "generated_at": utc_now_iso(),
        "graph_version": graph["version"],
        "state_version": state["version"],
        "status": "ready",
        "task": {
            "id": task["id"],
            "title": task["title"],
            "task_type": task["task_type"],
            "phase": task["phase"],
            "plane": task.get("plane"),
            "goal": task["goal"],
            "scope_in": task.get("scope_in", []),
            "scope_out": task.get("scope_out", []),
            "dependencies": task.get("prerequisites", {}),
            "deliverables": task.get("deliverables", []),
            "required_paths": task.get("required_paths", []),
            "acceptance_checks": task.get("acceptance_checks", []),
            "evidence_outputs": task.get("evidence_outputs", []),
            "contract_requirements": task.get("contract_requirements", []),
            "decision_records_required": task.get("decision_records_required", []),
            "source_docs": source_docs,
            "gate": task.get("gate"),
            "notes": task.get("notes", []),
        },
    }


def derive_next_task(root: Path = REPO_ROOT, write: bool = True) -> dict[str, Any]:
    graph = load_task_graph(root)
    state = load_program_state(root)
    registry = load_doc_registry(root)

    task = next_available_task(graph, state)
    payload = build_current_task_payload(task, graph, state, registry)

    updated_state = deepcopy(state)
    updated_state["active_task_id"] = task["id"] if task else None
    if task is not None:
        updated_state["current_phase"] = task["phase"]

    if write:
        write_json(root / PROGRAM_STATE_PATH.relative_to(REPO_ROOT), updated_state)
        write_json(root / CURRENT_TASK_PATH.relative_to(REPO_ROOT), payload)

    return payload


def verify_required_paths(root: Path, required_paths: list[str]) -> list[str]:
    missing = []
    for relative_path in required_paths:
        if not (root / relative_path).exists():
            missing.append(relative_path)
    return missing


def complete_current_task(
    *,
    root: Path = REPO_ROOT,
    status: str,
    decision: str,
    summary: str,
    recommendation_for_human: str,
    artifacts_changed: list[str],
    evidence_refs: list[str],
    drift_found: bool,
    gate_verdict: str | None,
    notes: list[str],
) -> dict[str, Any]:
    current = load_current_task(root)
    if current.get("status") != "ready":
        raise ValueError("No active ready task exists.")

    task = current["task"]
    required_paths = task.get("required_paths", [])
    if status == "completed":
        missing = verify_required_paths(root, required_paths)
        if missing:
            raise ValueError(f"Missing required deliverables: {', '.join(missing)}")

    if task.get("gate") and status == "completed" and gate_verdict is None:
        raise ValueError("Gate tasks require --gate-verdict.")

    completion_record = {
        "completed_at": utc_now_iso(),
        "task_id": task["id"],
        "phase": task["phase"],
        "task_type": task["task_type"],
        "status": status,
        "decision": decision,
        "summary": summary,
        "recommendation_for_human": recommendation_for_human,
        "artifacts_changed": artifacts_changed,
        "evidence_refs": evidence_refs,
        "drift_found": drift_found,
        "gate": task.get("gate"),
        "gate_verdict": gate_verdict,
        "notes": notes,
    }

    timestamp = completion_record["completed_at"].replace(":", "").replace("-", "")
    filename = f"{timestamp}_{task['id'].replace('.', '_')}.json"
    write_json(root / COMPLETIONS_DIR.relative_to(REPO_ROOT) / filename, completion_record)

    state = load_program_state(root)
    state.setdefault("task_statuses", {})[task["id"]] = status
    if status == "completed":
        completed = state.setdefault("completed_tasks", [])
        if task["id"] not in completed:
            completed.append(task["id"])
    if task.get("gate") and gate_verdict is not None:
        state.setdefault("gates", {})[task["gate"]] = gate_verdict

    state["last_completed_task_id"] = task["id"]
    state["last_transition_at"] = completion_record["completed_at"]
    state["active_task_id"] = None
    write_json(root / PROGRAM_STATE_PATH.relative_to(REPO_ROOT), state)

    append_jsonl(
        root / SESSION_LOG_PATH.relative_to(REPO_ROOT),
        {
            "timestamp": completion_record["completed_at"],
            "event": "task_completed",
            "task_id": task["id"],
            "phase": task["phase"],
            "status": status,
            "decision": decision,
            "gate": task.get("gate"),
            "gate_verdict": gate_verdict,
        },
    )

    next_task = None
    if status == "completed":
        next_task = derive_next_task(root=root, write=True)

    return {
        "completion_record": completion_record,
        "next_task": next_task,
    }
