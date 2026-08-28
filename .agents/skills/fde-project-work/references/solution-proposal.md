# Operating solution

Use this reference when the user asks what an operation should become, which intervention fits, or what should happen next. Produce the least detail that supports the decision.

## Minimum contract

1. **Operating problem and outcome.** Bound the user, workflow location, pain or opportunity, and desired operating result. Label unsupported enterprise claims and reference hypotheses.
2. **Current-work diagnosis.** Explain normal, exception, escalation, and rework paths and the material causes of delay, ambiguity, duplication, or risk.
3. **Target workflow.** Show what is eliminated, simplified, standardized, reassigned, or repaired before technology is selected.
4. **Intervention decision.** Choose the simplest sufficient mix of process change, information repair, deterministic software, human judgment, AI assistance, or governed action. State the AI-fit decision and evidence limits.
5. **Next accountable action.** Name the next decision or work package, its owner role, required input, and observable completion condition.

This contract is complete when the user can choose the next action without an unstated material assumption. It does not require a build backlog, pilot design, formal artefacts, or implementation unless the request or risk does.

## Conditional depth

Add only the detail activated by the case:

- **Material process ambiguity:** map handoffs, bottlenecks, exceptions, ownership, and change hypotheses in more detail.
- **Proposed implementation:** identify the first user-visible slice, capability and integration seams, acceptance checks, rollout, and rollback.
- **AI justified:** state model inputs, grounded outputs, abstention and escalation, prohibited autonomy, evaluation against the non-AI baseline, and how corrections become governed evidence.
- **Sensitive access or persistent effect:** state identity, privacy, security, approval, audit, idempotency, recovery, and authority evidence.
- **Value or expansion claim:** state baseline, target, adoption or outcome evidence, deviations, and the accountable follow-up.

When enterprise evidence is unavailable, a generic case may use explicit reference hypotheses and explain how a real operator or owner would validate them. Do not turn a missing fact into a fictional approval, integration, threshold, or outcome.

## Responsibility test

| Responsibility | Default fit |
| --- | --- |
| Remove work, clarify ownership, accept policy, resolve trade-offs | Human process owners and affected operators |
| Retrieval, stable calculations, schemas, access checks, policy enforcement | Deterministic software |
| Language interpretation, synthesis, explanation, bounded reasoning | AI, when it adds measured value |
| Ambiguous policy, exception ownership, accountable judgment | Human |
| Persistent side effects | Named, authorized, audited, idempotent, recoverable system action |

Keep policy thresholds out of prompts, keep missing evidence visible, and describe deterministic rules as deterministic rules. The value is a better operating decision or workflow, not the presence of a model.
