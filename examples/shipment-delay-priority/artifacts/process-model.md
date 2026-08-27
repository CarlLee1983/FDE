# Current and target process model

> **Synthetic demo only。** 人員、系統、問題與步驟僅描述此範例；現況診斷不是任何企業的現場觀察結果。

## Current-process hypothesis

```text
Daily export becomes available
  → coordinator opens and scans the file
  → coordinator mentally compares urgency signals across records
  → coordinator discovers stale or incomplete data while triaging
  → coordinator chooses an informal review order
  → coordinator decides follow-up outside this FDE scope
```

| Proposed problem | Effect to validate |
| --- | --- |
| Repeated manual comparison | Avoidable review time and inconsistent traceability |
| Entry readiness is not visible | Stale or incomplete data can consume triage effort |
| Normal and data-quality work are mixed | The coordinator must separate exceptions while ranking |
| Ranking reasons are not structured | A disagreement requires manual recalculation |

## Process changes before technology

1. Standardize snapshot identity, freshness, required fields, semantic version, and access decision as entry conditions.
2. Stop stale batches and route incomplete records to a separate data-quality escalation path.
3. Make the priority policy and tie-break explicit, deterministic, and traceable.
4. Present one review queue while keeping operational follow-up human-owned and outside the first slice.

## Technology-neutral target process

```text
Daily demo ERP export (read-only snapshot)
  → validate freshness, access, semantics, and required inputs
  → stop the stale batch or separate incomplete records
  → deterministically rank valid shipments with a reason trace
  → Demo Logistics Coordinator decides follow-up
  → manual ERP update remains outside this FDE capability
```

完成上述流程重設後，candidate FDE intervention node 才位於「daily export 已取得、物流人員尚未開始人工排序」之間。缺少決策必要欄位或資料超過 freshness SLA 時，流程輸出 escalation，而非推測分數或執行動作。

## Paths

| Path | Condition | Outcome |
| --- | --- | --- |
| Normal | snapshot fresh，且每個必要欄位都存在 | 產生 recommendation，交由人員審閱 |
| Exception | snapshot 超過 freshness SLA | 不計分，要求重新取得 snapshot |
| Escalation | 個別記錄缺少必要欄位 | 該筆不計分，送交 demo data-quality escalation |

這三條路徑、現況假設與目標變更已由 [process-validation.json](../evidence/process-validation.json) 中的合成角色在 demo scope 內接受；該紀錄不代表企業使用者驗收。

## Intervention candidates

| Need | Selected or deferred intervention |
| --- | --- |
| Entry readiness and data quality | Deterministic contract checks and explicit workflow paths |
| Priority comparison | Deterministic decision service |
| Evidence and disagreement | Structured review workbench with rule trace |
| Explanation or comparison in natural language | AI experiment deferred until a non-AI shadow exposes residual burden |
| ERP mutation | Governed action deferred until G5 evidence exists |

| 節點 | 輸入 | 輸出 | Authority |
| --- | --- | --- | --- |
| Demo shipment export | synthetic snapshot | shipment records + capturedAt | read-only query |
| FDE ranking | validated fields + semantic definitions | ranked recommendation or escalation | recommendation |
| Human review | ranked list | human decision | human-owned |
| ERP update | human decision | persistent shipment update | outside this demo; denied |
