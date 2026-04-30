#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime_engine.devmasterd import DEFAULT_SMOKE_STATE_PATH, DEFAULT_STATE_DIR, create_server
from runtime_engine.devmasterd import run_smoke as run_devmasterd_smoke


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local devmasterd control plane.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument("--token-env", default="DEVMASTERD_TOKEN")
    parser.add_argument("--test-token", help="Explicit local test token for smoke tests only.")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--smoke-output", type=Path, default=DEFAULT_SMOKE_STATE_PATH)
    args = parser.parse_args()

    token = args.test_token or os.environ.get(args.token_env)
    if not token:
        print(f"{args.token_env} is required", file=sys.stderr)
        return 2

    if args.smoke:
        result = run_devmasterd_smoke(
            token=token,
            state_dir=args.state_dir.resolve(),
            output_path=args.smoke_output.resolve(),
        )
        print(
            json.dumps(
                {
                    "output": args.smoke_output.as_posix(),
                    "pass": result["pass"],
                    "unauthorized_status": result["unauthorized_status"],
                    "provider_status": result["provider_run"]["status"],
                },
                indent=2,
                ensure_ascii=True,
            )
        )
        return 0 if result["pass"] else 1

    server = create_server(
        host=args.host,
        port=args.port,
        token=token,
        state_dir=args.state_dir.resolve(),
    )
    print(f"devmasterd listening on http://{args.host}:{args.port}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
