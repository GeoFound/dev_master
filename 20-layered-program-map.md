---
status: active
scope: window
authority: this
---

# Layered Program Map

---

## Product Scope

`dev_master` is an independent AI automation pipeline product. Product scope
includes:

- multi-agent software delivery
- specification, critique, implementation, testing, security, and review
- Result Gate and evidence-based approval
- release, canary, rollback, and operations feedback
- proactive Ops AI, Advisor AI, and TechRadar sensing
- project adapters
- model governance
- rewrite governance
- disaster recovery and knowledge transfer

The recovered v3 design is preserved as an outdated historical reference at
[recovered/AI-autonomous-dev-pipeline-v3.md](recovered/AI-autonomous-dev-pipeline-v3.md).
Use it to recover durable ideas, not as the current authority.

---

## Current Implementation Window

Current active implementation is limited to the next gates:

1. Phase 0: cold start and design recovery
2. Phase 1: first executable kernel
3. Phase 2: green reliability
4. Phase 3: yellow preparation

This window constrains implementation work. It does not constrain product
identity.

---

## Active Core

Active files constrain the current window:

- [00-index.md](00-index.md)
- [02-tools-cost.md](02-tools-cost.md)
- [03-ai-roles.md](03-ai-roles.md)
- [04-pipeline.md](04-pipeline.md)
- [05-quality.md](05-quality.md)
- [06b-state-persistence.md](06b-state-persistence.md)
- [07-governance.md](07-governance.md)
- [08-repo-structure.md](08-repo-structure.md)
- [09-roadmap.md](09-roadmap.md)
- [13-appendix.md](13-appendix.md)
- [14-master-program.md](14-master-program.md)
- [15-phase-gates.md](15-phase-gates.md)
- [16-drift-control.md](16-drift-control.md)
- [17-task-templates.md](17-task-templates.md)
- [18-master-execution-task.md](18-master-execution-task.md)
- [19-human-governance-boundary.md](19-human-governance-boundary.md)
- [21-agent-behavior-guidelines.md](21-agent-behavior-guidelines.md)
- [22-three-plane-architecture.md](22-three-plane-architecture.md)
- [23-menmery-integration.md](23-menmery-integration.md)
- [24-ai-cold-start.md](24-ai-cold-start.md)
- [25-implementation-language-baseline.md](25-implementation-language-baseline.md)
- [26-design-closure-review.md](26-design-closure-review.md)
- [27-external-systems-boundary.md](27-external-systems-boundary.md)
- [28-product-principles.md](28-product-principles.md)
- [AGENTS.md](AGENTS.md)

Active repository AI base:

- [26-design-closure-review.md](26-design-closure-review.md)
- [recovered/AI-autonomous-dev-pipeline-v3.md](recovered/AI-autonomous-dev-pipeline-v3.md) as stale reference only
- root design/system specification docs

Implementation scaffolding was intentionally removed on 2026-04-27. Runner,
verifier, contracts, task pointers, reports, templates, and scripts are design
references until a rewrite plan recreates them.

---

## Deferred Runtime, Not Deferred Product

These files describe product capabilities that are not current runtime tasks:

- [06-observability.md](06-observability.md)
- [09b-adaptation-selftest.md](09b-adaptation-selftest.md)
- [10-ops-ai.md](10-ops-ai.md)
- [11-advisor-ai.md](11-advisor-ai.md)
- [12-disaster-recovery.md](12-disaster-recovery.md)

Archive/deferred status means "not activated as runtime in the current window".
It must not be read as "outside dev_master".

---

## External Dependencies

- `menmery`: long-term cognitive infrastructure providing truth,
  governance/action preview, approval lane, audit, and evidence capture.
- `auto_router`: LLM routing control plane providing runtime planner,
  model execution boundary, failover, feedback, learner reports, and guarded
  low-risk routing optimization.
- execution workers: isolated repo mutation, tests, scans, runner facts.

None of these dependencies owns `dev_master` product identity.

---

## Activation Rule

To move a roadmap capability into active runtime, require:

- current-window evidence that the capability is needed
- bounded first slice
- human gate decision
- clear rollback path
- no silent expansion of autonomy

Do not shrink the product roadmap to satisfy a current-window gate.
