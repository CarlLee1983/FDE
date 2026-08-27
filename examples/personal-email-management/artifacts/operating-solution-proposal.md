# 個人 Email 管理：操作方案提案

> **證據邊界：Synthetic / Proposed。** 本文描述的是可演練方案，不是任何真實信箱的授權或成效證據。缺少的事實標示為 `missing` 或 `unverifiable`。

## 1. 要改善的生活結果

使用者每天反覆掃描同一批信件，仍可能漏掉需要回覆、付款、確認或追蹤的內容。方案要讓使用者在一次審閱中得到可追溯的「今日需處理／等待中／參考／可略過」清單，並保留最後判斷權。

| 指標 | 現況 | 提議方向 |
| --- | --- | --- |
| 漏掉的行動信件比例 | `missing` | 在不增加審閱時間下下降 |
| 每日主動審閱時間 | `missing` | 在不提高漏信率下下降 |
| 重複打開但未處理的討論串 | `missing` | 透過明確 review status 減少 |

數值門檻必須由真實使用者在 baseline 後接受；demo 不替使用者決定「重要」。

## 2. 現況流程診斷

### 正常路徑

```text
收到信 → 看寄件者與標題 → 打開內文 → 判斷重要性
     → 當下處理，或留在收件匣期待稍後記得
```

### 例外、升級與重工

- 同一討論串的新回覆讓舊信重複出現在視野中。
- 電子報、系統通知與收據排擠真正需要回覆的信件。
- 「稍後處理」沒有一致狀態，使用者反覆打開同一封信。
- 期限可能藏在長篇內文或附件中；缺少附件時無法可靠判斷。
- 寄件者熟悉不代表內容重要，陌生寄件者也可能是帳務或安全事件。
- 涉及健康、財務、法律、身分驗證或私人關係時，需要更嚴格的隱私與人工判斷。
- 判斷不清時，使用者通常保留信件並稍後再次掃描；目前沒有一致的升級對象或重審條件。
- 已經看過但未決定的信件會回到下一輪 inbox scan，形成重工；真實頻率為 `missing`。

這份診斷尚未由真實使用者以實際流程確認，狀態為 `proposed`。

## 3. 先改流程，再選技術

在引入 AI 前先做五件事：

1. 以「討論串」而非單封信作為審閱單位，移除重複掃描。
2. 統一四個 review status：需處理、等待中、參考、略過。
3. 將「重要」拆成可觀察欄位：是否直接寄給我、是否已有使用者標記、是否存在未完成狀態、多久未處理。
4. 將建議與信箱變更分開；第一切片只顯示與記錄審閱決定。
5. 先定義排除範圍，例如身分驗證碼、特定私人寄件者或敏感資料夾。

這些改善即使沒有 AI 也能產生價值，並提供可比較的 baseline。

## 4. 技術中立的目標流程

```text
使用者開始每日審閱
  → 取得明確允許且仍新鮮的信件證據
  → 依討論串合併並套用已接受的確定性分組
  → 顯示來源、時間、收件方式、未完成狀態與資料缺口
  → 使用者標記：需處理／等待中／參考／略過
  → 使用者確認下一步與期限，或標記無法判斷
  → 無法判斷項進入「需要使用者確認」，由 mailbox owner 決定處理、排除或指定重審日期
  → 經獨立授權後，保存審閱決定與原因，供下一次審閱與評估使用
```

若來源無法讀取、權限不明、內容過期或討論串不完整，該項必須標為無法判斷，並由 mailbox owner 決定是否補資料、排除或在具名日期重審；不得無限自動重試。任何後續信箱變更都需要另一個具名、授權、可稽核且可回復的行動流程。

### Process-readiness decision

真實使用者尚未確認 normal／exception／escalation 路徑、敏感資料排除範圍、狀態定義與 baseline，因此 readiness 為 `missing`，整體方案維持 `proposed`，AI selection 維持 `deferred`。

## 5. 介入選擇與 AI-fit

| 保留問題 | 最簡單充分的介入 |
| --- | --- |
| 同一對話重複出現 | 確定性 thread 合併 |
| 新信與舊待辦混在一起 | review status 與簡單工作清單 UI |
| 已知大量寄件者或通知類型 | 使用者可見、可修改的確定性規則 |
| 長討論串難以快速理解 | readiness 後評估 AI 摘要 |
| 行動與期限藏在自然語言中 | readiness 後評估 AI 候選抽取；使用者確認 |
| 撰寫回覆耗時 | readiness 後評估 AI 草稿；禁止自行寄送 |
| 寄送、刪除、封存、退訂 | 第一切片延後；未來只由受治理系統行動執行 |

AI 的條件性優勢在語言綜整與候選抽取，不在權限、排序門檻或執行控制。要從 `deferred` 變成 `justified`，必須在同一份版本化測試集上證明它相較非 AI baseline 能降低漏信或審閱時間，且沒有不可接受的敏感資料處理與錯誤自信。

AI 輸入只包含當次獲准的 message/thread context bundle。輸出必須包含摘要、候選行動、候選期限、來源 message id、信心或不確定性與 abstention reason。禁止自行補寫缺少的附件內容、推測使用者關係、改變優先級政策或執行任何 mailbox action。

## 6. 責任與能力邊界

| 步驟 | 責任 |
| --- | --- |
| 身分、授權、來源取得、新鮮度與 thread 合併 | 確定性軟體 |
| 已接受的分類規則與狀態轉換 | 確定性軟體 |
| 語言摘要、行動／期限候選、草稿 | AI shadow 候選 |
| 重要性、例外、敏感性、最終行動與文字確認 | 使用者 |
| 永久變更信箱或寄出內容 | 經授權、可稽核、冪等且可回復的系統行動 |

