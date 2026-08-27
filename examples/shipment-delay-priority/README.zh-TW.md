# 出貨延誤優先序：最小可重播 FDE 範例

> **Synthetic demo only。** 所有人員、資料、授權、基線、目標與結果都是 repository fixture；不能據此推論任何企業已授權、可上線或已產生價值。

這個範例只證明一件事：一位具名的合成物流使用者，可以在具名情境與唯讀權限內，從新鮮且語意完整的出貨快照取得確定性排序、原因與資料品質 escalation。它不使用 AI、不保存人工 disposition，也不執行 ERP 回寫。

## 三步使用

1. 驗證整個範例：

   ```bash
   examples/shipment-delay-priority/scripts/validate-example.sh
   ```

2. 產生預設 fixture 的唯讀結果：

   ```bash
   python3 examples/shipment-delay-priority/scripts/replay_shipment_delay_priority.py
   ```

3. 需要理解流程、控制與 Gate 時，閱讀 [case-analysis.md](artifacts/case-analysis.md)；需要機器可讀的結論時，查看 [assurance.json](evidence/assurance.json)。

## 會得到什麼

正常 fixture 會得到三筆 recommendation：

| Shipment | 分數 | 主要原因 |
| --- | ---: | --- |
| SHP-1001 | 90 | 逾期至少 48 小時、critical、customer commitment at risk |
| SHP-1002 | 65 | 逾期至少 24 小時、temperature controlled、customer commitment at risk |
| SHP-1003 | 35 | 逾期少於 24 小時、critical |

缺少 `overdueHours` 的 SHP-1004 會進入 escalation，不會被猜測或計分。輸出同時包含：

```text
result + semantic-definition version + source evidence + freshness + access decision
```

下列任一情況會 fail closed，不產生 recommendation：

- snapshot stale；
- query 或 recommendation 被拒絕；
- request actor 或 scenario 與 access decision 不符；
- `shipmentId` 重複；
- semantic、source、decision 或 non-persistent contract drift。

## 可選操作

預設 CLI 已綁定本範例的 fixture、`2026-08-25T09:00:00Z` 查詢時間、合成 actor 與 scenario。測試或除錯時仍可用 `--snapshot`、`--semantic-definitions`、`--decision-service`、`--access-decision`、`--as-of`、`--actor` 與 `--scenario` 明確覆寫。

一次 CLI session 可加入：

```bash
--disposition SHP-1001=accepted
--disposition SHP-1002=rejected
--disposition SHP-1003=needs-investigation
```

Disposition 只出現在本次輸出，固定標示 `persistence: none`。前置條件失敗、shipment 未被推薦、值不支援或同一 shipment 重複 disposition 時，CLI 會 non-zero 結束。

## 核心檔案

| 檔案 | 責任 |
| --- | --- |
| [scenario.json](scenario.json) | 情境、使用者、決策、成果與 synthetic scope |
| [case-analysis.md](artifacts/case-analysis.md) | 現況假設、目標流程、介入、控制、Gate 與下一步 |
| [semantic-definitions.json](artifacts/semantic-definitions.json) | 語意、identity、state、metric、source owner 與 mappings |
| [decision-service.json](artifacts/decision-service.json) | 確定性規則、input bindings、escalation 與輸出限制 |
| [access-decision.json](evidence/access-decision.json) | actor、scenario、source、freshness 與 permission binding |
| [shipments.json](evidence/shipments.json) | 合成來源 snapshot |
| [read-only-result.json](expected/read-only-result.json) | golden output contract |
| [assurance.json](evidence/assurance.json) | synthetic evidence ledger 與 G1–G6 結論 |

## 邊界

目前只支援合成範例的 query 與 recommendation。G5 仍為 `missing`，因此沒有 controlled execution、audit、idempotency、recovery 或 ERP adapter；G6 仍為 `unverifiable`，因此不能聲稱 45→15 分鐘改善、真實 adoption 或 production value。

若要進入真實企業，必須以該企業自己的 owner、process acceptance、semantics、source、identity、privacy、access、persistence、telemetry、support、baseline、rollback 與 acceptance evidence 取代所有 fixture。不要複製本範例的 synthetic 狀態作為企業授權。
