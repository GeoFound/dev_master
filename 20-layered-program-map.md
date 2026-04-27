# Layered Program Map

---

## Active Core

Active files constrain Phase 0-3 work:

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
- [AGENTS.md](AGENTS.md)

Active repository AI base:

- [tasks/current.md](tasks/current.md)
- [tasks/backlog.md](tasks/backlog.md)
- [contracts/software-change-runner-v1.yaml](contracts/software-change-runner-v1.yaml)
- [templates/](templates/)
- [reports/](reports/)
- [scripts/check_ai_base.sh](scripts/check_ai_base.sh)

---

## Deferred / Future Archive

These are not active constraints:

- [archive/deferred/06-observability.md](archive/deferred/06-observability.md)
- [archive/deferred/09b-adaptation-selftest.md](archive/deferred/09b-adaptation-selftest.md)
- [archive/deferred/10-ops-ai.md](archive/deferred/10-ops-ai.md)
- [archive/deferred/11-advisor-ai.md](archive/deferred/11-advisor-ai.md)
- [archive/deferred/12-disaster-recovery.md](archive/deferred/12-disaster-recovery.md)

---

## Current Build Program

Only Phase 0-3 exist:

1. Phase 0: design freeze
2. Phase 1: first executable kernel
3. Phase 2: green reliability
4. Phase 3: yellow preparation

Hard boundaries:

- `menmery` owns truth/governance/evidence.
- `auto_router` owns LLM routing/model governance.
- `dev_master` owns runner contract and software-change evidence facts.
- `dev_master` owns repository-level AI cold-start scaffolding for this harness.
- Phase 1 `dev_master` runner / harness / verifier defaults to Python; `just`
  and Bash are command wrappers, not complex runtime logic.
- No parallel canonical store, approval controller, or highest policy schema.
- No standing nine-agent system.
- No active Ops/Advisor/TechRadar/rewrite/model governance/adapters.

---

## Activation Rule

Anything outside Phase 0-3 requires an activation proposal with evidence that the current kernel has encountered a real gap.
