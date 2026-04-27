#!/usr/bin/env python3
"""Emit software-change-runner-v1 facts for the current local worktree.

This runner is deliberately small: it packages git diff facts, check statuses,
and software-change risk facts. It does not approve work, write canonical
truth, call model routing, or mutate repositories.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "software-change-runner-v1"


DEPENDENCY_FILES = {
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "poetry.lock",
    "uv.lock",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
}

DOC_EXTENSIONS = {".md", ".markdown", ".txt", ".rst"}


def run_git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def repo_root() -> Path:
    return Path(run_git(["rev-parse", "--show-toplevel"], Path.cwd()).strip())


def changed_files(root: Path) -> list[str]:
    tracked = run_git(["diff", "HEAD", "--name-only", "--"], root).splitlines()
    untracked = run_git(["ls-files", "--others", "--exclude-standard"], root).splitlines()
    return sorted({path for path in [*tracked, *untracked] if path})


def diff_material(root: Path, files: list[str]) -> str:
    diff = run_git(["diff", "HEAD", "--no-ext-diff", "--"], root)
    untracked = []
    tracked = set(run_git(["ls-files"], root).splitlines())
    for rel in files:
        if rel in tracked:
            continue
        path = root / rel
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            untracked.append(f"UNTRACKED {rel} sha256:{digest}")
    return diff + ("\n".join(untracked) + "\n" if untracked else "")


def has_path_part(path: str, parts: set[str]) -> bool:
    return bool(set(Path(path).parts) & parts)


def classify(files: list[str]) -> dict[str, Any]:
    docs_only = bool(files) and all(Path(path).suffix in DOC_EXTENSIONS for path in files)
    dependency_changed = any(Path(path).name in DEPENDENCY_FILES for path in files)
    secrets_or_permissions_changed = any(
        Path(path).name.startswith(".env")
        or "secret" in path.lower()
        or "permission" in path.lower()
        or path.endswith((".pem", ".key", ".p12"))
        for path in files
    )
    infra_or_deploy_path_changed = any(
        has_path_part(path, {".github", "deploy", "deployment", "k8s", "terraform"})
        or Path(path).name in {"Dockerfile", "docker-compose.yml", "compose.yml"}
        for path in files
    )
    repo_local_ai_scaffold = bool(files) and all(
        path.startswith(
            (
                "runner/",
                "verifier/",
                "scripts/",
                "tests/",
                "tasks/",
                "reports/",
                "templates/",
                "contracts/",
            )
        )
        or path
        in {
            "justfile",
            "README.md",
            "AGENTS.md",
            "ai-instructions.md",
            "00-index.md",
            "04-pipeline.md",
            "05-quality.md",
            "08-repo-structure.md",
            "14-master-program.md",
            "15-phase-gates.md",
            "18-master-execution-task.md",
            "20-layered-program-map.md",
            "24-ai-cold-start.md",
            "25-implementation-language-baseline.md",
        }
        for path in files
    )

    if secrets_or_permissions_changed or infra_or_deploy_path_changed:
        risk_label = "red"
        action_level = 4
    elif dependency_changed:
        risk_label = "yellow"
        action_level = 3
    elif files:
        risk_label = "green"
        action_level = 2
    else:
        risk_label = "green"
        action_level = 1

    return {
        "docs_only": docs_only,
        "repo_local_ai_scaffold": repo_local_ai_scaffold,
        "dependency_changed": dependency_changed,
        "secrets_or_permissions_changed": secrets_or_permissions_changed,
        "infra_or_deploy_path_changed": infra_or_deploy_path_changed,
        "external_write": False,
        "action_level": action_level,
        "risk_label": risk_label,
    }


def build_facts(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root()
    excluded = set(args.exclude_path or [])
    files = [path for path in changed_files(root) if path not in excluded]
    if files or args.allow_empty:
        material = diff_material(root, files)
    else:
        raise SystemExit("no local diff found; pass --allow-empty for a read-only smoke run")

    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], root).strip()
    head = run_git(["rev-parse", "--short", "HEAD"], root).strip()

    return {
        "runner_contract_version": CONTRACT_VERSION,
        "trace_id": args.trace_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "menmery_context_ref": args.menmery_context_ref,
        "requested_change": args.requested_change,
        "repo_ref": f"{root.name}@{branch}:{head}",
        "diff_digest": f"sha256:{digest}",
        "files_changed": files,
        "checks": {
            "lint": args.lint,
            "tests": args.tests,
            "security": args.security,
        },
        "risk_facts": classify(files),
        "evidence_writeback": {
            "method": args.evidence_method,
            "id": args.evidence_id,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit software-change-runner-v1 facts")
    parser.add_argument("--requested-change", required=True)
    parser.add_argument("--menmery-context-ref", required=True)
    parser.add_argument("--trace-id", default="phase1-local-runner")
    parser.add_argument("--output", required=True)
    parser.add_argument("--lint", choices=["pass", "fail", "not_run"], default="not_run")
    parser.add_argument("--tests", choices=["pass", "fail", "not_run"], default="not_run")
    parser.add_argument("--security", choices=["pass", "fail", "not_run"], default="not_run")
    parser.add_argument("--evidence-method", default="fallback_local")
    parser.add_argument("--evidence-id", default="pending")
    parser.add_argument(
        "--exclude-path",
        action="append",
        help="Relative path to exclude from diff digest and files_changed.",
    )
    parser.add_argument("--allow-empty", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    facts = build_facts(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(facts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
