# FED Project Work Skill 功能說明

> 本文件為繁體中文使用說明；維護中的行為來源是 [`fed-project-work` skill](../../.agents/skills/fed-project-work/SKILL.md) 及其 references。若說明與 skill 不一致，以 skill 與專案英文 canonical 文件為準。

## 目的

`fed-project-work` 是本 repository 專用的 Codex skill。它協助 AI agent 將 FED 工作請求路由到正確的方法、Schema、決策關卡與權限邊界，避免在證據不足時直接跳到平台實作或持久性回寫。

這個 skill 是一個薄路由器，不保存企業的實際業務事實，也不複製完整 FED 方法論。每次使用時，它會依任務需要重新讀取 repository 內的英文維護來源。

## 適用範圍

| 適合使用 | 不屬於此 skill |
| --- | --- |
| 準備或檢查 FED scenario | 一般 Markdown 翻譯或編輯 |
| 設計或建置受治理的 FED capability | 靜態 HTML／CSS 調整 |
| 判斷目前可通過哪個 G1–G6 關卡 | 例行 Git 或 repository 維護 |
| 檢查唯讀、建議或受控執行的權限邊界 | 與 FED domain 決策無關的程式修改 |
| 審查工件、證據與發布條件 | 在缺少授權時代替負責人做決策 |

Skill 預設允許自動觸發，也可以明確使用 `$fed-project-work` 呼叫。

## 三種工作模式

### 1. Scenario preparation

用於建立或審查可量測的 FED 情境。

主要功能：

- 依 [`fed-scenario.schema.json`](../../schemas/fed-scenario.schema.json) 檢查情境資料形狀與必填欄位。
- 識別營運成果、流程或案例節點、使用者、決策或行動。
- 檢查 owner、metrics、baseline、target、ontology references、source references 與 acceptance criteria 是否有真實證據。
- 指出進入後續階段前仍缺少的分析工件。

Schema 合法只代表資料形狀正確，不代表情境已核准、資料可用或 Gate 已通過。

### 2. Capability design or build

用於選擇最小可用垂直切片，或在 repository 已具備實作表面時進行建置。

主要功能：

- 依目前 Gate 決定可以進行的下一步。
- 對照 capability map、module seams、delivery sequence 與 validation strategy。
- 優先規劃具證據的唯讀查詢，再逐步提升至建議與受控執行。
- 將尚未證實的 integration、policy、permission、source authority 與 acceptance 明確列為假設或缺口。

第一個唯讀切片的輸出契約為：

```text
result
+ semantic-definition version
+ source evidence
+ freshness
+ access decision
```

任何無法由證據建立的項目都必須標為 `missing` 或 `unverifiable`。

### 3. Gate-based review or assurance

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
6. 證據不足時停在分析、設計或 advisory 結果，並顯示缺口。

## 使用流程

```text
使用者要求
  → 判斷適用工作模式
  → 讀取該模式需要的英文 canonical 來源
  → 判斷目前 Gate 與建議 authority tier
  → 檢查目標企業的實際證據
  → 產出工件、缺口、驗證結果與最高安全下一步
```

若一個要求跨越多種模式，skill 會依實際工件與 Gate 的相依順序處理；通常先準備 scenario，再設計或建置 capability，並在需要判斷的關卡執行 review/assurance。第一個未滿足的 Gate 會停止後續權限提升。

## 使用範例

### 準備情境

```text
使用 $fed-project-work，把客服處理出貨延誤的流程整理成 FED scenario，並列出 G1 前缺少的證據。
```

### 設計唯讀切片

```text
使用 $fed-project-work，依這份 scenario 設計第一個 read-only context inquiry，包含來源、freshness、semantic version 與 access decision。
```

### 審查回寫條件

```text
使用 $fed-project-work，審查目前證據是否足以讓 agent 把出貨優先序寫回 ERP；依 passed、missing、unverifiable 回報。
```

在第三個例子中，skill 不會因為使用者要求回寫就假設 ERP 已授權。缺少 G5 所需證據時，它會停在 proposed read-only 或 recommendation scope。

## 檔案結構

```text
.agents/skills/fed-project-work/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── source-map.md
    └── task-modes.md
```

- [`SKILL.md`](../../.agents/skills/fed-project-work/SKILL.md)：觸發條件、共同流程與控制邊界。
- [`source-map.md`](../../.agents/skills/fed-project-work/references/source-map.md)：依問題導向英文 canonical 文件與指定 heading。
- [`task-modes.md`](../../.agents/skills/fed-project-work/references/task-modes.md)：三種模式的輸入、步驟、輸出與停止條件。
- [`openai.yaml`](../../.agents/skills/fed-project-work/agents/openai.yaml)：UI 名稱、簡介、預設 prompt 與 implicit invocation 設定。

Skill 目前沒有 `scripts/` 或 `assets/`。共用的 Schema 或工件驗證若要自動化，應優先成為 repository 工具鏈或 CI 能力，讓人員與其他工具也能直接使用。

## 維護與驗證

修改 skill 後至少應完成：

1. 執行 skill structure validator。
2. 確認所有 Markdown 相對連結仍可解析。
3. 確認 source map 的英文路徑與 heading 仍存在。
4. 使用 scenario、跨模式 capability 與 write-back request 做行為測試。
5. 確認一般翻譯、CSS 與 Git 維護不會誤觸發。

Source map 使用路徑與 heading，不固定行號；專案文件移動或改名時，應同步更新路由並重新執行行為測試。

## 參考

- [FED Scenario-to-Action Method](../../FED-Scenario-to-Action-Method.md)
- [FED Capability Enhancement Plan](../../FED-Capability-Enhancement-Plan.md)
- [OpenAI 官方：Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk/)
