# Gate review

> **Synthetic demo evidence only。** `passed` 僅表示下列工件在此 sandbox 範圍內彼此可檢查；不表示目標企業的真實 Gate 已通過。

| Gate | Demo conclusion | Direct demo evidence | Boundary / next step |
| --- | --- | --- | --- |
| G1 | passed | [scenario.json](../scenario.json) 與 [scenario-approval.json](../evidence/scenario-approval.json) | 僅是 sandbox scenario approval，不能替代 enterprise approval。 |
| G2 | passed | [semantic-definitions.json](../artifacts/semantic-definitions.json) 的 released `demo-shipment-semantics@1.0.0` 定義全部決策 facts、lifecycle、metric、source mappings、semantic/source/metric owners，以及 `serviceLevel` 允許值；[process-validation.json](../evidence/process-validation.json) 驗證 demo paths | 真實導入前要由目標企業提供並驗證語意、source、process owners 與 mappings。 |
| G3 | passed | [read-only-result.json](read-only-result.json) 包含 result、semantic-definition version、source evidence、freshness、access decision；[access-decision.json](../evidence/access-decision.json) 限定 demo scope；[validate-example.sh](../scripts/validate-example.sh) 重播 fresh、stale 與 denied access | 只允許 query 與 recommendation。 |
| G4 | passed | [decision-service.json](../artifacts/decision-service.json) 具名 policy owner、input bindings、logic、output 與 escalation；[decision-test-report.json](../evidence/decision-test-report.json) 覆蓋 normal、24/48 小時邊界、tie-breakers 與 escalation；[replay tests](../tests/test_replay_shipment_delay_priority.py) 以 CLI/contract seam 重播它們 | 測試只證明合成資料和規則的一致性。 |
| G5 | missing | [access-decision.json](../evidence/access-decision.json) 明確為 `controlledExecution: denied` | 缺少 controlled execution 授權、audit、idempotency、recovery 與 ERP write adapter；Gate 未通過且不得 write back。 |
| G6 | unverifiable | 沒有 shadow、production 或價值衡量證據 | 不可聲稱達成 45→15 分鐘，需取得可查驗的真實營運證據。 |

此範例的最高安全結果是人工審閱用的唯讀 recommendation。任何持久性動作都必須在 G5 以真實證據重新審查後才可進行。

`validate-example.sh` 的 gate assertions 僅確認上述 **synthetic** evidence chain 是否仍一致：G1–G4 `passed`、G5 `missing`、G6 `unverifiable`。它不會把這些結果提升為 enterprise approval、real-data access、controlled execution 或 value proof。

若要準備真實企業 shadow，使用 [enterprise-shadow-preparation.md](../artifacts/enterprise-shadow-preparation.md) 收集企業自己的流程、owner、語意、來源、access、persistence、量測與 rollback 證據。準備包存在不會改變本表的 Gate 結論。

## Synthetic shadow rehearsal

[Current Project User authorization](../evidence/shadow-rehearsal-authorization.json) 只涵蓋一個綁定既有 synthetic fixtures 與 access decision 的 read-only rehearsal event。[Rehearsal result](../evidence/shadow-rehearsal-result.json) 證明 authorization 內的 allowlisted CLI command 在三種 seeded disposition 下仍維持 `persistence: none`、沒有 persistent action，且其餘輸出與完整 read-only contract 一致。這是 documentary event scope，不是 CLI 的一次性 runtime token；每個新 event 都須另建 authorization／result pair。它不證明 observed human adoption、企業 authority、真實 shadow readiness 或營運價值，因此不改變 G1–G6 結論。
