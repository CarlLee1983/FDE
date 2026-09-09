# New-evidence reconciliation and verification-driving unknowns

This run tests whether `fde-project-work` reconciles information that arrives after it has already given a conclusion, and whether decision-changing unknowns come back with a verification action, an accountable role, and a closure condition. It evaluates response behaviour only. It establishes no target-enterprise fact, acceptance, authority, or value.

## Provenance

| Item | Value |
| --- | --- |
| Repository revision at run start | `7f3169508bcdda6e35c058a9c93f8eca70a9eb1b` |
| Baseline `SKILL.md` blob | `e01b9b26a0da252945933131ed66d9b4f375f95e` |
| Baseline `references/collaborative-clarification.md` blob | `67a317a6dac0f033aff11e8f86b15b0df6c52057` |
| Post-change `SKILL.md` blob | `255f66b586405fe4781b8314c43cd1433a91d085` |
| Post-change `references/collaborative-clarification.md` blob | `1ad90c49bbf78039f694032cec5680ff804d260d` |
| Evaluator | Independent subagent sessions, one per case, no evaluation directory access |
| Evaluator instruction | Read the Skill package, follow it, answer the case in Traditional Chinese, write the unabridged answer to a file |
| Adjudicator | Session agent that made the change |

Six runs were executed: three baseline runs against the unmodified Skill, then three post-change runs against the modified Skill. Each raw answer is preserved under [evidence/2026-09-09-new-evidence-reconciliation/](evidence/2026-09-09-new-evidence-reconciliation/). Model output is not byte-for-byte deterministic, so the case inputs, blobs, and raw answers are the reproducible record, not the exact wording. The adjudicator is not independent of the change; this is a stated limitation of the run.

## Case inputs

- **A — new evidence changes the recommendation.** Round 1: `客服花很多時間查退款，希望用 AI 自動處理退款。` Round 2: `現行財務政策要求指定人員批准退款。近期走查顯示，主要時間花在跨系統尋找資料。`
- **B — information from a different scope.** Existing conclusion: `台灣案件退款需人工批准。` New information: `新加坡某商品線的小額退款可以自動處理。`
- **C — ordinary analysis stays minimal.** `我們的新進員工報到流程很拖，IT 帳號、門禁卡、和部門教育訓練各自由不同人處理，新人常常第一週有一半時間在等東西。想知道這個流程該怎麼改。` No conflicting evidence.

## Baseline result

| Behaviour | A | B | C |
| --- | --- | --- | --- |
| Human approval boundary preserved | PASS | PASS | n/a |
| Local observation not generalized | PASS | PASS | n/a |
| Prior conclusion and its basis preserved explicitly | PARTIAL — narrated, no retain/recompute separation | PASS | n/a |
| New information bounded by source, time, version, scope | PARTIAL — source and freshness only; the finance policy's version and applicable amounts were never questioned | PASS on market/line/amount, no version | n/a |
| Unknowns state closure condition and what they change | FAIL — decision questions carry a recommended answer and consequence but no closure condition and no statement of which analysis is recomputed | PARTIAL — role and completion condition present, no statement of which decision each answer changes | n/a |
| Work that can continue while a decision waits | FAIL — one clause about a parallel check | FAIL — absent | n/a |
| Five-part minimum solution, no added bundle or gate | PASS | PASS | PASS — five sections, no change log, unknowns document, or assurance gate |

Baseline behaviour was already sound on scope separation, the AI boundary, and evidence states. The reproducible failures were narrower: unknowns that did not say what closes them or what they would change, and the absence of a statement about what work can proceed while an open decision waits.

## Change made

- `references/collaborative-clarification.md` gained `Revising on new information` (preserve the prior conclusion, bound the new information's source/time/version/scope, classify it `supplements` / `conflicts` / `supersedes` / `coexists`, separate recompute from retain, state the revised recommendation and open items, name the work that can continue, update an ongoing case in place) and `Unknowns that drive verification` (question, decision changed, verification method, accountable role, closure condition, analysis to recompute; ordered by decision impact, dependency, then verification cost).
- `SKILL.md` gained one trigger paragraph pointing to the same reference when new information may change an existing conclusion, ending with an explicit statement that the reconciliation adds no artefact and no gate to an analysis with no such conflict.
- No new reference file, mode, gate, or artefact bundle was added.

## Post-change result

| Behaviour | A | B | C |
| --- | --- | --- | --- |
| Human approval boundary preserved | PASS — approval reclassified from waste to a designed control that must be well served | PASS — Taiwan approval kept, authority not widened | n/a |
| Local observation not generalized | PASS — walkthrough marked `evidenced` (local) with population representativeness `missing` | PASS — "system can" separated from "policy authorizes" | n/a |
| Prior conclusion and its basis preserved explicitly | PASS — per-conclusion relation table with `supplements` / `conflicts` / `coexists` and an explicit retain list | PASS — prior conclusion restated and left unchanged | n/a |
| New information bounded by source, time, version, scope | PASS — table separates policy existence (`evidenced`) from its thresholds and effective version (`missing`) | PASS — table marks source, time, version, product line, and amount band `missing` | n/a |
| Unknowns state closure condition and what they change | PASS — five-column table: question, decision affected, verification method, provider role, closure condition, analysis recomputed | PASS — three open decisions each state what the answer changes; owner role marked `missing` | n/a |
| Work that can continue while a decision waits | PASS — semantic definition and read-only access inventory named as parallel; approval routing and write-back named as blocked | PASS — parallel and must-wait lists given separately | n/a |
| Five-part minimum solution, no added bundle or gate | PASS | PASS | PASS — five sections, unknowns inline, no change log, unknowns document, or assurance gate |

Case A also produced a reconciliation the baseline missed: `消除重複查核` was reclassified as `conflicts` and rewritten to "eliminate duplicate evidence gathering, retain independent judgement", because the finance policy makes the second review a control rather than waste.

## Classification

Baseline gaps are a runtime defect in the Skill's guidance, not an evaluation-contract defect and not a case-specific limitation: the Skill contained no instruction for information arriving after a conclusion, and the two failing behaviours were absent in both conflict cases. The change is the smallest one that addresses them, and case C confirms no cost to an analysis without conflicting evidence.

## Limitations

- The adjudicator authored the change; scoring is not independent.
- Three cases, one run each, one model family. The result shows the guidance is followed, not that it is followed under every phrasing.
- Case B's "existing conclusion" was supplied in the prompt rather than produced by a real prior session, so the in-place update of a persisted case record is untested.
- No target-enterprise evidence was used or established anywhere in this run.
