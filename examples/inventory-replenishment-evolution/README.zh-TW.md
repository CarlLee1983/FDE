# 庫存補貨能力演進：從 AI 探索到受治理工具

> **Synthetic demo only。** 本案例的人員、數字、資料來源、權限、基線與結果都是為了說明方法而虛構。它不能證明任何企業已經核准、上線或得到效益。

這個案例回答一個常見問題：傳統程式只能等庫存低於安全量才通知；FDE 能不能先用 AI 處理尚未整理清楚的分析需求，提早提出補貨建議與進貨單草稿，再把已經證明穩定的部分寫成正式工具？

案例的答案不是「永遠讓 AI 做所有事情」，也不是「工具完成後把 AI 拿掉」。它採用兩條同時運作的迴路：

- **營運迴路**處理每天已知、可重複、需要穩定結果的工作。
- **演進迴路**讓 AI 觀察例外、人工修改與結果偏差，提出下一個改善候選。

當候選方法被證據支持並由負責人接受，它才會被寫成有版本、有測試、可監控、可回復的工具。AI 接著使用這些工具，把注意力移到下一個尚未解決的缺口。

## 主要入口

- 適合展示與講解：[index.html](index.html)
- 詳細案例與交付方案：[artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)
- 原始需求：[request.md](request.md)
- 提議中的 scenario record：[scenario.json](scenario.json)
- 可執行的唯讀 baseline：[補貨決策契約](artifacts/replenishment-decision-contract.md)

## 可執行的唯讀補貨清單

此案例現在包含一個不使用 AI、只使用 Python 標準函式庫的 deterministic baseline。它只讀取本地 synthetic JSON snapshot，計算「補貨到達日」的預計庫存，並產生供人員審閱的候選量；不連接、建立、修改、核准或提交任何採購系統資料。

在 repository root 執行：

```bash
examples/inventory-replenishment-evolution/scripts/validate-example.sh
```

只重播 fixture 並將結果印到終端：

```bash
python3 examples/inventory-replenishment-evolution/scripts/recommend_replenishment.py \
  examples/inventory-replenishment-evolution/fixtures/replenishment-snapshot.json
```

輸入必須有固定的 `asOf`、semantic definition version、明確標示非企業授權的 synthetic access profile、三個必要來源的 evidence/freshness、已實作的 policy version/review period，以及每個 SKU 的現有量、保留量、每日需求、安全庫存、交期、確認會在補貨到達日前抵達的在途量、MOQ 和 pack size。若 access 不符、policy 未支援、來源衝突／缺失／過期，整份結果會 `abstained`；單一 SKU 資料無效時，只有該 SKU abstain。

輸出固定包含 `result`、semantic definition version、source evidence、freshness、access decision、policy、未評估的不確定性和明確的 `writeBack: false` 邊界。這只是 proposal 中 deterministic baseline 的子切片，尚未包含 planner feedback 與進貨單草稿。正常 fixture 展示候選、無候選、以及「到貨時剛好等於安全庫存」的邊界；另一份 fixture 展示過期來源的全體 abstain。這些都是 synthetic/local-only 測試資料，不能當成企業資料、授權或採購指令。

## 一分鐘理解

舊流程只有一條固定規則：`庫存低於 80 → 通知人員`。它簡單可靠，但看不到銷售變快、促銷即將開始、供應商交期變長或在途庫存延誤。

條件性的新流程先每天檢查未來的庫存壓力。流程與 baseline 經真實 owner／使用者確認後，才評估由 AI 助手組合允許使用的資料、解釋異常並產生補貨建議與進貨單草稿；採購人員核准、修改或拒絕。系統保留修改原因。當同一種修正反覆發生，例如每次促銷都要加上相同的需求調整，就將它提升為正式工具，而不是每次重新問 AI。

## 案例中的簡化數字

商品 A 現有 120 件，最近每日平均賣出 10 件，供應商交期是 10 天，另有 50 件在途。只看安全庫存 80 件時，系統不會通知。但下週有促銷，去年同期每日曾賣出 18 件，因此「現在看起來安全」不代表「補貨到達前仍然安全」。

案例中的 AI 可以整理這些因素並提出：商品 A 可能在補貨到達前進入壓力區間，建議人員審閱一個補貨量範圍。這個數字只是示範輸出形狀，不是已核准的企業政策。

## 最重要的責任邊界

| 工作 | 最適合的負責者 |
| --- | --- |
| 排程、資料取得、權限與新鮮度檢查 | 確定性軟體 |
| 已穩定的公式、門檻、預測和採購限制 | 版本化工具或模型 |
| 跨來源整理、解釋異常、發現重複人工修正 | AI 助手 |
| 接受政策、處理模糊例外、核准進貨單 | 人類負責人 |
| 正式寫入採購系統 | 經授權、可稽核、冪等且可復原的系統行動 |

AI 可以準備草稿，不能自行核准或提交。AI 可以提出工具變更，不能自行修改正式政策或在沒有驗證時發布新版本。

## 這個案例要驗證什麼

1. FDE 是否能把被動告警改成提前發現風險的決策支援。
2. AI 是否能在需求還沒完全結構化時帶來增量價值。
3. 人工修改是否能留下原因，成為下一輪改善證據。
4. 穩定做法是否能被提升為共享工具，而不是永遠留在 prompt 裡。
5. 工具化後，AI 是否仍能負責例外、解釋與能力演進。
6. 任何進貨單寫入是否仍遵守核准、權限、稽核與復原邊界。

## 證據狀態

本案例目前是 `proposed`，AI selection 是 `deferred`。真實流程負責人、使用者驗證、來源權限、資料品質、歷史基線、補貨政策、AI 增量價值和採購系統控制全部是 `missing` 或 `unverifiable`。因此目前只能用來解釋與演練方法，不能宣稱已通過 FDE gates 或可直接進入企業上線。

## 建議的第一個真實工作包

先選擇 10–30 個商品，用可重播的非 AI baseline 進行唯讀 shadow，確認流程、資料與人工理由紀錄可信。Readiness 通過後，才在同一批決策加入條件性 AI shadow，比較它是否真的帶來增量價值；全程不寫入採購系統。之後只挑一種重複、穩定且能被測試的修正，建立第一個版本化工具，再比較工具前後的結果。
