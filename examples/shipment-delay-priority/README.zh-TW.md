# 出貨延誤優先序：FDE 可重播範例

> **Synthetic demo only。** 本目錄中的人員、授權、資料、基線、核准與測試結果都是為了說明工件關係而虛構；不能據此推論任何企業已授權、已上線或已產生價值。

這個範例把一個「每天先處理哪些延誤出貨」的問題，先做現況流程診斷，再收斂成不依賴 AI 的目標流程：先驗證快照與必要欄位、分開正常與資料品質路徑、用確定性規則產生排序與 reason trace，最後交物流人員審閱。第一個交付切片不含 AI；只有 process shadow 證明仍有解釋或比較負擔時，才評估可拔除的 AI 實驗。ERP 的持久性回寫仍在 G5 被阻擋。

## 主要入口

直接開啟 [出貨延誤範例：從流程分析到可交付方案](index.html)。這個 standalone HTML 先說明現況問題、流程優化、無技術預設的目標流程、介入選擇、第一個垂直切片與 AI-fit 結論，再用「界定情境、畫出工作流程、定義資料語意、寫出決策規則、跑出唯讀結果、審查證據邊界」六個步驟交代方案依據。

完整文字版提案位於 [artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)。它清楚區分 demo 已證明的 deterministic core、仍待現場確認的流程診斷與目標流程，以及為什麼 AI 在第一切片被延後。

以下 JSON 與 Markdown 只在需要追查原始證據或驗證規則時閱讀。

## 證據重播順序

1. 先讀 [artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)，確認流程診斷、目標流程、介入選擇、第一個切片與證據邊界。
2. 由 [request.md](request.md) 看使用者要解決的流程問題。
3. 由 [scenario.json](scenario.json) 看被核准的 demo scenario、可量測成果與來源／語意引用。
4. 對照 [artifacts/process-model.md](artifacts/process-model.md)、[artifacts/semantic-definitions.json](artifacts/semantic-definitions.json) 與 [artifacts/decision-service.json](artifacts/decision-service.json)，確認流程節點、定義與規則是一致的。
5. 由 [evidence/process-validation.json](evidence/process-validation.json) 確認 normal、exception 與 escalation path 已在 demo 中被角色驗證，再使用 [evidence/shipments.json](evidence/shipments.json) 的 snapshot，在 [evidence/access-decision.json](evidence/access-decision.json) 指定的 demo 權限內，手動計算優先序。
6. 核對 [expected/read-only-result.json](expected/read-only-result.json)：它提供唯讀結果的完整契約：`result + semantic-definition version + source evidence + freshness + access decision`。
7. 最後閱讀 [expected/gate-review.md](expected/gate-review.md)，確認 demo 可用的證據只支撐 G1–G4，G5 與 G6 沒有被誤判為通過。

## 手動重播

資料 snapshot 於 `2026-08-25T08:45:00Z` 擷取；查詢時間是 `2026-08-25T09:00:00Z`，故資料新鮮度是 15 分鐘，符合 60 分鐘 SLA。

每筆資料必須具備作為記錄 identity 與同分排序用的 `shipmentId`，以及計分用的 `overdueHours`、`serviceLevel`、`temperatureControlled`、`atRiskCustomerCommitment`。計分規則如下：

| 條件 | 分數 |
| --- | ---: |
| overdueHours ≥ 48 | 50 |
| overdueHours ≥ 24 且 < 48 | 30 |
| overdueHours < 24 | 10 |
| serviceLevel = critical | +25 |
| temperatureControlled = true | +20 |
| atRiskCustomerCommitment = true | +15 |

因此：

| Shipment | 計算 | 結果 |
| --- | --- | ---: |
| SHP-1001 | 50 + 25 + 15 | 90 |
| SHP-1002 | 30 + 20 + 15 | 65 |
| SHP-1003 | 10 + 25 | 35 |
| SHP-1004 | 缺 `overdueHours` | escalation，無分數 |

排序依 score 由高至低；若同分，依 `overdueHours` 由高至低，再依 `shipmentId` 遞增。結果只交由物流人員審閱，不呼叫任何 ERP 寫入介面。

## 工件、證據與決策的關係

```text
request → scenario → process model
                    ├─ semantic definitions (v1.0.0)
                    ├─ shipment snapshot + access decision
                    └─ decision service → read-only result → gate review
                                                       ↓
                                  proposed operating solution + first slice
```

`scenario-approval.json`、`process-validation.json` 與 `decision-test-report.json` 是本 demo 可檢查的合成證據，分別支撐 scenario、流程與 decision 的判定。`semantic-definitions.json` 為每個決策輸入提供 source mapping，並具名 semantic owner、source owner、metric owner 與最小 lifecycle；`access-decision.json` 只授權 demo scope 的 query 與 recommendation，並明確拒絕 controlled execution。

## 非目標與下一步

這不是 ERP 整合範例，也不是實際的企業核准紀錄。下一個可建置工作是 demo 的 context／decision contract 與不含 AI 的唯讀 review workbench。進入真實 process shadow 前，仍須取得可查驗的 process acceptance、baseline、source、identity、privacy、telemetry 與 support；只有 shadow 證明殘餘解釋負擔後，才決定是否建立 AI evaluation。若要再提升到回寫，還必須具備 controlled-execution 授權、稽核、冪等性、復原與 write adapter 證據，然後重新審查 G5。
