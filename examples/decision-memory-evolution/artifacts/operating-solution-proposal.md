# AI 數據分析師與模型演進：操作方案提案

> **證據邊界：Synthetic / Proposed。** 本文是一個可演練的 FDE 案例，不是任何企業的現況、授權或成效證據。所有角色、數字、來源與系統名稱只表示解決方案應有的形狀；缺少的企業事實標示為 `missing` 或 `unverifiable`。

## 1. 要改善的營運結果

主要使用者是商業營運主管、帳戶負責人與分析人員。案例聚焦一項決策：當 B2B 客戶的訂購模式發生重大變化時，應繼續觀察、請帳戶負責人查證，還是升級處理？

現況痛點不是缺少週報，而是訊號、解讀、決策、理由、行動和結果分散在不同位置。團隊無法可靠回答「上次遇到相似狀況時，當時知道什麼、為何如此判斷、後來如何」。

| 指標 | 定義 | 現況 | 提議目標 |
| --- | --- | --- | --- |
| 決策鏈完整率 | 訊號、證據、解讀、決策、理由、期限與結果都有連結的比例 | `missing` | shadow 後由流程負責人接受 |
| 重複調查工時 | 重建已出現過之相似案例所花分析時間 | `missing` | 採用可信決策記憶後下降 |
| 無證據解釋率 | 未引證來源或標示假設便宣稱原因的摘要比例 | `missing` | 第一切片提議為零 |
| 決策結果品質 | 由 owner 接受的案例級結果分類與比較方式 | `missing` | 先定義，不以單一留存率替代 |

數字基線與目標均未被真實 owner 接受，因此不可用合成案例宣稱改善留存或營收。

## 2. 現況流程診斷

### 正常路徑

1. 每週報表顯示帳戶營收或訂購量變化。
2. 主管請分析人員找出原因。
3. 分析人員查訂單、客服、續約與業務備註。
4. 會議中形成判斷並請帳戶負責人跟進。
5. 下週或下月再查看營收。

### 例外、升級與重工

- 服務事件、季節性、採購排程與商業流失可能呈現相同的訂購下降。
- 不同分析人員使用不同比較期或「重大變化」定義。
- 會議決策與 CRM 記錄不一定能回連原始證據。
- 後續結果缺少固定觀察期限，成功或失敗容易由印象判定。
- 相似案例再次出現時，團隊重新匯出資料和詢問相同的人。
- 原因不明時，升級責任人與棄答條件不清楚。

真正問題不是缺少一段自動生成的解讀，而是缺少可重用的診斷方法、競爭性假設分析、共同決策記錄與回饋路徑。此診斷尚未由真實流程 owner 和 affected users 確認，狀態為 `proposed`。

### Process-readiness decision

目前未達 readiness：normal、exception、escalation、rework 路徑尚未被真實使用者接受；重大變化定義、決策 owner、例外 owner、基線、合法來源與結果觀察方式都是 `missing`。因此 AI selection 維持 `deferred`，先設計可在沒有 AI 時成立的目標流程。

## 3. 先改善流程，再選技術

在引入 AI 前，先進行五項改變：

1. **統一審閱單位。** 一次審閱一個具名訊號，而不是在會議中自由瀏覽整份報表。
2. **分開事實與解讀。** 原始證據、確定性計算、人類解讀、待驗假設不得寫在同一個自由文字欄位。
3. **限制決策選項。** 第一切片只使用 `monitor`、`verify`、`escalate`，並允許具名例外理由。
4. **預先設定觀察期限。** 決策當下就指定何時、用什麼結果判斷，不事後挑選有利證據。
5. **建立回連。** 後續結果必須回到原始決策，而不是只留在新一週報表。
6. **保留時間邊界。** 一筆 `DecisionEpisode` 只能追加更正，不可覆寫；歷史重播只能使用決策當時可見的 evidence-as-of，禁止未來資料洩漏。

這些流程改變能先降低重工與語意混亂，也為未來 AI、dashboard 或工具提供同一條證據鏈。

## 4. 技術中立的目標流程

```text
排程取得允許的帳戶與訂購證據
  → 檢查 access、來源、資料新鮮度與指標版本
  → 使用已接受的比較方法產生待審訊號
  → 組裝服務、續約、活動與過往決策脈絡
  → 人員區分事實、假設與缺少的證據
  → 人員選擇 monitor／verify／escalate 並記錄理由
  → 指定觀察期限、結果指標與跟進 owner
  → 到期後記錄觀察結果及無法判斷的原因
  → 將完整決策鏈納入演進分析
```

