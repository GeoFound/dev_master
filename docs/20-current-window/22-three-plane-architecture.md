---
status: active
scope: product
authority: this
---

# 三平面架构：Orchestration / Execution / Evidence

> **分层状态：Active Core（蓝图层）。** 本文件定义 `dev_master` 产品在实现后必须遵守的系统边界。三平面是**执行纪律的设计目标**，不是已运行的运行时；当前仓库尚未重建三平面 runtime。本文件不表示 `dev_master` 要自建与 `menmery` 平行的 truth / governance / evidence runtime，也不表示 `dev_master` 是 `menmery` 的附属品。

---

## 22.1 核心结论

`dev_master` 是独立的 AI 自动化开发流水线产品，不应设计成一个把状态、代码执行、审批和审计都混在一起的单体 agent。正确结构是：

```text
menmery integration  ->  optional context、memory、audit、governance preview、evidence sink
auto_router          ->  optional LLM routing planner、model execution boundary、failover、routing feedback

Orchestration Plane  ->  只管长期状态、调度、重试、审批等待
Execution Plane      ->  只管隔离执行、仓库变更、测试、安全扫描
Evidence Plane       ->  只管不可变本地证据、签名、索引、追溯
```

任何模块必须先声明自己属于哪个平面。跨平面通信只能通过结构化 artifact、policy decision 和 immutable evidence reference 完成。若使用 `menmery`，本地 evidence reference 可以额外映射到 `menmery` record / inbox / audit ID。

---

## 22.2 Orchestration Plane

职责：
- 工作流状态
- stage 顺序
- retries / timers / compensation
- human approval wait state
- policy decision 调用
- evidence reference 记录

禁止：
- clone repo
- 运行 shell 命令
- 修改文件
- 直接合并 PR
- 存储大型产物
- 把模型输出当作最终审批结果

推荐实现：
- Phase 0-1：先建立本地 orchestrator/worker/verifier 核心；当任务需要长期上下文或治理预览时，再通过 `menmery` 公开服务面补充
- Temporal 自托管：保留为默认长运行编排目标，但只在 `menmery` facade 无法承载 wait/retry/resume 时引入
- Phase 2-3：若真实样本证明需要，再接入单环境自托管 Temporal，不提前引入 HA / Kubernetes 复杂度
- Temporal Cloud：仅作为后期备选，不作为当前默认

设计理由：
- Temporal 的 workflow model 适合长时间运行、崩溃恢复、timer、signal、人类审批等待和可重放状态。
- OpenAI / Codex / Claude / Agents SDK 应作为被调度的执行或分析能力，而不是长期状态的唯一来源。
- Temporal 只保存 workflow history、approval state、timer/retry state 和 evidence reference；大型 artifact、签名 envelope、完整日志、SBOM 等必须留在 evidence plane。若使用 `menmery`，相关 audit / governance refs 可作为附加索引，而不是唯一 evidence 入口。

---

## 22.3 Execution Plane

职责：
- repo checkout / worktree / sandbox
- Codex CLI、Claude Code、OpenAI Agents SDK sandbox 等执行入口
- build / test / lint / security scan
- 生成 diff、patch、PR draft
- 产生 structured facts
- 产出 artifact digest

禁止：
- 决定最终审批
- 自行放宽 policy
- 修改 orchestration state
- 写入不可回滚的生产状态，除非 orchestration plane 已授权

推荐实现：
- Phase 1：本地隔离 worktree / Docker sandbox
- 后续可选：Argo Workflows 或 Tekton Pipelines
- OpenAI Sandbox Agents 可作为执行 worker 的一种实现，但必须受 orchestration plane 调度

设计规则：
- execution plane 可以说“发生了什么”，不能说“因此可以合并”。
- 所有 side effecting step 必须有 idempotency key，并在执行后产生 evidence artifact。

---

## 22.4 Evidence Plane

职责：
- append-only audit records
- artifact metadata
- input / output digest
- policy decision snapshot
- approval decision snapshot
- signed provenance / attestation
- 可查询索引

禁止：
- 被 execution plane 覆写
- 存储未签名的最终放行证据
- 只依赖工作流日志作为长期审计证据

推荐实现：
- Phase 1：本地 append-only evidence index + runner artifact digest；若使用 `menmery`，再附加 canonical / audit refs
- Phase 2：DSSE envelope + in-toto statement + cosign signing
- 后续可选：Tekton Chains / SLSA provenance / GUAC metadata graph

