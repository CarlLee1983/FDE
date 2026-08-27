# 出貨延誤優先序：FDE 可重播範例

> **Synthetic demo only。** 本目錄中的人員、授權、資料、基線、核准與測試結果都是為了說明工件關係而虛構；不能據此推論任何企業已授權、已上線或已產生價值。

這個範例把一個「每天先處理哪些延誤出貨」的問題，先做現況流程診斷，再收斂成不依賴 AI 的目標流程：先驗證快照與必要欄位、分開正常與資料品質路徑、用確定性規則產生排序與 reason trace，最後交物流人員審閱。第一個交付切片不含 AI；只有 process shadow 證明仍有解釋或比較負擔時，才評估可拔除的 AI 實驗。ERP 的持久性回寫仍在 G5 被阻擋。

## 主要入口

直接開啟 [出貨延誤範例：從流程分析到可交付方案](index.html)。這個 standalone HTML 先說明現況問題、流程優化、無技術預設的目標流程、介入選擇、第一個垂直切片與 AI-fit 結論，再用「界定情境、畫出工作流程、定義資料語意、寫出決策規則、跑出唯讀結果、審查證據邊界」六個步驟交代方案依據。

完整文字版提案位於 [artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)。它清楚區分 demo 已證明的 deterministic core、仍待現場確認的流程診斷與目標流程，以及為什麼 AI 在第一切片被延後。

[企業 Process Shadow 準備包](artifacts/enterprise-shadow-preparation.md) 將這個 synthetic 範例轉成 process-framing workshop 可使用的決策前沿、證據需求、entry criteria 與 disposition persistence 選擇；它不是企業核准或真實 scenario。

以下 JSON 與 Markdown 只在需要追查原始證據或驗證規則時閱讀。

## 證據重播順序

1. 先讀 [artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)，確認流程診斷、目標流程、介入選擇、第一個切片與證據邊界。
2. 由 [request.md](request.md) 看使用者要解決的流程問題。
3. 由 [scenario.json](scenario.json) 看被核准的 demo scenario、可量測成果與來源／語意引用。
4. 對照 [artifacts/process-model.md](artifacts/process-model.md)、[artifacts/semantic-definitions.json](artifacts/semantic-definitions.json) 與 [artifacts/decision-service.json](artifacts/decision-service.json)，確認流程節點、定義與規則是一致的。
5. 由 [evidence/process-validation.json](evidence/process-validation.json) 確認 normal、exception 與 escalation path 已在 demo 中被角色驗證，再使用 [evidence/shipments.json](evidence/shipments.json) 的 snapshot，在 [evidence/access-decision.json](evidence/access-decision.json) 指定的 demo 權限內，手動計算優先序。
6. 使用 [scripts/validate-example.sh](scripts/validate-example.sh) 執行 scenario schema、replay tests、normal fixture contract、boundary/tie、stale、missing-field、access-denied 與 G1–G6 synthetic gate assertions。
7. 核對 [expected/read-only-result.json](expected/read-only-result.json)：它提供唯讀結果的完整契約：`result + semantic-definition version + source evidence + freshness + access decision`。
8. 最後閱讀 [expected/gate-review.md](expected/gate-review.md)，確認 demo 可用的證據只支撐 G1–G4，G5 與 G6 沒有被誤判為通過。
9. 若要帶入真實企業，使用 [artifacts/enterprise-shadow-preparation.md](artifacts/enterprise-shadow-preparation.md) 收集該企業自己的 process、owner、semantic、source、access、shadow 與 persistence 決策；不要複製 demo 核准。

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

## 一鍵驗證與 CLI replay

在 repository root 執行以下命令，可重播整個 synthetic slice；它只讀取本目錄 fixture／contract，且不建立、修改或提交任何企業資料：

```bash
examples/shipment-delay-priority/scripts/validate-example.sh
```

只輸出一份唯讀 JSON 時，明確傳入 snapshot、semantic、decision 與 access contract：

```bash
python3 examples/shipment-delay-priority/scripts/replay_shipment_delay_priority.py \
  --snapshot examples/shipment-delay-priority/evidence/shipments.json \
  --semantic-definitions examples/shipment-delay-priority/artifacts/semantic-definitions.json \
  --decision-service examples/shipment-delay-priority/artifacts/decision-service.json \
  --access-decision examples/shipment-delay-priority/evidence/access-decision.json \
  --as-of 2026-08-25T09:00:00Z
```

人員可在一次 CLI session 內加入 `--disposition SHP-1001=accepted`、`rejected` 或 `needs-investigation`。輸出會為每項 disposition 列出 Demo Logistics Coordinator 的下一個 accountable outcome；它標示為 `sessionDispositions.persistence: none`，不保存 feedback、也不改變 shipment、規則、語意或 access evidence。若 snapshot stale、query/recommendation access denied 或任何 contract 驗證失敗，帶 disposition 的 CLI 會以 non-zero 結束並清楚報錯，不會靜默忽略人工決定。

CLI 會 fail closed：四份 artifact 都必須維持已知的 synthetic scope、released semantic/source binding、decision input binding/rules、`controlledExecution: denied`、`demo-access-decision-001`、60-minute freshness SLA 與 non-persistent boundary。`Shipment.serviceLevel` 的 semantic `allowedValues` 必須恰為且依序為 `critical`、`standard`（extra、duplicate 或 drift 都拒絕）；`shipmentId` 必須是非空字串，`overdueHours` 必須是有限且非負的數字，兩個風險 flags 都必須是 boolean。每筆不合法資料會在讀取結果中以具名 escalation 顯示，不會進入排序。Freshness 以完整秒數比較：正好 60 分鐘仍 fresh，超過一秒即 stale，並同時輸出 `ageSeconds`，避免 `ageMinutes` 的顯示掩蓋超時。同一個 `shipmentId` 重複傳入 `--disposition` 會 non-zero 拒絕，不會採用最後一筆值。

## 工件、證據與決策的關係

```text
request → scenario → process model
                    ├─ semantic definitions (v1.0.0)
                    ├─ shipment snapshot + access decision
                    └─ decision service → read-only result → gate review
                                                       ↓
                                  operating solution + synthetic CLI validation
                                                       ↓
                                  enterprise shadow preparation (no approval)
```

`scenario-approval.json`、`process-validation.json` 與 `decision-test-report.json` 是本 demo 可檢查的合成證據，分別支撐 scenario、流程與 decision 的判定。`semantic-definitions.json` 為每個決策輸入提供 source mapping，並具名 semantic owner、source owner、metric owner 與最小 lifecycle；`access-decision.json` 只授權 demo scope 的 query 與 recommendation，並明確拒絕 controlled execution。

## 非目標與下一步

這不是 ERP 整合範例，也不是實際的企業核准紀錄。Repository 的 synthetic context／decision contract、唯讀 CLI replay 與 session-local disposition 已完成驗證；CLI 是正式的 synthetic validation seam，不代表正式使用者介面。下一步是依 [企業 Process Shadow 準備包](artifacts/enterprise-shadow-preparation.md) 取得真實 process acceptance、baseline、source、identity、privacy、telemetry、support 與 persistence 決定，而不是繼續擴充 demo UI 或 AI。只有 shadow 證明殘餘解釋負擔後，才決定是否建立 AI evaluation。若要再提升到回寫，還必須具備 controlled-execution 授權、稽核、冪等性、復原與 write adapter 證據，然後重新審查 G5。