缺少必要證據、來源過期、定義衝突或權限不明時，流程停止形成結論並交由具名 owner 處理。結果不應因無法取得資料就被補成「客戶流失」。

## 5. 客戶 A 的合成決策鏈

| 階段 | 合成內容 | 證據界線 |
| --- | --- | --- |
| 訊號 | 最近四週訂購金額下降 24% | 只表示變化 |
| 拆解 | 頻率由每月 4 次降至 2 次，平均單價持平 | 確定性計算 |
| 脈絡 | 有一件未結服務事件，續約在 45 天後 | 可能相關，不證明因果 |
| 人類解讀 | 「需確認採購排程與服務影響」 | 待查證假設 |
| 決策 | `verify` | 由主管負責 |
| 行動 | 帳戶負責人五個工作日內查證 | 尚無 CRM 寫入授權 |
| 觀察 | 三十天後訂購恢復 | 後續事實，不單獨證明原假設 |
| 修正 | 不應只以訂購下降標記商業流失 | 能力候選證據之一 |

三組合成 `DecisionEpisode` 的初版與 superseding revision 都顯示團隊反覆漏看決策當時仍未結案的服務事件，因此案例提出 `assembleAccountReviewContext(accountId, asOfDate, contextVersion)` 候選，把 as-of 服務事件與 provenance 穩定加入 context bundle。這只證明 synthetic story 可重播，不證明真實企業有相同模式或候選值得發布。

## 6. 介入選擇與 AI-fit

| 保留的工作 | 最簡介入 | 原因 |
| --- | --- | --- |
| 訊號排程與資料檢查 | 確定性軟體 | 可測試、可重試，不需模型 |
| 比較期、變化量與門檻 | 版本化計算工具 | 定義不能藏在 prompt |
| 事實／假設／決策欄位 | 工作流程與介面 | 先修復記錄方式 |
| 文字脈絡與矛盾證據綜整 | 條件性 AI | readiness 後才比較增量價值 |
| 過往案例比較 | 檢索工具＋條件性 AI | 只使用允許且語意相容的案例 |
| 接受解讀、選擇行動 | 人類 | 涉及客戶責任與模糊判斷 |
| 客戶聯繫、派工、CRM 更新 | 人類或受治理系統行動 | 需要真實授權、稽核與復原 |

### AI-fit 結論

目前為 `deferred`。若流程 readiness 成立，AI 在「綜整分散文字脈絡、揭露互相矛盾的證據、比較允許使用的過往決策紀錄、產生明確標示假設的摘要」可能具有條件性價值。它必須與重設後的非 AI baseline 在相同案例上比較時間、groundedness、棄答與修正率。

AI 不負責異常計算、政策門檻、access decision、因果認定、最終決策或外部行動。

### 分析師與模型的演進關係

案例中的 AI 身份是「企業數據分析師」，不是報表摘要器。它使用已發布的語意、指標、診斷、行為、決策與結果模型處理已知工作；遇到模型無法回答的問題時，才負責跨證據綜整、競爭性假設、反證與下一查證。重複且穩定的方法依 [`analyst-model-evolution.md`](analyst-model-evolution.md) 的模型生命週期下沉為版本化資產，再由 AI 使用。

## 7. 營運迴路與演進迴路

### 營運迴路

```text
可信訊號 → 證據包 → 人類審閱 → 決策與理由
→ 有 owner 的跟進 → 到期結果 → 完整決策時間線
```

### 演進迴路

```text
收集決策、修正、例外與結果
  → 找出重複調查和判斷差異
  → 提出流程、語意、規則、工具、模型或控制候選
  → 用封存案例重播並與現行方法比較
  → 負責人接受或拒絕
  → 交付團隊測試、發布、監控和回復
  → 營運迴路使用新版本，AI 繼續尋找下一個缺口
```

候選能力只有在重複、可規格化、可重播、由 owner 接受且可版本化、測試、觀測與回復時才能提升。人工 workaround 不得靜默成為新標準。

可能的候選工具包括：

