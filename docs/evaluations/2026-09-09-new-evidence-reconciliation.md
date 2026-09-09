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
| Adjudicator | Round 1 and round 2 first pass: the session agent that made the change. Round 2 also scored independently by a separate subagent with no report access, no knowledge of the change, and no git history. |

Six runs were executed in round 1: three baseline runs against the unmodified Skill, then three post-change runs against the modified Skill. Round 2 added six more — a case B re-run, three fact-verification situations, a case-document partial update, and an ordinary-analysis regression — against a further-modified Skill whose blobs are recorded in that section. Each raw answer is preserved under [evidence/2026-09-09-new-evidence-reconciliation/](evidence/2026-09-09-new-evidence-reconciliation/). Model output is not byte-for-byte deterministic, so the case inputs, blobs, and raw answers are the reproducible record, not the exact wording. The adjudicator is not independent of the change; this is a stated limitation of the run.

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

## Second round: scope discipline, fact verification, and in-place case update

The first round's case B was scored PASS on every criterion. Re-reading the preserved answer shows the scoring missed an over-reach that no criterion named, so a second round of changes and runs followed.

### Re-adjudication of case B (round 1)

**Original score: PASS on all seven behaviours. Revised score: FAIL on scope discipline.** Both scores stand on the record; the original was not rewritten.

The behaviour the original scoring did not check is whether the response kept the case's own scope. [after-B.md](evidence/2026-09-09-new-evidence-reconciliation/after-B.md) preserved the Taiwan conclusion, which is what the round-1 table asked, and then widened the analysis anyway:

- Under `必須重算（recompute）` it listed `退款批准是否應為單一全域規則`, and rewrote the target workflow as `一張分層的核准矩陣` — a required recompute produced by information that changed no fact, rule, or assumption the Taiwan conclusion depended on.
- The same list opened `人工批准這道控制是否對所有金額帶都在降低實質風險`, turning a different market's observation into a live question about simplifying the Taiwan control.
- The revised recommendation added `把「退款核准權限」重新界定為一張分層矩陣` as a recommendation, not an option.
- The parallel-work list required measuring the Taiwan small-amount rejection rate, work created solely by the out-of-scope input.

The round-1 table's `Local observation not generalized` row read "system can" versus "policy authorizes" and stopped there. Preserving a conclusion and not expanding the analysis around it are two different behaviours, and only the first was scored.

### Change made (round 2)

- `references/collaborative-clarification.md`, `Revising on new information`: added step 1 `Restate the case scope` and step 5 `Test for dependency before recomputing` (a conclusion is recomputed only when the new information changes a fact, rule, or assumption it depends on; different scope with no dependency produces no recompute task and no new open decision), extended the in-place update step to leave an unclear replacement scope open rather than overwrite it, and added three limits: different scope without dependency is context; widening the analysis is an option carrying its reason and cost, never a work requirement; an unstated scope is asked about, not assumed.
- `references/collaborative-clarification.md`: added a `Facts and decisions` section separating who knows a fact from who may decide it — investigate what is reachable, request unreachable facts from a knowing role, route policy/scope/authorization to the accountable role, assume no permission and no approval right, keep an unconfirmed account as an account. The previous wording `ask people only for policy, scope, ownership, and trade-off decisions` and the `Resolve facts` and `Ask the frontier` steps were rewritten to match.
- `SKILL.md`: the clarification trigger no longer says "ask accountable participants only for decisions"; the reconciliation trigger now says to recompute only dependent conclusions and to offer cross-scope comparison as an option.
- `FDE-Scenario-to-Action-Method.md`, `Collaborative Clarification`: the FDE requests unreachable facts from the roles that hold them; asking a knowledgeable role for a fact is not asking for a decision. Re-synchronized into the Skill package with `scripts/sync-skill-references.py`.

Round-2 blobs: `SKILL.md` `53f96e6605f3d13c17d5fe9c49635f92c84642eb`; `references/collaborative-clarification.md` `445fe2362d061028a64b8dfb64cc83c3d5db6478`; `FDE-Scenario-to-Action-Method.md` `70a810914dfe2b37670aafc04acb81e1ce49b662`. Repository revision at round-2 run start: `02c2da1e337ba8bce2c0bf46a5976c4d148a9970` with these four files modified in the working tree. Evaluator and adjudicator arrangement is unchanged from round 1, and the adjudicator is still not independent.

