# Task modes

Use [the source map](source-map.md) to open only the canonical sources needed by the selected mode. Each mode works from current repository sources and supplied evidence; it never fills a factual gap with a plausible enterprise detail. If a request spans modes, follow their dependency order and stop at the first unmet gate.

## Scenario preparation

**Required inputs.** A bounded operating outcome, process or case location, prospective users, a decision or action, and evidence for the scenario contract's required fields. For claims about ownership, sources, semantic assets, metrics, baseline, target, or acceptance, require the corresponding real evidence.

**Steps and sources.** Read the current scenario schema and the method's `The Six Stages`, `Stage Details`, and `Required Artefact Set`. Use the schema as the structural contract and the method to determine which analysis artifacts remain before delivery.

**Output contract.** Produce a scenario record or preparation package that identifies the current schema result, source evidence, and the required follow-up artifacts. State the semantic-definition version, freshness, and access decision for any proposed read-only inquiry only when evidence establishes them; mark each unavailable component `missing` or `unverifiable`. Label a suggested safe scope as `proposed`, not as an access decision.

**Stop or gap condition.** Do not call a scenario approved, usable for delivery, or ready for a later gate merely because it has a well-formed shape. Stop at preparation when the necessary real evidence or accountable acceptance is absent.

## Capability design or build

**Required inputs.** A scenario and its validated scope, the requested capability boundary, and evidence for any source, semantic-definition, identity, permission, target-system, or acceptance assertion involved. A build request also needs the actual repository surface to change.

**Steps and sources.** Read the scenario schema, the method's applicable stage and gate, the plan's `Guardrails`, and the implementation strategy's `Capability Map`, `Recommended Delivery Sequence`, `Module Seams and Ownership`, `Architecture Decision Rules`, and `Validation Strategy`. When the request changes authority or includes write-back, also read `Application Forms and Control Boundaries` from the authority-tier source. Inspect the current codebase before describing implementation as present. Keep the slice end-to-end and route shared definition, evidence, and access complexity through the documented seams.

**Output contract.** Deliver the narrowest coherent design or implementation with its evidence boundary, validation result, and a list of unresolved operational assumptions. A read-only slice returns `result + semantic-definition version + source evidence + freshness + access decision` and does not conceal a missing component. Keep the proposed authority tier separate from the evidenced access decision.

**Stop or gap condition.** Do not invent an integration, policy, permission, source authority, current baseline or target, or acceptance result. If a write-back would be in scope, stop before authorizing or implementing it until the current gate/control evidence supports it; report the unmet evidence and the highest safe advisory/read-only outcome.

## Gate-based review or assurance

**Required inputs.** The gate or control decision under review, the candidate artifacts, and direct evidence for the relevant scenario, semantics, result, decision, action, or value claim.

**Steps and sources.** Read the method's `Decision Gates`, the applicable `Stage Details`, and `Required Artefact Set`; read the plan's `Guardrails` and the implementation strategy's `Validation Strategy` when reviewing a capability slice. Read `Application Forms and Control Boundaries` when the review changes authority or includes write-back. Compare evidence to the current gate question and allowed next step. Verify freshness, provenance, access, and semantic-definition version for read-only results. Verify named controls, authorization, audit, idempotency, and recovery evidence before a write-back conclusion.

**Output contract.** Return `passed`, `missing`, and `unverifiable` sections. Each `passed` item names the supported criterion and direct evidence. Each `missing` or `unverifiable` item names the criterion, evidence status, and the resulting restriction on the next step. Include source evidence, freshness, access decision, and semantic-definition version where a read-only result is assessed.

**Stop or gap condition.** A proposed design, a schema-valid record, or a repository document alone does not prove target-enterprise acceptance, permissions, integrations, or live value. With incomplete evidence, issue an assurance result with the unresolved items rather than a gate pass or authority increase.