```text
detectAccountOrderPatternShift(accountId, window, definitionVersion)
assembleAccountReviewContext(accountId, asOfDate, contextVersion)
findComparableDecisionRecords(signalId, semanticVersion)
classifyReviewReason(decisionId, taxonomyVersion)
compareDecisionMethod(candidateVersion, baselineVersion, replaySet)
```

## 8. 責任、能力與整合邊界

| 責任 | 負責者 | 第一切片邊界 |
| --- | --- | --- |
| 來源、權限、品質、新鮮度 | 確定性 context resolution | `proposed` integration |
| 指標與變化計算 | 版本化 decision-support tool | 一個定義版本 |
| 決策記錄與結果回連 | 工作流程支援 | 不自動寫入 CRM |
| 脈絡綜整與案例比較 | 條件性 AI shadow | readiness 後評估 |
| 商業判斷與例外 | 具名人類 | 保留 override 理由 |
| 追加決策 journal | 具名受治理系統行動 | 第一切片需要真實授權與控制證據 |
| CRM、客戶聯繫等外部行動 | 授權系統或人類 | 第一切片延後 |

AI 輸入只能是經 access decision 過濾的 context bundle；輸出必須列出事實、假設、矛盾、缺口、來源、時間與版本。證據不足時輸出 `abstain` 和所需的 owner action。禁止自行標記 churn、改變帳戶狀態、聯繫客戶、派工或發布能力。

## 9. 第一個可交付垂直切片

### 使用者可見結果

為一個商業單位建立 10–20 筆歷史或已獲准案例的決策時間線。來源讀取維持唯讀；確定性 baseline 標示訂購模式變化。主管透過具名 `appendDecisionEpisodeRevision` action 記錄 `monitor`、`verify` 或 `escalate`、理由、owner 與觀察期限，之後以新 revision 補記結果。這個 journal 是受控持久寫入，不得被描述成唯讀。

每筆唯讀訊號輸出遵守：

```text
result + semantic-definition version + source evidence + freshness + access decision
```

### 第一切片包含

- 一個合成或已獲准的訂購 snapshot。
- 最小語意：signal、evidence、interpretation、decision、rationale、action、outcome、correction。
- 一個可重播的非 AI 變化 baseline。
- 結構化人工決策與結果紀錄。
- 從訊號到結果的時間線與稽核資訊。
- [`decision-episode.schema.json`](decision-episode.schema.json) 定義 episode／revision ID、supersedes lineage、actor、時間、來源 revision／hash、available-at 與 outcome observation。

### 明確延後

- 自動判定流失或成功。
- AI 正式進入營運迴路。
- 客戶聯繫、任務派送或 CRM 寫入。
- 全公司帳戶與跨部門資料整合。
- AI 自行接受或發布能力變更。
- 用單次結果訓練或改寫正式政策。

## 10. 權限與控制

提議的第一階 application form 是「shared operational view + controlled append-only decision journal」。真實 read access 與 journal write authorization 都是 `missing`；因此本文件能定義 action 與控制要求，但不能宣稱真實持久寫入已獲准。

第一切片需要證明使用者能查看哪些帳戶、訂單、服務與續約資料；敏感欄位最小化。`appendDecisionEpisodeRevision` 必須驗證具名 actor 與 episode 權限、使用 `revisionId` 作冪等鍵、拒絕重複或衝突 revision、保存 append-only audit trail，並能以 superseding revision 更正而不覆寫歷史。Action 層還必須驗證 schema 無法單獨表達的跨紀錄不變量：revision 不得 supersede 自己；前版必須存在且屬於相同 episode；lineage 不得分叉或循環；`availableAt ≤ decisionAsOf ≤ recordedAt`；outcome 的 `observedAt` 與 `recordedAt` 不得早於原決策。任何不變量失敗都阻擋寫入與能力發布。備份／還原不得破壞 episode 順序或來源 hash。若這些證據缺失，真實切片只能使用不具企業紀錄效力的 synthetic sandbox。未來連接 CRM、派工或客戶溝通仍須另行證明其核准與補償控制。

## 11. 驗證、推出與回復

### 測試案例

- 訂購頻率下降但平均單價持平。
- 季節性造成的正常下降。
- 同時存在未結服務事件。
- 續約資料過期或互相矛盾。
- 帳戶無權由目前使用者查看。
- 缺少足夠證據時正確棄答。
- 人類修改解讀但保留原版本。
- 歷史重播看不到決策日期之後才產生的資料。
- 結果未到觀察期限，不提早宣稱成敗。
- prompt injection 或帳戶備註要求越權時被拒絕。

