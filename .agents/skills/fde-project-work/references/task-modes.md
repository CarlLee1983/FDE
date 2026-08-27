# Task modes

Use [the source map](source-map.md) to open only the canonical sources needed by the selected mode. Each mode works from current repository sources and supplied evidence; it never fills a factual gap with a plausible enterprise detail. If a request spans modes, follow their dependency order. An unmet gate restricts authority, release, or completion claims; it does not prevent a bounded `proposed` solution from being designed.

## Scenario preparation

**Required inputs.** A bounded operating outcome, process or case location, prospective users, a decision or action, and evidence for the scenario contract's required fields. For claims about ownership, sources, semantic assets, metrics, baseline, target, or acceptance, require the corresponding real evidence.

**Steps and sources.** Read the current scenario schema and the method's `The Six Stages`, `Stage Details`, and `Required Artefact Set`. Use the schema as the structural contract and the method to determine which analysis artifacts remain before delivery. When required inputs contain material unresolved decisions, run [collaborative clarification](collaborative-clarification.md) before completing the record.

**Output contract.** Produce a scenario record or preparation package that identifies the current schema result, source evidence, and the decisions that a solution still needs. State the semantic-definition version, freshness, and access decision for any proposed read-only inquiry only when evidence establishes them; mark each unavailable component `missing` or `unverifiable`. Label a suggested safe scope as `proposed`, not as an access decision. End with the concrete inputs and participants needed to shape the solution; do not make artifact completion the outcome.

**Stop or gap condition.** Do not call a scenario approved, usable for delivery, or ready for a later gate merely because it has a well-formed shape. When real evidence or accountable acceptance is absent, keep the scenario `proposed`, identify the owner action needed, and continue to solution shaping only at the authority level the evidence supports.

## Operating solution shaping

Use this mode by default for an open-ended FDE request asking what to do, how the operation should improve, where AI could fit, or what solution to propose.

**Required inputs.** A bounded operating problem, prospective users, a process or case location, a decision or action, and whatever evidence is available for the current workflow, handoffs, exceptions, sources, semantics, constraints, and value. A fully approved scenario is helpful but not required to produce a `proposed` solution.

**Steps and sources.** Read the method's applicable stages and gates, the plan's `Capability Target` and `Guardrails`, and the implementation strategy's `Capability Map`, `Recommended Delivery Sequence`, `Module Seams and Ownership`, `Architecture Decision Rules`, and `Validation Strategy`. When material process or policy decisions are unresolved, run [collaborative clarification](collaborative-clarification.md) and carry its settled answers and evidence into the proposal. First map the as-is normal, exception, escalation, and rework paths and identify waiting, duplicate work, unclear ownership, semantic or evidence gaps, and avoidable controls. Redesign the workflow without assuming a technology: eliminate, simplify, standardize, clarify ownership, repair data or meaning, and use deterministic automation where it is sufficient. Only then evaluate AI against the remaining work. Read the authority-tier source when recommending an application form or any action. Use the [solution proposal contract](solution-proposal.md) to synthesize the deliverable.

**Output contract.** Deliver an evidence-grounded operating solution that changes a named workflow and gives a delivery team a buildable first vertical slice. Include the as-is diagnosis, changes made before technology selection, a technology-neutral target workflow, intervention choices, capability and integration seams, responsibility and authority boundaries, slice backlog, validation, rollout, measures, evidence status, and the next accountable action. Explicitly state whether AI is unnecessary, deferred, or justified at a specific retained step; when justified, separate deterministic logic, model responsibility, human judgment, and governed system actions. Keep the proposed authority tier separate from the evidenced access decision.

**Stop or gap condition.** Do not select AI before the process redesign is complete enough to show what work remains, and do not force AI into a task where elimination, standardization, deterministic software, or workflow change is the better fit. Report the AI-fit decision honestly, including `not needed` or `deferred pending evidence`. Do not invent an integration, policy, permission, source authority, baseline, target, or acceptance result. Bound unsupported parts of the solution as `proposed`, `missing`, or `unverifiable`. Stop only before an unsupported implementation, release, write-back, or authority claim—not before producing the safest useful solution and delivery plan.

## Capability build

**Required inputs.** An accepted solution boundary, evidence for any source, semantic-definition, identity, permission, target-system, or acceptance assertion involved, and the actual repository surface to change.

**Steps and sources.** Read the solution proposal, scenario schema, applicable method stage and gate, plan guardrails, and implementation strategy. Inspect the current codebase before describing implementation as present. Keep the slice end-to-end and route shared definition, evidence, and access complexity through the documented seams. When the request changes authority or includes write-back, read `Application Forms and Control Boundaries` and require the applicable control evidence.

**Output contract.** Deliver the narrowest working vertical slice with its code, tests, necessary documentation, evidence boundary, validation result, rollout or rollback instructions, and unresolved operational assumptions. A read-only slice returns `result + semantic-definition version + source evidence + freshness + access decision` and does not conceal a missing component.

**Stop or gap condition.** Do not implement an integration, permission, or persistent action on invented authority. If the accepted slice cannot be built within the evidenced boundary, deliver only the safe in-scope portion and report the exact blocked implementation decision.

## Gate-based review or assurance

**Required inputs.** The gate or control decision under review, the candidate artifacts, and direct evidence for the relevant scenario, semantics, result, decision, action, or value claim.

**Steps and sources.** Read the method's `Decision Gates`, the applicable `Stage Details`, and `Required Artefact Set`; read the plan's `Guardrails` and the implementation strategy's `Validation Strategy` when reviewing a capability slice. Read `Application Forms and Control Boundaries` when the review changes authority or includes write-back. Compare evidence to the current gate question and allowed next step. Verify freshness, provenance, access, and semantic-definition version for read-only results. Verify named controls, authorization, audit, idempotency, and recovery evidence before a write-back conclusion.

**Output contract.** Return `passed`, `missing`, and `unverifiable` sections. Each `passed` item names the supported criterion and direct evidence. Each `missing` or `unverifiable` item names the criterion, evidence status, and the resulting restriction on the next step. Include source evidence, freshness, access decision, and semantic-definition version where a read-only result is assessed.

**Stop or gap condition.** A proposed design, a schema-valid record, or a repository document alone does not prove target-enterprise acceptance, permissions, integrations, or live value. With incomplete evidence, issue an assurance result with the unresolved items rather than a gate pass or authority increase.
