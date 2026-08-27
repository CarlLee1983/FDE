# Proposed operating solution: Customer Refund-Status Inquiry

> **Proposed synthetic.** This package validates an FDE analysis-to-proposal delivery flow. It does not establish target-enterprise facts, permissions, integrations, acceptance, or value.

## Decision requested

Decide whether to authorize a de-identified, read-only shadow replay of the deterministic first slice.

**Recommendation:** Standardize evidence and refund-state interpretation before adding technology; a deterministic read-only summary is sufficient for the first slice, so AI is not needed.

## Operating outcome and scope

For the **Customer-service representative** at **Refund-status inquiry handling**, the proposed change is to confirm an evidence-bearing refund-status response or route the inquiry to finance. The synthetic handling-time hypothesis is **8 minutes to 3 minutes**; **incorrect refund-status responses must not increase**.

### Included

- Refund-status inquiry only
- Read-only order and payment evidence
- Human-confirmed response template
- Finance escalation for every unsupported or unsafe case

### Excluded

- Refund approval
- Compensation
- Payment disputes
- Direct AI-to-customer responses
- Write-back

## Current-process diagnosis

The proposed current normal flow is:

```text
Receive inquiry → Find order → Open payment system → Inspect refund state → Compose response → Confirm response with customer
```

The proposed exception path is:

```text
Representative detects an unclear, missing, or unsafe state → Representative gathers context again → Representative escalates to finance → Finance interprets the exception → Representative resumes response handling
```

| Diagnosis hypothesis | Operational effect | Evidence status |
| --- | --- | --- |
| Cross-system lookup | The representative switches context and reconstructs evidence before answering. | `proposed` |
| Manual state interpretation | Source-specific refund states must be translated into customer-safe language during every inquiry. | `proposed` |
| Exceptions are discovered late | Missing, conflicting, stale, prohibited, or unauthorized cases consume handling time before escalation. | `proposed` |
| Prose composition is not the primary delay | Automating language first would leave the evidence and semantic bottlenecks intact. | `proposed` |

These are synthetic hypotheses to confirm or correct with the process owner and affected users. They are not findings from observed enterprise work.

## Process redesign before technology

1. **Eliminate repeated lookup.** Assemble one permitted read-only evidence bundle before the representative interprets status.
2. **Standardize meaning.** Publish one finance-owned semantic version for the three supported normalized states.
3. **Move controls forward.** Check record presence, consistency, freshness, dispute status, and access before presenting a status.
4. **Clarify ownership.** Customer service owns the normal inquiry; finance owns every unsupported or unsafe state.
5. **Keep judgment human.** The representative confirms the response; the view never answers the customer directly.

## Technology-neutral target flow

```text
Retrieve — Resolve permitted order and payment evidence with source identity and retrieval time.
  → Control — Evaluate record presence, consistency, freshness, dispute status, and access.
  → Normalize — Map only one of the three supported states using finance-owned versioned rules.
  → Confirm — Review the evidence-bearing summary and confirm or reject the response template.
  → Escalate — Resolve every abstained, disputed, failed, rejected, stale, conflicting, missing, or unauthorized case.
```

**Normal outcome:** A human-confirmed response based on a supported normalized state.

**Exception outcome:** An explicit abstention with a finance escalation reason.

**Human override:** A representative may reject the template and escalate, but cannot alter the normalized state or policy.

## Process-readiness decision

The as-is path, target flow, handoffs, exception ownership, baseline, and semantic contract have not been accepted by accountable target-enterprise participants. The process therefore remains `proposed`. This package supports a decision about preparing a shadow replay; it does not authorize implementation or pilot use.

## Intervention selection

| Retained need | Selected intervention | Responsibility | Why sufficient |
| --- | --- | --- | --- |
| Evidence spread across systems | Read-only evidence aggregation | Deterministic software | Retrieval and provenance assembly are stable and testable. |
| Source-specific refund states | Versioned deterministic mapping | Deterministic software with finance policy ownership | The supported state set is closed and identical inputs must produce identical outcomes. |
| Unsafe or ambiguous cases | Abstention and finance escalation | Deterministic routing plus human judgment | The first slice must not infer policy or conceal missing evidence. |
| Customer response | Response template for human confirmation | Customer-service representative | A template is sufficient; direct automation would exceed the proposed authority. |

## AI-fit decision

**AI-fit: not needed for the first slice.** Retrieval, state mapping, access checks, exception rules, and response templates are deterministic. Adding AI would not remove the diagnosed bottleneck.

Evaluate AI later only for measurable language or wording value after the deterministic shadow baseline is accepted; AI may not map states, fill missing evidence, answer customers directly, or authorize an action.

## Semantic and exception contract

Proposed semantic version: `refund-status-semantics@0.1.0-proposed`. Proposed owner: **Finance refund owner**.

| Normalized state | Meaning | Route |
| --- | --- | --- |
| Refund not initiated | No refund initiation is evidenced for the order. | Present read-only summary for human confirmation. |
| Refund processing | Refund initiation is evidenced and completion is not yet evidenced. | Present read-only summary for human confirmation. |
| Refund completed | Refund completion is evidenced by the permitted payment source. | Present read-only summary for human confirmation. |

Every other or unsafe case abstains and escalates:

- Missing records
- Conflicting states
- Stale data
- Failed refunds
- Rejected refunds
- Payment disputes
- Insufficient access
- Any unsupported state

