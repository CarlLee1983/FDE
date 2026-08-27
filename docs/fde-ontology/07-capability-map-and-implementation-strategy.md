# 07 | Capability Map and Implementation Strategy

Back to the [chapter index](README.md).

## Purpose and Scope

This chapter converts the ontology-driven FDE model into a practical capability map. It is a product and technical-design proposal, not evidence of current implementation: the project currently contains no application code or technology constraints.

The recommended first objective is deliberately narrow: validate and improve one bounded operating process, then enable only the trusted context and controlled next action that its accepted target flow requires. The system should earn the right to automate more only after the process owner and affected users accept the workflow change and the less risky path is explainable and governed.

## Capability Map

| Capability | User value | Core responsibility | Depends on |
| --- | --- | --- | --- |
| Business scenario definition | Keeps delivery tied to a measurable operating problem | Captures topic, actors, process node, metric, and acceptance rule | Accountable business owner |
| Ontology asset lifecycle | Gives all applications shared business meaning | Defines, versions, reviews, and retires objects, links, and actions | Business definitions and governance |
| Source ingestion and alignment | Makes trusted data and knowledge available | Connects sources, maps semantics, checks quality, and records lineage | Source access and source owners |
| Governed context retrieval | Lets a user or agent work from relevant, permitted evidence | Resolves an ontology scope into data, knowledge, and provenance | Ontology, ingestion, and authorization |
| Decision support | Converts context into an understandable operating view | Produces dashboard measures, answers, or recommendations with evidence | Governed context retrieval |
| Controlled action execution | Turns approved decisions into real process outcomes | Validates preconditions, requests approval when required, writes back, and audits | Defined actions, target-system adapters, and authorization |
| Delivery and operating governance | Prevents assets and applications from becoming stale | Manages release, review, observability, incident response, and adoption metrics | All preceding capabilities |

## What to Build First

Before selecting a capability, validate the current normal, exception, escalation, and rework paths; identify the bottleneck or control problem; and obtain process-owner and user acceptance of a technology-neutral target flow. Compare process change, data or semantic repair, deterministic automation, interface support, AI assistance, and governed execution. Build the simplest intervention that can prove the change hypothesis; do not use a capability or model concept to decide the process prematurely.

### Capability 1: Scenario and Metric Registry

Create a small, structured record for every delivered scenario. It establishes the link between a business topic and an observable result.

| Minimum field | Why it matters |
| --- | --- |
| Scenario name and description | Gives the delivery a stable business identity |
| Process node and user role | Limits the scope to real work |
| Decision or action | Avoids building passive demonstrations |
| Metric baseline and target | Establishes a value test |
| Accountable business owner | Resolves definition and acceptance questions |
| Ontology assets and sources used | Creates the traceability chain |

This capability is lightweight but high leverage: it provides the single record against which every later dashboard, agent, workflow, and release can be judged.

### Capability 2: Ontology Asset Registry

Implement one **Ontology Asset Module** that owns the lifecycle of objects, links, and actions. Its interface should be small: callers request a defined asset version or submit a governed change; they do not manipulate raw definitions in scattered application code.

**Interface contract (conceptual):**

```text
getAsset(assetId, version) -> governed asset definition
resolveScope(scenarioId) -> allowed objects, links, actions, and definitions
proposeChange(change) -> reviewable change request
releaseChange(changeId) -> released asset version or validation failure
```

Its implementation may contain rich validation, version comparison, ownership checks, and impact analysis. That complexity belongs behind the module’s interface. This gives applications leverage and gives maintainers locality when definitions change.

### Capability 3: Provenance-Aware Context Retrieval

Implement a **Context Resolution Module** that accepts a user, a scenario, and a requested object or question. It returns only authorized enterprise context plus the evidence required to explain it.

```text
resolveContext(user, scenario, request) -> context bundle

context bundle =
  permitted objects and links
  source records or document references
  ontology asset version
  data freshness and quality status
  provenance references
```

