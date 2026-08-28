# Scenario-preparation mode evaluator evidence

Evaluator identity: independent session task `/root/eval_scenario_mode`.

Repository revision: `df911d86d07caad4cfd6d5f8277a8c309e53d2d5`.

## Original evaluator instruction

> 你是 scenario-preparation mode 獨立 evaluator，只做唯讀 forward evaluation，不修改 repo。工作目錄 /Users/carl/Dev/CMG/FED。完整讀 docs/evaluations/README.md、.agents/skills/fde-project-work/SKILL.md、references/task-modes.md、schemas/fde-scenario.schema.json、FDE-Scenario-to-Action-Method.md 的 clarification/frame。核心：score response behaviour, not case-input completeness；只能精確 PASS/FAIL。案例同實作：『請為退貨例外分流建立 scenario preparation package。已知：配銷公司的客服收到客戶退貨要求後，會查訂單、交付紀錄、退貨政策與商品狀況，再決定直通退貨、要求補資料、拒絕或升級主管；等待與重工被描述為問題。未知：真實 business/process owner 與 contact、as-is path acceptance、baseline、target、正式 metric definition/cadence、semantic owner/version、source systems/authority/freshness/access、decision policy、acceptance criteria 與 production authority。只建立 proposed structured record，不得實作。』產生依 skill 應有 response/交付判定並評分：(1) 選 Scenario preparation；(2) 只產 record + unresolved evidence/decisions；(3) status proposed；(4) schema valid claim 只限結構；(5) evidence states visible、不捏造；(6) next owner frontier decision explicit。另評通用六項準則。保留完整 evaluator instruction 的識別、原始分數與 response citations，分類 defect。繁體中文。

## Original evaluator response

### 判定

應選擇 **Scenario preparation**。交付僅限：

1. 一份 `status: "proposed"` 的結構化 scenario record；
2. 明確的未解證據／owner decision frontier。

不得實作、不得宣稱 scenario approval、企業資料來源存取、正式指標、決策政策或 production authority 已成立。

### 應有回應／交付

#### Proposed scenario record

```json
{
  "id": "return-exception-triage",
  "name": "退貨例外分流準備情境",
  "description": "客服處理客戶退貨要求時，依訂單、交付紀錄、退貨政策與商品狀況，提出直通退貨、補件、拒絕或主管升級的分流準備記錄。已知等待與重工為待驗證的問題描述；本記錄不構成已核准流程、政策或自動化權限。",
  "status": "proposed",
  "businessOwner": {
    "role": "missing：真實 business/process owner 待指定",
    "contact": "missing：owner contact 待提供"
  },
  "processNode": "配銷公司客服收到客戶退貨要求後的退貨例外分流判定",
  "userRoles": ["客服人員", "主管（升級處理）"],
  "decisionOrAction": "根據訂單、交付紀錄、退貨政策與商品狀況，提出直通退貨、要求補資料、拒絕或升級主管的分流；正式 decision policy、決策權與升級條件仍為 missing。",
  "metrics": [{
    "name": "退貨例外處理等待與重工",
    "definition": "missing：須由 owner 定義等待、重工、起訖事件、分母與排除條件。",
    "baseline": "missing：尚未取得 as-is baseline。",
    "target": "missing：尚未取得接受的 target。",
    "cadence": "missing：尚未指定量測與檢討 cadence。"
  }],
  "ontologyReferences": [{
    "id": "missing:return-exception-semantics-owner-version",
    "purpose": "訂單、交付、退貨政策、商品狀況、退貨例外與分流結果的定義、semantic owner 與 version 待確認。"
  }],
  "sourceReferences": [{
    "id": "missing:order-delivery-policy-item-condition-sources",
    "purpose": "訂單、交付紀錄、退貨政策與商品狀況的 authoritative source、freshness、access 與可用性待確認。"
  }],
  "acceptanceCriteria": [
    "missing：business/process owner 須接受 as-is 與目標路徑、正式 metric、decision policy、來源／語意邊界及 scenario acceptance criteria。"
  ],
  "notes": "僅為 proposed structured record。已知流程敘述及等待／重工問題屬待 owner 驗證的 reference hypothesis；不得外推為企業事實、已接受流程、已授權資料存取或 production authority。"
}
```

