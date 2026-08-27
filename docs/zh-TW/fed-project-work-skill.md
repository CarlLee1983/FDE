# FED Project Work Skill 功能說明

> 本文件為繁體中文使用說明；維護中的行為來源是 [`fed-project-work` skill](../../.agents/skills/fed-project-work/SKILL.md) 及其 references。若說明與 skill 不一致，以 skill 與專案英文 canonical 文件為準。

## 目的

`fed-project-work` 是本 repository 專用的 Codex skill。它的目的，是把一個真實營運問題轉成有證據邊界、可由交付團隊開始實作的 FED 營運方案。它會先診斷現況流程，找出可消除、簡化、標準化、重新分工或修復資料與語意的部分，形成不預設技術的目標流程；完成這一步後，才比較流程變更、確定性軟體、介面、AI 與受控系統動作。第一個端到端切片不必含 AI，`不需要 AI` 或 `延後 AI` 都是完整結論。

Scenario、流程、語意、規則、控制與 Gate 是方案的可信基礎，不是最終成果。這個 skill 仍是一個薄路由器，不保存企業的實際業務事實，也不複製完整 FED 方法論；每次使用時，它會依任務需要重新讀取 repository 內的英文維護來源。

## 適用範圍

| 適合使用 | 不屬於此 skill |
| --- | --- |
| 準備或檢查 FED scenario | 一般 Markdown 翻譯或編輯 |
| 將營運問題轉成流程優先的落地方案與第一個垂直切片 | 靜態 HTML／CSS 調整 |
| 設計或建置受治理的 FED capability | 單純要求「加上 AI」但沒有營運問題 |
| 判斷目前可通過哪個 G1–G6 關卡 | 例行 Git 或 repository 維護 |
| 檢查唯讀、建議或受控執行的權限邊界 | 與 FED domain 決策無關的程式修改 |
| 審查工件、證據與發布條件 | 在缺少授權時代替負責人做決策 |

Skill 預設允許自動觸發，也可以明確使用 `$fed-project-work` 呼叫。

## 四種工作模式

### 1. Scenario preparation

用於建立或審查可量測的 FED 情境。

主要功能：

- 依 [`fed-scenario.schema.json`](../../schemas/fed-scenario.schema.json) 檢查情境資料形狀與必填欄位。
- 識別營運成果、流程或案例節點、使用者、決策或行動。
- 檢查 owner、metrics、baseline、target、ontology references、source references 與 acceptance criteria 是否有真實證據。
- 指出形成方案前仍缺少的決策與證據，並列出需要哪些參與者與輸入。

Schema 合法只代表資料形狀正確，不代表情境已核准、資料可用或 Gate 已通過。準備情境是方案工作的入口，不是交付終點。

### 2. Operating solution shaping

用於回答「我們該做什麼」、「整個流程該怎麼改善」、「AI 應該放在哪裡」或「如何形成能落地的方案」。這是開放式 FED 要求的預設模式。

主要功能：

- 驗證 as-is 的 normal、exception、escalation 與 rework，找出等待、重複檢查、模糊 handoff、owner、資料、語意與控制問題。
- 在不預設技術的情況下，先 eliminate、simplify、standardize、clarify ownership，並修復必要資料或語意。
- 由 process owner 與受影響使用者接受或修正現況診斷、target flow、handoff、exception owner 與 change hypothesis；缺少證據時保持 `proposed`。
- 對 target flow 剩下的問題，比較流程／policy、資料／語意、確定性軟體、介面、AI 與受控系統動作，選擇最簡單足夠的介入。
- 只有仍需要語言理解、綜合或有限推理，而且能相對非 AI baseline 證明增量價值時，才設計 AI、abstention 與 human override。
- 提出資料、語意、整合、權限、觀測性與應用介面設計。
- 切出一個對使用者完整可用的第一個垂直切片；原則上先證明目標流程與非 AI baseline，除非 AI 對該切片不可或缺。
- 將 integration、policy、permission、source authority 與 acceptance 分成 `evidenced`、`proposed`、`missing` 或 `unverifiable`。

完整方案契約位於 [`solution-proposal.md`](../../.agents/skills/fed-project-work/references/solution-proposal.md)。Gate 未通過時，skill 會限制方案的權限與完成宣稱，但仍要提出最高安全範圍的方案與下一個可交付工作包，不會只回傳缺口清單。

### 3. Capability build

用於方案邊界已被接受、repository 也有實際建置表面時，交付最小可用的端到端切片。

主要功能：

- 對照 capability map、module seams、delivery sequence 與 validation strategy。
- 實作同一條使用者流程所需的程式、測試、必要文件與操作影響。
- 提供 evidence boundary、驗證結果、rollout／rollback 與尚未解決的營運假設。
- 缺少授權時，只實作證據支持的安全範圍，不自行建立 write-back 權限。

第一個唯讀切片的輸出契約為：

```text
result
+ semantic-definition version
+ source evidence
+ freshness
+ access decision
```

任何無法由證據建立的項目都必須標為 `missing` 或 `unverifiable`。

### 4. Gate-based review or assurance

用於依 FED 工件與 G1–G6 關卡審查 scenario、設計、實作或營運證據。

審查輸出分為：

- `passed`：條件已有直接證據支持。
- `missing`：必要證據不存在。
- `unverifiable`：目前無法檢查證據是否成立。