### Case B re-run after the change

Raw answer: [after2-B.md](evidence/2026-09-09-new-evidence-reconciliation/after2-B.md). Same input as round 1.

| Acceptance condition | Result | Response evidence |
| --- | --- | --- |
| Taiwan conclusion retained | PASS | `既有結論「台灣案件退款需人工批准」維持不變，不需要重算` |
| Singapore statement keeps its source and scope limits | PASS | source, observation time, version, product line, and amount band each marked `missing`; `它能支持的最大主張是：「有人陳述新加坡某商品線的小額退款存在自動處理路徑。」` |
| No global approval matrix required | PASS | `需要重算的結論：無`; the cross-market question appears under `可選（非工作要求）` with its cost, and `這是一個新的、需要你發動的問題，不是這則資訊自動產生的任務` |
| No Taiwan approval simplification started | PASS | `台灣照原結論執行，不做任何流程或控制變更` |
| Expansion only on a real dependency or an explicit request | PASS | `沒有相依，因此不觸發重算，也不產生新的待決事項`; the dependency that would change this is named (`共用同一套退款政策文件或同一個核准引擎設定`) and marked `missing` |
| Unstated scope not assumed global | PASS | `一個市場的案子，不等於要求設計一套全球規則。若你的原意其實是要做跨市場的退款政策收斂，請直接說` |

### Fact verification: three situations

| Situation | Result | Response evidence |
| --- | --- | --- |
| A — current policy document supplied ([fact-A.md](evidence/2026-09-09-new-evidence-reconciliation/fact-A.md)) | PASS | The five policy clauses are read and classified `evidenced` with document id and effective date; `我不會把已經給我的政策再退回去問你`. Questions cover only what the policy does not state — the four systems' read access, time distribution, the `已判定免退回` decision source, the `原始付款金額` comparison basis. |
| B — no walkthrough record, no access tooling ([fact-B.md](evidence/2026-09-09-new-evidence-reconciliation/fact-B.md)) | PASS | `我現在無法依「走查結果」做流程分析…這是事實缺口，不是決策問題`. Five named evidence requests, each with the role that holds it (`主持該次走查的人或流程負責人`, `能匯出退款交易紀錄的…角色`), and `我不會…宣稱自己能自行驗證任何一項`. The walkthrough is bounded as a local observation, not a population fact. |
| C — operator says the system can skip approval ([fact-C.md](evidence/2026-09-09-new-evidence-reconciliation/fact-C.md)) | PASS | Classified `supplements`, not `supersedes`: `這則訪談不推翻…它談的是另一件事——系統有沒有把這條規則擋住`. `做得到不等於被允許`. The compliance question is routed to `退款政策的當責主管／風險或法遵負責人` with `受訪的第一線人員描述了行為，但無權認定其合規性`, and the accountable role stays `missing`. The three verifiable facts (permission matrix, frequency, audit trail) are separated from that one decision. |

Situation C also demonstrates the round-2 scope rule under a case where recomputation *is* warranted: the response recomputes control effectiveness and the exception path, because the interview changes an assumption the Taiwan conclusion rested on, and offers the cross-market control sweep as `一項可選、非任務的建議`.

### Case D — in-place partial update of an ongoing case document

This case closes round 1's stated limitation that "the in-place update of a persisted case record is untested". Fixture, input, before and after documents, raw answer, and the file diff are under [case-D/](evidence/2026-09-09-new-evidence-reconciliation/case-D/). All content is synthetic and labelled as such in the fixture itself.

The fixture holds a Taiwan approval rule, two Singapore product-line rules from one document, a read-only refund-status lookup unrelated to approval, four conclusions, and two open items. The input supplies `SG-FIN-POL-2025-04` v2.0, effective 2025-04-01, issued by the Singapore finance policy owner, which states that it replaces only the Home Appliance product line's approval clause.

Verified against [case-record.diff](evidence/2026-09-09-new-evidence-reconciliation/case-D/case-record.diff):

