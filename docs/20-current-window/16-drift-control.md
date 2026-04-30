---
status: active
scope: window
authority: this
---

# 漂移控制與糾偏機制

> 本文件定義如何防止目標漂移、實現漂移和治理漂移。它同時治理「系統偏了」和「gate 設錯了」兩類問題。

---

## 16.1 漂移類型

### 目標漂移
- 原始目標被悄悄改寫
- 範圍在未批准下擴大或縮小

### 實現漂移
- 代碼 / 文檔輸出不再對齊當初設計
- 階段產物與驗收標準脫節

### 治理漂移
- 原本要在 gate 停下來，實際卻被跳過
- 原本只是記錄的點，被錯誤升級成阻塞點

### 契約漂移
- `trace_id` 在同一條鏈路中丟失、分叉或無法對齊
- `schema_version` / `policy_version` / `ruleset_version` 與實際產物不一致
- evidence reference、writeback reference 或 artifact digest 無法回溯到同一變更

---

## 16.2 每個 Gate 都必跑的三個檢查

### Reality Check
檢查當前現實是否仍符合設計假設。

輸出：
- 成立的假設
- 弱成立的假設
- 已失效的假設

### Drift Check
檢查是否出現目標、實現、治理漂移。

輸出：
- `drift_type`
- `drift_description`
- `severity`
- `evidence`
- `trace_integrity`
- `contract_integrity`
- `writeback_integrity`

### Correction Decision
對每個漂移只能做四種決策：
- `accept`
- `correct`
- `rollback`
- `freeze`

---

## 16.3 Correction Task 的固定格式

每次 drift-check 失敗，必須創建 correction task，格式固定：

1. 偏離點是什麼
2. 偏離是何時開始的
3. 根因是什麼
4. 影響到哪些文檔 / 模塊 / 規則
5. 修正方案是什麼
6. 修正後如何重新驗證
7. 若修正失敗，回退到哪裡

沒有這 7 項，不算有效 correction。

任何 correction 若要覆寫現有 machine-readable 產物或 gate 決策，還必須說明：

- 受影響的 `trace_id`
- 受影響的 `artifact_family`
- 是否牽涉 `schema_version` / `policy_version` / `ruleset_version` 變更
- 修正後哪些 evidence ref 需要重建

---

## 16.4 何時更新設計，何時修正實現

只有在下列情況下，偏離可以被接受並反向更新設計：

- 新現實被證據穩定支持
- 原設計假設已被明確證偽
- 更新設計比修正實現更低風險

下列情況必須修正實現，不得改設計來圓：

- 只是為了繞過 gate
- 只是為了讓當前任務更快完成
- 沒有新證據，只有主觀偏好

---

## 16.5 Meta-Gate Review

Meta-Gate Review 是對 gate 本身的糾偏。它專門回答：

- 這個 gate 是否停得太早？
- 這個 gate 是否停得太晚？
- 這個 gate 是否拿到了真正有用的證據？
- 這個 gate 是否已經變成流程表演？

### 觸發條件
- 每完成 2 個正式 gate
- 或連續 2 次 correction 仍失敗
- 或人工明確認為 gate 設計不合理

### 允許的操作
- 刪除一個無價值 gate
- 合併兩個重複 gate
- 拆分一個過大的 gate
- 前移 / 後移一個 gate

### 不允許的操作
- 因為趕進度直接跳過 gate
- 沒有證據就降低 gate 要求

---

## 16.6 暫停條件

出現以下任一情況，主程序必須暫停：

- 無法判斷當前偏離是設計錯還是實現錯
- correction 已連續兩輪失敗
- 生產 incident 已證明當前放權假設錯誤
- gate 指標無法再預測後續結果
- 紅區操作在缺少人工批准或 lane 依據時被嘗試執行
- `trace_id`、`evidence[]` 或 contract triplet 缺失，導致自動決策不可審計
- 出現未授權跨切片依賴、受保護不變量變更或 writeback 假成功

暫停後只能做：
- 調查
- correction
- rollback

不得繼續向後推進 phase。

---

## 16.7 不可接受的「用漂移圓過去」

以下情況不得被標記為 `accept`：

- 缺少 `trace_id` 卻仍想保留自動決策
- 缺少 `evidence[]` 卻仍想保留放行結果
- 用修改 task scope 的方式掩蓋實際超界變更
- 用「只是文檔」的說法掩蓋邊界、治理或契約語義變更
- 用補寫敘述替代真正的 `menmery` / fallback evidence writeback
- 用人類口頭結論替代缺失的 verifier / gate artifact
