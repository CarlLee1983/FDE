# FDE Scenario-to-Action Method

This method is the standard way to turn one business scenario into a governed FDE capability. It composes established system-analysis methods into a small sequence of durable artefacts and decision gates. It is deliberately lighter than adopting every source framework end to end.

The method uses the research in [System-Analysis Methods That Can Inform FDE](docs/research/system-analysis-methods.md). That memo cites the official ISO, OMG, NIST, and SEI sources behind the method choices.

## Design Objective

Every FDE capability should be able to answer these questions before it is released:

1. What operating outcome and decision matter?
2. What in the current process creates avoidable delay, rework, ambiguity, or risk, and what should the target process become before technology is selected?
3. Which business facts, states, and relationships make the answer valid?
4. Which source evidence and semantic definitions support it?
5. Which decision logic, risk controls, and quality trade-offs constrain it?
6. How will we prove its value before increasing its authority?

## Collaborative Clarification

When the operating problem is too ambiguous to enter the six stages, clarify it as a dependency-ordered decision tree. The FDE investigates available facts and evidence; accountable participants decide intent, policy, ownership, trade-offs, and acceptance. Ask only the current **frontier**: decisions whose prerequisites are already settled. Give each decision a recommended answer grounded in known evidence, record the answer and rationale, then recompute the frontier.

Clarification is complete when every material branch is either decided, evidenced, or explicitly marked `missing` or `unverifiable`, and the result identifies a bounded operating outcome, user, process or case location, decision or action, and next accountable owner. It produces inputs for the applicable stage; it is not itself scenario approval, enterprise acceptance, or authority to implement.

## The Six Stages

```text
Frame → Map Work → Model Meaning → Specify Decision → Assure Control → Prove and Evolve
```

| Stage | Primary question | Method basis | Persistent artefact | Exit gate |
| --- | --- | --- | --- | --- |
| 1. Frame | What bounded outcome should an FDE improve? | ISO/IEC/IEEE 29148 requirements engineering | Approved scenario record | An owner accepts scope, constraints, baseline, target, and acceptance criteria |
| 2. Map Work | What should be removed, simplified, standardized, or reassigned before technology is selected? | BPMN / CMMN | Validated current and target process or case models with bottlenecks, change hypothesis, and intervention candidates | The process owner and affected users accept the current diagnosis, target paths, handoffs, exception ownership, and change hypothesis |
| 3. Model Meaning | What are the stable business facts and allowed lifecycle changes? | UML structure/state modelling; ISO/IEC 11179 registration pattern | Versioned object, link, state, metric, and source definitions | Owner, identity, definition, status, and lineage are present |
| 4. Specify Decision | What recommendation or action is being made, from which inputs? | DMN | Named decision service and rule/test set | Test cases cover normal, boundary, and escalation outcomes |
| 5. Assure Control | What access, action, and quality risks must be controlled? | NIST RMF; SEI ATAM | Risk/control record and quality-scenario decision record | Controls, approvals, trade-offs, and recovery needs are explicit |
| 6. Prove and Evolve | Does the smallest useful slice work in real operating conditions? | ISO/IEC/IEEE 15288 | Vertical-slice evidence and change record | Acceptance criteria pass; deviations have an accountable follow-up |

## Stage Details

### 1. Frame

Begin with an approved [scenario record](schemas/fde-scenario.schema.json), not a request to “build an agent.” The record captures the operating owner, user roles, process node, decision or action, baseline, target, required sources, semantic references, and acceptance criteria.

**Rule:** if there is no identifiable decision, action, or measurable outcome, it is research work—not yet an FDE delivery scenario.

### 2. Map Work

Use a BPMN model for a repeatable, prescriptive flow: handoffs, timers, approvals, and integrations. Use a CMMN-style case model when the next task depends on the evolving facts of an exception rather than a predetermined sequence.

First validate the current normal, exception, escalation, and rework paths. Identify waiting, duplicate checks, unclear ownership, semantic or evidence gaps, and controls that do not reduce material risk. Then design a technology-neutral target process: eliminate unnecessary work, simplify handoffs, standardize policy and meaning, clarify decision rights and exception ownership, and repair evidence or data gaps.

Record the change hypothesis and baseline that would show whether the redesign helps. The process owner and affected users must accept or correct the diagnosis and target flow before capability or AI selection. When that evidence is absent, keep the target process `proposed`.

Only after this process-readiness decision should the team mark candidate **FDE intervention nodes**. At a selected node an FDE may retrieve context, provide a recommendation, request approval, or execute an already approved controlled action. Compare workflow change, data or semantic repair, deterministic software, user-interface support, AI assistance, and governed action; select the simplest sufficient intervention. Do not treat every process step as a technology or AI opportunity, and treat `no AI` as a complete decision.

### 3. Model Meaning

Model three distinct things rather than collapsing them into one diagram:

