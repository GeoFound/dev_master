---
status: active
scope: product
authority: this
---

# Product Principles

> Current product principles for `dev_master`. These principles preserve durable
> ideas from older design discussions, but they are current only because they
> are restated here and reconciled with `27-external-systems-boundary.md`.

---

## 28.1 North Star

`dev_master` exists to make AI a governed software-delivery operator:

- AI should do the day-to-day development work.
- Humans should set goals, define boundaries, approve high-risk decisions, and
  correct strategy.
- Evidence, gates, and rollback paths decide whether autonomy is safe.

This is not a `menmery` subproject and not a model-router project. `menmery`
and `auto_router` are sibling systems that `dev_master` integrates with.

---

## 28.2 Result Over Ritual

The pipeline should judge work by verified results, not by whether every
historical role ran as a separate process.

A result is not acceptable unless it has:

- bounded request
- exact diff or artifact reference
- tests / lint / security facts
- risk facts
- evidence writeback path
- verifier decision
- rollback or correction path

Process can be compressed. Evidence cannot.

---

## 28.3 Contracts Are Agent Interfaces

AI roles must communicate through contracts and facts, not vague prose.

Relevant contract surfaces include:

- requirements and acceptance criteria
- spec / test / security expectations
- runner facts
- diff and artifact digests
- risk facts
- evidence references
- release and rollback status

The minimum machine-readable discipline is the contract triplet:

- `schema_version`
- `policy_version`
- `ruleset_version`

When implementation is rebuilt, contracts should be machine-checkable where
reasonable. Markdown can explain intent, but the runner/verifier path needs
structured facts. `CONTRACTS.md` is the authority for this layer.

---

## 28.4 Boundaries Beat Micromanagement

Human review should focus on boundaries and decisions, not every line of
ordinary work.

Humans own:

- goal freeze
- red-zone approval
- boundary changes
- promote / hold / correct / rollback decisions
- autonomy expansion

AI owns:

- collecting evidence
- challenging gaps
- generating implementation and tests
- preparing decision recommendations
- surfacing drift and risk

If AI hands humans raw uncertainty without a recommendation, it has not done
its job.

---

## 28.5 Vertical Slices Are Authorization Boundaries

Vertical slices are not only a context-window convenience. They are authorization
boundaries.

Each execution worker should have:

- explicit scope
- allowed files or modules
- forbidden side effects
- expected checks
- rollback path

Cross-slice edits, hidden dependency changes, or opportunistic refactors should
be verifier-blocking unless explicitly approved.

---

## 28.6 Proactive Sensing Is Product Scope

Ops AI, Advisor AI, and TechRadar are part of the product direction. They are
not active runtime after the reset, but they must not be erased.

Their durable purpose:

- detect operational degradation before it becomes an incident
- notice external ecosystem changes
- turn findings into evidence-backed proposals
- preserve human approval for high-risk action

Activation requires evidence, bounded first slice, cost policy, and human gate.

---

## 28.7 Cost And Routing Discipline

LLM usage is a product cost and quality concern, but `dev_master` must not
rebuild the routing control plane.

`auto_router` owns:

- model routing
- runtime planner
- failover and escalation
- routing feedback and learner artifacts
- low-risk routing optimization

`dev_master` owns:

- stage-level model requirements
- quality/evidence expectations for pipeline work
- feedback it sends back to `auto_router`
- local degradation behavior when the gateway is unavailable

---

## 28.8 Cognitive Governance Discipline

Long-term context, evidence, and governed action should use `menmery` when
available.

`menmery` owns:

- cognitive truth maintenance
- canonical records
- audit
- governance preview
- action level and approval lane
- evidence capture

`dev_master` owns:

- repo mutation harness expectations
- runner facts
- verifier policy
- software-delivery product decisions

No runner log is final evidence by itself.

---

## 28.9 Rewrite And Recovery Are First-Class

A long-lived AI development pipeline must treat rewrite, migration, rollback,
and knowledge transfer as governed product capabilities, not emergency
afterthoughts.

Future rewrite work must include:

- proposal and reason
- capability matrix
- migration waves
- rollback rehearsal
- retirement gates
- knowledge transfer record
- audit trail

Rewrite Controller is future runtime, not current implementation permission.