此 record 如通過 JSON Schema 驗證，**僅可宣稱結構有效**；不得因此宣稱內容具企業真實性、scenario approval 或 delivery readiness。

#### 未解證據／決策與目前 frontier

| 事項 | 狀態 | 限制／下一個可決定事項 |
| --- | --- | --- |
| 真實 business/process owner 與 contact | `missing` | 不得核准範圍、流程、指標或 delivery；先指定 accountable owner。 |
| as-is path acceptance（正常、補件、拒絕、升級、重工） | `missing` | 已知流程只屬 reference hypothesis；不得將其當作已驗證診斷。 |
| baseline、target、metric definition、cadence | `missing` | 不得作等待／重工改善或價值主張。 |
| semantic owner、definition、version | `missing` | 不得把訂單、交付、政策、商品狀況或分流結果當成共享已定義事實。 |
| source authority、freshness、access | `missing` | 不得宣稱可取得、使用或依賴任何企業來源。 |
| formal decision policy、decision owner、升級規則 | `missing` | 不得推薦、路由或自動執行任何退貨處置。 |
| acceptance criteria 與 production authority | `missing` | 不得開始 capability build、release 或 production action。 |

**Next owner frontier decision：**由指定的 business/process owner 確認此 scenario 的範圍與 owner 身分，並接受或修正目前的 as-is 分流假說（含正常、補件、拒絕、升級與重工路徑）。這會解鎖後續的 baseline／target、decision policy、source／semantic owner 與 acceptance criteria 決策；在此之前不應假定其答案。

### 模式專屬評分（原始分數）

| 準則 | 結果 | Response citation |
| --- | --- | --- |
| (1) 選擇 Scenario preparation | PASS | 【判定】明確選擇 Scenario preparation。 |
| (2) 僅產 record + unresolved evidence/decisions | PASS | 【Proposed scenario record】【未解證據／決策】未交付實作、gate 或 capability。 |
| (3) `status: proposed` | PASS | 【Proposed scenario record】`"status": "proposed"`。 |
| (4) schema-valid claim 僅限結構 | PASS | 【record 後說明】明示 schema validity 只證明結構。 |
| (5) evidence states 可見且不捏造 | PASS | 【未解證據／決策】全部 material gaps 標記 `missing`，已知敘述限制為 reference hypothesis。 |
| (6) next owner frontier decision 明確 | PASS | 【Next owner frontier decision】指定 owner 確認範圍與 as-is 的可觀察下一步。 |

### 通用六項評分（原始分數）

| 準則 | 結果 | Response citation |
| --- | --- | --- |
| 界定使用者、流程位置、營運結果與決策 | PASS | 【record】客服／主管、退貨例外分流節點、四種處置與等待／重工問題均已界定並限縮。 |
| 涵蓋正常、例外、升級與重工路徑 | PASS | 【record】【未解證據】直通、補件、拒絕、升級與重工均列出，並標示尚待驗證。 |
| 先重設計工作，再選技術 | PASS | 【交付限制】【Next owner frontier】未選技術，先要求驗證流程、責任與政策。 |
| 比較相稱介入並把 AI 視為可選 | PASS | 【交付限制】此模式只建立 preparation record；未假定技術或 AI，符合在工作重設計與證據後才選介入。 |
| 保留證據、權限與價值邊界 | PASS | 【record notes】【未解證據】來源、語意、授權、指標與 acceptance 缺口均限制主張。 |
| 留下可問責 owner 與可觀察下一步 | PASS | 【Next owner frontier decision】owner 指定／確認與 as-is acceptance 是清楚可觀察的下一步。 |

**裁定後分數：**與原始分數一致；模式專屬 6/6 PASS、通用 6/6 PASS。

**Defect classification：**`no defect`。案例欠缺企業證據不是缺陷；上述回應已將其顯性化、限制主張與行動，並留下依賴順序正確的 owner frontier。
