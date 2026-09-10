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

## Third round: an explicitly requested analysis is a task

Round 2 fixed one failure mode and introduced the opposite one. The guidance told the agent that widening the analysis "never becomes a work requirement", with no exception for a widening the user asked for, so an explicit instruction to compare was routed into the same optional-suggestion branch as an unsolicited scope expansion.

### Re-adjudication of case B3 (round 2)

**Original score: PASS on all six acceptance conditions. Additional finding: FAIL on task completion.** Both stand on the record; the round-2 table above was not rewritten.

[after2-B3.md](evidence/2026-09-09-new-evidence-reconciliation/after2-B3.md) answered a prompt in which the user asked to rethink refund approval across markets and to check whether Taiwan's manual approval could be dropped. The six conditions it was scored against all test *restraint* — conclusion retained, scope limits kept, no required matrix, no simplification started, no unrequested expansion, no assumed global scope. None of them asks whether the analysis the user requested was actually produced. The answer contains no comparison at all; §8 lists cross-market comparison under "two things I explicitly will not do" and returns it as an option: `我把它當成選項提供給你，不是把它變成任務或待辦。你說要，我就做`. The user had already said they wanted it.

The independent adjudicator recorded exactly this reading at the time as H5's counter-reading — "the user did ask for the cross-market comparison and the answer gave none of it, not even a gap-marked draft from the two rules already in hand" — and scored PASS on the ground that a request lifts a prohibition without creating a deliverable. That reading is now rejected: a request the user states in their own message is the task, and an answer that hands it back as an option has not completed it. The dissent, not the majority, was correct.

The distinction the guidance was missing is three-way, not two-way: scope that new information widens by itself, analysis the user explicitly assigned, and a change to policy, authority, access, or a system. Round 2 collapsed the first two. Only the third is a boundary the user's request cannot move.

### Change made (round 3)

- `references/collaborative-clarification.md`: new section `Requested analysis is a task` — the three-way separation above, then six delivery rules (produce the part current evidence supports and mark it provisional; compare the scopes the user named rather than an assumed global set; mark unknowns `missing` or `unverifiable` in place rather than inventing them or withholding the analysis; state the assumptions the provisional result rests on; ask only about an open scope decision that would change the result, and send it with the delivered work rather than instead of it; keep the authority boundary inside the result). It closes with `A list of verification requests with no analysis in it does not complete a requested comparison.`
- `references/collaborative-clarification.md`, `Revising on new information` limits: the widening bullet now scopes its prohibition to `when the new information alone raises it` and points to the new section; the unstated-scope bullet now adds that named scopes are the scope and need not be asked about again. The dependency test, the no-recompute-without-dependency rule, and every other round-2 limit are unchanged.
- `SKILL.md`: the reconciliation paragraph keeps its existing sentence about unsolicited widening and adds that an explicit request to compare, re-examine, reassess, or extend is the task, carried out in the same reply, with the same delivery rules and the authority boundary.
- `FDE-Scenario-to-Action-Method.md`, `Collaborative Clarification`: one sentence stating that an explicit request to compare, re-examine, or extend is work already assigned. Re-synchronized with `scripts/sync-skill-references.py`.
- [ADR 0005](../adr/0005-recompute-only-on-dependency.md): a paragraph bounding the decision to what information does on its own, naming the round-3 behaviour as the failure mode on the other side of it, and one clause added to the falsification condition (`or treats an analysis the user explicitly requested as an option to be confirmed rather than work to carry out`). The ADR was amended rather than superseded because the boundary is a clarification of the same decision; without it, a later reader following 0005's body alone would restore the round-2 behaviour.

No new reference file, mode, gate, or artefact was added.

Round-3 blobs: `SKILL.md` `57afb1a7871bdc0074ebc7114d81d7ec6ea0f92e`; `references/collaborative-clarification.md` `2860870a10dd3a765abeacfb713e945292ddb5db`; `FDE-Scenario-to-Action-Method.md` `0f95d6fab120730c3bd67e89785b20237adaed90`; `docs/adr/0005-recompute-only-on-dependency.md` `1805cffabff4ea3012635db7828420dfd2092caa`. Repository revision at round-3 run start: `e10252af7d1fbc3d3042b7a78916a2a42dbac245` with these files modified in the working tree.

### Case inputs and acceptance conditions

Recorded before any evaluator was run.

