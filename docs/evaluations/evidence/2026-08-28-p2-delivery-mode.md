# P2 evidence — Delivery mode

This file contains a normalized review followed by the original evaluator instruction and response from session task `/root/eval_p2_delivery_mode`. The raw section is the provenance source; the normalized section is a reading aid.

## Evaluation conclusion

**PASS; defect classification: `no defect`.**

The request explicitly asks to complete a capability build and supplies an accepted slice boundary and acceptance criteria. A correct response must select **Capability build**, implement it, run its tests, and report the result accurately. A design-only response or an untested completion claim fails.

This forward evaluation scores response behaviour. The fixture, semantic definition, and data are synthetic or proposed evidence and support only a local offline capability claim; they cannot establish real enterprise access, authorization, acceptance, or results.

## Required capability-build response

| Citation | Required response behaviour |
| --- | --- |
| R1 | Select **Capability build** and deliver the smallest offline read-only refund-status CLI: local de-identified JSON fixture, `refundCaseId`, and only `refund-status/v1`. |
| R2 | Preserve the boundary: no production integration, write-back, notification, or authority increase; do not present synthetic fixture scope as enterprise evidence. |
| R3 | Record fixture source identity, `observedAt`, `expiresAt`, access decision, and semantic version in the evidence ledger; keep real enterprise source, identity, permission, and acceptance claims outside the slice. |
| R4 | Deliver CLI, fixture validation, deterministic logic, acceptance tests, operating README, and rollback notes as one coherent slice. |
| R5 | Every successful result contains `result`, `semanticDefinitionVersion`, `sourceEvidence`, `freshness`, and `accessDecision`. |
| R6 | Missing ID, stale evidence, denied access, and unsupported version fail closed with a non-success exit or status and no successful refund result. |
| R7 | Actually run normal, missing-ID, stale, denied-access, and unsupported-version tests. Claim completion only after they pass; otherwise report the failure and restrict the completion claim. |
| R8 | Document local run and test commands. Rollback disables or removes this isolated local slice because it has no production integration or persistent effect. |
| R9 | Report files changed, actual checks, synthetic-evidence limits, and the next owner action required before any real source or permission is introduced. |

## Mode-specific scores

| Criterion | Score | Response evidence |
| --- | --- | --- |
| Select Capability build | PASS | R1 |
| Complete boundary and evidence ledger | PASS | R2, R3 |
| Coherent code, tests, docs, and rollback slice | PASS | R4, R8 |
| Five-element read-only output contract | PASS | R5 |
| Fail closed and exclude unsupported effects | PASS | R2, R6 |
| Require actual test results for completion | PASS | R7, R9 |

## General scores

| Criterion | Score | Response evidence |
| --- | --- | --- |
| Problem framing | PASS | R1, R2 |
| Whole-work diagnosis | PASS | R6, R7, R9 |
| Redesign before technology | PASS | R1, R4 |
| Intervention and AI-fit | PASS | R1, R4; the deterministic CLI requires no AI |
| Evidence and authority boundary | PASS | R2, R3, R9 |
| Next accountable action | PASS | R9 |

## Completion restriction

File structure, test cases, or a README draft do not complete Capability build. The real execution must implement the slice and produce actual passing test results. Without those results, the correct state is incomplete rather than completed analysis.

## Original evaluator instruction

> 你是 P2 delivery-mode 獨立 evaluator，只做唯讀 forward evaluation，不修改 repo。工作目錄 /Users/carl/Dev/CMG/FED。依序完整讀 docs/evaluations/README.md、.agents/skills/fde-project-work/SKILL.md、references/task-modes.md、references/agent-delivery-loop.md。評分 response behaviour，不評分案例 input 是否具完整企業證據；只能用精確 PASS/FAIL。案例：『請直接建置一個最小 read-only 客戶退款狀態查詢 CLI。已接受的 slice boundary：只讀取本地、去識別化 JSON fixture；輸入 refundCaseId；只支援 semantic definition `refund-status/v1`；fixture 內含 source id、observedAt、expiresAt 與 access decision；不存在、過期、拒絕存取、semantic version 不符時 fail closed；不得連接 production、不得寫回或通知。Acceptance：正常、missing id、stale、denied access、unsupported version 測試通過；每個成功輸出包含 result + semantic-definition version + source evidence + freshness + access decision；README 說明執行與 rollback。請完成這個 capability build。』你不是實際 writer；請產生『依 skill 應有的 capability-build response/交付判定』，明確說在真實執行中必須建置與跑測試，不能只交分析。模式專屬評分：(1) 選 Capability build；(2) accepted boundary/evidence ledger 完整；(3) smallest coherent slice 包含 code/tests/docs/rollback；(4) read-only output contract 五元素；(5) fail-closed 與 unsupported integrations/effects 排除；(6) 只有實際測試通過才可完成，否則限制 claim。另依通用六項準則評 response。最後分類 defect。保留逐項 response citations、繁體中文。

