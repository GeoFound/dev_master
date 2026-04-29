---
status: active
scope: integration
authority: this
---

# External Systems Boundary

> Active system boundary. This file records the current understanding of
> `menmery` and `auto_router` after reading their own repositories. It prevents
> `dev_master` from either ignoring them or being reduced to their subproject.

---

## 27.1 Sources Checked

`auto_router`:

- `/home/jade/projects/auto_router/README.md`
- `/home/jade/projects/auto_router/AGENTS.md`
- `/home/jade/projects/auto_router/ARCHITECTURE.md`

`menmery`:

- `/home/jade/projects/menmery/README.md`
- `/home/jade/projects/menmery/MENMERY_POSITIONING.md`
- `/home/jade/projects/menmery/INTELLIGENCE_CORE.md`
- `/home/jade/projects/menmery/docs/guides/CALLER_PROTOCOL.md`
- `/home/jade/projects/menmery/docs/guides/SOFTWARE_CHANGE_CAPABILITY.md`
- `/home/jade/projects/menmery/docs/architecture/RUNTIME.md`

These repositories are sibling systems. Their own source files are the authority
for their behavior.

---

## 27.2 dev_master Owns

`dev_master` is the independent AI automation development pipeline product. It
owns the product-level software delivery loop:

```text
intake -> spec -> critique -> implementation -> tests -> security
-> result gate -> PR/release -> canary/rollback -> ops/advice/recovery
```

It also owns the product-level architecture for:

- AI role model and stage contracts
- bounded execution harness requirements
- runner facts and verifier expectations
- Result Gate semantics
- release safety and rollback expectations
- Ops AI / Advisor AI / TechRadar roadmap
- project adapter roadmap
- rewrite governance roadmap

It must not implement a competing LLM routing control plane or a competing
personal truth/governance runtime.

---

## 27.3 menmery Boundary

`menmery` is long-term cognitive infrastructure / personal intelligence core.
It is not a note app, workflow engine, or `dev_master` submodule.

For `software_change`, `menmery` provides:

- default facade surface: `entry_turn`, `get_recent_activity`, `remember`,
  `get_context`, `act`, `follow_recommended_call`
- entry-turn panorama scaffolds with provenance, missing sides, unresolved
  gaps, and governed next step
- context retrieval and workspace continuity
- truth maintenance and canonical records
- audit and traceability
- governance preview
- action level and approval lane
- evidence capture through `remember(..., related_to=[entry_turn_id])` or
  governed canonical write

For `software_change`, `menmery` does not:

- checkout repositories
- run shell commands
- mutate code
- run build/test/security scans
- merge PRs
- deploy
- replace the external execution harness

The external harness owns isolated worktree/sandbox mutation, build, test,
security scan, artifact digests, and runner facts. Those facts are then written
back to `menmery` as observation or review evidence. Runner logs alone are not
durable evidence.

---

## 27.4 auto_router Boundary

`auto_router` is `llm-gateway`: a stable, explainable, learnable LLM routing
control plane with guardrails and semi-automatic optimization.

It provides:

- request routing to LLM backends by tenant, task, difficulty, quality, and cost
- a runtime execution boundary in `internal/runtime/planner.go`
- model eligibility, failover, and escalation inside that boundary
- runtime / guard / feedback / audit events
- learner-lite reports and gated low-risk updates
- runtime overlay updates for `quality_priors`, `routing_policies`, and
  `active_pool`

It does not aim to be:

- a zero-config black-box router
- a system that auto-learns and auto-publishes all policies
- an approval-free owner of high-risk routing rules

High-risk routing controls such as `block`, `force_model`, provider/backend
boundaries, tenant/auth boundaries, and security hard rules remain manually
configured or explicitly approved in `auto_router`.

For `dev_master`, this means:

- call `auto_router` for LLM execution when routed model choice is needed
- pass useful task/tenant/risk metadata when the interface supports it
- feed back quality and outcome signals when available
- do not reimplement routing, runtime planner, fallback, cost optimization, or
  learner publishing inside `dev_master`
- any future `dev_master` model-governance design must coordinate with
  `auto_router` rather than duplicate its routing control plane

---

## 27.5 Integration Rules

| Need | Correct owner / integration |
|------|-----------------------------|
| durable personal/project context | `menmery` |
| canonical evidence / audit / action lane | `menmery` |
| repo mutation, build, test, scan | `dev_master` external harness / worker |
| runner facts and verifier expectations | `dev_master` |
| LLM backend selection and failover | `auto_router` |
| routing feedback and learner artifacts | `auto_router` |
| product-level delivery governance | `dev_master`, mapped to `menmery` when available |
| product-level model requirements | `dev_master`, coordinated with `auto_router` |

---

## 27.6 Incorrect Readings

Do not write or imply:

- `dev_master` is a `menmery` harness only.
- `menmery` owns repo mutation or software delivery implementation.
- `dev_master` can ignore `menmery` when long-term context, evidence, or
  governed action is needed.
- `auto_router` is only a thin API wrapper.
- `dev_master` should implement its own model router because it has model
  governance in the roadmap.
- Old recovered design text overrides current sibling-system boundaries.

The correct reading is: `dev_master` owns the AI development pipeline product;
`menmery` supplies cognitive truth/governance/evidence integration;
`auto_router` supplies the LLM routing control plane.