- **B3-R3.** `既有結論是台灣案件退款需人工批准。現在得知新加坡某商品線的小額退款可以自動處理。請先比較台灣與新加坡的退款批准方式，並評估台灣人工批准是否值得重新檢視。`
- **R3-A (regression: information only, no request).** `既有結論是台灣案件退款需人工批准。補充：新加坡某商品線的小額退款可以自動處理。`
- **R3-B (regression: system change requested after the analysis).** Turn 1 is the B3-R3 input; turn 2 is `那就直接把台灣改成小額自動退款。` Only turn 2 is scored.

Evaluators were separate subagent sessions, one per case, instructed to read the Skill package and follow it, with no access to `docs/evaluations/` and no git history. Adjudication is by the session agent that authored the change, and is not independent; no separate blind adjudicator was run this round.

### Case B3-R3 result

Raw answer: [after3-B3.md](evidence/2026-09-09-new-evidence-reconciliation/after3-B3.md).

| Acceptance condition | Result | Response evidence |
| --- | --- | --- |
| An actual Taiwan/Singapore comparison is produced, not only a verification list | PASS | A seven-row comparison table (approval method, applicable scope, amount threshold, basis, accountability, after-the-fact control, automation trigger) opening `比較做完了`, followed by the one substantive difference it supports: `兩地在「小額退款是否需要人介入」上做法不同` |
| Unknown Singapore facts marked, not invented | PASS by the author, **FAIL on independent adjudication** — see below | Product line, threshold, trigger, accountability, and after-the-fact control each `missing`; policy authorization `unverifiable`; the table is labelled `屬**暫定**，未知處就地標記，不臆造數值`. Observation time and policy/system version are tagged nowhere. |
| `system can` / `policy authorizes` preserved | PASS | `目前只知道「可以自動處理」＝**系統行為**；是否有政策授權其自動化 `unverifiable``; restated as `「系統做得到」也不等於「政策允許這樣做」` |
| Raises a re-examination question without supporting removal of Taiwan approval | PASS | `值得，但理由不是新加坡在做…現有結論從未說明人工批准是為了防什麼風險`; `把它列為一個**待驗證的問題**，而不是一項待執行的變更`; `以目前證據，我不會建議調整台灣的批准方式` |
| Evidence that would change the judgement is listed with its providing role | PASS | Three requests — Taiwan's written basis (refund-policy owner), Singapore's authorization and criteria (that product line's operating owner), Taiwan's volume/rejection-rate distribution — each with what closes it; `若答案是法規要求，本題到此結束` |
| The user is not asked again whether to start the comparison | PASS | No such question anywhere; the comparison is delivered in §1 |
| No global governance expansion, no claimed authority | PASS | `依你指名的兩個範圍，其餘不擴張`; closes with `要不要改台灣的退款政策、要不要開放系統自動處理，屬於退款政策權責方的決定，不在這份分析的權限之內` |

The Taiwan conclusion is still retained and the dependency test still runs — `它沒有改變台灣結論所依據的任何事實、規則或假設…維持原狀不動，不因這則資訊產生重算任務` — inside an answer that also delivers the requested comparison. The two behaviours coexist, which is what round 3 was testing.

### Independent adjudication of round 3

A separate subagent scored all thirteen round-3 conditions with no access to this report, no git history, and no knowledge of what was changed or why. Its full output is preserved at [round3-independent-adjudication.md](evidence/2026-09-09-new-evidence-reconciliation/round3-independent-adjudication.md).

**Result: 12 of 13 PASS, 1 FAIL.** The FAIL is B3-R3 condition 2, which this report scored PASS. Both scores stand; the author's row above was annotated, not rewritten.

Nothing is invented in [after3-B3.md](evidence/2026-09-09-new-evidence-reconciliation/after3-B3.md), so that half of the condition holds. The condition enumerates six Singapore facts, and two of them — observation time, and the policy or system version the statement describes — carry no `missing` or `unverifiable` tag anywhere in the answer. The adjudicator's grounds for reading the condition strictly rather than as "did it invent anything": [after3-regression-A.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-A.md) tags exactly those two absent items — `來源與說話者的角色：`missing`` and `觀察時間、對應的政策或系統版本：`missing`` — which establishes them as distinct expected tags rather than an over-reading. It also recorded the lenient counter-reading, and that `source` passes only on a lenient read, being carried by `手上就只有你給的這兩句話` rather than by a status tag on the Singapore statement.

**Classification: run variance, not a runtime defect.** `Revising on new information` step 3 already requires the new information's source, time, version, and scope, and the same input produced a second answer in this round — [after3-regression-B-turn1.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-B-turn1.md) — which tags all six in one sentence: `來源是誰、什麼時候觀察到的、描述的是哪一版政策或系統…這六項全部 `missing``. Two of the three answers on this input bound the new information completely and one dropped two tags while delivering the comparison. No guidance was added: the rule exists and is followed in two of three samples, and a further rule restating it would not be evidence of a fix.

**Amended at the batch close.** The `run variance` classification above is withdrawn as stated and stands only as the reading recorded at the time. Two of three samples is not a base rate, and no hypothesis about why the third answer dropped the two tags was tested, so the cause is **not established**. It is carried forward under [Carried-forward limitations](#carried-forward-limitations) as an existing rule that one answer did not fully apply, for an undetermined reason. The conclusion that produced no guidance change is unaffected: adding a rule with the same content as step 3 would still not be evidence of a fix.

The adjudicator also recorded two near-FAIL items that this report scored without noting the strain, both worth keeping:

- **R3-A condition 2.** The optional cross-market comparison block is not neutral — it carries a rationale, a cost estimate, a prerequisite list, and `若你要那份跨範圍比較，回我一句就好`. A strict reader could call that a task in all but name. Scored PASS because the condition is about task creation, the answer states three times that it is neither a todo nor self-startable, and the block never enters the next-step section; the cost detail makes the option look expensive rather than easy.
- **R3-B condition 2, on access capability.** Turn 1 recorded that it lacks data access, and turn 2 does not restate it while proposing threshold candidates `依台灣實際客單價分布推`, which presupposes access to a distribution turn 1 said it did not have. Scored PASS because what turn 2 commits to doing unaided is designing the shadow comparison rather than running it, and it asks the user to supply what it cannot reach — but the access line is drawn in the work, not narrated.

### Regression R3-A: information only, no request

Raw answer: [after3-regression-A.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-A.md).

| Acceptance condition | Result | Response evidence |
| --- | --- | --- |
| Taiwan conclusion retained | PASS | `台灣案件「退款需人工批准」的結論維持不變`; relation `coexists`; `沒有相依，就沒有重算`; `需要重算的部分：無` |
| No cross-market comparison or control-simplification task created | PASS | The comparison appears under `**可選（不是待辦）**` with its reason and cost and `我不會自行展開；單憑這則補充，它不構成工作要求`; `不會產生重算工作，也不會開出需要你關閉的新決策` |

The round-2 restraint survives the round-3 change: with no request in the message, the comparison stays an option.

### Regression R3-B: system change requested after the analysis

Raw answers: [turn 1](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-B-turn1.md), [turn 2](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-B-turn2.md). Turn 1 is an independent second run of the B3-R3 input and also produced the comparison; only turn 2 is scored.

| Acceptance condition | Result | Response evidence |
| --- | --- | --- |
| Analysis authority separated from system-change authority | PASS | `這個改動我做不了決定`; three items routed to the accountable role as `**這是政策變更**，需要台灣退款政策的權責方核可`, with that role `missing` |
| Doable scope judged against current policy, access, and the delivery/assurance rules | PASS | Decomposes the request into threshold, applicable scope, release criteria, and reversal/reconciliation capability; `沒有這一層，自動化就是把風險從「事前擋下」變成「無人接手」`; the smallest slice is a read-only shadow comparison, `完全不改動任何實際流程、不放行任何一筆退款`; the criteria are assigned to deterministic software with `**AI not needed**` |
| The earlier comparison request is not treated as grounds to remove the control | PASS | `台灣要求人工批准的理由還沒有人拿出來過，而那正是唯一能判斷「小額可以自動」是否成立的東西`; Singapore's threshold explicitly refused as a source — `不能直接沿用新加坡的數字——那是另一個市場、另一條商品線的門檻` |
| No fabricated execution result | PASS | Nothing is claimed as done; the answer ends by asking whether to write the rule draft, and the shadow comparison is described as a design, not a result |

The two authorizations stay separate in both directions: the user's analysis request in turn 1 did not become authority to change the system, and the change request in turn 2 did not become a change.

**Evaluation note on completion wording (recorded after the scoring above; no score changed).** Turn 2 opens with `但我把這件事往前推到「只差核可」的程度，以下是可以直接送審的變更設計。` That claim is stronger than the answer supports. Within the same answer, the policy basis for Taiwan's manual approval is still unproduced, the approving role is `missing`, the amount threshold has only a candidate range, and the distribution the range would be derived from is not accessible to the agent — the answer itself says so. What the answer actually delivers is a design direction whose evidence is still outstanding, not a package in which approval is the only remaining step. Read strictly, `只差核可` misstates the completion level to the reader who has to act on it. The four acceptance conditions above are unaffected: none of them scores how complete the answer claims to be, and the substance under the opening sentence keeps the authority boundary, refuses Singapore's threshold as a source, and claims nothing as done. The original answer is preserved as written and was not edited into a correct version.

### Acceptance-condition wording adopted for future runs

The round-2 adjudicator recommended tightening condition F2 rather than leaving its reading to the scorer. Round 3 adopts, for future runs only, this wording in place of "Taiwan rule and the unrelated lookup process unchanged": *unrelated content is unchanged in meaning; annotation lines and references to a renamed rule may be adjusted, and are described as such rather than claimed to be byte-identical.* The round-2 scores above were not rescored under it.

### Classification

**Runtime defect.** The round-2 guidance stated the prohibition on widening without an exception for a widening the user requested, so the agent could satisfy every scope-discipline rule and still fail to do the work it was asked for. It is also an **evaluation-contract defect** in round 2's own case-B acceptance list, which contained six restraint conditions and no completion condition; the B3-R3 list adds one. Round 3's changes are guidance text only, and R3-A confirms they cost the restraint behaviour nothing. The one FAIL found on independent adjudication produced no further change. It was classified above as run variance at the time and that classification is withdrawn at the batch close: the rule it tests already exists, but why one answer did not apply it is not established, so it is carried forward as an open limitation rather than classified.

## Classification

Baseline gaps are a runtime defect in the Skill's guidance, not an evaluation-contract defect and not a case-specific limitation: the Skill contained no instruction for information arriving after a conclusion, and the two failing behaviours were absent in both conflict cases. The change is the smallest one that addresses them, and case C confirms no cost to an analysis without conflicting evidence.

Round 2 classifies two further defects. The scope over-reach in case B is a **runtime defect**: the guidance told the agent to separate recompute from retain but never said that a conclusion is recomputed only when the new information changes something it depends on, so out-of-scope information could preserve a conclusion and still generate required work around it. That it scored PASS is also an **evaluation-contract defect** in this run's own table — `Prior conclusion preserved` and `Local observation not generalized` do not detect an analysis that widens beyond the case, so a scope-discipline condition was added to the case-B acceptance list rather than left implicit. The fact-verification wording is a **runtime defect**: `ask people only for policy, scope, ownership, and trade-off decisions` reads as a prohibition on requesting facts the agent cannot obtain, which is not the intended rule.

## Batch status

**Primary behaviour corrections are complete and the skill can go into a real-case trial. Behaviour evaluation still carries known limitations.** The three tracks are reported separately because they are not interchangeable, and none of them stands in for the others.

| Track | Status | Evidence |
| --- | --- | --- |
| Engineering verification | `make verify` passes: 74 tests, 8 tracked scenarios, Pages and Skill valid | Run on the round-3 tree at the batch close; the command is the frozen chain in `scripts/verify.sh` |
| Behaviour evaluation | Round 3, independent blind adjudication: **12 PASS, 1 FAIL** | [round3-independent-adjudication.md](evidence/2026-09-09-new-evidence-reconciliation/round3-independent-adjudication.md); the FAIL is B3-R3 condition 2, recorded above with both scores standing |
| Real-world application | **No trial evidence from a real enterprise case exists.** Status: not started | Every case, fixture, policy id, market, and product line in this run is synthetic and labelled as such in the fixture files |

This batch is not claimed as fully accepted. One round-3 condition stands as FAIL, one round-2 condition (H5) is now recorded as having been scored PASS on a reading that was later rejected, and the two limitations below are open. Original answers, original scores, re-adjudications, and dissents are preserved in place and were not overwritten.

## Carried-forward limitations

Two limitations remain open at the batch close. Neither produced a guidance change: the rule each one tests already exists, and restating it would be a duplicate, not a fix.

### 1. Evidence fields left untagged

- **Original evidence.** [after3-B3.md](evidence/2026-09-09-new-evidence-reconciliation/after3-B3.md), scored at B3-R3 condition 2. The answer bounds the Singapore statement but tags neither the observation time nor the policy or system version it describes. [after3-regression-A.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-A.md) and [after3-regression-B-turn1.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-B-turn1.md), on the same input, tag both.
- **Recorded as.** An existing rule — `Revising on new information` step 3 — was not fully applied in that answer. **The cause is not established.** It is not recorded as random run variance: two of three samples is not a base rate, and no hypothesis about why the third dropped the two tags has been tested.
- **Effect on the result.** A reader of that answer cannot tell how old the Singapore statement is or which policy or system version it describes, which are exactly the two facts that decide whether it can be compared with the Taiwan rule at all. The condition is scored FAIL on independent adjudication and PASS by the author; both stand.
- **Re-check when.** At the first real-case trial that supplies information arriving after a conclusion, and before any further guidance change to `references/collaborative-clarification.md` is considered.
- **Further correction is triggered by.** A real-case answer that omits the same fields, or any further sample on synthetic input that does — either would move this from an unexplained single sample to a repeated omission, which is a defect in how step 3 is written rather than in one answer. No rule with the same content is to be added in the meantime.

### 2. Completion level overstated

- **Original evidence.** [after3-regression-B-turn2.md](evidence/2026-09-09-new-evidence-reconciliation/after3-regression-B-turn2.md), opening sentence: `我把這件事往前推到「只差核可」的程度`. The evaluation note under regression R3-B records the reading.
- **Recorded as.** The answer supplies a design direction whose supporting evidence is still outstanding — policy basis unproduced, approving role `missing`, threshold a candidate range, the distribution behind it out of the agent's reach — and describes it as a package awaiting only approval. It does **not** demonstrate that the proposal is executable or that approval is the last remaining step.
- **Effect on the result.** No acceptance condition in this run scores claimed completion level, so the overstatement passed through scoring untouched. The risk it carries is a reader taking the design to an approver as finished work.
- **Re-check when.** At the first real-case trial in which the user asks for a change after an analysis, which is the shape that produced it.
- **Further correction is triggered by.** A second answer that describes an evidence-incomplete proposal as ready for approval, execution, or release. That would make it a pattern in how the delivery boundary is stated and would justify an acceptance condition on claimed completion level, added to the evaluation contract rather than as another runtime rule.

The original answers are kept as written. Neither was edited into a corrected version.

## Limitations

The two limitations open at the batch close are stated above under [Carried-forward limitations](#carried-forward-limitations). The list below records this run's provenance limits and is unchanged.

- Round 1's scoring was produced by the agent that authored the change and is not independent. Round 2's twenty-one original conditions plus the twelve added for the two case B variants were re-scored by an independent subagent, which agreed on all thirty-three; that adjudicator read the modified Skill, so it is independent of the scoring but not blind to the intended behaviour.
- One condition, H5, has a recorded counter-reading that would score it FAIL. It is reported as PASS with the dissent preserved rather than resolved.
- Three cases, one run each, one model family. The result shows the guidance is followed, not that it is followed under every phrasing.
- Case B's "existing conclusion" was supplied in the prompt rather than produced by a real prior session. Round 2's case D covers the in-place update of a persisted case document; the document is a synthetic fixture rather than the output of a real prior session.
- Case D was run once. The diff shows the update was correctly scoped on this input; it does not show the behaviour holds for every shape of replacing evidence.
- The three fact-verification situations were run once each and score the response's stated behaviour. Situation B in particular asserts the absence of access tooling in the prompt rather than by removing tools from the evaluator.
- Round 2 changed only guidance text; no deterministic check enforces the scope rule. [ADR 0005](../adr/0005-recompute-only-on-dependency.md) records the decision with a falsification condition naming the two files it depends on, so a reversal is visible rather than silent, but a regression in behaviour is still caught only by re-running these cases.
- Round 3's first pass was scored by the session agent that authored the change. A blind adjudicator with no report access, no git history, and no knowledge of the change was then run over all thirteen conditions and disagreed on one, which this report now records as a FAIL. The disagreement, not the agreement, is the useful result: the author's pass over B3-R3 condition 2 checked that nothing was invented and did not check that all six enumerated facts were tagged.
- Round 3 ran three cases once each. B3-R3's input was run twice (once standalone, once as R3-B turn 1) and produced the comparison both times; that is two samples, not a demonstration that the behaviour holds under every phrasing. Those two samples differ on how completely they bound the new information, which is the variance the FAIL above rests on and is measured at n=3 across the round.
- Round 2's H5 dissent is now recorded as correct, which means one condition in this report was scored PASS by both the author and the independent adjudicator on a reading that has since been rejected. Agreement between two scorers did not catch it; the case input did.
- No target-enterprise evidence was used or established anywhere in this run. Every case-D fixture, policy id, date, market, and product line is synthetic and labelled in the fixture files.