每個缺口都應說明它限制了哪個下一步。Schema 合法、設計提案或 repository 文件本身，都不能證明目標企業已接受、已授權或已產生營運價值。

## 證據與權限護欄

Skill 會遵守以下邊界：

1. 不自行發明真實 owner、source authority、baseline、target、policy、permission、integration 或 acceptance result。
2. 示例 scenario 只用來理解資料形狀，不會被當成真實業務資料。
3. 專案建議的安全範圍與目標企業已證實的 access decision 必須分開表達。
4. 權限提升依序區分 read-only query、recommendation 與 controlled execution。
5. 持久性回寫前必須有對應 Gate、授權、核准、稽核、冪等性與復原證據。
6. 證據不足時只提出標為 `proposed` 的 analysis、design、shadow、read-only 或 advisory 範圍，仍交付最高安全方案與下一步，但不推論已獲營運權限。

## 使用流程

```text
使用者要求
  → 判斷適用工作模式
  → 讀取該模式需要的英文 canonical 來源
  → 診斷現況流程、瓶頸與根因
  → 先形成不預設技術的目標流程
  → 比較流程、資料、規則、介面、AI 與系統介入
  → 定義責任與第一個垂直切片
  → 以實際證據限制 authority、rollout 與完成宣稱
  → 產出可實作方案、驗證方式與下一個 accountable action
```

若一個要求跨越多種模式，skill 會依實際相依順序處理；通常先準備 scenario，再形成營運方案、建置 capability，並在需要判斷的關卡執行 review/assurance。流程尚未被 owner／users 接受時，AI 選擇會被延後；第一個未滿足的 Gate 會停止後續權限提升或發布宣稱，但不會阻止產出標為 `proposed` 的安全方案。

## 使用範例

### 準備情境

```text
使用 $fed-project-work，把客服處理出貨延誤的流程整理成 FED scenario，並列出 G1 前缺少的證據。
```

### 形成流程優先的落地方案

```text
使用 $fed-project-work，先分析並優化客服處理出貨延誤的完整流程，再比較流程變更、規則、介面與 AI；提出第一個可交付垂直切片、整合、shadow rollout 與驗收。
```

### 建置第一個切片

```text
使用 $fed-project-work，依已接受的方案在目前 repository 實作不含 AI 的 read-only review workbench，包含來源、freshness、semantic version、access decision、測試與 rollback。
```

### 審查回寫條件

```text
使用 $fed-project-work，審查目前證據是否足以讓 agent 把出貨優先序寫回 ERP；依 passed、missing、unverifiable 回報。
```

在最後一個例子中，skill 不會因為使用者要求回寫就假設 ERP 已授權。缺少 G5 所需證據時，方案仍可做到 proposed read-only、shadow 或 recommendation scope，但不能宣稱 write-back 已獲授權。

## 可重播的落地範例

[出貨延誤優先序實作詳解](../../examples/shipment-delay-priority/index.html) 先診斷人工掃描與例外混雜的流程問題，再提出不依賴 AI 的目標流程與「出貨延誤審閱工作台」第一切片；確定性排序、evidence trace 與人工 review 先形成可衡量 baseline，AI explanation 被延後到 shadow 證明仍有殘餘負擔之後。全數合成的 scenario、流程、語意定義、決策規則、來源 snapshot、access decision 與 Gate 證據用來說明方案邊界，而不是把工件本身當成成果。

## 檔案結構

```text
.agents/skills/fed-project-work/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── source-map.md
    ├── task-modes.md
    └── solution-proposal.md
```

- [`SKILL.md`](../../.agents/skills/fed-project-work/SKILL.md)：觸發條件、共同流程與控制邊界。
- [`source-map.md`](../../.agents/skills/fed-project-work/references/source-map.md)：依問題導向英文 canonical 文件與指定 heading。
- [`task-modes.md`](../../.agents/skills/fed-project-work/references/task-modes.md)：四種模式的輸入、步驟、輸出與停止條件。
- [`solution-proposal.md`](../../.agents/skills/fed-project-work/references/solution-proposal.md)：流程優先營運方案的必要內容、介入選擇、責任分工與完成條件。
- [`openai.yaml`](../../.agents/skills/fed-project-work/agents/openai.yaml)：UI 名稱、簡介、預設 prompt 與 implicit invocation 設定。

Skill 目前沒有 `scripts/` 或 `assets/`。共用的 Schema 或工件驗證若要自動化，應優先成為 repository 工具鏈或 CI 能力，讓人員與其他工具也能直接使用。

## 維護與驗證

修改 skill 後至少應完成：

1. 執行 skill structure validator。
2. 確認所有 Markdown 相對連結仍可解析。
3. 確認 source map 的英文路徑與 heading 仍存在。
4. 使用開放式「我們該做什麼」、scenario、capability build 與 write-back request 做行為測試。
5. 確認一般翻譯、CSS 與 Git 維護不會誤觸發。

Source map 使用路徑與 heading，不固定行號；專案文件移動或改名時，應同步更新路由並重新執行行為測試。

## 參考

- [FED Scenario-to-Action Method](../../FED-Scenario-to-Action-Method.md)
- [FED Capability Enhancement Plan](../../FED-Capability-Enhancement-Plan.md)
- [OpenAI 官方：Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk/)
