# 合成帳務對帳：先重作業流，再選技術

> 此文件是通用、合成的設計假說。目標企業的 owner、現況、來源權威、存取權、基線、目標與驗收均為 `missing` 或 `unverifiable`；以下 target flow 均為 `proposed`。

## As-is 假說與先做的改變

| 路徑 | 假設的現況問題 | 先於技術的處理 |
| --- | --- | --- |
| 正常 | 操作員下載兩份資料、手動篩選、逐筆比 reference、版本、日期、金額與幣別 | 移除重複比對；標準化版本化 reference、日期、整數 minor units 與 currency；一次輸出精準 match。 |
| 例外 | 缺資料、金額不同、只存在單邊資料時，理由散落在試算表註記 | 將這些固定分類為具原因的 human review queue，而非在正常清單中猜測或重複處理。 |
| 升級 | 資料過期、來源互相衝突或存取不清時，仍可能繼續人工比對 | 定義批次 stop：新鮮度、來源一致性、access binding、有效 ID 與無重複 ID 任一失敗即 fail closed。 |
| Rework | 不清楚前次比對版本或誰應處理差異，導致重跑與重覆追問 | 保留 snapshot 時間與來源證據；由人負責 residual disposition，這個 slice 不保存 disposition。 |

這個優先序是：**移除**手動重複篩選、**簡化**為單一 bounded snapshot、**標準化** identity／金額／幣別與例外原因、**明確化**人員責任，才加入穩定的確定性程式。

## Proposed target flow 與責任

```text
單一帳戶、單一幣別、單一已關帳期間的兩個不可變唯讀來源
  -> 驗證來源、控制總數、時效、資料形狀、ID 唯一性與 local access binding
  -> 任一批次控制失敗：停止，回傳無結果
  -> 一對一精準比對 (reference + referenceVersion + amountMinor + currency + bookingDate)
  -> exact matches / 人工 review queue（ambiguous、amount mismatch、unmatched）
  -> 人類操作員在外部既有流程判斷與處理
```

| 責任 | 配置 | 邊界 |
| --- | --- | --- |
| source、freshness、access、資料驗證與 exact matching | 確定性 replay | 唯讀；不寫檔、不連線、不寫回。 |
| residual 的業務判斷與升級 | 人類操作員 | 目標企業 owner 與責任分派為 `missing`。 |
| 流程、語意、閾值與 access 的接受 | 目標企業 accountable owner | `missing`；不得從此範例推論。 |
| persistent system action | 不做 | writeBack 永遠 `false`。 |

## AI fit、slice 與驗證

第一個 slice **沒有 AI**：exact matching 及所有控制是明確且可重播的，使用模型不增加價值。多候選絕不 tie-break，而是 abstain。只有在完成這個非 AI 基線後，仍有經 evidence 證實的非結構化描述、模糊付款參考或跨文件解釋負擔，才可將 AI 作為「對 residual ambiguity 提出可拒絕的建議」而非自動決策的後續提案。

這個 slice 的驗證為 synthetic：golden replay、exact、ambiguous、unmatched、stale、denied/mismatched access、duplicate IDs、determinism、no-write 與 source totals tests。通過只證明 repository fixture 的行為，不能證明 target-enterprise value、安全、權限、整合、基線或接受。目標企業仍缺少 manual touches/100、cycle time、exception age、false-match/withdrawal、rework 與 close delay 的基線與目標；matched coverage 單獨不足以宣稱價值。下一個 accountable action 是由目標企業 process owner 提供並驗證上述缺失證據，才可決定是否進行 shadow。
