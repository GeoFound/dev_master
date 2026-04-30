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

Product scope must not be read as a promise of fully unattended production
autonomy. The current strategic target is a 24/7 `L1` prototype / bounded
artifact factory plus an `L2` semi-automatic product assistant. `L2` production
work may be prepared by AI, but account, payment, multi-tenant, security,
release, and business decisions remain human-governed. Fully autonomous `L2`
or `L3` delivery is outside the current capability boundary.

`dev_master` is the control plane for scheduling, authorization, governance,
evidence, cost, review state, and autonomy changes. Codex, Claude Code, API
models, `auto_router`, and future agent systems are worker providers or
integrations. They may propose and execute work only through the governed
handoff in [task-proposal-contract.md](../10-product/task-proposal-contract.md).

The recovered v3 source has been removed from active docs. Durable mined ideas
are tracked at
[durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md).

---

## Current Implementation Window

Current active implementation is limited to the next gates:

1. Phase 0: cold start and design recovery
2. Phase 1: first executable kernel
3. Phase 2: green reliability
4. Phase 3: yellow preparation
5. Phase 4: repo-local operational validation

This window constrains implementation work. It does not constrain product
identity.

---

## Active Core

Active files constrain the current window:

- [00-index.md](../00-entry/00-index.md)
- [02-tools-cost.md](../10-product/02-tools-cost.md)
- [03-ai-roles.md](../10-product/03-ai-roles.md)
- [04-pipeline.md](../10-product/04-pipeline.md)
- [05-quality.md](../10-product/05-quality.md)
- [06b-state-persistence.md](06b-state-persistence.md)
- [07-governance.md](../10-product/07-governance.md)
- [08-repo-structure.md](../90-reference/08-repo-structure.md)
- [09-roadmap.md](../10-product/09-roadmap.md)
- [product-architecture-decision.md](../10-product/product-architecture-decision.md)
- [task-proposal-contract.md](../10-product/task-proposal-contract.md)
- [13-appendix.md](../90-reference/13-appendix.md)
- [14-master-program.md](14-master-program.md)
- [15-phase-gates.md](15-phase-gates.md)
- [16-drift-control.md](16-drift-control.md)
- [17-task-templates.md](17-task-templates.md)
- [18-master-execution-task.md](18-master-execution-task.md)
- [19-human-governance-boundary.md](19-human-governance-boundary.md)
- [21-agent-behavior-guidelines.md](21-agent-behavior-guidelines.md)
- [22-three-plane-architecture.md](22-three-plane-architecture.md)
- [autonomy-ratchet.md](autonomy-ratchet.md)
- [human-review-inbox.md](human-review-inbox.md)
- [cost-ceilings.md](cost-ceilings.md)
- [23-menmery-integration.md](../30-integrations/23-menmery-integration.md)
- [24-ai-cold-start.md](../00-entry/24-ai-cold-start.md)
- [25-implementation-language-baseline.md](25-implementation-language-baseline.md)
- [26-design-closure-review.md](../00-entry/26-design-closure-review.md)
- [27-external-systems-boundary.md](../30-integrations/27-external-systems-boundary.md)
- [28-product-principles.md](../10-product/28-product-principles.md)
- [AGENTS.md](../../AGENTS.md)

Active repository AI base:

- [26-design-closure-review.md](../00-entry/26-design-closure-review.md)
- [durable-ideas-from-v3.md](../90-reference/durable-ideas-from-v3.md) as mapped historical idea index
- root design/system specification docs

Implementation scaffolding was intentionally removed on 2026-04-27. Runner,
verifier, contracts, task pointers, reports, templates, and scripts must be
regenerated from the active blueprint and current gate program. Their absence
means "rebuild from authority", not "stop at documentation".

---

## Deferred Runtime, Not Deferred Product

These files describe product capabilities that are not current runtime tasks:

- [06-observability.md](../10-product/06-observability.md)
- [09b-adaptation-selftest.md](../40-future/09b-adaptation-selftest.md)
- [10-ops-ai.md](../40-future/10-ops-ai.md)
- [11-advisor-ai.md](../40-future/11-advisor-ai.md)
- [12-disaster-recovery.md](../40-future/12-disaster-recovery.md)

Archive/deferred status means "not activated as runtime in the current window".
It must not be read as "outside dev_master".

---

## External Dependencies

- `menmery`: long-term cognitive infrastructure providing context,
  governance/action preview, audit, and evidence capture when that service is
  used.
- `auto_router`: LLM routing control plane providing runtime planner,
  model execution boundary, failover, feedback, learner reports, and guarded
  low-risk routing optimization when routed execution is chosen.
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

Do not activate these as current runtime work without a new human decision:

- fully autonomous `L2` SaaS/product delivery
- `L3` high-compliance or high-integration automation
- autonomous product, pricing, market, or release judgment without human review

Do not shrink the product roadmap to satisfy a current-window gate.