This is the key seam between business applications and source systems. A dashboard, agent, or workflow should not independently discover databases, files, and permissions. The module hides source connectivity, semantic mapping, authorization, and lineage while presenting one usable context bundle.

### Capability 4: Controlled Action Orchestration

Implement an **Action Execution Module** only after read-only retrieval is trusted. It evaluates a declared ontology action, checks preconditions and permissions, requests approval where needed, invokes a target-system adapter, and emits an audit record.

```text
prepareAction(actor, action, input) -> proposed action or validation failure
approveAction(approver, actionRunId) -> approval decision
executeAction(actionRunId) -> outcome with audit reference
```

The interface exposes a controlled lifecycle rather than target-system details. Its implementation encapsulates retries, idempotency, write-back adapters, timeout handling, and compensation. This is a deep module: a few calls give every application the same safety behavior.

## Recommended Delivery Sequence

Build vertical slices that remain useful on their own. Do not start by constructing a generic agent platform or a company-wide knowledge graph.

Each slice assumes an accepted target-process boundary and named operational owner. If that evidence is absent, the slice remains a `proposed` design rather than implementation-ready work.

| Slice | End-to-end outcome | New capabilities | Acceptance evidence |
| --- | --- | --- | --- |
| 1. Trusted read-only inquiry | A named user answers one scenario question from permitted evidence | Scenario registry, minimum ontology assets, one source adapter, context resolution | Answer identifies source, freshness, definition version, and access decision |
| 2. Shared operational view | The same scenario appears as a dashboard metric and evidence trail | Metric calculation and dashboard adapter over the same context module | Dashboard and inquiry agree on definitions and values |
| 3. Human-approved recommendation | A user receives a recommended next action and can approve or reject it | Action definitions, recommendation recording, approval step | Each recommendation shows preconditions, evidence, owner, and decision log |
| 4. Controlled write-back | An approved action updates one business system safely | Action execution, one target-system adapter, audit and recovery path | Write-back is authorized, idempotent, traceable, and recoverable |
| 5. Adjacent scenario reuse | A second scenario reuses most semantic assets and controls | New scenario record and incremental ontology extension | Reuse is measured; no parallel definition of existing concepts is created |

## Module Seams and Ownership

The proposed modules are intentionally organized around changing concerns. Each module has one interface and may have multiple internal adapters. An adapter is justified only when a variation is real, such as a second source system or target system.

| Module | External interface is responsible for | Internal implementation may hide | Likely adapters when needed |
| --- | --- | --- | --- |
| Scenario Registry Module | Registering and resolving a delivery scenario | Validation, ownership rules, metric metadata | None initially |
| Ontology Asset Module | Reading released definitions and governing changes | Versioning, impact analysis, review workflow | Storage adapter only when storage varies |
| Context Resolution Module | Returning permitted, sourced context for a request | Source routing, mapping, data-quality checks, lineage assembly | ERP, CRM, document, and search adapters |
| Decision Support Module | Rendering a measure, answer, or recommendation from context | Prompting, calculations, ranking, presentation formatting | Dashboard and model adapters |
| Action Execution Module | Preparing, approving, and executing declared actions | Preconditions, retries, idempotency, audit, and compensation | Workflow, ERP, ticketing, or messaging adapters |
| Operations Module | Reporting health and handling review/release events | Monitoring, alert routing, review schedules, incident records | Observability adapter only when an external system is adopted |

## Non-Goals for the First Slice

- A universal ontology for the whole enterprise.
- Autonomous execution of high-impact actions.
- Ingestion of every document, spreadsheet, and system before a use case exists.
- A separate data-access implementation for each dashboard, agent, or workflow.
- Unversioned prompts or definitions that cannot be connected to business outcomes.

## Architecture Decision Rules