第一切片只需要 scenario registry、最小 email semantic definition、單一合成或獲准的唯讀來源、context resolution、review list 與 decision log。真實 Gmail、Outlook 或其他 provider integration 均為 `proposed`，不是已建立事實。

## 7. 第一個可交付垂直切片

### 使用者可見流程

每天打開一份 mailbox-read-only review list。系統依 thread 顯示寄件者、標題、最後活動時間、是否直接寄給使用者、未讀數、既有 review status、來源與資料新鮮度。使用者可以記錄分類、下一步與理由；這不回寫信箱，但會在另一個 decision store 產生持久紀錄。

### 包含

- 合成或明確獲准的唯讀 email snapshot。
- Message、Thread、ReviewStatus、UserDecision 與 EvidenceReference 的版本化定義。
- thread 合併、穩定排序與資料缺口檢查。
- review list，以及另行授權的人工決定紀錄：每筆含 actor、時間、來源 thread、decision id、理由與版本；相同 decision id 重試不得產生重複紀錄。
- 可重播 baseline 與每週量測。

### 延後

- AI 摘要、行動與期限抽取、回覆草稿。
- 寄送、刪除、封存、移動、標記已讀與退訂。
- 自動學習或發布新的分類規則。
- 未經證明的真實 mailbox provider integration。

## 8. 驗證、推出與回復

第一切片測試至少涵蓋：單封信、長 thread、自己被 CC、已知大量通知、陌生寄件者、內容缺失、來源過期、權限拒絕、重複抓取、重複提交決定，以及使用者修改或刪除既有決定。每個 review 結果需回傳：

```text
result + semantic-definition version + source evidence
       + freshness status + access decision
```

提議推出順序：

1. 用一週人工日誌建立 baseline 與排除範圍。
2. 以合成或去識別 snapshot 重播確定性 baseline。
3. 進行唯讀 shadow；每日由使用者核對漏項與誤分。
4. readiness 被接受後，才在同一資料上比較 AI shadow。
5. 若 AI 沒有可量測的增量價值，保留非 AI review workflow。

### 提議門檻與裁定者

| 關卡 | 提議 pass 條件 | 失敗效果 |
| --- | --- | --- |
| 進入 deterministic shadow | mailbox owner 接受流程、排除範圍、baseline、read access、decision-store write access 與 retention；資料集可重播 | 不處理真實內容，只能使用 synthetic data |
| 第一切片技術驗收 | 100% review item 帶 access decision、freshness、semantic version 與來源；0 次 mailbox mutation；0 筆被排除內容外洩；重複 decision id 產生 1 筆有效紀錄；使用者可匯出並刪除自己的 decision records | 阻擋真實 shadow 或回到修正 |
| 第一切片使用者驗收 | 在 owner 接受的評估期間內，漏掉的 actionable thread 不高於人工 baseline，且 review time 有下降；數字門檻目前 `missing` | 保留人工流程，不進入 AI shadow |
| 進入 AI shadow | 上述關卡通過，評估集版本固定，敏感資料與 prompt-injection 測試已接受 | AI 維持 `deferred` |
| AI 增量驗收 | task success、groundedness、abstention、敏感資料、延遲與成本門檻由 mailbox owner 接受，且至少一個主要指標優於 deterministic baseline、其他主要指標不惡化 | AI 不進入營運流程 |

所有百分比與 owner acceptance 目前都是 `proposed`；真實 acceptance owner 只有在 mailbox owner 明確加入後才成立。FDE delivery owner 提供技術證據，mailbox owner 裁定流程與個人風險是否可接受。

AI 評估集必須版本化，並測試 task success、來源 groundedness、正確 abstention、prompt injection、敏感資料處理、輸出契約、延遲、成本，以及相較非 AI baseline 的增量價值。任何來源、權限、隱私或重大漏信失敗都阻擋擴大範圍。

第一切片的 rollback 是停止產生 review list，撤銷 mailbox read token，並依已接受 retention policy 匯出或刪除 decision records 與其他衍生資料；刪除要有 audit receipt。因為它不回寫信箱，不需要復原郵件狀態。真實 decision-store write access 與 retention policy 目前為 `missing`，所以在這兩項被接受前只能使用不持久化的 synthetic demo。

## 9. 證據帳本

| 主張 | 狀態 | 依據與限制 |
| --- | --- | --- |
| 專案應先證明唯讀結果再增加寫入權限 | `evidenced`（專案方法） | FDE guardrails 與 delivery sequence；不證明任何信箱已授權 |
| thread review 與四種狀態能減少重複掃描 | `proposed` | 需要真實使用者流程與 shadow evidence |
| AI 能改善摘要、行動抽取與草稿 | `unverifiable` | 尚未和非 AI baseline 比較 |
| 真實 mailbox read access 已核准 | `missing` | 第一切片只能使用合成或另行獲准資料 |
| decision-store write access 與 retention 已核准 | `missing` | 只能使用不持久化的 synthetic demo，不能保存真實使用者決定 |
| 寄送、刪除、封存或退訂已獲授權 | `missing` | 明確排除於第一切片之外 |
| 方案能節省時間或降低漏信 | `unverifiable` | 尚無 baseline、目標或觀察結果 |

## 10. 下一個負責行動

由一位自願的 mailbox owner 與 FDE delivery owner 完成 60 分鐘流程工作坊：確認四種 review status、列出敏感內容排除範圍、選定合成或去識別資料集，並定義一週 baseline 的記錄方式。

完成條件是：使用者接受技術中立的目標流程與例外處理；資料集的來源、範圍、保留方式與 access decision 可被直接驗證；交付團隊能重播同一批 thread 並產生唯讀 review list。在此之前不得連接真實信箱，也不得把 AI selection 標為 `justified`。
