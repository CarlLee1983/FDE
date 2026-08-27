# Gate review

> **Synthetic demo evidence only。** `passed` 僅表示下列工件在此 sandbox 範圍內彼此可檢查；不表示目標企業的真實 Gate 已通過。

| Gate | Demo conclusion | Direct demo evidence | Boundary / next step |
| --- | --- | --- | --- |
| G1 | passed | [scenario.json](../scenario.json) 與 [scenario-approval.json](../evidence/scenario-approval.json) | 僅是 sandbox scenario approval，不能替代 enterprise approval。 |
| G2 | passed | [semantic-definitions.json](../artifacts/semantic-definitions.json) 的 released `demo-shipment-semantics@1.0.0` 定義全部決策 facts、lifecycle、metric、source mappings、semantic/source/metric owners；[process-validation.json](../evidence/process-validation.json) 驗證 demo paths | 真實導入前要由目標企業提供並驗證語意、source、process owners 與 mappings。 |
| G3 | passed | [read-only-result.json](read-only-result.json) 包含 result、semantic-definition version、source evidence、freshness、access decision；[access-decision.json](../evidence/access-decision.json) 限定 demo scope | 只允許 query 與 recommendation。 |
| G4 | passed | [decision-service.json](../artifacts/decision-service.json) 具名 policy owner、input bindings、logic、output 與 escalation；[decision-test-report.json](../evidence/decision-test-report.json) 覆蓋 normal、24/48 小時邊界、tie-breakers 與 escalation | 測試只證明合成資料和規則的一致性。 |
| G5 | missing | [access-decision.json](../evidence/access-decision.json) 明確為 `controlledExecution: denied` | 缺少 controlled execution 授權、audit、idempotency、recovery 與 ERP write adapter；Gate 未通過且不得 write back。 |
| G6 | unverifiable | 沒有 shadow、production 或價值衡量證據 | 不可聲稱達成 45→15 分鐘，需取得可查驗的真實營運證據。 |

此範例的最高安全結果是人工審閱用的唯讀 recommendation。任何持久性動作都必須在 G5 以真實證據重新審查後才可進行。
