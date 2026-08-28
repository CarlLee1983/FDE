# 三方 API 版本更新監測：從被動人工查看到可稽核的影響審查

> **通用、合成的 FDE 範例。** 本案例沒有連接任何真實供應商，也不能證明既有權限、來源完整性、節省工時或降低事故。三個實際服務、負責人、基線、目標與驗收均為 `missing` 或 `unverifiable`，所有落地設計目前都是 `proposed`。

團隊目前串接三個外部服務，但 API 是否升版、棄用或改變行為，主要靠工程師偶爾查看文件或收到問題後才回頭確認。這不是單純的「少一個 AI bot」，而是缺少固定來源、內部使用清冊、審查責任與可追溯決策的作業問題。

## 1. 作業問題與預期結果

要改善的不是「自動讀更多公告」，而是讓每個可能影響串接的變更都能在合理時間內被發現、連回實際使用點、交給明確的人決定，並保留來源與處置證據。

第一階段只追求唯讀決策支援，不讓系統自動改 code、升 SDK、切換 API version 或更動供應商設定。應量測：變更偵測延遲、相關變更召回率、無關通知造成的審查負擔；實際 baseline 與 target 必須由團隊先量測與接受。

## 2. 現況診斷（待企業證據驗證的參考假說）

| 路徑 | 可能的現況 | 作業風險 |
| --- | --- | --- |
| 正常 | 每位工程師自行追蹤 release notes、文件頁或 email | 重複查看，仍無法知道三個服務是否都被涵蓋 |
| 例外 | 公告只說功能改變，沒有直接標示對既有 endpoint、SDK 或 auth 的影響 | 必須重新讀公告、搜尋程式碼並詢問原作者 |
| 升級 | 發現 breaking change 或 deprecation 後，才臨時找 owner 與排期 | 責任和時限不清，風險停留在聊天訊息 |
| Rework | 同一公告被不同人重複判讀，或因來源更新而失去當時依據 | 無內容 hash、使用點版本與接受／拒絕理由，不能重播決策 |

在開始做工具前，先由團隊驗證：三個服務的實際人工檢查方式、曾漏掉的變更、每週花費、官方來源與真正的 integration owner。若問題主要是責任未定，先修責任，不應用 AI 遮住流程缺口。

## 3. 先重作業流，再加入技術

```text
供應商來源登錄（每個服務的官方 changelog / deprecation / OpenAPI / SDK）
  -> 排程唯讀擷取，保存來源、時間、版本與內容 hash
  -> 確定性比較版本、schema、endpoint、欄位與棄用日期
  -> 對照版本化的內部 API 使用清冊
  -> 產生 change record 與 raw diff
  -> [需要語言解讀時] AI 提供有引用的摘要與影響候選
  -> 依 owner 接受的 severity policy 指派 owner 與 review-by time
  -> integration owner 接受、拒絕或要求補證據
  -> 逾期未審查則交給具名 fallback owner，保留在 queue 直到有證據的結案
  -> 另行建立受治理的升級工作；第一切片不自動執行
```

先做四個非技術修正：

1. **移除**每位工程師各自查同一來源的重複工作。
2. **簡化**成每個供應商一份被 owner 接受的來源登錄。
3. **標準化** vendor、API product、version、endpoint、SDK、deprecation、internal usage point 與 review disposition。
4. **重新分責**：平台或整合維運者維護監測，服務 maintainer 判斷實際影響，integration owner 決定是否建立升級工作。

## 4. 介入方式與 AI 適配

| 工作 | 最簡充分介入 | 原因與邊界 |
| --- | --- | --- |
| 排程、抓取、hash、版本比較、OpenAPI/schema diff、棄用日期計算 | 確定性軟體 | 規則穩定，必須可重播；失敗時應 fail closed 並標示來源缺口 |
| internal usage inventory 與 owner mapping | 資訊與責任修復 | 沒有可靠使用清冊，AI 也無法判斷公告與誰有關；每次判讀須綁定不可變 revision |
| 自然語言 release notes 摘要、不同文件合併、對照使用點提出影響候選 | AI（條件式、shadow） | 只在語言解讀是保留下來的主要負擔時使用；必須引用來源、呈現不確定性並可拒絕 |
| relevant / not relevant、風險等級、是否升級、期限與排程 | 人類 owner | 涉及業務影響、相依風險與資源承諾，不由模型自動決定 |
| 修改程式碼、升版、切換 endpoint 或 vendor 設定 | 另案受治理行動 | 需要獨立授權、測試、稽核、回復方案；不在監測第一切片內 |

