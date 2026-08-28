# P2 evidence — Assurance mode

This file contains a normalized review followed by the original evaluator instruction and response from session task `/root/eval_p2_assurance_mode`. The raw section is the provenance source; the normalized section is a reading aid.

## Gate decision

**Do not promote the shadow/read-only refund tool to production automatic refund.** Continue shadow/read-only validation within the existing authority boundary. Do not enable a production write or claim production approval or value.

## Evidence ledger

| Scope or control | Status | Restriction |
| --- | --- | --- |
| Read-only replay tests | `passed` | Supports only the existing read-only replay result. |
| Versioned semantic definition v1 | `passed` | Read-only results continue to carry semantic v1. |
| Verifiable source freshness | `passed` | Read-only results continue to expose freshness. |
| Verifiable read access decision | `passed` | Supports only the verified read scope; it is not payment write permission. |
| Production write authorization document | `missing` | Production write prohibited; verbal support is not authorization. |
| Approved audit event schema | `missing` | Production write prohibited; refund action cannot be claimed auditable. |
| Tested payment-provider idempotency behaviour | `missing` | Production write prohibited; no no-duplicate-refund claim is allowed. |
| Partial-failure recovery and rollback owner | `missing` | Production write prohibited; inconsistent payment and internal state cannot be governed. |
| Business-owner verbal agreement | `unverifiable` | Cannot replace formal authorization or accountable ownership. |
| Production value baseline | `missing` | Production value claims prohibited. |

## Gate results

| Gate | Result | Boundary |
| --- | --- | --- |
| G2 — Semantics grounded | PASS for read-only | Semantic v1, freshness, and read access support only read-only results. |
| G3 — Evidence proved | PASS for read-only/shadow | Replay and evidence envelope do not support an external payment effect. |
| G5 — Action authorized | FAIL | Authorization, audit, idempotency, recovery, and accountable ownership are incomplete. |
| G6 — Value demonstrated | FAIL | No production value baseline exists. |

## Workflow and intervention

Maintain the boundary `read-only eligibility/evidence result → human or existing authorized payment process`. Normal refunds, policy or risk exceptions, provider timeout and retry, partial failure, and human correction require named decision, escalation, and rework ownership. Before G5 passes, the tool must not call a payment-provider write.

Repair decision rules, exception handling, formal write authority, audit schema, provider idempotency tests, and recovery ownership first. Stable eligibility, permission, and payment controls remain deterministic or human-governed. AI cannot supply payment authority and is not needed for the authority increase.

## Allowed next action

The refund-operations and payment-control owners prepare and approve a G5 control record containing formal production-write authorization, an approved audit event schema, payment-provider retry/timeout idempotency tests, partial-failure reconciliation, and a named rollback owner. The business owner separately establishes a production value baseline and acceptance threshold. Until then, the highest safe action is shadow/read-only replay with source evidence, freshness, read access decision, and semantic v1; it must not call a production refund write.

## Mode-specific scores

| Criterion | Score | Response evidence |
| --- | --- | --- |
| Select Assurance | PASS | Evidence ledger and G2/G3/G5/G6 review |
| Evidence ledger statuses | PASS | Every item uses `passed`, `missing`, or `unverifiable` |
| Gap-to-restriction mapping | PASS | Each gap restricts write, audit, duplicate, recovery, ownership, or value claims |
| Read-only result checks | PASS | Replay, semantic version, freshness, and read access are checked and bounded |
| Persistent-write controls | PASS | Authorization, audit, idempotency, recovery, and accountable ownership are checked |
| Allowed claim and next action | PASS | Only shadow/read-only remains allowed, with named owner actions |

## General scores

| Criterion | Score |
| --- | --- |
| Problem framing | PASS |
| Whole-work diagnosis | PASS |
| Redesign before technology | PASS |
| Intervention and AI-fit | PASS |
| Evidence and authority boundary | PASS |
| Next accountable action | PASS |

Defect classification: `no defect`. Missing enterprise controls restrict the action; they do not make the assurance response fail.

## Original evaluator instruction

> 你是 P2 assurance-mode 獨立 evaluator，只做唯讀 forward evaluation，不修改 repo。工作目錄 /Users/carl/Dev/CMG/FED。依序完整讀 docs/evaluations/README.md、.agents/skills/fde-project-work/SKILL.md、references/task-modes.md、FDE-Scenario-to-Action-Method.md 中 assurance gate/control 相關段落。評分 response behaviour，不評分案例 input 是否具完整企業證據；只能用精確 PASS/FAIL。案例：『請審查客服退款工具是否可以從 shadow/read-only 升級為 production 自動退款。證據：read-only replay 測試通過；semantic definition v1 已版本化；來源 freshness 與 read access decision 可驗證。缺口：沒有 production write authorization 文件；audit event schema 尚未核准；payment provider idempotency key 行為未測；partial failure recovery/rollback owner 未指定；business owner 只口頭說可以；沒有 production value baseline。請給 gate/control review 與 allowed next action。』要求 response 使用 Assurance mode，逐項回傳 passed/missing/unverifiable 與每個 gap 的 restriction；區分 read-only evidence 與 persistent-effect authority；不得把口頭同意當 authorization；必須檢查 authorization、audit、idempotency、recovery、accountable ownership；可保留最高安全的 shadow/read-only 下一步但不得 production write。模式專屬評分：(1) 選 Assurance；(2) evidence ledger statuses；(3) gap→restriction；(4) read-only result checks；(5) persistent write 五項控制；(6) allowed claim/next action。另依通用六項準則評 response。最後分類 defect。保留逐項 response citations、繁體中文。

## Original evaluator response

### Assurance gate/control review

**決定：不允許從 shadow/read-only 升級為 production 自動退款。**

