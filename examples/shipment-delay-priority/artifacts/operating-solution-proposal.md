# Proposed operating solution: Delayed Shipment Review Workbench

> **Synthetic proposal only.** This document turns the replayable shipment-delay evidence into a process-first operating solution. It is not evidence that a target enterprise has accepted the workflow, authorized an integration or model, or achieved the stated value.

## Operating outcome

A logistics coordinator should receive a fresh, evidence-bearing review queue instead of manually scanning and repeatedly comparing a daily shipment export. The proposed intervention occurs after a read-only snapshot is available and before the coordinator decides what operational follow-up to take.

The synthetic scenario proposes reducing daily triage from 45 to 15 minutes. Those values are demo assumptions, not measured enterprise facts. The highest evidenced authority is read-only query and recommendation; ERP write-back remains denied.

## Current-process diagnosis

The supplied evidence supports only a bounded synthetic as-is flow:

```text
Daily export becomes available
  → coordinator opens the file
  → coordinator checks records and mentally compares urgency signals
  → coordinator decides an informal review order
  → missing inputs and stale data are handled case by case
  → coordinator chooses operational follow-up outside this FED scope
```

The proposed diagnosis is:

| Current issue | Operational effect | Evidence status |
| --- | --- | --- |
| Priority policy is applied by repeated manual reading and comparison | Avoidable review effort and inconsistent traceability | `proposed`; the request describes manual scanning, but no observed time study exists |
| Freshness and required-field checks are not a visible entry condition | A stale batch or incomplete record can appear equally actionable | `proposed`; demo rules show the intended control, not the real current process |
| Missing data, normal work, and exceptions share one review surface | Coordinators must discover data-quality problems while triaging | `proposed` |
| The reason for a ranking is not preserved as a structured trace | Review and disagreement require recalculation | `proposed` |
| Ownership after human review is outside the supplied boundary | The solution cannot claim end-to-end shipment resolution | `missing` for a target enterprise |

These are hypotheses to validate with the coordinator and process owner, not findings from a live operational study.

## Process redesign before technology

1. **Standardize the entry condition.** Define the snapshot identity, freshness SLA, required decision fields, semantic version, and evidenced access decision before review begins.
2. **Separate normal work from data-quality work.** Stale batches stop at the batch boundary; incomplete records enter a named escalation path rather than being silently guessed or mixed into the ranked queue.
3. **Make the priority policy explicit.** Use one accepted score, tie-break, and reason-trace definition instead of asking each coordinator to repeat the comparison mentally.
4. **Give the coordinator one bounded review state.** Present the ranked queue and its evidence; the human decides follow-up. In the demo, review status remains session-local. Persistent telemetry needs separate identity, retention, privacy, and access decisions.
5. **Keep operational execution outside the first slice.** No shipment update, dispatch, or ERP write-back occurs until a separately governed action path is evidenced and accepted.

This redesign removes repeated comparison and makes exception handling explicit. It does not require AI.

## Technology-neutral target operating flow

```text
Read-only shipment snapshot
  → freshness, schema, semantic-version, and access checks
  → deterministic ranking or data-quality escalation
  → evidence-bearing review queue with reason trace
  → logistics coordinator accepts, rejects, or investigates the recommendation
  → coordinator chooses operational follow-up outside this slice
```

Normal records receive a score and trace. A stale snapshot stops the batch. A record missing a required decision input abstains from scoring and enters the data-quality escalation path. Human disagreement never changes the deterministic result automatically; a governed owner reviews reason patterns before changing policy, semantics, data, or workflow.

## Process-readiness gate

AI-fit assessment may begin only after the accountable process owner and affected coordinators have:

- confirmed or corrected the as-is normal, exception, escalation, and rework paths;
- accepted the redesigned target flow and named ownership at every handoff;
- agreed on the deterministic priority policy and baseline measures; and
- identified a residual task that still creates material review cost or quality risk.

That evidence is `missing` for a target enterprise. The repository demo can therefore validate the proposed process and deterministic workbench, but it cannot yet establish a need for AI.

## Intervention selection

| Retained need | Selected intervention | Why this is the simplest sufficient choice |
| --- | --- | --- |
| Unclear entry readiness | Data contract plus deterministic freshness, schema, semantic, and access checks | The checks are stable and testable |
| Repeated priority comparison | Deterministic decision service | The policy is explicit; identical inputs must produce identical results |
| Missing decision inputs | Explicit escalation state | A workflow boundary is safer than inference |
| Review context is spread across fields | Evidence-bearing read-only workbench | Structured presentation can expose the score and reason trace directly |
| Accountable operational decision | Human review | The supplied authority does not permit autonomous action |
| Shipment or ERP mutation | Deferred governed action service | Authorization and G5 control evidence are absent |

## AI-fit decision: deferred

AI is not needed in the first vertical slice. A structured interface can display the deterministic reason trace and side-by-side fields without a model, giving the delivery team a lower-risk baseline against which any later AI claim can be measured.

A removable explanation experiment may be justified later if shadow evidence shows that coordinators still spend material time interpreting traces or comparing records after the process and interface redesign. That experiment would translate only the permitted context bundle into a concise explanation or bounded comparison, cite its evidence, and abstain when the bundle is insufficient. It would not calculate scores, fill missing fields, set policy, approve follow-up, or access ERP.

## Responsibility and capability design