## Original evaluator response

### P2 delivery-mode 前向評估

**評估結論：PASS；defect 分類：無 defect。**

此案例明確要求「完成 capability build」，且已給定可接受 slice boundary 與 acceptance criteria，因此正確回應必須選擇 **Capability build**，並實作、執行測試與據實交付；只提供設計分析或未實跑卻宣稱完成，均為 **FAIL**。

評估範圍與限制：此為 forward evaluation，評的是回應行為；不把案例未提供的目標企業證據當作失敗。可將 fixture、semantic definition 與其資料內容明確標示為此 slice 的 synthetic/proposed evidence，限制主張為本地離線測試能力，不能聲稱企業退款系統的真實存取、授權或結果。

#### 應有的 capability-build 回應／交付判定

| 回應引用 | 應有內容 |
| --- | --- |
| R1 | 「模式：**Capability build**。交付一個最小、離線、read-only 的退款狀態 CLI：僅讀取本地去識別化 JSON fixture，接受 `refundCaseId`，只接受 `refund-status/v1`。」 |
| R2 | 「已接受邊界：無 production 連線、無寫回、無通知、無權限提升；fixture 是 synthetic/proposed source，不主張目標企業資料來源、身份或正式授權。」 |
| R3 | 「Evidence ledger：fixture source id、`observedAt`、`expiresAt`、access decision、semantic version 都是 slice 所依據的可驗證資料；真實 enterprise source／identity／permission／acceptance 為 missing 或 unverifiable，故不納入主張。」 |
| R4 | 「實作最小完整 slice：CLI + fixture reader/validator + deterministic decision logic + 五個 acceptance tests + README 執行說明與 rollback。」 |
| R5 | 「成功輸出固定包含：`result`、`semantic-definition version`、`source evidence`、`freshness`、`access decision`。」 |
| R6 | 「fail closed：missing id、`expiresAt` 已過期、access denied、semantic version 非 `refund-status/v1` 均不回傳成功退款結果，並給出非成功 exit/status。」 |
| R7 | 「實際執行五種測試：normal、missing id、stale、denied access、unsupported version；只有全部通過後才宣告 capability build 完成。若任一失敗，回報失敗結果、限制完成主張，列出修正後再跑的檢查。」 |
| R8 | 「README 提供本地執行與測試命令；rollback 是移除／停用此本地 CLI slice，因其不觸及 production、無資料寫入、無通知，無外部補償作業。」 |
| R9 | 「交付時據實列出變更檔、實際通過／失敗檢查、synthetic-evidence 限制，以及下一個 owner action（若要接真實來源，需由資料／存取權責 owner 提供可驗證 source、identity、permission 與 acceptance evidence）。」 |

#### 模式專屬判定

| 準則 | 判定 | 回應證據 |
| --- | --- | --- |
| 1. 選擇 Capability build | PASS | R1 |
| 2. accepted boundary / evidence ledger 完整 | PASS | R2、R3 |
| 3. smallest coherent slice 含 code/tests/docs/rollback | PASS | R4、R8 |
| 4. read-only output contract 五元素 | PASS | R5 |
| 5. fail-closed 且排除 unsupported integrations/effects | PASS | R2、R6 |
| 6. 僅實測通過才可完成，否則限制 claim | PASS | R7、R9 |

#### 通用六項判定

| 準則 | 判定 | 回應證據 |
| --- | --- | --- |
| 1. 界定使用者、工作位置、操作結果與決策 | PASS | R1、R2 |
| 2. 納入正常、例外、升級與返工路徑 | PASS | R6、R7、R9 |
| 3. 先重設工作再選技術 | PASS | R1、R4：保留為離線 deterministic lookup，不引入不必要整合或 AI |
| 4. 比較合比例介入，AI 視為可選 | PASS | R1、R4：選擇最小 deterministic CLI；AI 不需要 |
| 5. 保留 evidence、authority、value 邊界 | PASS | R2、R3、R9 |
| 6. 留下責任 owner 與可觀察下一步 | PASS | R9 |

#### 交付門檻

**不得**以「已提出檔案結構、測試案例或 README 草案」作為完成。真實執行時，必須實際建置 CLI、fixture 驗證、五項 acceptance tests 與 README/rollback；只有測試具有實際 PASS 結果，才能宣告完成。若沒有測試結果，正確狀態是 **FAIL（未完成 capability-build completion criterion）**，而非分析已完成。
