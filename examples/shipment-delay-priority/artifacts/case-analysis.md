# Shipment delay priority: synthetic case analysis

> **Synthetic repository example only.** Every person, source, permission, baseline, target, and acceptance statement in this case is illustrative. Nothing here establishes target-enterprise authority, access, readiness, or value.

## Outcome and evidence boundary

The example answers one bounded question: which delayed shipments should a demo logistics coordinator review first?

The proposed outcome is a fresh, evidence-bearing review queue instead of repeated manual comparison of a daily export. The synthetic 45-minute baseline and 15-minute target show record shape only; neither is an observed enterprise measure. The highest supported authority is a recommendation for one named synthetic user in one named synthetic scenario. The replay never writes to an ERP or persists a human disposition.

## Current and target work

The current-process hypothesis is:

```text
daily export becomes available
  -> coordinator scans records and compares urgency signals
  -> stale or incomplete data is discovered during triage
  -> coordinator chooses an informal review order
  -> operational follow-up occurs outside this example
```

This is a proposal, not a live observation. It identifies repeated comparison, invisible entry readiness, mixed normal and data-quality work, and unstructured ranking reasons as issues to validate in a real engagement.

The target flow removes those problems before selecting technology:

```text
read-only snapshot
  -> bind request actor, scenario, source, semantics, freshness, and access
  -> stop the batch when a contract or access precondition fails
  -> separate invalid or incomplete records into named escalations
  -> rank valid records deterministically with reason traces
  -> coordinator accepts, rejects, or investigates in the current session
  -> operational follow-up remains human-owned and outside this example
```

| Path | Condition | Result |
| --- | --- | --- |
| Normal | Bound synthetic actor and scenario, fresh snapshot, valid contracts | Ranked recommendation with evidence and reasons |
| Batch stop | Stale data, denied access, actor/scenario mismatch, duplicate identity, or contract drift | No recommendation; failed preconditions are returned |
| Record escalation | A record is missing or has an invalid required fact | The record is not scored and receives a named escalation |

## Intervention and responsibility

The simplest sufficient intervention is deterministic software plus human review:

| Retained responsibility | Owner |
| --- | --- |
| Snapshot, semantic, source, freshness, access, and identity checks | Deterministic replay Module |
| Priority score, tie-break, and reason trace | Deterministic replay Module |
| Accept, reject, or investigate | Demo logistics coordinator; session-local only |
| Policy, semantic, or workflow changes | Accountable human owner outside the replay |
| ERP mutation | Outside scope and denied |

AI is **deferred**. The explicit rules and evidence checks do not benefit from a model. A future enterprise shadow must first demonstrate a remaining language, synthesis, or explanation burden against this deterministic baseline.

## Contracts and controls

The example keeps independently governed records separate:

- `scenario.json` bounds the question, roles, outcome, and synthetic acceptance criteria.
- `semantic-definitions.json` versions the facts, identity, lifecycle, metric, source, ownership, and mappings.
- `decision-service.json` names the policy owner, inputs, deterministic rules, escalation, and non-persistent output.
- `access-decision.json` binds query and recommendation to a named synthetic subject, scenario, and source while denying controlled execution.
- `shipments.json` is the source snapshot; `read-only-result.json` is the golden result contract.

The replay fails closed when those records drift:

| Quality scenario | Required behavior |
| --- | --- |
| Source freshness | Exactly 60 minutes is accepted; any older snapshot returns no recommendation |
| Access | Denied permission, actor/scenario mismatch, or an access decision later than the replay returns no recommendation |
| Semantic integrity | Missing owner, review history, lifecycle, metric owner, definition, or source mapping returns no recommendation |
| Identity conflict | Duplicate `shipmentId` values stop the batch before ranking |
| Missing fact | The affected record escalates without a score |
| Persistent effect | Controlled execution remains denied and dispositions remain session-local |

## Validation and gates

`scripts/validate-example.sh` is the validation entry point. It validates the scenario schema and runs CLI contract tests for the golden replay, boundaries, tie-breaks, invalid facts, stale data, denied or mismatched access, contract drift, duplicate identities, session-local dispositions, the five-part read-only output contract, and the restrictions in `evidence/assurance.json`.

| Gate | Result | Restriction |
| --- | --- | --- |
| G1 | `passed` | Synthetic scenario shape only; not enterprise approval |
| G2 | `passed` | Synthetic released definitions and contract validation only |
| G3 | `passed` | Named synthetic subject/scenario and fixture access only |
| G4 | `passed` | Deterministic synthetic policy and replay tests only |
| G5 | `missing` | No controlled execution, audit, idempotency, recovery, or ERP adapter |
| G6 | `unverifiable` | No real shadow, production measure, adoption, or value evidence |

## Change, rollback, and next action

This revision replaces duplicated narrative documents, fictional approval reports, and documentary rehearsal events with one analysis and one machine-readable assurance ledger. The replay remains synthetic, deterministic, read-only, and reversible through Git; no data or runtime migration is involved.

For a real engagement, the accountable business owner must replace every synthetic owner, definition, source, access decision, baseline, target, support path, persistence decision, and acceptance statement with target-enterprise evidence. Until then, do not connect a real source, run an enterprise shadow, add AI, or enable write-back.
