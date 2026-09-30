# Borrowed-Case Hypotheses — 2026-09-30

## Purpose and boundary

This run tests two hypotheses that the recorded cases A–G left open. Every earlier AI-fit decision ended as `not needed` or `deferred`, and no earlier input prescribed the solution before the problem was framed. Both cases are synthetic; their scenarios are adapted from the synthetic teaching cases `05-流程型工单Agent` and `04-合同单据审核HITL` in [VanGong1999/FDE](https://github.com/VanGong1999/FDE) (MIT, retrieved 2026-09-30). Only the scenario was borrowed; the inputs below were rewritten for this run and neither case's original answer was shown to an evaluator. The run establishes repository behaviour only.

| Hypothesis | Observable failure |
| --- | --- |
| H — a user who prescribes the technology pulls the skill into designing it | The response designs the agent's tools and permissions before diagnosing the workflow, or accepts "an all-purpose agent" as the outcome |
| I — the skill defers AI by reflex even when the input supplies the evidence it normally asks for | The response defers or rejects AI without naming a specific missing evidence item, or selects AI as approver |

## Run provenance

| Field | Value |
| --- | --- |
| Repository revision | `1621e6e` |
| Skill blob | `.agents/skills/fde-project-work/SKILL.md` @ `57afb1a` |
| Evaluators | Two independent Claude Code subagents (general-purpose), dispatched in parallel, each without the other's output |
| Evaluator instruction | Read `SKILL.md` in full and follow its own reference-loading rules; do not open `docs/evaluations/` or `examples/`; edit nothing; return the five-part minimum operating solution and list every file read |
| Primary scorer | The dispatching session, against the [evaluation contract](README.md) |
| Recording method | Inputs are verbatim. Outputs are normalized summaries; decisions and evidence boundaries are preserved. Raw messages are session evidence, `unverifiable` from a repository-only checkout |

## Case H — Prescribed all-purpose agent

### Input

> Our internal service desk handles IT and HR requests for about 3,000 employees: VPN access, mailbox group membership, laptop replacement, leave-balance questions, and permission changes across AD, the ITSM tool, and the HR system. Employees often submit incomplete tickets, specialists go back and forth asking for missing details, and even simple requests wait in the same queue as complex ones. The CIO has already decided: build one all-purpose AI agent that talks to employees in Teams and completes any request end-to-end, including changing permissions directly. Design the agent — its tools, its permissions, and a rollout plan.

### Minimum operating solution

1. **Problem and outcome.** Shorter cycle time for standard requests and fewer clarification loops without more access incidents; baselines `missing`. The decision is what form and authority the prescribed agent may take.
2. **Current-work diagnosis.** Four kinds of work share one queue; "give me access" maps to many undefined operations; approvers are implicit. Four reference hypotheses (field gaps concentrated in few types, volume in 10–15 catalogue items, stable approval rules, leave-balance lookups need no ticket) are marked `proposed`.
3. **Target workflow.** Catalogue with required fields, eligibility, approver and rollback per item; completeness at intake; four lanes (information, standard fulfilment, judgment/privileged, physical); traceable access changes; IT and HR each own their items.
4. **Intervention and AI-fit.** Catalogue, routing and policy enforcement are deterministic. AI fits free-text-to-catalogue intake and specialist summaries, only if it beats a plain form. The agent holds no standing admin rights; direct permission writes are not recommended, and governed execution through whitelisted catalogue items is deferred until authorization, audit, idempotency, rollback and ownership evidence exist. The requested tools, permissions and phased rollout are given within those bounds, with a form-only baseline before any agent phase.
5. **Next accountable action.** The CIO decides between the entry-point and self-writing positions, with the cost of the latter stated; IAM/security and HR operations own two further decisions; phase-0 sampling of about 200 closed tickets starts without waiting on them.

### Result

| Criterion | Decision | Response evidence |
| --- | --- | --- |
| 1 Bounded | PASS | Scope, outcome metrics and the decision about the agent's form are stated |
| 2 Paths | PASS | Missing approver, SoD conflict, HR data visibility, physical logistics and IT/HR transfer; the clarification loop is named as rework |
| 3 Work before technology | PASS | Catalogue, lanes and ownership precede the tool list; phase 1 is form-only |
| 4 Proportionate, AI optional | PASS | Per-element table with `not needed`, `fits` and `deferred`; agent must beat a form or fall back |
| 5 Boundaries | PASS | All enterprise facts tagged; write-back refused pending five named evidence items; no authority assumed from the CIO's decision |
| 6 Owner and action | PASS | D1–D3 have owners; the sampling can start now. The owner of the sampling itself is implied (service-desk lead as data source), not named |

Hypothesis H not reproduced. The response met the explicit design request instead of refusing it, and bounded it rather than letting it replace the diagnosis. **Classification: no defect.**

## Case I — Evidenced AI fit

### Input

> I lead the legal team's supplier-contract first review. We review about 600 supplier contracts a month with four reviewers. Last quarter we already fixed the process side: one intake queue, a named reviewer per contract, a written clause playbook covering indemnity, auto-renewal, exclusivity, and liability caps, and a deterministic comparison that flags every deviation from our own template automatically. That works for the 60% of contracts on our paper. The other 40% arrive on the supplier's paper. A two-week time study (attached summary): first review of a supplier-paper contract averages 70 minutes, of which about 50 minutes is reading to locate and classify the four risk clause types, because the wording and placement vary freely. We tried keyword rules on these last quarter; against 200 clauses our senior counsel labelled, keyword rules found 58% of the high-risk clauses. Missed high-risk clauses cost us twice last year. Contracts may not leave our environment; IT security has approved a privately hosted model for read-only use on contract text. Reviewers will keep sign-off. What should we do next?

### Minimum operating solution

1. **Problem and outcome.** About 240 supplier-paper contracts a month; reduce locate-and-classify time while missing fewer high-risk clauses, judged together. The 200 hours a month is an upper bound, not a forecast.
2. **Current-work diagnosis.** Own-paper process kept unchanged. The residual burden is language work that fixed rules already failed on. New gaps: absent clauses, terms incorporated by reference, unreadable scans. The attached summary did not arrive and is `unverifiable`; the human baseline recall, the high-risk count within the 200, the cause of the two misses and the format mix are `missing`.
3. **Target workflow.** Intake completeness check; clause map with quoted text, location and explicit "not found"; reviewer confirms each entry and checks each "not found"; playbook and sign-off unchanged; corrections logged; periodic full re-read sampling.
4. **Intervention and AI-fit.** AI, privately hosted and read-only, builds the clause map only; keyword hits stay as a safety net; everything else is deterministic or human. Decision recorded as `AI deferred pending evidence, with a defined path to a pilot`: the gap is model recall against reviewers, not against keywords. An acceptance bar and a held-out test set are fixed in advance; the non-AI fallback is named.
5. **Next accountable action.** The legal lead, within about four weeks: set the bar with senior counsel, label 50–100 recent supplier-paper contracts with the reviewers' original findings as baseline, diagnose the two misses, clear hosting and retention with IT security, then run the offline test to a go/no-go for a shadow pilot. Intake and "not found" checks start now.

### Result

| Criterion | Decision | Response evidence |
| --- | --- | --- |
| 1 Bounded | PASS | Scope narrowed to the supplier-paper step; speed and safety outcomes paired |
| 2 Paths | PASS | Absent clauses, referenced terms, unreadable input, send-back rework, unchanged escalation, sampling |
| 3 Work before technology | PASS | Intake and "not found" controls are added and start regardless of the AI decision |
| 4 Proportionate, AI optional | PASS | AI is the selected candidate for one step, tested next, with a non-AI fallback |
| 5 Boundaries | PASS | Evidence table; the missing attachment is marked `unverifiable`; value stated as an upper bound; AI excluded from judging risk and sign-off |
| 6 Owner and action | PASS | Named owner, deadline and ordered steps to a go/no-go |

Hypothesis I not reproduced: the deferral names the missing items, and the model evaluation itself is the next action. **Classification: no defect.** One observation, not scored as a failure: the label `deferred` reads more conservative than the behaviour, which schedules the AI evaluation immediately. It is worth watching for in a real case, where a reader may take the label alone as "not now".

## Limits

- The primary scorer is the session that wrote the inputs. No blind adjudication was run over this pair.
- The case H evaluator answered in Traditional Chinese although the input was English. It inherited the user-level language policy of the dispatching session. This is an environment effect, not skill behaviour.
- One run per case. Model output is not deterministic, and a PASS here does not establish that the hypothesis cannot occur.
- Both cases are synthetic. Per [Continue or stop](README.md#continue-or-stop), this run does not replace the real-case trial, which is still not started.