### 推出順序

1. 由 owner 與使用者確認現況和技術中立目標流程。
2. 以封存案例重播既有人工調查方式，建立工時和完整率 baseline。
3. 上線非 AI 唯讀訊號與人工決策時間線 shadow。
4. 確認來源、定義、access 與人工結果紀錄可信。
5. 條件性加入 AI shadow，比較任務成功、groundedness、棄答、敏感資料、格式、延遲、成本與增量價值。
6. 只選一個重複且可測試的修正建立能力候選。
7. 重播新舊方法，由具名 owner 接受後才版本化發布。

### 提議中的 gate 門檻

| Gate | Acceptance owner | `proposed` 通過門檻 | 阻擋條件 |
| --- | --- | --- | --- |
| 非 AI 決策時間線 | 商業營運流程 owner＋資料 owner | 100% 測試訊號包含 result、semantic version、source、freshness、access decision；100% revision 通過 schema；0 次未授權揭露；0 次覆寫既有 revision；0 筆 evidence `availableAt` 晚於 `decisionAsOf` | 任一 provenance、access、append-only 或 future-data leakage 失敗 |
| 使用者 shadow | 商業營運流程 owner＋affected users | 至少 10 筆案例可從訊號重播至決策與到期結果；至少 90% 無需另建試算表即可完成規定欄位；所有缺資料案例明確升級 | 使用者拒絕目標流程、結果 owner 缺失或策略性填寫風險未處理 |
| AI shadow | 商業營運流程 owner＋AI quality owner＋security/privacy owner | 100% 事實主張有允許來源；100% 必要證據缺失案例棄答；0 次敏感資料或 prompt-injection 越界；相對非 AI baseline 審閱時間提議降低至少 25%，且決策鏈完整率不下降 | 任一 unsupported claim、access、安全或 prohibited-action 失敗；無增量價值 |
| 能力候選發布 | 流程／語意 owner＋release owner | 封存 replay set 0 future leakage；候選輸出契約、錯誤行為、版本、觀測與回復測試全部通過；owner 明確接受 | 無法重播、無 owner、無版本 pin／rollback 或結果劣於 baseline |

門檻仍需真實 acceptance owners 接受；表格提供可執行的起始判準，不代表已通過。

所有門檻目前都是 `proposed`。來源、access、主要定義或 owner 缺失會阻擋 shadow 擴張；任何未授權 CRM 寫入會阻擋受控執行。回復方式是關閉 AI shadow、將 context capability 版本固定回前一個已接受版本，並保留 append-only 的 `DecisionEpisode` 歷史供重播；taxonomy 更新只能發布新版本與 mapping，不得改寫舊紀錄。

## 12. 證據帳本

| 主張 | 狀態 | 依據 | 限制 |
| --- | --- | --- | --- |
| 分散的決策與結果會造成重複調查 | `proposed` | 合成問題陳述 | 需由真實流程與工時證據確認 |
| 穩定方法應經治理後提升為版本化能力 | `evidenced`（專案方法） | FDE capability-evolution contract | 不證明特定工具已成熟 |
| AI 可綜整文字脈絡並找出重複修正 | `proposed` | 條件性職責設計 | 需和非 AI baseline 比較 |
| 訂購下降代表客戶流失 | `unverifiable` | 單一合成訊號 | 不得作為客戶標記或行動依據 |
| 真實來源與 CRM 寫入已獲授權 | `missing` | 無企業 access/control evidence | 僅能設計唯讀 shadow |
| 方案能改善留存或營收 | `unverifiable` | 無真實 rollout 結果 | 不得宣稱商業成效 |

## 13. 下一個負責行動

由真實商業營運流程負責人召集商業主管、帳戶負責人、分析人員、資料 owner 與 FDE delivery owner，選定一個商業單位和 10–20 筆可合法使用的案例，確認現況四種路徑、最小決策欄位、結果觀察方式及 shadow 接受門檻。

完成條件是：負責人與 affected users 接受技術中立目標流程；必要來源、語意版本與 access decision 有直接證據；交付團隊能從原始訊號重播到人工決策和到期結果。達成以前，本方案維持 `proposed`，AI selection 維持 `deferred`。