1. **One definition, many consumers.** A metric or business term must be declared once in the ontology asset module, then reused by every consumer.
2. **Read before write.** Prove retrieval quality, provenance, and access control before enabling write-back.
3. **Actions are declared, not improvised.** An agent may recommend an action, but execution must use a named ontology action with explicit conditions.
4. **Evidence accompanies output.** An answer, metric, recommendation, and write-back must identify the source, definition version, and relevant audit trail.
5. **Prefer depth over pass-through modules.** A module should remove recurring complexity from callers; avoid thin wrappers that only relay data.
6. **Introduce seams only for actual variation.** Begin with one adapter per source or target type; generalize when a second real adapter requires it.

## Capability Ownership and Return

FDE is a capability for forming and governing operating capabilities; it is not the owner of each scenario's business behaviour.

| Owner | Owns | Does not own |
| --- | --- | --- |
| FDE core | Scenario-to-action method, evidence states, shared delivery contracts, gate assessment, authority constraints, and capability-promotion rules | Domain objects, policies, calculations, decision thresholds, source mappings, or target-system behaviour for a particular scenario |
| Case capability | Its domain semantics, inputs, decision logic, integrations, tests, operating evidence, version, and rollback | Cross-scenario FDE policy or authority to promote its own behaviour into FDE core |

Repository location does not change ownership: an example can demonstrate an FDE invariant without becoming its canonical source, and a reusable-looking function remains case-owned until promotion is accepted.

After a case slice is validated, return its learning as a reviewable capability-change candidate rather than moving case code into FDE core. Classify each observation as case-specific behaviour, an already-established FDE invariant, a proposed cross-scenario candidate, or rejected generalization. A candidate derived from cases is eligible for promotion only when:

1. At least two independent runnable scenarios exhibit the same non-domain complexity.
2. The proposed Module has a small domain-neutral Interface and hides meaningful repeated Implementation complexity.
3. Both scenarios replay equivalently through the proposed seam, including normal, boundary, missing, conflicting, and prohibited cases where applicable.
4. An accountable project owner accepts the shared contract, version, observability, release, and rollback path.
5. Promotion preserves each case's independent authority, versioning, and rollback; it does not turn schema validity or synthetic evidence into enterprise acceptance.

A requirement already established by this project's canonical method or control sources remains an FDE invariant; it does not need to be rediscovered through two cases. Case evidence may test that invariant but does not redefine it.

## Validation Strategy

| Level | What to verify | Example evidence |
| --- | --- | --- |
| Ontology asset | Definition, owner, source, version, and impact are valid | A proposed asset change is rejected when ownership or source is missing |
| Context resolution | Access, semantic mapping, freshness, and provenance are correct | Two users receive different permitted context for the same request |
| Decision support | Result uses the resolved context and does not conceal uncertainty | Dashboard and agent agree on a metric and source basis |
| Action execution | Preconditions, approval, audit, idempotency, and recovery work | A repeated approved request does not duplicate an external action |
| Scenario outcome | The operating metric improves or the scenario is retired | Baseline and post-release measures are reproducible |

## Decisions Needed Before Implementation

1. Which business scenario and current operating path will be the first vertical slice?
2. Which bottleneck or control problem is evidenced, and has the process owner accepted the technology-neutral target flow, ownership, and change hypothesis?
3. Which intervention is the simplest sufficient choice, and which higher-complexity options—including AI—were deferred or rejected?
4. Which source system can provide the required read-only data with an accountable owner?
5. What identities, permissions, and audit mechanisms already exist and must be integrated?
6. Which delivery environment and technology constraints apply to the project?
7. What action, if any, is appropriate for the first controlled write-back?

## Proposed Next Working Session

Select one scenario, validate its current process, and agree on a technology-neutral target flow and change hypothesis. Then choose the simplest sufficient intervention and define only the minimum object/link/action set and evidence-producing path it needs. That produces a concrete implementation contract without prematurely choosing AI, a generic platform, or an ontology broader than the first useful purpose.