## First buildable vertical slice

**Read-only refund summary.** A customer-service representative receives one evidence-bearing summary or a finance escalation, then confirms the response.

Every returned result must expose:

- Normalized refund status or abstention
- Source evidence
- Retrieval time
- Semantic-definition version
- Freshness status
- Access decision
- Response template or escalation reason

Capability and integration seams remain case-owned and proposed:

| Case seam | Status | Restriction |
| --- | --- | --- |
| Proposed order and payment read model | `proposed` | No enterprise source or freshness SLA is established. |
| Refund semantic definition | `proposed` | Finance-owner acceptance is missing. |
| Context and access decision | `proposed` | No enterprise identity or permission evidence is established. |
| Customer-service support view | `proposed` | No runtime, hosting, or telemetry decision is established. |

Explicitly deferred:

- Enterprise source integration
- Identity and authorization integration
- Persistent telemetry
- Direct customer response
- AI wording assistance
- Refund approval or compensation
- Write-back

## Authority and controls

**Proposed application form:** Read-only customer-service support view.

**Authority boundary:** Read-only; no write-back; human confirmation required.

**Enterprise access decision:** `missing`. The package authorizes no enterprise access, pilot, direct customer response, persistent telemetry, or system effect.

## Validation, rollout, and rollback

Proposed method: **De-identified historical shadow replay**.

Entry criteria:

- Both owner roles accept the target flow and semantic contract
- A de-identified replay set is authorized and available
- Source, identity, access, freshness, and retention decisions are evidenced
- An accepted handling-time and incorrect-response baseline exists

| ID | Criterion | Proposed threshold | Failure effect |
| --- | --- | --- | --- |
| V1 | Supported-state mapping | 100% mapping for Refund not initiated, Refund processing, and Refund completed | Blocks shadow acceptance |
| V2 | Abstention | 100% of missing, conflicting, stale, failed, rejected, disputed, unauthorized, and unsupported cases abstain | Blocks shadow acceptance |
| V3 | Handling time | Average simulated handling time <= 3 minutes | Blocks pilot proposal |
| V4 | Evidence contract | Every result exposes source evidence, retrieval time, semantic version, freshness, and access decision | Blocks shadow acceptance |
| V5 | Response quality | Incorrect refund-status responses do not increase against an accepted baseline | Blocks pilot proposal |
| V6 | Owner acceptance | Both named owner roles accept the shadow result | Blocks pilot proposal |

**Rollback:** Remove the support view from the shadow workflow and return to the current inquiry process. No business-system compensation is required because the slice performs no write-back.

## Evidence ledger

| ID | Statement | Status | Source | Delivery restriction |
| --- | --- | --- | --- | --- |
| E1 | The package and every business fact or number in it are proposed synthetic. | `evidenced` | request.md and analysis-package.json | No target-enterprise fact may be inferred. |
| E2 | Cross-system lookup and manual state interpretation are the main delays. | `proposed` | request.md diagnosis hypothesis | Requires process observation and owner/user confirmation. |
| E3 | Average handling time can improve from 8 minutes to 3 minutes without increasing incorrect responses. | `unverifiable` | proposed synthetic baseline and target in request.md | Requires an accepted baseline and authorized shadow replay. |
| E4 | The three normalized refund states and exception policy are accepted business definitions. | `missing` | finance-owner evidence not supplied | Blocks G2 and any real-data implementation. |
| E5 | Enterprise order and payment sources can be read with appropriate freshness and access decisions. | `missing` | source, identity, permission, and freshness evidence not supplied | Blocks enterprise integration and shadow replay. |
| E6 | The named owner roles accept the current diagnosis, target flow, semantics, thresholds, and rollout. | `missing` | no accountable acceptance record supplied | Keeps the scenario and solution proposed. |
| E7 | AI is unnecessary for the deterministic first-slice contract. | `proposed` | process diagnosis, intervention allocation, and closed rule set in this package | Revisit only after shadow evidence shows residual language or wording burden. |
| E8 | Write-back or direct customer response is authorized. | `missing` | no authorization or G5 control evidence supplied | Write-back and direct automation remain prohibited. |

## Next accountable action

Run a process-and-semantics acceptance session, then authorize a de-identified shadow replay only if the entry criteria are met.

**Owner roles:** Customer-service operations lead and Finance refund owner.

Required inputs:

- Observed current normal, exception, escalation, and rework paths
- Accepted handling-time and response-quality baselines
- Finance-owned state and exception definitions
- Source, identity, access, freshness, privacy, and retention decisions
- Authorized de-identified replay set

**Observable completion:** Both owners sign an acceptance record that names the target flow, semantic version, thresholds, evidence access, and shadow boundary.

## Cross-format consistency anchors

These anchors are generated from the canonical package and checked deterministically across the document, HTML, and decision deck:

- C1 — Evidence boundary: Proposed synthetic
- C2 — Scope: Refund-status inquiry only
- C3 — Baseline and target: 8 minutes to 3 minutes
- C4 — Supported states: Refund not initiated | Refund processing | Refund completed
- C5 — AI-fit: AI-fit: not needed for the first slice
- C6 — Authority: Read-only; no write-back
- C7 — Process owner: Customer-service operations lead
- C8 — Semantic owner: Finance refund owner
