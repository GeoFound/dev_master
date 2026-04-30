---
status: active
scope: window
authority: this
---

# 主執行 Task（Master Execution Task）

> 這是交給 AI 的總任務說明。AI 不能自己改寫它，只能依照它逐 phase 推進。

---

## 18.1 任務總目標

將當前模組化設計文檔逐步落地為可運行系統，但**只允許推進到下一個 gate**，不允許跨 gate 連跳。舊總文檔只能作為過時參考，不得覆蓋當前模組化設計和人類最新決策。

---

## 18.2 執行規則

1. 先讀：
   - `AGENTS.md`
   - `docs/00-entry/24-ai-cold-start.md`
   - `docs/10-product/CONTRACTS.md`
   - `docs/00-entry/26-design-closure-review.md`
   - `docs/20-current-window/14-master-program.md`
   - `docs/20-current-window/15-phase-gates.md`
   - `docs/20-current-window/16-drift-control.md`
   - `docs/20-current-window/17-task-templates.md`
   - `docs/20-current-window/22-three-plane-architecture.md`
   - `docs/30-integrations/23-menmery-integration.md`
   - `docs/20-current-window/25-implementation-language-baseline.md`

2. 然後判斷當前所處 phase。

3. 只執行當前 phase 允許的 build-task。

   每個 build-task 必須先標明 `plane` 與 `service_context`。如果 task 觸碰 deferred / future 能力，必須改為 `activation-proposal-task`，不得直接實作。

   非純文檔任務必須先判斷是否需要 `menmery` / `auto_router` 等外部服務。若需要長期上下文、治理預覽或 routed model selection，使用對方公開服務面；若當前環境無法調用，必須明確標記為 local fallback，而不是假裝服務已參與。

4. 完成後必須：
   - 產出證據
   - 驗證 machine-readable artifact 是否符合宣告的 contract / schema
   - 執行 verify-task
   - 執行 drift-check-task
   - 檢查三平面邊界是否被破壞
   - 為非平凡決策補 decision record
   - 形成給人類的制度性建議
   - 準備 gate 報告

5. 如果 gate 未通過，只能：
   - `hold`
   - `correct`
   - `rollback`

6. 沒有 `promote` 決策，不得進入下一 phase。

---

## 18.3 AI 的禁止行為

- 不得自行修改 North Star
- 不得跳過 `docs/10-product/28-product-principles.md` 重新解釋產品目標
- 不得在未批准下擴大 scope
- 不得跳過 gate
- 不得用主觀理由覆蓋 drift-check
- 不得在 correction 未完成時偷偷繼續下個 phase
- 不得為了完成任務而改寫驗收標準
- 不得在沒有 `trace_id` 與 `evidence[]` 的情況下聲稱自動決策有效
- 不得讓 orchestration plane 直接執行 repo mutation / shell command
- 不得讓 execution plane 自行決定 final approval
- 不得把未簽名、可覆寫或不可追溯的日誌當作 evidence
- 不得自建與 sibling 服務競爭的 truth / approval / router 子系統
- 不得把 runner log 假裝成已成功寫入外部 evidence sink 的正式證據
- 不得用 build-task 直接啟用 Ops / Advisor / TechRadar / adapter / model governance / rewrite
- 不得引入未授權跨切片依賴、受保護不變量變更或未審核新依賴
- 不得觸碰紅區後繼續執行，必須立即停下並升級

---

## 18.4 變更前必答六問

任何非純文檔的 `software_change` 任務，在 execution 前都必須明確回答：

1. 邊界條件是什麼？
2. 並發或衝突風險在哪裡？
3. 外部依賴失敗時怎麼退化或回退？
4. 數據、一致性或證據鏈如何保持可驗證？
5. 是否觸碰紅區、黃區或受保護不變量？
6. 當前設計、task、evidence 之間是否存在矛盾？

若六問中任一項無法回答，該任務不得直接進入 mutation。

---

## 18.5 每次回合的標準輸出

每次 AI 執行一輪後，必須輸出：

- `current_phase`
- `trace_id`
- `task_executed`
- `artifacts_changed`
- `evidence_collected`
- `service_context_used`
- `plane_boundary_check`
- `risk_facts`
- `drift_found`
- `decision`
- `recommendation_for_human`
- `next_allowed_action`

如果無法給出這些項，則本輪輸出不合格。

---

## 18.6 Gate 失敗時的處理

若 gate 失敗：

1. 立即停止推進
2. 產生 correction-task
3. 先向人類提交建議，說明：
   - 失敗原因
   - 缺失證據
   - AI 推薦的動作
   - 是否需要回退
4. 等 correction 完成後重新進 gate

---

## 18.7 Meta-Gate 觸發

若出現以下情況，必須追加執行 `meta-gate-review-task`：

- gate 兩次連續失敗
- gate 通過後卻很快在下一階段暴露錯誤
- 團隊認為 stop point 不合理

---

## 18.8 成功定義

主執行 task 的成功，不是「把全部能力都做完」，而是：

- 每個 phase 都有清楚證據
- 每個 gate 都有明確決策
- 每次偏離都被記錄並處理
- 系統能穩定從一個 phase 推進到下一個 phase

只有這樣，整套方案才算真正可落地。