AI 不是每筆變更的必經步驟。若 OpenAPI diff 已能明確指出刪除 endpoint 或新增 required field，直接用確定性結果通知即可。只有公告是散文、多來源描述不一致，或必須把文字對照多個內部使用點時，才讓 AI 產生「候選判讀」。

## 5. 最小落地切片與驗證

### 第 0 週：建立可驗證的人工基線

- 指定一位 accountable integration owner，列出三個供應商與官方來源。
- 建立最小內部使用清冊：服務、repo/module、endpoint 或 SDK、目前版本、auth 方式、maintainer；指定不可變 revision，並另定可送入模型的欄位 view。
- 由 accountable data owner 核准欄位層級的模型輸入範圍與遮罩政策；憑證、secret、原始 auth material、未核准的 code 或 metadata 一律排除。
- 回看一段雙方同意的歷史期間，整理已知 relevant changes 與人工發現時間；若資料不存在，明確記為 `missing`，不要捏造基線。

### 第 1–2 週：唯讀 deterministic shadow

- 每日或依 owner 接受的 cadence 擷取來源，保存 provenance、freshness、版本與 hash。
- 對結構化 contract 做 reproducible diff，產生 change record；不發出自動升級指令。
- 依 owner 核准的 severity policy 設定 owner 與 review-by time；逾期案件升級給具名 fallback owner，且不可因逾期自動結案。
- 由 maintainer 在既有審查介面標記 relevant、not relevant、need evidence，並留下理由與使用的 inventory revision。

### 第 3–4 週：AI shadow A/B

- 只把非結構化公告與核准、遮罩後的內部使用點 view 送入 AI；每次請求記錄 input-scope access decision，敏感 code、憑證、原始 auth material 與未授權內容不得進入。
- 同一批 change records 同時保留「deterministic-only」與「AI-assisted」結果，比較召回、誤報、審查時間與引用正確性。
- AI 讀不到官方證據、使用清冊過期、來源互相衝突時必須 abstain，不能補猜。

### 第一階段驗收條件

- 每筆輸出保留來源識別、publication/observation time、retrieval time、內容 hash 或 contract version、semantic-definition version、不可變 internal-usage-inventory revision 與 source/input-scope access decision。
- raw diff 可重播；AI 摘要不能成為唯一證據。
- shadow 期間沒有自動改 code、升 dependency、改供應商設定或自動建立升級任務。
- owner 根據實測結果接受 source coverage、通知閾值、review-by time、fallback owner 與 escalation responsibility 後，才能規劃下一階段。

## 證據帳與下一個負責行動

| 主張 | 狀態 | 目前限制 |
| --- | --- | --- |
| 團隊串接三個外部服務，且以被動人工方式檢查 | `proposed`（來自案例需求，未有企業紀錄佐證） | 可用於案例定義，不能宣稱實際工時或漏報率 |
| 官方來源、抓取條款與完整性 | `missing` | 不得啟用真實來源擷取 |
| 內部使用點與 owner 清冊 | `missing` | 不得宣稱影響判讀完整 |
| AI 比非 AI baseline 更有價值 | `unverifiable` | AI selection 維持 conditional，先做 shadow 比較 |
| 自動升級或寫回權限 | `missing` 且不在範圍 | 第一切片嚴格唯讀 |

**下一個 accountable action：** 由真正的 External Integration Owner 在 60–90 分鐘工作坊中確認三個服務、每個服務的官方來源、內部使用點 owner、兩週 shadow 要採用的 baseline 與通知閾值；同時指定具核准權的 Internal Data Owner，由其確認允許送入模型的欄位 view、遮罩政策與 input-scope access decision。完成前，本案例僅能用合成資料演練。

## 使用方式

驗證 scenario record：

```bash
examples/third-party-api-change-monitoring/scripts/validate-example.sh
```

主要檔案：

- [可直接開啟與列印的 HTML 案例頁](index.html)
- [交給 AI agent 的開發交接契約](artifacts/development-handoff.md)
- [原始需求](request.md)
- [提議中的 scenario record](scenario.json)
