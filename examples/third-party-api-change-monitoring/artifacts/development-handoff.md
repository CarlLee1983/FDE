# AI Agent 開發交接契約：第三方 API 變更監測

> 狀態：`proposed`。這份文件把已完成的 FDE 作業分析轉成開發 agent 可採用的邊界與驗收契約；它不代表已授權真實來源、已選定技術棧、已完成開發或已證明成效。

## 何時使用

當 accountable owner 已接受第一切片的作業邊界，並明確要求在某個目標 repository 開發唯讀 shadow capability 時，將本文件連同 [scenario.json](../scenario.json) 與 [README.zh-TW.md](../README.zh-TW.md) 交給開發 agent。

FDE project-work skill 的責任在此停止於：作業問題、目標流程、介入選擇、證據限制、開發邊界與驗收條件均已清楚。程式設計、套件選擇、實作、測試、部署與維運由目標 repository 的開發流程及其 agent 負責。

## 開始條件

開發 agent 必須先確認下列輸入。缺少真實企業證據時，可以使用合成 fixtures 建立離線 reference implementation，但不得連接真實來源或宣稱 production-ready。

| 輸入 | 最低狀態 | 缺少時的限制 |
| --- | --- | --- |
| 目標 repository 與適用的 `AGENTS.md` | `evidenced` | 不開始修改程式 |
| 三個 vendor 的 source registry | `evidenced` 或合成 fixture | 僅能離線重播 |
| internal usage inventory schema 與 revision 規則 | `evidenced` 或合成 fixture | 不得宣稱 impact coverage |
| source access／抓取條款 | `evidenced` | 不得連接真實來源 |
| integration owner、fallback owner、severity／review-by policy | `evidenced` | 只產生 change record，不發通知或 escalation |
| model-visible field view、redaction policy、input-scope access decision | `evidenced` | AI path 關閉，只做 deterministic baseline |
| baseline、target 與 shadow acceptance | `evidenced` | 不得宣稱 AI 或流程改善有效 |

## 第一個開發切片

交付一個可在合成資料上重播的唯讀 vertical slice：

```text
versioned source fixture
  -> validate source identity, access decision, freshness and content hash
  -> normalize vendor publication / contract snapshot
  -> deterministic version, endpoint, field and deprecation diff
  -> bind immutable internal-usage-inventory revision
  -> emit reviewable change record with raw evidence
  -> optional AI shadow adapter for unstructured text only
  -> record human disposition fixture; no external or persistent action
```

此切片的完成條件是：合成輸入能產生可重播的 change record；結構化差異完全不依賴模型；AI adapter 可關閉；所有 authority-bearing action 保持在介面之外。

## 建議模組邊界

名稱可依目標 repository 慣例調整，責任不可混合：

| Seam | 責任 | 必要輸出 |
| --- | --- | --- |
| Source registry | 定義允許的 vendor source、source kind、cadence 與 access profile | versioned registry entry |
| Source snapshot | 保存 observation／retrieval time、content hash、contract version、freshness 與 access decision | immutable snapshot |
| Normalizer | 將 changelog、OpenAPI、schema 或 SDK metadata 轉成版本化 canonical representation | normalized publication／contract |
| Deterministic differ | 比較 version、endpoint、field、requiredness 與 deprecation date | reproducible raw diff |
| Usage inventory | 提供不可變 internal usage revision 與 owner mapping | cited usage points |
| Change record | 聚合來源、diff、inventory revision、severity candidate 與 review state | auditable review item |
| AI shadow adapter | 只處理核准的非結構化文字，輸出有引用的 summary／impact candidates／abstention | grounded candidate output |
| Review policy | 依 owner 接受的 deterministic policy 設定 owner、review-by 與 fallback escalation | proposed review assignment |

第一切片可把 review disposition 保存在 fixture 或測試 harness；真實資料庫、通知系統、issue tracker 與 write-back 都是後續獨立授權的 integration seam。

