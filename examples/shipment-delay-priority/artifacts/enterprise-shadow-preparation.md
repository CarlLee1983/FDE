# 企業 Process Shadow 準備包

> **Preparation only — not enterprise approval。** 本文件把 synthetic 範例整理成可帶進企業 process-framing workshop 的決策清單。它不是任何企業的 scenario、核准、資料存取決定或 shadow 啟動紀錄，也不得用 demo 的人員、資料、基線或規則代替企業證據。

## 目前可交付邊界

Repository 已有一條可重播的 synthetic validation seam：CLI 會驗證資料新鮮度、必要欄位、語意版本、來源 binding、access decision、確定性排序、data-quality escalation，以及 session-local 的 `accepted`、`rejected`、`needs-investigation` disposition。這足以驗證範例工件是否形成一致的端到端唯讀契約。

目前仍不能：

- 宣稱真實企業接受現況診斷、目標流程、優先規則或 45→15 分鐘目標；
- 讀取或複製真實 shipment／ERP 資料；
- 建立真實 enterprise `scenario.json` 或沿用 demo owner 身分；
- 保存使用者 disposition、執行 ERP write-back，或啟動 production pilot；
- 因為 repository replay 通過就判定企業 Gate 通過；
- 因為可能使用 AI 就預先選定模型、prompt、agent、RAG、framework 或 UI。

## Process-framing workshop 的決策前沿

下列決策依賴前一項的結果；每項都要由可問責的人員以可查驗證據確認。

| 順序 | 必須確定的決策 | 需要的直接證據 | 未完成時的限制 |
| --- | --- | --- | --- |
| D1 | 目標企業／營運單位、要改善的 bounded process、使用者與可量測 outcome | 具名 business owner 的 scenario scope 與問題陳述 | 不建立 enterprise scenario，不接資料 |
| D2 | Business owner、process-change authority、logistics users、source owner、semantic／policy／metric owner、FDE delivery owner | 角色接受紀錄與 escalation path | demo owner 不可沿用；無人可接受流程或規則 |
| D3 | 真實 as-is normal、exception、escalation、rework、handoff，以及 proposed target flow | 現場觀察、操作紀錄、SOP 與使用者 walkthrough；來源衝突需保留 | synthetic process 只能當訪談假設 |
| D4 | Shipment identity、delay、service level、risk signals、priority policy、tie-break、baseline 與 target | 已發布語意／policy 版本、source mappings、樣本與可重現 baseline | demo rules 不可直接提升為企業規則 |
| D5 | Approved source、資料範圍、identity、query／recommendation 權限、privacy、retention、freshness SLA | Source owner 與 security/privacy 的 access decision；可追溯 snapshot | 不讀真實資料，不啟動 shadow |
| D6 | 人工 disposition 是否需要持久化，以及寫到哪個既有受治理系統 | Process owner 的使用需求與 system owner 授權 | 預設維持 session-local；不得自行建 feedback store |
| D7 | Shadow cohort、期間、baseline、pass/fail threshold、telemetry、support、incident owner、rollback | 核准的 shadow plan、可重現 baseline，以及 telemetry owner／purpose／data controls | 不宣稱營運效益，不進 pilot |
| D8 | Shadow 後是否仍有值得處理的 residual burden | 實測的解釋／比較成本、錯誤型態與 non-AI baseline | 沒有證據就不啟動 AI experiment |

## 人工 disposition 的持久化選擇

先由量測需求決定是否需要跨 session 關聯：不需要時維持 session-local；確有必要時，優先把 disposition 記入企業既有、已核准且具身分與稽核能力的工作系統。只有當 D3–D5 證明既有系統不適合，且持久化確實是 shadow measurement 的必要條件時，才設計獨立 store。

任何持久化方案都必須先確認：

- 使用者 identity、授權範圍與最小必要欄位；
- audit trail、retention、privacy、匯出與刪除責任；
- 重複提交的 idempotency、錯誤更正與 provenance；
- disposition 是否會觸發營運動作；若會，必須另走 G5 controlled-execution 審查；
- rollback 時如何停寫、保留或移轉既有紀錄。

在這些決策完成前，現有 CLI 的 `persistence: none` 是刻意的安全邊界，不是缺少一個順手補上的功能。

選擇 session-local 時，telemetry、log、cache 或 replay fixture 也不得保存 raw disposition，或保存能以穩定 identity 重建個別 disposition 的關聯鍵；若需要這類資料，就視為 persistent mode 並先完成 D6 controls。

