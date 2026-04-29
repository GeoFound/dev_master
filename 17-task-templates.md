---
status: active
scope: window
authority: this
---

# 標準 Task 模板

> 本文件把整個 program 拆成 AI 可直接執行的標準 task 類型。AI 不應自由發明 task 類型。

---

## 17.1 build-task

用途：
- 實現一個具體能力

固定字段：
- `trace_id`
- `goal`
- `plane`: `orchestration | execution | evidence | verification | docs`
- `scope_in`
- `scope_out`
- `dependencies`
- `deliverables`
- `acceptance_checks`
- `rollback_if_failed`
- `side_effects`: 聲明是否會修改 repo、執行 shell、調用外部服務或寫入 evidence
- `evidence_outputs`: 本 task 必須產生的 evidence record / artifact digest
- `evidence_inputs`: 本 task 依賴哪些既有 evidence / decision / digest
- `risk_facts`: 如需治理判斷，列出 runner facts 與 action level 映射
- `contract_requirements`: 若產生 machine-readable artifact，聲明 `artifact_family` 與版本要求
- `decision_records_required`: 哪些非平凡決策必須留下結構化 decision record
- `menmery_context`: 是否已調用 / 應調用 `entry_turn`、recommended call、`remember`

限制：
- 非純文檔 build-task 必須先聲明對應 `menmery` intent / action level / approval lane
- `orchestration` build-task 不得包含 repo mutation 或 shell execution
- `execution` build-task 不得包含 final approval decision
- `evidence` build-task 必須 append-only；當 `menmery` 可用時必須回寫 canonical / inbox / audit reference
- `docs` build-task 不得把 deferred / future 能力改寫為 active 承諾
- 不得用 build-task 自建與 `menmery` 平行的 canonical store、approval controller 或 governance schema
- 不得未經批准引入跨切片直接依賴、受保護不變量變更或未審核的新依賴
- 沒有 `trace_id` 或 `evidence_outputs` 的自動決策型 build-task 不合格

---

## 17.2 verify-task

用途：
- 驗證 build-task 是否符合設計

固定字段：
- `target_artifact`
- `expected_behavior`
- `check_method`
- `pass_conditions`
- `fail_conditions`
- `required_contracts`
- `required_evidence_refs`
- `schema_or_contract_validation`

---

## 17.3 drift-check-task

用途：
- 檢查當前輸出是否偏離主程序

固定字段：
- `baseline_design`
- `current_output`
- `drift_dimensions`
- `severity_rules`
- `required_decision`
- `trace_integrity_check`
- `contract_integrity_check`

---

## 17.4 correction-task

用途：
- 糾正 drift-check 發現的偏離

固定字段：
- `drift_source`
- `root_cause`
- `correction_plan`
- `affected_docs`
- `affected_modules`
- `revalidation_steps`
- `rollback_path`

---

## 17.5 freeze-task

用途：
- 凍結某個階段的接口、規則或邊界

固定字段：
- `freeze_target`
- `why_now`
- `what_becomes_change-controlled`
- `how_changes_are_requested`

---

## 17.6 rollback-task

用途：
- 當 gate 失敗或 correction 無法收斂時回退

固定字段：
- `rollback_target_phase`
- `rollback_reason`
- `what_to_restore`
- `what_to_keep`
- `re-entry_conditions`

---

## 17.7 meta-gate-review-task

用途：
- 檢查 gate 本身設計是否合理

固定字段：
- `gate_under_review`
- `evidence_collected`
- `why_gate_failed_or_underperformed`
- `proposed_gate_change`
- `expected_effect`

---

## 17.8 Task 使用規則

- 一次只允許執行一個主 build-task
- 每個 build-task 完成後必須接 verify-task
- 每個 gate 前必須接 drift-check-task
- drift-check 失敗後必須先跑 correction-task
- 未通過 correction，不得開新 build-task
- deferred / future 能力不得用 build-task 直接落地，必須先走 activation-proposal-task

---

## 17.9 activation-proposal-task

用途：
- 將 deferred / future 能力提議升級為 active
- 只產出決策材料，不直接實作能力

固定字段：
- `capability_name`
- `current_layer`: `deferred | future`
- `proposed_active_scope`
- `evidence_that_need_exists`
- `human_bandwidth_required`
- `new_risks`
- `rollback_plan`
- `minimal_first_slice`
- `gate_to_review`
- `recommended_decision`: `promote | hold | reject`

限制：
- 不得同時包含 implementation deliverables
- 不得創建 runtime 目錄或 worker
- 不得修改自動化邊界，除非 gate 明確批准

---

## 17.10 Decision Record 最低格式

任何非平凡設計、依賴、風險或降級決策，至少應留下以下結構：

```yaml
decision_record:
  trace_id: "tr_..."
  decision: "short statement"
  reason: "why this path was chosen"
  alternatives:
    - "option A"
    - "option B"
  risks:
    - "known downside"
  confidence: 0
  evidence_refs:
    - "ev_..."
```

沒有 `evidence_refs` 的 decision record 只能作為建議，不能支撐自動執行
或 gate 放行。