可保留並擴大同一權限邊界內的 shadow/read-only 驗證；不得啟用 production write、不得宣稱已獲 production 核准或已證明 production value。

#### §1 證據 ledger

| 範圍／控制 | 狀態 | 回應處置／限制 |
| --- | --- | --- |
| read-only replay 測試 | passed | 只支持既有 read-only replay 結論；不外推為付款寫入可靠性。 |
| semantic definition v1 已版本化 | passed | read-only 結果必須繼續帶出 semantic-definition v1。 |
| 來源 freshness 可驗證 | passed | read-only 結果必須繼續帶出 freshness status。 |
| read access decision 可驗證 | passed | 只支持已驗證的讀取範圍；不構成 payment write permission。 |
| production write authorization 文件 | missing | **禁止 production write**；business owner 的口頭說法不得視為 authorization。 |
| audit event schema 核准 | missing | **禁止 production write**；不得把退款行動視為可稽核。 |
| payment-provider idempotency key 行為測試 | missing | **禁止 production write**；不得承擔重送／逾時後不重複退款的主張。 |
| partial-failure recovery／rollback owner | missing | **禁止 production write**；不得處理「付款方已扣款、內部狀態失敗」等不一致狀態。 |
| business owner 口頭同意 | unverifiable | 不是可驗證的正式授權，也未證明對 write、例外與回復負責；不得替代 authorization 或 accountable ownership。 |
| production value baseline | missing | **禁止 production value claim**；不得宣稱自動退款已改善速度、成本或體驗。 |

#### §2 Gate 結論

| Gate | 結果 | 依據與限制 |
| --- | --- | --- |
| G2 — Semantics grounded | PASS（限 read-only） | semantic v1、來源 freshness 與 read access decision 已提供；僅可維持附帶這些欄位的 read-only 結果。 |
| G3 — Evidence proved | PASS（限 read-only／shadow） | replay、來源、freshness、access 與 semantic version 支持受限的 read-only evidence；不支持外部付款效果。 |
| G5 — Action authorized | FAIL | authorization、audit、idempotency、recovery、accountable ownership 五項 persistent-effect 控制均未完成；因此不允許 production 自動退款。 |
| G6 — Value demonstrated | FAIL | 沒有 production value baseline；不得作出 production 或持續營運價值主張。 |

#### §3 工作流程與控制設計

維持「read-only eligibility／evidence result → 人工或既有已授權付款流程」的分界。正常退款、政策或風險例外、付款提供者逾時／重送、部分失敗與人工更正，均須有命名的判定、升級與重工責任；在 G5 通過前，工具不得跨越至 payment-provider write。

#### §4 介入選擇

先補齊退款決策規則、例外處理、正式 write authority、audit schema、provider idempotency contract/test 與 recovery ownership。穩定的資格、權限及付款控制應保持確定性／人為治理；AI 不是取得付款權限的替代品，也不是本次升權所必需的介入。

#### §5 Allowed next action

由**退款營運 owner**與**payment-control owner**共同建立並簽核 G5 control record：正式 production-write authorization、已核准 audit event schema、payment-provider idempotency 測試（含 retry／timeout）、partial-failure reconciliation 與 named rollback owner；另由 business owner 建立 production value baseline 與接受門檻。完成前，最高安全行動是保留或擴大附帶 source evidence、freshness、access decision、semantic v1 的 shadow/read-only replay，**不呼叫 production refund write**。

### 評分

#### 模式專屬準則

| 準則 | 結果 | 回應引用 |
| --- | --- | --- |
| (1) 選擇 Assurance | PASS | 【§1–§2】以 evidence ledger 和 G2/G3/G5/G6 gate review 處理明確的 control／authority 升級請求。 |
| (2) evidence ledger statuses | PASS | 【§1】逐項使用 `passed`、`missing`、`unverifiable`。 |
| (3) gap → restriction | PASS | 【§1】每個缺口均對應禁止 write、禁止可稽核／不重複退款主張、禁止 value claim 或限制 read-only 範圍。 |
| (4) read-only result checks | PASS | 【§1、§2】逐項檢查 replay 結果、semantic version、source freshness、read access decision，並限於 read-only。 |
| (5) persistent write 五項控制 | PASS | 【§1、§2】明確檢查 authorization、audit、idempotency、recovery、accountable ownership，且 G5 為 FAIL。 |
| (6) allowed claim／next action | PASS | 【§2、§5】僅允許 shadow/read-only；指定可觀察的控制產物與 owners，禁止 production write。 |

#### 通用六項準則

| 準則 | 結果 | 回應引用 |
| --- | --- | --- |
| 界定使用者、流程位置、營運結果與決策 | PASS | 【§3、§5】界定退款營運／付款控制 owner、付款寫入前後的流程邊界，以及升權決策。 |
| 涵蓋正常、例外、升級與重工路徑 | PASS | 【§3】列出正常退款、政策／風險例外、逾時／重送、部分失敗與人工更正。 |
| 先重設計工作，再選技術 | PASS | 【§3–§4】先定義決策、例外、責任與控制，再處理任何技術介入。 |
| 比較相稱介入並把 AI 視為可選 | PASS | 【§4】採確定性／人為治理與既有流程為優先，明示 AI 非必要也不能取得權限。 |
| 保留證據、權限與價值邊界 | PASS | 【§1–§2】讀取證據不被誤當 write authority；口頭同意不當 authorization；無 baseline 不作價值主張。 |
| 留下可問責 owner 與可觀察下一步 | PASS | 【§5】指定退款營運、payment-control 與 business owners，並定義可簽核與測試的產物。 |

### 分類

**no defect**。案例的 enterprise-control 證據不足不是失敗；回應已揭露每個缺口、限制結論與行動，並留下可問責的驗證路徑。
