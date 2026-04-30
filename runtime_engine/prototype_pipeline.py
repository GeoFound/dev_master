from __future__ import annotations

import html
import json
import re
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import partial
from hashlib import sha256
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IDEA_PATH = REPO_ROOT / "runtime/fixtures/l1-idea.simple.json"
DEFAULT_PROTOTYPE_ROOT = REPO_ROOT / "runtime/prototypes"
DEFAULT_VALIDATION_PATH = REPO_ROOT / "runtime/prototype-validation/l1-prototype-report.json"
POLICY_VERSION = "l1-local-prototype-pipeline-v1"


@dataclass(frozen=True)
class PrototypeResult:
    prototype_id: str
    prototype_dir: Path
    index_path: Path
    manifest_path: Path
    runbook_path: Path


class QuietPrototypeHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def load_idea(path: Path) -> dict[str, Any]:
    payload = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    validate_idea(payload)
    return payload


def validate_idea(payload: dict[str, Any]) -> None:
    for field in ("idea_id", "title", "audience", "problem", "promise"):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} is required")
    actions = payload.get("primary_actions")
    if not isinstance(actions, list) or not actions:
        raise ValueError("primary_actions must be a non-empty list")
    if any(not isinstance(action, str) or not action.strip() for action in actions):
        raise ValueError("primary_actions must contain non-empty strings")


def build_prototype(
    *,
    idea_path: Path = DEFAULT_IDEA_PATH,
    prototype_root: Path = DEFAULT_PROTOTYPE_ROOT,
) -> PrototypeResult:
    idea = load_idea(idea_path)
    prototype_id = _slugify(_required_str(idea, "idea_id"))
    prototype_dir = prototype_root / prototype_id
    prototype_dir.mkdir(parents=True, exist_ok=True)

    index_path = prototype_dir / "index.html"
    manifest_path = prototype_dir / "manifest.json"
    runbook_path = prototype_dir / "runbook.md"

    index_path.write_text(_render_index_html(idea), encoding="utf-8")
    _write_json(
        manifest_path,
        {
            "artifact_family": "l1_local_prototype_manifest",
            "schema_version": "1.0.0",
            "policy_version": POLICY_VERSION,
            "prototype_id": prototype_id,
            "created_at": utc_now_iso(),
            "source_idea_ref": _relative(idea_path),
            "provider_kind": "local_tool",
            "files": [
                "index.html",
                "manifest.json",
                "runbook.md",
            ],
            "scope": _scope_flags(),
        },
    )
    runbook_path.write_text(_render_runbook(idea, prototype_dir), encoding="utf-8")
    return PrototypeResult(
        prototype_id=prototype_id,
        prototype_dir=prototype_dir,
        index_path=index_path,
        manifest_path=manifest_path,
        runbook_path=runbook_path,
    )


def validate_prototype(
    *,
    prototype: PrototypeResult,
    idea_path: Path = DEFAULT_IDEA_PATH,
    output_path: Path = DEFAULT_VALIDATION_PATH,
) -> dict[str, Any]:
    idea = load_idea(idea_path)
    with _serve_directory(prototype.prototype_dir) as base_url:
        status, body = _fetch_text(f"{base_url}/")

    title = _required_str(idea, "title")
    expected_markers = [title, "Workflow"]
    marker_results = {marker: marker in body for marker in expected_markers}
    artifact_refs = [
        _artifact_ref(prototype.index_path),
        _artifact_ref(prototype.manifest_path),
        _artifact_ref(prototype.runbook_path),
    ]
    report = {
        "artifact_family": "l1_prototype_validation_report",
        "schema_version": "1.0.0",
        "policy_version": POLICY_VERSION,
        "created_at": utc_now_iso(),
        "prototype_id": prototype.prototype_id,
        "prototype_dir": _relative(prototype.prototype_dir),
        "source_idea_ref": _relative(idea_path),
        "localhost_http_status": status,
        "content_markers": marker_results,
        "artifact_refs": artifact_refs,
        "external_side_effects": False,
        "scope": _scope_flags(),
        "pass": (
            status == HTTPStatus.OK.value
            and all(marker_results.values())
            and all(Path(ref["path"]).suffix in {".html", ".json", ".md"} for ref in artifact_refs)
        ),
    }
    _write_json(output_path, report)
    return report