| Model | Answers | Examples |
| --- | --- | --- |
| Structure model | What business things exist and how are they related? | Order, customer, exception, supplier |
| State model | Which lifecycle states and transitions are allowed? | Created → blocked → triaged → resolved |
| Semantic registry | What do terms, metrics, rules, and source mappings mean and who governs them? | `OrderException`, triage-cycle-time, authoritative order source |

Use a stable identity, definition, owner, source, status/version, and review history for every reusable semantic asset. A process sequence is not a substitute for a lifecycle state model; a source column name is not a business definition.

### 4. Specify Decision

If an FDE solution recommends, ranks, approves, or routes something consequential, write it as a named decision service. A DMN-style decision table is particularly useful where policies must be inspected and tested.

| Decision element | Required statement |
| --- | --- |
| Decision name | The specific decision being made |
| Inputs | Defined objects, states, measures, policies, and source versions |
| Logic | Rules, thresholds, priority, or reasoned advisory logic |
| Output | Recommendation, route, explanation, or requested action |
| Owner | Person or role accountable for the decision policy |
| Escalation | What happens when evidence is missing, rules conflict, or confidence is insufficient |

Separate decision logic from the process that calls it and from the UI or agent that presents it. This enables the same decision to be reused by a dashboard, workflow, or agent.

### 5. Assure Control

Evaluate risk before granting access to sensitive context or allowing a persistent action. Apply the NIST risk pattern proportionately: classify the scenario and action, select controls, test them, obtain the required authorization, and monitor ongoing evidence.

Capture material design trade-offs as quality scenarios before choosing implementation details. Examples include source freshness, authorization latency, explanation completeness, semantic-change impact, recovery time, and availability.

**Rule:** read-only evidence must be trustworthy before FDE delivery gains write authority. Controlled actions remain named, permissioned, approved where required, auditable, idempotent, and recoverable.

### 6. Prove and Evolve

Release the smallest end-to-end slice, usually one read-only inquiry for one approved scenario. It should return:

```text
result + semantic-definition version + source evidence + freshness status + access decision
```

Run new and existing processes in parallel when the outcome affects operating work. Compare results, reasons for differences, exceptions, user intervention, and the business metric. Accepted deviations become changes to the process, semantic assets, decision logic, controls, or application—not undocumented workarounds.

## Required Artefact Set

The following artefacts form the minimum analysis package for a scenario.

| Artefact | Created in | Maintained by | Needed before |
| --- | --- | --- | --- |
| Scenario record | Frame | Business owner with an FDE | Any delivery work |
| Current and target process/case models, bottleneck evidence, change hypothesis, and intervention candidates | Map Work | Business translator / process owner | Capability or decision-support design |
| Object, link, state, metric, and source definitions | Model Meaning | Ontology and data owners | Context retrieval |
| Decision service and tests | Specify Decision | Policy / decision owner | Recommendation or action |
| Risk/control and quality-scenario records | Assure Control | Security, privacy, architecture, and business owners | Release or permission increase |
| Vertical-slice evidence and change record | Prove and Evolve | FDE delivery owner | Expansion or automation |

## Decision Gates

| Gate | Question | Allowed next step |
| --- | --- | --- |
| G1 — Scenario approved | Is the outcome bounded, owned, and measurable? | Model work and meaning |
| G2 — Semantics grounded | Are required facts, states, metrics, sources, and owners defined? | Build read-only context retrieval |
| G3 — Evidence proved | Can users obtain a permitted, fresh, explainable result? | Build shared dashboard or advisory decision support |
| G4 — Decision controlled | Is consequential logic testable and governed? | Enable approval workflow |
| G5 — Action authorized | Are access, approval, audit, idempotency, and recovery controls tested? | Permit controlled write-back |
| G6 — Value demonstrated | Does production or shadow evidence meet acceptance criteria? | Reuse assets in an adjacent scenario |

## How This Fits the FDE Capability Roadmap

The method creates the inputs consumed by the proposed FDE modules:

```text
Scenario record
  → Scenario Registry Module
  → Ontology Asset Module
  → Context Resolution Module
  → Decision Support Module
  → Action Execution Module
```

The modules should use these artefacts through their interfaces rather than recreate them. This concentrates definition, validation, authorization, and traceability complexity in a few deep modules, providing leverage for all future FDE capabilities.

## First Workshop Sequence

| Workshop | Participants | Outcome |
| --- | --- | --- |
| Scenario framing | Business owner, users, FDE delivery owner | Approved scenario record and baseline/target |
| Work and meaning | Process owner, affected users, domain expert, data/ontology owner | Accepted current/target process models, bottleneck and change hypothesis, intervention candidates, minimum semantic asset set |
| Decision and control | Decision owner, security/privacy owner, architecture owner | Decision service outline, risk/control record, quality scenarios, first-slice acceptance test |

The next concrete step is to populate the scenario record with the project's first real FDE operating problem, then run the first two workshops. No platform-wide build should begin before G1 and G2 are satisfied.