## Shadow entry criteria

只有以下項目全部具備直接證據，才可把狀態從「準備」改為「可啟動 read-only shadow」：

- D1–D6 已由具名 owner 接受，企業 scenario 與 demo scenario 明確分離，disposition 明確選定 session-local 或 approved persistent system；
- 真實資料的最小 scope、freshness、privacy、identity 與 query／recommendation access 已核准；
- 企業語意、policy 與 source bindings 已版本化，normal、boundary、missing、conflicting、stale、denied cases 可重播；
- 使用者看得到 `result + semantic-definition version + source evidence + freshness + access decision`；
- shadow 與既有人工流程並行，不改 shipment／ERP 狀態；
- D7 的 baseline、support、incident escalation、停用條件與 rollback 已核准；
- shadow telemetry 已具名 owner 與 purpose，並核准最小必要欄位、identity／access、privacy、retention／deletion、provenance、audit，以及停止收集與 rollback 的方式；
- disposition 若選擇持久化，D6 的 access、audit、retention、idempotency 與 correction controls 已通過；若選擇 session-local，shadow plan 明確記錄不保存 disposition。

即使 read-only shadow 通過，ERP write-back 仍保持 denied。G5 必須另有 action authorization、approval boundary、audit、idempotency、recovery 與 target-system adapter 證據；G6 必須有可重現的 shadow 或 production outcome 才能判定。

Persistent shadow telemetry 屬於受治理的 measurement evidence，不等於 G5 business write-back。Collector 必須使用獨立 sink、service identity 與 credential，不得呼叫 ERP／workflow adapter、修改 domain state，或觸發營運 queue／notification；一旦產生營運 side effect 就必須另走 G5。停止或 rollback 時，要從 collector source 停止 emission、驗證 cutoff 後沒有新增紀錄，再依核准的 retention／deletion 決定處置已收資料。

## Workshop 產出與完成標準

參與者至少包含 accountable business owner、process-change authority、實際 logistics users、source owner、security/privacy 代表與 FDE delivery owner。一次 workshop 不必強迫所有 Gate 通過；它必須讓未知事項有 owner 與下一個可查驗證據。

準備階段完成時，應交付：

1. 企業自己的 scenario scope、owner map 與 process acceptance record；
2. 修正後的 as-is／target flow，以及 normal、exception、escalation、rework cases；
3. 企業 semantic／policy／source／access contracts 與 evaluation fixtures；
4. disposition persistence 的明確決定；
5. read-only shadow plan、entry checklist、量測、support 與 rollback；
6. 一份 evidence ledger，逐項標示 `evidenced`、`proposed`、`missing` 或 `unverifiable`。

完成上述產出後，才為該企業建立獨立 case workspace，並以企業證據填寫其 scenario；不要複製本 demo 的核准檔後改名。

## 目前 evidence ledger

| Statement | Status | Evidence / next evidence |
| --- | --- | --- |
| Repository 的 synthetic CLI 可重播唯讀契約與三種 session-local disposition | `evidenced` | `scripts/validate-example.sh`、CLI tests、expected result |
| 本準備包列出企業 process shadow 所需決策與 entry criteria | `evidenced` | 本文件；只證明準備內容存在 |
| 目標企業、process owner、使用者與 source owner 已具名接受 | `missing` | D1–D3 workshop evidence |
| 企業語意、規則、來源、identity、privacy 與 access 已核准 | `missing` | D4–D5 contracts and decisions |
| 人工 disposition 已明確決定為 session-local 或在受治理系統持久化 | `missing` | D6 decision |
| Read-only shadow 已核准且達到 entry criteria | `missing` | D7 approved shadow plan |
| 流程能把 triage 從 45 分鐘降到 15 分鐘 | `unverifiable` | Reproducible enterprise baseline and shadow result |
| AI 對接受後的 non-AI flow 有增量價值 | `unverifiable` | D8 residual-burden evidence and controlled comparison |
| ERP write-back 已獲授權且安全 | `missing` | Separate G5 controlled-execution evidence |

## 下一個 accountable action

由 business owner 召集 process-framing workshop，先完成 D1–D3，並為 D4–D7 的缺口指派 owner、證據來源與期限。在 D1–D5 完成前，repository 不建立真實 enterprise case、不接來源、不保存 disposition，也不做 AI／UI 實作。
