---
name: fde-project-work
description: Analyze an operating problem, redesign its workflow, and select the simplest sufficient intervention, including whether AI fits. Use for FDE case analysis and operating-solution shaping, or for delivery and assurance assistance when the user explicitly requests them; not for routine repository maintenance.
---

# FDE operating analysis

Turn an operating problem into a decision the user can act on. The default outcome is a **minimum operating solution**, not an artefact package or implementation:

1. operating problem and outcome;
2. current-work diagnosis;
3. technology-neutral target workflow;
4. intervention and AI-fit decision with evidence limits;
5. next accountable action.

Analysis is complete when these five parts let the user choose the next action. Enterprise acceptance, gate passage, or working code are separate outcomes.

## Core analysis flow

1. **Frame.** Bound the user, workflow location, operating outcome, and decision. In a generic case, state testable **reference hypotheses** instead of demanding enterprise evidence or presenting assumptions as facts.
2. **Diagnose.** Trace normal, exception, escalation, and rework paths. Identify avoidable work, waiting, duplicate checks, unclear ownership, semantic ambiguity, evidence gaps, and controls that do not reduce material risk.
3. **Redesign.** First eliminate, simplify, standardize, reassign, and repair the work without assuming technology.
4. **Select.** Compare process or responsibility change, information or semantic repair, deterministic software, interface support, human judgment, AI assistance, and governed action. Choose the simplest sufficient intervention.
5. **Form the solution.** Return the five-part minimum operating solution at the least depth that supports a sound decision.

When the user asks for a **proposal**, read [operating solution](references/solution-proposal.md) and persist the proposal as an editable Markdown source plus a standalone, responsive, print-ready HTML communication document in the requested repository location, or beside the case material when no location is specified. These files are the proposal deliverable; a chat summary alone is incomplete. Keep them `proposed` until the required enterprise evidence and accountable acceptance exist.

When unresolved choices materially change the diagnosis or recommendation, read [collaborative clarification](references/collaborative-clarification.md), investigate the facts you can reach safely, request the facts you cannot reach from a role that holds them, and route policy, scope, ownership, and authorization decisions to the accountable role.

When new information arrives that may change the bounded problem, target workflow, intervention, authority, acceptance, or value of a conclusion you already gave, read the same reference before revising. Keep the prior conclusion and its basis, bound the new information's source, time, version, and scope, recompute only the conclusions whose facts, rules, or assumptions the new information actually changes, retain the rest unchanged, and name the work that can continue while an open decision waits. Information under a different scope with no dependency on the case widens nothing: offer any cross-scope comparison or control change as an option, never as a task. This reconciliation adds no artefact and no gate to an analysis that has no such conflict.

## Depth and evidence

Use **sufficient depth**. Add models, schemas, formal decision logic, controls, research, or executable validation only when material uncertainty, risk, authority, persistence, or an explicit request justifies them.

Keep repository proposals separate from target-enterprise facts. Classify material claims as `evidenced`, `proposed`, `missing`, or `unverifiable`; cite provenance and freshness when they matter. Examples may prove reasoning or repository behavior, never enterprise acceptance, access, authority, or value.

Use [the source map](references/source-map.md) only to locate detail needed by the current branch. Use [task modes](references/task-modes.md) when the user explicitly asks for a proposal, scenario record, implementation, or assurance review.

## AI boundary

**穩定規則交給軟體，語言負擔才考慮 AI。** Apply this as the core intervention principle after workflow redesign. Assign stable rules, calculations, permissions, policy enforcement, and repeatable state transitions to deterministic software. Consider AI only for retained work whose material burden comes from language interpretation, synthesis, explanation, or bounded reasoning, and require evidence that it adds value over the non-AI workflow. Keep persistent effects human-governed or explicitly authorized. `AI not needed` and `AI deferred pending evidence` are complete decisions.

## Conditional delivery and assurance

Implementation begins only from an explicit build or change request with an accepted boundary. Then read [the delivery loop](references/agent-delivery-loop.md), build the smallest coherent slice, and validate it proportionately.

Use assurance gates only when a conclusion depends on real source access, release, authority increase, persistent action, or a value claim. A gap restricts the claim or action; it does not make a generic analysis incomplete. Before recommending persistent write-back, require direct evidence for authorization, audit, idempotency, recovery, and accountable ownership.

When multiple independent cases reveal the same non-domain analysis need, read [capability-return review](references/capability-return-review.md). Case-specific behavior remains with the case until evidence justifies a governed change to the core skill.

## Case evaluation

Evaluate this skill across varied operating cases. A strong result bounds the problem, understands the whole workflow, redesigns work before technology, selects an appropriate intervention, preserves evidence boundaries, and enables the user's next action. File count, code volume, gate count, and runnable examples are not progress measures.