def run_pipeline(
    *,
    idea_path: Path = DEFAULT_IDEA_PATH,
    prototype_root: Path = DEFAULT_PROTOTYPE_ROOT,
    output_path: Path = DEFAULT_VALIDATION_PATH,
) -> dict[str, Any]:
    prototype = build_prototype(idea_path=idea_path, prototype_root=prototype_root)
    return validate_prototype(prototype=prototype, idea_path=idea_path, output_path=output_path)


def _render_index_html(idea: dict[str, Any]) -> str:
    title = html.escape(_required_str(idea, "title"))
    audience = html.escape(_required_str(idea, "audience"))
    problem = html.escape(_required_str(idea, "problem"))
    promise = html.escape(_required_str(idea, "promise"))
    action_items = "\n".join(
        f"        <li>{html.escape(str(action))}</li>"
        for action in cast(list[str], idea["primary_actions"])
    )
    success_signal = html.escape(str(idea.get("success_signal", "Prototype loads locally.")))
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
      :root {{
        color-scheme: light;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
          BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f7f8fa;
        color: #1c2430;
      }}
      body {{
        margin: 0;
      }}
      main {{
        max-width: 960px;
        margin: 0 auto;
        padding: 48px 24px;
      }}
      header, section {{
        background: #ffffff;
        border: 1px solid #d8dee8;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 18px;
      }}
      h1, h2 {{
        margin: 0 0 12px;
      }}
      p {{
        line-height: 1.55;
      }}
      li {{
        margin: 8px 0;
      }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>{title}</h1>
        <p><strong>Audience:</strong> {audience}</p>
        <p>{promise}</p>
      </header>
      <section>
        <h2>Problem</h2>
        <p>{problem}</p>
      </section>
      <section>
        <h2>Workflow</h2>
        <ol>
{action_items}
        </ol>
      </section>
      <section>
        <h2>Success Signal</h2>
        <p>{success_signal}</p>
      </section>
    </main>
  </body>
</html>
"""


def _render_runbook(idea: dict[str, Any], prototype_dir: Path) -> str:
    title = _required_str(idea, "title")
    relative_dir = _relative(prototype_dir)
    return f"""# {title}

## Run Locally

```bash
python3 -m http.server 8788 --directory {relative_dir}
```

Then open `http://127.0.0.1:8788/`.

## Scope

- Generated by the local L1 prototype pipeline.
- Uses deterministic local templates only.
- Does not call real providers, mutate external repositories, deploy, or create PRs.
"""


@contextmanager
def _serve_directory(directory: Path) -> Iterator[str]:
    handler = partial(QuietPrototypeHandler, directory=directory.as_posix())
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _fetch_text(url: str) -> tuple[int, str]:
    with urlopen(url, timeout=3) as response:  # noqa: S310 - localhost validation only.
        return int(response.status), response.read().decode("utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _artifact_ref(path: Path) -> dict[str, str]:
    return {
        "path": _relative(path),
        "digest": "sha256:" + sha256(path.read_bytes()).hexdigest(),
    }


def _scope_flags() -> dict[str, bool]:
    return {
        "local_tool_only": True,
        "real_provider_calls": False,
        "subscription_cli_daemonization": False,
        "live_auto_router_calls": False,
        "external_repo_mutation": False,
        "deploy": False,
        "pr_creation": False,
        "production_side_effect": False,
        "accounts_auth_payments_multitenancy": False,
        "web_console": False,
        "ide_extension": False,
    }


def _required_str(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("idea_id must contain at least one alphanumeric character")
    return slug


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
