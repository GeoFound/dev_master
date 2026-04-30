---
status: active
scope: product
authority: this
---

# Engineering Execution Boundaries

This file defines implementation-time boundaries for AI coding work. It is not
a static "AI cannot help" list. It separates responsibility red lines from
guardrails that may relax as evidence improves.

Core rule:

```text
AI capability growth may reduce friction and widen bounded execution.
It must not move responsibility for hard safety, money, secrets, production, or
distributed-foundation correctness away from governed human/system owners.
```

This file is interpreted with [autonomy-ratchet.md](../20-current-window/autonomy-ratchet.md),
[07-governance.md](07-governance.md), [cost-ceilings.md](../20-current-window/cost-ceilings.md),
[human-review-inbox.md](../20-current-window/human-review-inbox.md),
[product-architecture-decision.md](product-architecture-decision.md), and
[task-proposal-contract.md](task-proposal-contract.md).

---

## 1. Boundary Record Shape

Implementation boundaries should be expressible as:

```yaml
boundary_id: "auth.oauth2"
boundary_type: "hard_red_line|mature_library_only|ratchetable_guardrail|quality_floor"
ratchet_behavior: "never_relax|reduce_human_friction_only|relax_by_metrics|raise_only"
owner: "human|verifier|ratchet|external_service"
allowed_ai_work:
  - "design"
  - "analysis"
  - "adapter_integration"
forbidden_ai_work:
  - "from_scratch_core_implementation"
evidence_required:
  - "tests"
  - "verifier_decision"
```

Verifier and review tools should classify implementation work using this model
instead of treating the whole policy as one fixed block.

---

## 2. Hard Red Lines

`boundary_type: hard_red_line`
`ratchet_behavior: never_relax`

AI must not autonomously implement, merge, deploy, or approve:

- cryptographic algorithms, signing / verification cores, secure random
  generation, password hashing, token validation cores
- payment gateways, tax, invoice, fraud, or settlement cores
- production deploy, protected-branch merge, public release, canary promotion,
  or rollback execution
- secrets, credentials, permissions, tenant isolation, authz boundary changes
- destructive database or storage operations such as `DROP`, `TRUNCATE`,
  production data deletion, or irreversible cleanup
- distributed consensus, CRDT / OT cores, distributed lock algorithms, queue
  engines, or storage consistency protocols
- unrestricted natural-language-to-shell, natural-language-to-SQL, or
  production operations agents
- changes to [autonomy-ratchet.md](../20-current-window/autonomy-ratchet.md)
  thresholds, hard red lines, tier rules, or metric windows

Allowed AI work on hard red lines:

- explain risk
- design a human-owned plan
- compare mature services or libraries
- write adapters only after the human/system owner selects the service
- write mocks, tests, monitoring, and review payloads

---

## 3. Mature-Library-Only Boundaries

`boundary_type: mature_library_only`
`ratchet_behavior: reduce_human_friction_only`

For these areas, capability growth may reduce approval friction for adapters,
configuration, tests, and PR drafts. It must not allow from-scratch core
implementation.

| Area | Use mature library/service | AI may do |
|------|----------------------------|-----------|
| Auth / OIDC / MFA | Auth0, Clerk, Supabase Auth, provider SDKs | flow design, config advice, adapter, tests |
| RBAC / ABAC / FGA | Ory Keto, Casbin, Auth0 FGA, OPA where appropriate | role matrix, policy modeling, integration |
| Payments / billing | Stripe, Paddle, official SDKs | checkout/subscription adapter, idempotency, mocks |
| KMS / secrets / DLP / audit | AWS KMS, Vault, Macie, CloudTrail, equivalent services | field classification, retention, integration tests |
| Queue / scheduler / lock / cache | Kafka, RabbitMQ, SQS, BullMQ, Temporal, Celery, Redis, etcd | event schema, retry, DLQ, adapter |
| Search / vector / realtime / collaboration | Elasticsearch, Typesense, Qdrant, pgvector, Socket.io, Yjs, Liveblocks | index schema, channel model, integration |
| Media / documents / OCR / email | FFmpeg, Mux, Sharp, Cloudinary, Textract, SendGrid, SES | pipeline design, templates, queues |
| AI guardrails / RAG eval / model cost | LLM Guard, NeMo Guardrails, Ragas, TruLens, LangSmith, Helicone, Portkey | policy, eval sets, adapters |
| DB migration / ORM / observability / CI | Alembic, Prisma, SQLAlchemy, OpenTelemetry, Sentry, Prometheus, GitHub Actions | schema plan, non-destructive migration, dashboards |

Using a service or library from this table still requires approval from the
active phase and gate. For example, Temporal is the correct class of tool for
durable workflow when that capability is activated, but this table does not
authorize adding Temporal in Phase 1.

