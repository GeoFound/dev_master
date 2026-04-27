#!/usr/bin/env bash
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

python3 verifier/verifier.py \
  --facts tests/fixtures/good_runner_facts.yaml \
  --output "$tmpdir/good-verification.json" \
  --expect-decision allow

python3 verifier/verifier.py \
  --facts tests/fixtures/bad_runner_facts.yaml \
  --output "$tmpdir/bad-verification.json" \
  --expect-decision block

python3 runner/local_worktree_runner.py \
  --requested-change "Phase 1 smoke run for local runner facts emitter" \
  --menmery-context-ref "mcp:get_context:phase1-smoke" \
  --trace-id "phase1-smoke" \
  --output "$tmpdir/live-runner-facts.yaml" \
  --lint pass \
  --tests pass \
  --security not_run \
  --allow-empty

python3 verifier/verifier.py \
  --facts "$tmpdir/live-runner-facts.yaml" \
  --output "$tmpdir/live-verification.json" \
  --expect-decision allow

printf 'phase1 kernel smoke passed\n'