| Responsibility | Owner in the first slice | Status |
| --- | --- | --- |
| Accept the target workflow, policy, owners, baseline, and target | Process owner with affected coordinators | Demo assumptions are `proposed`; target-enterprise acceptance is `missing` |
| Validate freshness, required fields, semantic version, access, score, tie-break, and escalation | Deterministic context and decision services | Demo rules and tests are `evidenced`; production implementation is `proposed` |
| Present the queue, reason trace, evidence, and review states | Read-only review workbench | `proposed` |
| Accept, reject, or investigate a recommendation and choose operational follow-up | Logistics coordinator | Demo role is `evidenced`; target-enterprise owner and workflow acceptance are `missing` |
| Explain or compare records with AI | Deferred, removable experiment | Need and incremental benefit are `unverifiable` |
| Modify a shipment or write to ERP | Named governed action service | Out of scope and denied by demo access evidence |

The first slice needs a snapshot adapter, context resolver, deterministic decision service, review interface, and operational observability. Technology and hosting choices remain `missing`; the repository contains no application runtime constraints. No model runtime or model-evaluation infrastructure is required for the first slice.

## First buildable vertical slice

Deliver one read-only workbench where a named demo user can:

1. load the supplied shipment snapshot;
2. see freshness, semantic version, and access status before any recommendation;
3. receive the ranked list with deterministic score traces and separately escalated records;
4. inspect the source fields and reason trace used for each result;
5. mark a recommendation `accepted`, `rejected`, or `needs-investigation` with a session-local reason; and
6. observe a clear stop or escalation when data, evidence, or access is insufficient.

The slice explicitly defers AI explanation, authentication integration, enterprise source connectivity, persistent telemetry, ERP write-back, autonomous action, production scaling, and claims about operating value.

## Delivery work packages

| Work package | Observable result | Completion evidence |
| --- | --- | --- |
| 1. Validate and accept the process | Operators confirm or correct as-is and target paths, ownership, and exceptions | Process validation record with accountable acceptance |
| 2. Freeze the deterministic contract | Input, context bundle, decision result, escalation, and review-state schemas are agreed | Contract examples validate; prohibited side effects are explicit |
| 3. Implement deterministic replay | The supplied four records return 90, 65, 35, and one escalation | Existing decision and boundary tests pass |
| 4. Assemble the review workbench | A user can inspect queue, evidence, trace, and all three session-local review states | End-to-end workflow test; persistence remains disabled |
| 5. Prepare process shadow | Owners approve identity, source access, telemetry, support, rollback, and measures | Target-enterprise approvals and reproducible baseline; currently `missing` |
| 6. Decide whether to run an AI experiment | Shadow shows a material residual explanation or comparison burden | Accepted experiment hypothesis and non-AI baseline |

## Validation and rollout

1. **Replay validation:** use the synthetic fixtures to verify context, deterministic decision, evidence display, stop and escalation behavior, and all review states.
2. **Operator walkthrough:** have affected coordinators complete normal, stale-batch, missing-field, disagreement, and investigation cases; correct the target process before adding features.
3. **Target-enterprise process shadow:** run the workbench beside the existing manual process without changing ERP or operational decisions. Compare cycle time, ranking disagreements, review states, reason codes, escalations, and user trust. Authorization, telemetry retention, real data, and baseline are currently `missing`.
4. **Read-only pilot:** expose recommendations to approved users only after source, identity, privacy, telemetry, support, and acceptance decisions are evidenced.
5. **AI experiment, only if warranted:** compare the removable explanation feature against the accepted non-AI workbench. Require zero unsupported claims, correct abstention for every seeded insufficient-evidence case, no successful prompt injection or forbidden disclosure, schema-valid evidence-bearing output, agreement with the deterministic trace, and accepted latency and cost limits. Any hard-gate failure removes the experiment without affecting the core workflow.
6. **Authority review:** consider write-back only after G5 controls for approval, audit, idempotency, recovery, and target-system authorization have been tested.

Rollback for the first slice is to remove the workbench from the review workflow and return users to the existing export. No ERP state needs compensation because the slice performs no ERP write.

## Evidence ledger

| Statement | Status | Evidence or restriction |
| --- | --- | --- |
| The demo scenario, process, semantic definitions, rules, snapshot, and access decision form a replayable read-only evidence chain | `evidenced` | Files in this example and `expected/gate-review.md` |
| 90, 65, 35, and one escalation are the expected deterministic outputs | `evidenced` | `decision-test-report.json` and `read-only-result.json` |
| The proposed process redesign will reduce coordinator effort | `unverifiable` | Requires real as-is observation, an accepted baseline, and process shadow |
| A read-only workbench can expose the deterministic evidence chain without AI | `proposed` | Must be built and tested with affected users |
| AI explanation has incremental value after the redesign | `unverifiable` | Requires residual-burden evidence and comparison against the non-AI workbench |
| The target enterprise accepts the workflow, ownership, source access, identity, privacy, and telemetry | `missing` | Blocks real-data shadow or pilot |
| Triage time will improve from 45 to 15 minutes | `unverifiable` | Requires reproducible baseline and shadow or production measures |
| ERP write-back is authorized and safe | `missing` | Blocks controlled execution and G5 |

## Next accountable action

For this repository demo, the next work package is to record the as-is assumptions, target flow, owners, review-state behavior, and exception paths as an explicit process acceptance checklist, then implement the deterministic replay and read-only workbench without AI. Completion is observable when the synthetic workflow cases pass end to end and no integration, permission, or model dependency has been invented.

For a real enterprise engagement, the first action is a process-framing and validation session with the accountable business owner, logistics users, source owner, and FED delivery owner. It must replace the synthetic process, owner, baseline, target, source, access, and acceptance claims with verifiable enterprise evidence before process shadow can be authorized.
