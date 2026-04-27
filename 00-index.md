# dev_master · software_change reference harness

> v4.3 定位：`dev_master` 是 `menmery` 之上的 `software_change` capability / reference harness。它不自建 truth、canonical evidence、approval controller 或模型路由。它只定义软件变更如何被计划、隔离执行、验证，并把事实回写到 `menmery`。

---

## 1. 当前结论

三个项目边界：

| 项目 | 独立职责 | dev_master 不得做的事 |
|------|----------|------------------------|
| `menmery` | truth maintenance、canonical records、audit、governance preview、action level | 不 import dev_master runner，不执行 repo mutation |
| `auto_router` | LLM routing、model selection、cost/failover/model governance | dev_master 不做模型分类与治理 |
| `dev_master` | software-change protocol、runner contract、risk facts、verification harness | 不自建 canonical/governance runtime |

三平面仍保留，但只是 `software_change` capability 内部的执行纪律：

```text
menmery governance/evidence
  -> orchestration reference
  -> isolated execution worker
  -> verifier/risk facts
  -> remember / canonical evidence回写
```

---

## 2. Active Core

| 文件 | 作用 |
|------|------|
| [24-ai-cold-start.md](24-ai-cold-start.md) | AI 冷启动入口、当前任务、证据与检查命令 |
| [tasks/current.md](tasks/current.md) | 当前 phase / gate / task 指针 |
| [20-layered-program-map.md](20-layered-program-map.md) | 当前 active/deferred/future 分层 |
| [23-menmery-integration.md](23-menmery-integration.md) | dev_master 与 menmery 的 capability 映射 |
| [22-three-plane-architecture.md](22-three-plane-architecture.md) | software_change 内部三平面边界 |
| [03-ai-roles.md](03-ai-roles.md) | 三角色模型 |
| [04-pipeline.md](04-pipeline.md) | Phase 1 最小流水线 |
| [05-quality.md](05-quality.md) | Result Gate / Verifier / runner evidence |
| [07-governance.md](07-governance.md) | action level 与软件风险标签 |
| [09-roadmap.md](09-roadmap.md) | Phase 0-3 路线图 |
| [14-master-program.md](14-master-program.md) | 主推进程序 |
| [15-phase-gates.md](15-phase-gates.md) | Gate A-D |
| [17-task-templates.md](17-task-templates.md) | task 模板 |
| [18-master-execution-task.md](18-master-execution-task.md) | AI 执行入口 |
| [21-agent-behavior-guidelines.md](21-agent-behavior-guidelines.md) | 行为纪律 |
| [AGENTS.md](AGENTS.md) | 新会话硬边界 |

Repository AI base：

| 路径 | 作用 |
|------|------|
| [tasks/backlog.md](tasks/backlog.md) | 非授权任务队列，只能在 gate 允许后取用 |
| [contracts/software-change-runner-v1.yaml](contracts/software-change-runner-v1.yaml) | runner facts v1 合同参考 |
| [templates/](templates/) | build / verify / drift / gate / activation / runner facts 模板 |
| [reports/](reports/) | 本地 gate / drift fallback evidence |
| [scripts/check_ai_base.sh](scripts/check_ai_base.sh) | 仓库 AI 基座检查 |

Archived blueprint：

| 原文件 | 新位置 | 状态 |
|--------|--------|------|
| `10-ops-ai.md` | [archive/deferred/10-ops-ai.md](archive/deferred/10-ops-ai.md) | deferred |
| `11-advisor-ai.md` | [archive/deferred/11-advisor-ai.md](archive/deferred/11-advisor-ai.md) | deferred |
| `12-disaster-recovery.md` | [archive/deferred/12-disaster-recovery.md](archive/deferred/12-disaster-recovery.md) | future |

---

## 3. First Operational Version

第一版只证明一件事：

```text
menmery get_context
-> menmery act(intent="software_change", details=...)
-> isolated runner prepares local diff / test facts
-> verifier checks requested change vs diff vs tests vs risk facts
-> remember(...) captures evidence back into menmery
```

Phase 1 不包括：

- Ops AI / Advisor AI / TechRadar
- rewrite / model governance / adapter platform
- Temporal production cluster
- OPA as highest authority
- DSSE/cosign/Tekton/GUAC rollout
- any parallel canonical store or approval controller

---

## 4. Minimal Artifact Contract

Runner facts only need one local version field:

```yaml
runner_contract_version: "software-change-runner-v1"
trace_id: "stable change id"
menmery_context_ref: "record/inbox/audit id or context query"
requested_change: "bounded goal"
repo_ref: "repo + branch/ref"
diff_digest: "sha256:..."
checks:
  lint: "pass|fail|not_run"
  tests: "pass|fail|not_run"
  security: "pass|fail|not_run"
risk_facts:
  action_level: "0|1|2|3|4"
  risk_label: "green|yellow|red"
evidence_writeback:
  method: "remember|canonical_write"
  id: "menmery evidence id"
```

Schema and governance versions are not dev_master Phase 1 authority. Schema and governance belong to `menmery`; dev_master only maintains the runner contract.

---

## 5. Rule Of Thumb

如果一个设计问题听起来像 truth、memory、approval、governance、long-term state，先问 `menmery`。

如果它听起来像 model routing、model selection、cost/failover，问 `auto_router`。

如果它听起来像 repo mutation、diff、tests、security facts、runner isolation，才属于 `dev_master`。