## 開發順序與每步完成條件

1. **讀取目標 repository。** 找出適用的 `AGENTS.md`、既有語言／框架、依賴、測試、lint、typecheck 與執行命令。完成條件：開發契約引用的是 repository 事實，而非本文件猜測的技術棧。
2. **建立紅色驗收測試。** 先用 fixtures 固定 change record contract、raw diff、fail-closed、AI-off 與 no-write 行為。完成條件：測試會因 capability 尚未存在而失敗，且失敗原因對應本契約。
3. **完成 deterministic vertical slice。** 依序實作 snapshot validation、normalization、diff、inventory binding 與 change record。完成條件：結構化 fixtures 可重播、輸出 deterministic，invalid／stale／denied evidence 不產生可採用結果。
4. **加入 optional AI shadow seam。** 只有存在核准 model input view 時才啟用；模型輸出保留引用、不確定性與 abstention。完成條件：關閉或移除模型仍不影響 deterministic baseline，模型失敗不會阻斷 raw diff。
5. **驗證與檢閱。** 執行最窄測試，再執行 repository 要求的 broader checks，檢查 final diff 與無寫回證據。完成條件：所有 acceptance tests 實際通過，未驗證的整合仍明確停用。

## 輸出契約

每個 change record 至少保存：

- stable record ID 與 semantic-definition version；
- vendor、API product、source kind 與 source identifier；
- publication／observation time 與 retrieval time；
- source content hash 或 contract version；
- source access decision 與 freshness result；
- deterministic raw diff 與 differ version；
- immutable internal-usage-inventory revision 及被引用的 usage points；
- AI mode（`disabled`／`shadow`）、input-scope access decision、引用、候選輸出或 abstention reason；
- proposed owner、review-by time、fallback owner 與 policy version；
- `writeBack: false`。

實際欄位名稱由目標 repository 的 schema 決定，但以上語義不得遺失。

## 必要驗收案例

- 同一輸入重播得到相同 deterministic raw diff 與 record identity。
- 新增／刪除 endpoint、required field change、版本改變與 deprecation date 均有明確 fixture。
- source identity 錯誤、access denied／mismatched、內容 hash 不符、stale snapshot、inventory revision 缺失時 fail closed。
- 無變更時不製造 impact candidate；不確定的結構差異不由 AI 猜測。
- AI disabled 時完整 deterministic flow 仍通過。
- AI shadow output 引用實際提供的 source evidence 與 usage points；來源衝突、過期、超出核准 view 或引用不存在時 abstain。
- 模型 timeout／error 不會抹除 raw diff，也不會建立升級工作。
- review-by／fallback assignment 使用版本化 deterministic policy。
- 測試證明沒有修改 source fixture、integration code、dependency、vendor config 或外部系統。

## 硬性邊界

開發 agent 應建立以下正向安全狀態：

- capability 預設為 offline、read-only、AI disabled；
- 真實 connector、通知與 persistent store 透過明確介面隔離且預設未配置；
- 所有輸出標示 evidence freshness、access decision 與 authority level；
- 所有模型輸入經 field allowlist 與 redaction；
- 所有 action 只形成可拒絕的 proposed record。

第一切片不包含 production deployment、排程基礎設施、真實 vendor credential、issue／PR 建立、自動 dependency upgrade、程式修改、vendor configuration change 或任何 write-back。

## Agent 交付回報

完成後，開發 agent 必須回報：

1. 實作的 vertical slice 與刻意未實作的 integration seams；
2. material files changed；
3. 實際執行且通過／失敗／未執行的 checks；
4. fixtures 與真實 enterprise evidence 的區別；
5. source、access、AI input、notification、persistence 與 deployment 仍缺少的授權；
6. 下一個需由 accountable owner 決定的 gate。

上述六項均可由 final diff 與 check output 驗證時，開發交接才算完成；這仍不等於上線、企業接受或價值已被證明。
