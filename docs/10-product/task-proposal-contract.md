---
status: active
scope: product
authority: this
---

# Task Proposal Contract

This contract turns "AI proposes, dev_master authorizes" into a machine-checkable
handoff. Planner agents, humans, issue integrations, IDE clients, and provider
workers may propose tasks. Only `dev_master` may authorize dispatch.

This file is interpreted with [product-architecture-decision.md](product-architecture-decision.md),
[engineering-execution-boundaries.md](engineering-execution-boundaries.md),
[../20-current-window/autonomy-ratchet.md](../20-current-window/autonomy-ratchet.md),
and [../20-current-window/cost-ceilings.md](../20-current-window/cost-ceilings.md).

---

## 1. Proposal Shape

```yaml
task_proposal:
  schema_version: "1.0.0"
  proposal_id: "prop_..."
  trace_id: "tr_..."
  proposer: "human|codex|claude_code|api_agent|integration"
  source_ref:
    type: "manual|issue|ide|inbox|scheduled"
    uri: null
  goal: "bounded objective"
  slices:
    - slice_id: "slice_..."
      bounded_scope:
        repos: ["repo-name"]
        files: ["path/or/glob"]
        lines_max: 300
        forbidden_paths: []
      expected_diff_size_lines: 120
      expected_cost_usd: 0.15
      proposed_provider: "openai_api|anthropic_api|auto_router|codex_cli|claude_code_cli"
      provider_kind: "api|subscription_cli|subscription_sdk|local_tool"
      risk_label_estimate: "green|yellow|red"
      required_checks: ["tests", "lint"]
      expected_artifacts: ["diff", "runner_facts", "verifier_report"]
  rationale: "why this slice should run"
```

The proposal is not an approval. It is input to the authorization check.

---

## 2. Authorization Shape

```yaml
dev_master_decision:
  schema_version: "1.0.0"
  proposal_id: "prop_..."
  decision_id: "dec_..."
  decided_by: "dev_master"
  decision: "authorize|reject|request_change"
  reasons: []
  authorized_slices: ["slice_..."]
  rejected_slices: []
  checks:
    active_phase_check_passed: true
    ratchet_check_passed: true
    cost_check_passed: true
    boundary_check_passed: true
    provider_check_passed: true
  required_human_review: false
  evidence_refs: []
```

Only an `authorize` decision may create worker dispatch. A planner agent,
provider worker, or IDE client must not bypass this decision object.

---

## 3. Required Validator Checks

The `dev_master` proposal validator must check:

- active phase allows the requested surface, repo, provider kind, and side
  effects
- ratchet bounds allow the requested slice size, unattended duration, queue
  width, and autonomy tier
- cost ceilings allow the expected spend
- engineering boundaries allow the implementation class
- provider path is allowed for the phase
- subscription-tied provider has drift detection and raw-output capture before
  its output is admissible
- each authorized slice has a bounded scope, required checks, and expected
  evidence artifacts

Fail closed:

- missing cost estimate -> reject or request change
- missing bounded scope -> reject
- unknown provider -> reject
- provider drift -> hold
- yellow/red risk -> route to human review unless an active gate explicitly
  permits the requested behavior

---

## 4. Phase 1 Defaults

For Phase 1:

- default `provider_kind` is `api`
- subscription CLI/SDK providers are not required and cannot be the only worker
  path for Phase 1B
- no external repo mutation, deploy, PR, merge, paid service side effect, or
  production side effect is allowed
- CLI is the only product surface required for Phase 1B

