# Operating solution proposal

Use this contract when the requested outcome is a solution, roadmap, architecture, or answer to “what should we build?” The proposal is a delivery decision, not another inventory of method artefacts.

## Proposal contract

Produce the smallest solution that changes a named operating outcome and can be delivered end to end. Include:

1. **Operating outcome.** Name the user, current workflow or pain, decision or action, baseline and target. Mark unsupported enterprise facts `missing` or `unverifiable`.
2. **Current-process diagnosis.** Show the as-is normal, exception, escalation, and rework paths. Identify avoidable work, waiting, duplicate checks, unclear handoffs or ownership, semantic inconsistency, evidence gaps, and controls that do not reduce material risk.
3. **Process redesign.** State what should be eliminated, simplified, standardized, reassigned, or repaired before introducing technology. Explain which constraints genuinely remain and why.
4. **Target operating flow.** Show the improved sequence from source evidence to user decision and any system effect, including exception, escalation, and human-override paths. The flow must be understandable without naming a model or product.
5. **Process-readiness decision.** State whether the as-is diagnosis and target flow have been confirmed by the accountable process owner and affected users, whether handoffs and exception owners are named, and whether a baseline exists. If this evidence is absent, keep the process `proposed` and defer AI selection; do not use a model concept to conceal an unresolved process decision.
6. **Intervention selection.** For each retained problem, choose the simplest sufficient intervention: process or policy change, data or semantic repair, deterministic software, user-interface or workflow support, AI, or a governed system action. Explain rejected higher-complexity choices.
7. **AI-fit decision.** Only after steps 2–6, state whether AI is `not needed`, `deferred`, or `justified` at a named step. Justification must identify the interpretation, language, synthesis, or bounded-reasoning advantage and the evidence needed to prove incremental value over the redesigned non-AI baseline. Keep stable calculations, thresholds, access checks, policy enforcement, and execution controls deterministic.
8. **Responsibility, capability, and integration design.** Assign each retained step to deterministic software, an AI model if justified, a human, or a governed system action. Identify only the source, semantic, context, decision-support, application, identity, observability, and target-system seams required for the first slice. Treat an unverified integration as `proposed`. If AI is used, state model inputs, grounded outputs, abstention behavior, and prohibited autonomy.
9. **First vertical slice.** Define one user-visible workflow that remains useful on its own, the components and work packages needed to deliver it, and what is explicitly deferred. Prefer a slice that proves the redesigned process and deterministic baseline before adding AI; include AI only when the slice cannot deliver its intended outcome without it. Avoid platform-first backlogs.
10. **Authority and controls.** Separate the proposed application form from an evidenced access decision. Name approval, privacy, security, audit, quality, recovery, and write-back controls only when relevant to the slice.
11. **Validation and rollout.** Define test cases, explicit pass/fail thresholds, acceptance owners, pilot or shadow entry criteria, user feedback, operational measures, observability, rollback, and the evidence required to expand scope or authority. When an AI experiment is justified, add a versioned evaluation set and cover task success, groundedness, abstention, prompt injection, sensitive-data handling, output-contract adherence, latency, cost, and incremental benefit over the non-AI baseline when each is material. Label a threshold `proposed` until the accountable owner accepts it, and name which failure blocks the next rollout stage.
12. **Evidence ledger.** Classify material statements as `evidenced`, `proposed`, `missing`, or `unverifiable`, cite the supporting source, and explain how each gap limits delivery or authority.
13. **Next accountable action.** End with the next decision or work package, its owner role, required inputs, and observable completion criterion.

Use diagrams or tables only when they make responsibility, sequence, or architecture materially clearer. A proposal can reference scenario and analysis artefacts, but those artefacts are supporting evidence rather than the headline result.

## Responsibility test

Use the following allocation unless scenario evidence justifies another:

| Responsibility | Best fit |
| --- | --- |
| Remove unnecessary work, clarify ownership, accept policy, and resolve cross-functional trade-offs | Human process owners and affected operators |
| Source retrieval, stable calculations, thresholds, schemas, access checks, and policy enforcement | Deterministic software |
| Language understanding, synthesis, explanation, and bounded reasoning over a permitted context bundle | AI model |
| Ambiguous policy decisions, exception ownership, approval, and accountable operational judgment | Human |
| Persistent side effects | Named, authorized, audited, idempotent, and recoverable system action |

Do not hide a policy threshold inside a prompt, let a model silently fill missing business evidence, or describe a deterministic rules engine as AI. The competitive value must come from a better operating decision or workflow, not from the presence of a model.

## Completion test

The proposal is complete only when a delivery team can answer all of these from it:

- What changes for which user?
- What is wrong with the current process, and which work is removed or simplified before technology is added?
- What does the target process look like without assuming AI?
- Why is each intervention the simplest sufficient choice?
- Is AI unnecessary, deferred, or justified—and what evidence would prove incremental value?
- What is the first end-to-end workflow to build?
- Which real sources, permissions, and integrations are established versus proposed?
- If AI is in scope, how will the model abstain or escalate when evidence is insufficient?
- How will the slice be tested, introduced into real work, measured, and rolled back?
- What exact owner action unlocks the next step?

If one answer is unavailable, mark it with its evidence status and resulting restriction. Do not replace the missing answer with more documents or generic discovery work.