| Acceptance condition | Result | Diff evidence |
| --- | --- | --- |
| Only the affected Singapore content and its direct dependants change | PASS | Changed hunks touch R2 (marked superseded), the new R4, C2, and the P1 sentence that enumerated `R1–R3` — the last is a reference to the renamed rule, not a change to the lookup process. |
| Taiwan rule and the unrelated lookup process unchanged | PASS | R1's content, source, and evidence state are byte-identical; the only added line is `新證據影響：無。…與本規則無範圍相依`. P1's process text is unchanged apart from the rule reference. C1 and C4 carry `（保留，未改動）`. |
| Prior conclusion, its basis, and the reason it was replaced are kept | PASS | R2 retained in full as `已被 R4 取代，保留供追溯` with `證據狀態：evidenced（截至 2025-03-31 為現行）`; the previous C2 is kept verbatim beneath the new one as `該結論在其輸入下為正確，僅因政策改版而失效`. |
| New conclusion carries its new source and applicable scope | PASS | R4 records `SG-FIN-POL-2025-04` v2.0, effective date, owner, and `適用範圍：僅限新加坡 Home Appliance 商品線`; C2 cites R4. |
| No unrelated proposal, task, or document bundle added | PASS | The diff adds one reconciliation-record section, one rule, two open items derived from the new rule's own conditions, and a parallel/blocked work list. `未擴大範圍` states the cross-market threshold comparison is an option and `不是本案的工作項目，也不構成 U1 的答案`. No new file was created. |
| Unclear replacement scope left open rather than silently overwritten | PASS | U4 records that the policy document does not prove the operating system was configured accordingly, status `missing`; U3 leaves the authoritative data sources for the two new conditions open and states that C2's executability, and nothing else, is recomputed if they cannot be obtained. |

R3 keeps its content and gains only the annotation that the new document explicitly does not affect other product lines — the correct treatment for a rule that shares a superseded source document but not the superseded scope.

### Case B under two other phrasings

The behaviour that regressed in round 1 was re-run under two further phrasings to test whether the guidance holds the behaviour rather than the wording. Both are scored against the same six acceptance conditions as the case B re-run.

- **Authoritative same-topic policy** ([after2-B2.md](evidence/2026-09-09-new-evidence-reconciliation/after2-B2.md)). The new information is a formal Singapore policy with an owner, a version, and an effective date, and the prompt insists it is not hearsay. PASS on all six. The response accepts it as `evidenced` *within its own scope* and still classifies it `coexists`: `新加坡財務政策負責人的權責範圍是新加坡；他沒有、也不宣稱對台灣退款核決權責發言`. It tests each fact the Taiwan conclusion depends on — approval authority, applicable policy, risk threshold, product line and currency — and finds no dependency, noting that `SGD 500 的金額帶對 TWD 案件沒有換算後的自動適用效力，除非有台灣政策明文承接`. Evidence quality and applicable scope are handled as two independent dimensions, which is the distinction round 1's answer collapsed.
- **User pushes for expansion** ([after2-B3.md](evidence/2026-09-09-new-evidence-reconciliation/after2-B3.md)). The user asks to rethink refund approval across markets and to check whether Taiwan's manual approval can be dropped. PASS on all six. The response does not act on the second request without the control's rationale — `在拿到之前給出「可以拿掉」或「不能拿掉」的判斷，會是把推論偽裝成結論` — and does not assume the unstated scope is global: `你問句裡的「整個都該重想一遍」目前沒有標定範圍，我不替你假設它是全球`. It separates the four fact requests from the one scope decision that belongs to the user.

### Independent adjudication

The round-1 and round-2 scoring above was produced by the agent that authored the changes. To close that gap, a separate subagent scored all eight round-2 answers against the acceptance conditions with no access to this report, no knowledge of which change was made, and no git history. Its full output is preserved at [independent-adjudication.md](evidence/2026-09-09-new-evidence-reconciliation/independent-adjudication.md).

**Result: 33 of 33 conditions PASS**, agreeing with the adjudicating author's scoring on every item. It also recorded the three conditions nearest to FAIL, which are the useful part of the run:

- **F2 (Taiwan rule and unrelated lookup unchanged) is the weakest.** P1 did change one string, `不受 R1–R3 影響` → `不受 R1、R3、R4 影響`. Read as byte-identical, this is a FAIL. The adjudicator scored PASS because the process description, its read-only nature, and its applicability are untouched, and leaving the reference alone would point P1 at R2, now marked historical. Its recommendation: if the contract wants this tighter, the condition text should explicitly exclude reference synchronization and impact annotations rather than leave the reading to the scorer.
- **H5 (expansion only on dependency or request) is the only item the adjudicator considers genuinely arguable.** The user did ask for the cross-market comparison and the answer gave none of it, not even a gap-marked draft from the two rules already in hand. The adjudicator scored PASS on four grounds: condition 5 is a threshold, not a delivery obligation — a request lifts the prohibition without creating a deliverable; the request's own scope is unstated, so producing a cross-market rule set would require deciding the market list for the user, which condition 6 forbids; every other market's facts are `missing`, so the table could only be filled by invention, the contract's first named failure mode; and the answer does take a substantive position on the second request rather than deflecting it. The recorded counter-reading is that a contract intending "deliver what the evidence supports and mark the rest" would score this FAIL.
- **D2** — `fact-C.md` routes the compliance judgement to the policy owner correctly but never asks for or names the policy document and version the original conclusion rested on; its three evidence requests all point at system settings, transaction records, and audit logs. The condition is disjunctive, so the second clause carries it.

The acceptance conditions were **not** rewritten after scoring. Tightening F2 or H5 now would invalidate the scores just recorded; the suggested wording is preserved here so a future run can adopt it before it scores anything.

### Ordinary analysis regression

Raw answer: [after2-C.md](evidence/2026-09-09-new-evidence-reconciliation/after2-C.md). Same onboarding case as round 1's case C, with no conflicting evidence.

PASS: five sections matching the minimum operating solution, reference hypotheses labelled `proposed`, `AI not needed` reached explicitly, no change log, unknowns document, artefact bundle, or assurance gate. The round-2 additions cost nothing to an analysis with no new information to reconcile.

## Classification

Baseline gaps are a runtime defect in the Skill's guidance, not an evaluation-contract defect and not a case-specific limitation: the Skill contained no instruction for information arriving after a conclusion, and the two failing behaviours were absent in both conflict cases. The change is the smallest one that addresses them, and case C confirms no cost to an analysis without conflicting evidence.

Round 2 classifies two further defects. The scope over-reach in case B is a **runtime defect**: the guidance told the agent to separate recompute from retain but never said that a conclusion is recomputed only when the new information changes something it depends on, so out-of-scope information could preserve a conclusion and still generate required work around it. That it scored PASS is also an **evaluation-contract defect** in this run's own table — `Prior conclusion preserved` and `Local observation not generalized` do not detect an analysis that widens beyond the case, so a scope-discipline condition was added to the case-B acceptance list rather than left implicit. The fact-verification wording is a **runtime defect**: `ask people only for policy, scope, ownership, and trade-off decisions` reads as a prohibition on requesting facts the agent cannot obtain, which is not the intended rule.

## Limitations

- Round 1's scoring was produced by the agent that authored the change and is not independent. Round 2's twenty-one original conditions plus the twelve added for the two case B variants were re-scored by an independent subagent, which agreed on all thirty-three; that adjudicator read the modified Skill, so it is independent of the scoring but not blind to the intended behaviour.
- One condition, H5, has a recorded counter-reading that would score it FAIL. It is reported as PASS with the dissent preserved rather than resolved.
- Three cases, one run each, one model family. The result shows the guidance is followed, not that it is followed under every phrasing.
- Case B's "existing conclusion" was supplied in the prompt rather than produced by a real prior session. Round 2's case D covers the in-place update of a persisted case document; the document is a synthetic fixture rather than the output of a real prior session.
- Case D was run once. The diff shows the update was correctly scoped on this input; it does not show the behaviour holds for every shape of replacing evidence.
- The three fact-verification situations were run once each and score the response's stated behaviour. Situation B in particular asserts the absence of access tooling in the prompt rather than by removing tools from the evaluator.
- Round 2 changed only guidance text; no deterministic check enforces the scope rule. [ADR 0005](../adr/0005-recompute-only-on-dependency.md) records the decision with a falsification condition naming the two files it depends on, so a reversal is visible rather than silent, but a regression in behaviour is still caught only by re-running these cases.
- No target-enterprise evidence was used or established anywhere in this run. Every case-D fixture, policy id, date, market, and product line is synthetic and labelled in the fixture files.
