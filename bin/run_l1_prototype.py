#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "runtime/prototypes/l1-local-prototype"


def prototype_status(root: Path) -> dict[str, Any]:
    index_path = root / "index.html"
    provider_output_path = root / "provider-output.json"
    html = index_path.read_text(encoding="utf-8")
    provider_output = json.loads(provider_output_path.read_text(encoding="utf-8"))
    return {
        "prototype_root": root.relative_to(REPO_ROOT).as_posix(),
        "entrypoint": index_path.relative_to(REPO_ROOT).as_posix(),
        "visible_output": "<main" in html and "dev_master Factory Console" in html,
        "provider_path": provider_output["provider_kind"],
        "provider_drift_detected": provider_output["drift_detected"],
        "run_command": "uv run python bin/run_l1_prototype.py --port 8765",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Phase 1B local L1 prototype.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    if args.check:
        print(json.dumps(prototype_status(root), indent=2, ensure_ascii=True))
        return 0

    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        print(f"Serving Phase 1B prototype at http://{args.host}:{args.port}/", flush=True)
        server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