证据记录必须至少包含：
- `trace_id`
- `run_id`
- `parent_run_id`
- `attempt`
- `step_id`
- `actor`
- `repo`
- `ref`
- `commit`
- `input_artifacts[]`
- `output_artifacts[]`
- `runner_contract_version`
- `governance_ref`
- `risk_facts`
- `approval_decision`
- `timestamps`

---

## 22.5 Policy Boundary

Policy 不属于任一 AI 角色，也不属于 execution worker。Phase 1 的最低治理入口是 `dev_master` 本地 gate 与 risk facts；`menmery` governance preview / action level 是可选的外部加严面；OPA/Conftest 只是后续可选的 facts evaluator，不得成为 Phase 1 权威。

推荐实现：
- Phase 1：先由本地 risk facts 与 gate 决定 allow / block / escalate；若使用 `menmery`，记录其 governance preview ref
- Phase 2+：如确有需要，再引入 OPA/Conftest 作为 facts evaluator，并映射到本地 gate 或外部治理 ref

Risk facts 最低格式：

```json
{
  "risk_class": "green | yellow | red",
  "action": "auto_approve | require_human_review | deny",
  "reasons": [],
  "required_approvals": [],
  "runner_contract_version": "software-change-runner-v2"
}
```

规则：
- risk classification 必须由 runner emitted facts + evidence 计算。
- agent 可以建议风险等级，但不得作为最终 risk classification。
- final approval = 本地 gate + policy facts + human gate（如需要）；若使用 `menmery`，其 governance/action level 只能加严，不能放宽。

---

## 22.6 Trace Model

统一追踪模型：
- `trace_id`：一次软件变更请求的稳定 ID
- `run_id`：一次 orchestration attempt
- `step_id`：workflow 内一个 activity / stage / worker job
- `artifact_id`：content-addressed artifact reference
- `evidence_id`：append-only evidence record ID

human approval 必须记录：
- `approver`
- `approved_at`
- `governance_ref`
- `evidence_snapshot`
- `decision`
- `reason`

审批后恢复同一个 workflow，不得启动一个无关联的新任务绕过原始 trace。

---

## 22.7 当前实现窗口的目标交付清单

> 当前仓库尚未交付这些 runtime。以下清单是 Phase 0-3 实现时**应当交付**的项目，不是已落地内容。

Phase 0-3 应当交付：
- `dev_master` 产品范围与当前实现窗口的边界（已写入文档层）
- `menmery` optional service-consumption 语义映射（已写入文档层）
- `auto_router` optional service-consumption 语义映射（已写入文档层）
- 三平面接口契约（设计层完成；实现尚未开始）
- orchestration workflow skeleton（实现待启动）
- execution worker contract（实现待启动）
- evidence envelope schema（实现时默认写入本地 append-only evidence，可选附加外部 refs）
- risk facts schema（实现时默认映射到本地 gate，可选附加外部 governance refs）
- 最小 runner artifact digest / evidence reference（实现待启动）
- 人工审批 wait/resume 协议（实现待启动）

Phase 0-3 不作为主任务交付：
- 与 `menmery` 平行的 canonical store / approval controller / governance schema
- Argo / Tekton 生产集群
- Tekton Chains 全量接入
- GUAC metadata graph
- active sensing / advisor / tech radar runtime
- 泛化 adapter 体系
- model governance rollout that duplicates `auto_router`
- rewrite controller

这些能力属于产品范围，但只能作为 research task 或 activation proposal 进入当前实现窗口。

---

## 22.8 参考来源

- Temporal docs: https://docs.temporal.io/
- Argo Workflows: https://argoproj.github.io/workflows/
- OPA docs: https://www.openpolicyagent.org/docs
- Conftest docs: https://www.conftest.dev/
- in-toto attestation envelope: https://github.com/in-toto/attestation/blob/main/spec/v1/envelope.md
- Tekton Chains: https://tekton.dev/docs/chains/config/
- GUAC docs: https://docs.guac.sh/guac/
- OpenAI Agents SDK: https://developers.openai.com/api/docs/guides/agents
- OpenAI Sandbox Agents: https://developers.openai.com/api/docs/guides/agents/sandboxes
