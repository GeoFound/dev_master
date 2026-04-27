# menmery 集成定位：software_change capability

> **分层状态：Active Core。** 本文件是 v4.2 架构校正：`dev_master` 不是与 `menmery` 平级的新 truth / governance / evidence 系统，而是 `menmery` 之上的软件变更领域 capability / harness。

---

## 23.1 核心结论

`menmery` 已经承担以下稳定职责：

| 职责 | menmery 已有语义 |
|------|------------------|
| truth maintenance | claim -> observation -> inference -> truth |
| canonical evidence | canonical records + inbox + supersede |
| audit trail | runtime audit / governance audit |
| governance | governance preview + action level 0-4 |
| caller contract | `remember` / `get_context` / `act` / `follow_recommended_call` |
| semantic boundaries | Observation vs Inference、Canonical vs Derived、Policy vs Strategy、Analysis vs Agency |

因此 `dev_master` 的正确边界是：

```text
menmery
  owns: truth, canonical records, audit, governance preview, action levels

dev_master
  owns: software-change capability contract, worker isolation, repo mutation protocol,
        verifier evidence, risk facts, execution result packaging
```

`dev_master` 可以是 harness，但不是新的认知核心。它负责把“软件变更”这类行动变成可治理、可追溯、可验证的 capability。

---

## 23.2 与三平面的关系

[22-three-plane-architecture.md](22-three-plane-architecture.md) 仍然有效，但它描述的是 `software_change` capability 内部的工程边界，不再表示 `dev_master` 要自建完整 runtime。

| 三平面概念 | v4.2 默认实现 |
|------------|---------------|
| Orchestration Plane | `menmery act(...)` + governance preview + action level；必要时再接 Temporal 自托管 |
| Execution Plane | 隔离 worktree / sandbox / container 中的 Claude Code、Codex CLI、OpenAI sandbox worker |
| Evidence Plane | `menmery` canonical records、inbox、supersede、audit；artifact digest 可由 dev_master runner 产生 |
| Policy Boundary | `menmery` governance/action level 是最高治理入口；OPA/Conftest 只能作为软件变更领域的 facts evaluator |

Temporal、OPA、DSSE、cosign、Tekton Chains、GUAC 都可以保留为后续工具选项，但不得在 Phase 1 作为替代 `menmery` truth/governance/evidence 的新核心。

---

## 23.3 最小端到端流程

Phase 1 的最小闭环应改为：

```text
1. caller 先 get_context("software_change / dev_master / target repo")
2. caller 调 act(intent="software_change", details=...)
3. menmery 返回 governance preview、recommended_call、action level / approval lane
4. 若 lane 允许，dev_master execution worker 在隔离 worktree 中执行
5. worker 只产出 diff、test result、security facts、artifact digest、risk facts
6. caller 通过 remember(...) 或受控 canonical write 把结果作为 observation / review evidence 回写 menmery
7. 最终 approval 绑定到固定 evidence snapshot / canonical record IDs
```

关键点：

- AI session 不是常驻进程；长期状态由 `menmery` 维护。
- execution worker 可以产生事实，不能决定最终批准。
- approval 必须记录“谁在什么 policy / action level / evidence snapshot 下批准”。
- 如果某步无法通过 `menmery` facade 表达，先记录为 capability gap，不直接扩张 dev_master runtime。

---

## 23.4 action level 映射

| 软件变更动作 | 默认 action level | 说明 |
|--------------|-------------------|------|
| 读文档、读代码、生成分析 | 0 | Pure Analysis |
| 只读扫描、依赖查询、CI 状态读取 | 1 | Verification |
| 本地 worktree 生成 diff、测试、创建草稿 PR | 2 | Reversible Operation |
| 写外部 issue、发通知、提交 PR、低风险配置写入 | 3 | Controlled External Effect |
| 合并、部署、删除、迁移、支付、权限变更 | 4 | Irreversible / High-Stakes |

`dev_master` 的红黄绿区只作为软件领域的便捷标签。最终治理必须映射到 `menmery` action level 与 approval lane，不能另起一套更高优先级的风险系统。

---

## 23.5 Active Core 调整

当前 build program 的优先级调整为：

1. Phase 0：冻结 `software_change` capability 的语义映射、runner 边界、menmery 调用路径。
2. Phase 1：用 `menmery` facade + 隔离 worker 跑通一条低风险软件变更。
3. Phase 2：补 Verifier、risk facts、green-zone 自动化样本。
4. Phase 3：再讨论黄区扩展与更强 orchestration。

Phase 1 不应优先建设：

- 新的 canonical/evidence 数据库
- 与 `menmery` 平行的 governance schema
- 独立 approval controller
- Temporal 生产化集群
- OPA 作为最高治理权威

这些只有在真实使用证明 `menmery` 当前 facade 无法表达软件变更长运行状态时，才进入 activation proposal。

---

## 23.6 menmery host 层风险

`menmery` 当前 runtime / host 层已经明显变重。`dev_master` 接入前必须承认这个上游风险：

- `src/menmery/runtime/host_reviews.py`、`host_facade_context.py`、`host_facade_adapters.py`、`scheduler.py` 等文件体量较大。
- 近期提交集中在 typing、extract、facade/refactor，说明 host 层正在进入治理成本上升期。
- `INTELLIGENCE_CORE.md` 3.6 明确禁止系统偏航成“只推进流程、不维护 truth object 的工作流引擎”。

约束：

- `dev_master` 不在本仓库内改写 `menmery` host 层。
- full integration 前，应把 host 层瘦身列为 `menmery` 上游前置任务。
- 在瘦身完成前，`dev_master` 只接最窄 facade：`get_context`、`act`、`remember`、`follow_recommended_call`。
- 不通过直接 import `menmery` 内部模块耦合实现，只通过 MCP / CLI / documented caller protocol 交互。

---

## 23.7 Repo 策略

默认 repo 边界：

- `menmery`：认知核心、治理、canonical truth、capability registry。
- `dev_master`：软件变更领域文档、runner contract、验证样例、隔离执行 harness。
- untrusted runner：可独立 repo，特别是需要独立权限、沙箱、语言栈或 release cadence 的执行 worker。

不建议把 `dev_master` 做成一个自包含平台仓库。更合理的长期结构是：

```text
menmery core repo
  capability registry: software_change

dev_master reference repo
  software_change protocol docs + runner contracts + tests/examples

runner repos
  codex-worker / claude-code-worker / sandbox-worker
```

---

## 23.8 不变量

1. `menmery` 是默认 truth / governance / evidence runtime。
2. `dev_master` 是 software-change harness，不是新认知核心。
3. 三平面是 execution discipline，不是要求重建三套基础设施。
4. Temporal 是长运行编排选项，不是 Phase 1 前置条件。
5. OPA/Conftest 可以生成软件领域 policy facts，但不得绕过 `menmery` action level。
6. 所有软件变更结果必须回到 observation / evidence / canonical path，而不是停留在 runner log。
