---
status: deferred
scope: window
authority: ref-only
---

# Implementation Language Baseline

> Historical/candidate baseline. Implementation scaffolding was deleted on
> 2026-04-27 at human request. This file may inform the rewrite plan, but it no
> longer authorizes new implementation by itself.

---

## 25.1 Decision

Previous Phase 1 `dev_master` implementation defaulted to:

| Area | Baseline |
|------|----------|
| runner / harness / verifier | Python |
| local state interfaces | Python |
| repository commands | `just` + small Bash scripts |
| contracts and runner facts | YAML |
| machine-readable evidence snapshots | JSON / JSONL when needed |
| human-readable evidence and reports | Markdown |
| LLM routing | external `auto_router` routing control plane, not implemented here |
| `menmery` integration | MCP / CLI / documented caller protocol, not internal imports |

This is not active implementation approval. A new rewrite slice must explicitly
accept, revise, or replace this baseline.

---

## 25.2 Why Python For Phase 1

Python was the default candidate for the first `dev_master` implementation
because:

- the documented `StateStore` interface is already Python-shaped
- the first local runner is described as `local_worktree_runner.py`
- verifier logic is primarily structured file/diff/fact validation
- `menmery` is a Python project, but `dev_master` still must not import its
  internals
- Python keeps Phase 1 close to local CLI, JSON/YAML, filesystem, and test
  integration without adding a frontend or service framework

The choice is pragmatic: it reduces early implementation variance while the
real contract remains runner facts and `menmery` evidence references.

---

## 25.3 Language Boundaries

### Python

If the rewrite re-accepts this baseline, Python may be used for:

- local worktree runner
- runner facts emitter
- verifier checks
- local fallback state/index helpers
- caller-side adapters to documented `menmery` facade commands
- local gateway client calls to `auto_router`, if needed

Python code must stay within `dev_master` ownership boundaries. It must not
turn `dev_master` into a truth runtime, approval controller, model router, or
general platform.

### `just` And Bash

If the rewrite re-accepts this baseline, `just` and Bash may be used for
command orchestration and guardrail checks:

- historical examples: `just check`, `just validate-contract`,
  `just drift-check`, `just gate-a`
- small repository validation scripts

Bash must not accumulate complex runner, verifier, or governance logic. If the
logic needs structured parsing, state, tests, or non-trivial branching, move it
to Python and keep Bash as a command wrapper.

### YAML / JSON / Markdown

Use:

- YAML for runner facts examples and lightweight contracts
- JSON / JSONL for machine-readable snapshots or append-only local indexes
- Markdown for human-readable reports, tasks, gate evidence, and drift records

Do not create a dev_master-owned schema or policy authority that competes with
`menmery`. `dev_master` owns `runner_contract_version` and the local runner
facts shape only.

### Go

Go belongs to `auto_router` in the current system map. `dev_master` must not
reimplement routing, runtime planner, failover, learner publishing, or cost
classification in Go.

Calling `auto_router` from Python or shell is allowed when the task needs LLM
analysis and the call is recorded as part of runner facts or evidence.

### TypeScript / JavaScript

Do not introduce TypeScript or JavaScript for Phase 1 core implementation.
There is no active frontend or Node service in the current build program.

### Rust / Other Languages

Do not introduce Rust or another systems language for Phase 1 core
implementation. Such a change requires evidence that Python plus local tool
calls cannot meet the runner/verifier requirement.

---

## 25.4 Runner Repository Exception

Untrusted or high-permission execution workers may later live in separate repos
with their own language choices. That does not change the Phase 1 baseline for
this reference repo.

Any external runner must communicate through:

- `software-change-runner-v1` runner facts
- diff/artifact digests
- check results
- `menmery` context/evidence references

It must not communicate through direct imports of `dev_master` or `menmery`
internals.

---

## 25.5 Change Rule

Reactivating or changing the implementation language baseline requires one of:

- correction evidence that the current baseline blocks Gate B
- activation proposal for a separately owned runner repo
- human-approved gate decision that explicitly changes this baseline

Without one of these, do not add new implementation files.