Friction may ratchet down like this:

```text
design only
-> adapter draft with mocks
-> adapter PR draft with verifier report
-> green auto-run for preapproved adapter updates
```

It may not ratchet into from-scratch auth, payment, crypto, distributed
foundation, or production-operation cores.

---

## 4. Provider And Workspace Boundaries

`boundary_type: ratchetable_guardrail`
`ratchet_behavior: reduce_human_friction_only`

Provider adapters may wrap Codex, Claude Code, API models, `auto_router`, or
other approved execution providers. They must not become governance owners.

Rules:

- `dev_master` is the only dispatch and authorization owner for governed work
- API-backed providers are the default worker path for Phase 1-2
- subscription-tied CLI/SDK providers are Phase 2+ cost-reduction options, not
  the default path
- subscription-tied providers require current terms/docs review before
  headless or automated use
- all provider adapters must capture raw output digest/ref, parsed output,
  adapter version, parse schema version, and drift status
- provider drift fails closed: it may hold or request change, but may not
  authorize dispatch, approval, release, or ratchet widening
- direct Codex, Claude Code, API, or IDE-agent calls that bypass `devmasterd`
  do not produce admissible evidence for governed work

Provider-output evidence shape is defined in
[product-architecture-decision.md](product-architecture-decision.md).

---

## 5. Ratchetable Guardrails

`boundary_type: ratchetable_guardrail`
`ratchet_behavior: relax_by_metrics`

These may widen only through append-only ratchet evidence:

| Guardrail | Earliest tier | Notes |
|-----------|---------------|-------|
| bounded slice file count and line count | `L1` | local bounded artifact work |
| unattended run duration | `L1` | limited by verifier/evidence checkpoints |
| green queue parallelism | `L1.5` | requires async inbox and cost ceilings |
| number of projects in the queue | `L1.5` | queue expansion only, not autonomy expansion |
| automatic integration of mature-library adapters in non-production paths | `L1.5` | mature-library-only cores remain forbidden |
| automatic generation of draft PRs | `L2-assisted` | draft only; no merge or protected-branch action |
| automatic generation of deploy-preview payloads | `L2-assisted` | preview-only; no production deploy or promotion |

Preview rule:

- AI may design and prepare deploy-preview payloads when the active phase allows
  it.
- Preview payloads must not imply production deploy, canary promotion, or merge.
- Preview work must flow through async review when human approval is required.

---

## 6. Algorithms

`boundary_type: quality_floor` for allowed algorithms.
`boundary_type: hard_red_line` for forbidden foundations.

Allowed from-scratch, with tests and complexity notes:

- sorting, searching, basic data structures
- BFS / DFS / Dijkstra / topological sort / MST
- bounded dynamic programming
- bounded recursion / backtracking with explicit depth, node, or timeout limits
- non-critical recommendation or ranking logic
- small offline statistical algorithms

Allowed only with strict review:

- Tarjan / Kosaraju SCC
- bipartite matching, max flow, or fuzz-tested graph algorithms in non-money,
  non-security paths
- low-level locks or mutexes, only with deadlock and exception-release analysis

Strict review owner:

```yaml
strict_review_owner: "human|semantic_verifier"
```

Use `semantic_verifier` only after Gate C has benchmarked it for the relevant
class of risk. Before that, strict review means human review.

Must use mature libraries or services:

- cryptography, password hashing, JWT validation
- distributed consensus, CRDT / OT, queue engines, distributed locks
- neural network / transformer / training internals
- large-scale graph/community algorithms
- codec, real-time scheduling, or congestion-control algorithms

Algorithm implementations must include:

- correctness tests
- boundary tests
- large-input or performance tests when the code can run on large data
- documented time and space complexity
- statement whether the function is suitable for online request paths

---

## 7. Quality Floors

`boundary_type: quality_floor`
`ratchet_behavior: raise_only`

AI-delivered code is not acceptable without:

- tests for business logic and edge cases
- mocks/stubs for external services
- explicit error handling for external calls
- no hardcoded secrets
- no SQL string concatenation from user input
- input validation at API and tool boundaries
- no obvious N+1 queries or repeated expensive work inside hot loops
- coverage target: 80% overall, 90% for critical paths where measurable

If coverage cannot be measured in the current slice, the reason must be
recorded in evidence.

---

## 8. Refusal Pattern

When asked to implement a forbidden core, AI should respond with:

```text
This belongs to a hard red line or mature-library-only boundary.
Use a mature library or service from the Section 3 table, or an explicitly
approved alternative.
I can help with design, comparison, adapter integration, tests, monitoring, and
review payloads.
```

The same boundary should be represented in runner facts so verifier can block
forbidden from-scratch implementation.
