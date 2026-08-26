# System-Analysis Methods That Can Inform FED

**Purpose.** This memo identifies established methods that complement FED’s scenario registry, ontology assets, evidence-aware context resolution, decision support, controlled action, and governance. It is research input, not a claim that FED must certify against or fully implement any standard.

## Source facts

### 1. Requirements engineering — ISO/IEC/IEEE 29148:2018

[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) specifies requirements-engineering processes, required information items and their contents, and guidance for applying the system and software life-cycle processes. ISO records the 2018 edition as confirmed in 2024.

**FED use.** Treat the scenario record as the initial requirements information item, then make its decision, users, scope, success metric, constraints, source evidence, and acceptance criteria explicit and reviewable. This gives scenario discovery a disciplined path to a testable requirement without prescribing a particular delivery method.

### 2. Process and case modelling — OMG BPMN and CMMN

[BPMN 2.0.1](https://www.omg.org/spec/BPMN/2.0.1) is an OMG/ISO notation for business processes. OMG describes it as a graphical notation intended to be understandable by business users while retaining process semantics useful to technical users. [CMMN](https://www.omg.org/spec/CMMN/) is the companion standard for case-oriented work; OMG positions BPMN, CMMN, and DMN as complementary standards.

**FED use.** Use BPMN for repeatable, prescriptive flows (handoffs, timers, approvals, integrations); use a case model when work is exception-driven and the next task depends on the evolving situation. In either, mark the exact process/case node at which the FED scenario reads context, recommends a decision, or requests a controlled action.

### 3. State and structural modelling — OMG UML

[UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) is a formal OMG specification. Its normative specification groups structural modelling separately from behavioural modelling and includes dedicated state-machine and activity formalisms.

**FED use.** Model an operational object’s permitted states, transitions, triggering events, and guards separately from the process diagram. Model the stable business concepts and their relationships separately again. This prevents an ontology’s object definitions, a workflow’s sequence, and a record’s lifecycle from being silently conflated.

### 4. Metadata and semantic asset registration — ISO/IEC 11179

[ISO/IEC 11179-1:2023](https://www.iso.org/standard/78914.html) provides the framework for metadata registries, where metadata means descriptions of data. [ISO/IEC 11179-6:2023](https://www.iso.org/standard/78916.html) defines common registration information and procedures, including administration, identification, naming, and definition, for registry items.

**FED use.** Borrow the registry discipline for semantic assets: give each business term, metric, object, relationship, source mapping, and rule a stable identity, clear definition, owner, status/version, and change/review history. This complements an ontology; it does not require FED to implement a full ISO metadata registry.

### 5. Decision modelling — OMG DMN

[DMN](https://www.omg.org/dmn/) is an OMG modelling language and notation for precise business-decision and business-rule specification. OMG states that it is designed to work alongside BPMN and/or CMMN and supports unambiguous decision tables; the [DMN 1.4 specification](https://www.omg.org/spec/DMN/1.4/PDF) defines syntax and semantics, including the FEEL expression language.

**FED use.** Express high-consequence or repeatable decisions as named decision services: required inputs, source/definition versions, decision logic or policy, output, owner, and escalation. Keep decision logic distinct from both the process that calls it and the agent interface that explains it.

### 6. Risk, controls, authorization, and monitoring — NIST RMF

[NIST SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) defines a disciplined risk-management process covering categorization; control selection, implementation, and assessment; authorization; and continuous monitoring. NIST states that the framework integrates security and privacy into the system development life cycle and establishes control responsibility and accountability.

**FED use.** Apply the pattern proportionately to every capability that accesses sensitive context or performs a write: classify the scenario and action risk; select and document controls; test them; require the right approval; continuously monitor evidence, access, failure, and drift. This supports the project’s existing principle that advisory capability precedes autonomous write authority.

### 7. Architecture quality trade-offs — SEI ATAM

The original [Architecture Tradeoff Analysis Method (ATAM) report](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/) describes a structured technique for evaluating a software architecture against competing quality attributes such as modifiability, security, performance, and availability. The [SEI method collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) describes scenario-based evaluation that exposes risks, sensitivity points, and trade-off points.

**FED use.** Before choosing an integration, storage, agent, or workflow architecture, express the decisive quality attributes as measurable scenarios—for example, source freshness, authorization latency, traceability, recovery time, and semantic-change impact. Record the trade-off and its accepted risk; do not conceal it in a technology choice.

### 8. Life-cycle tailoring, validation, and iterative delivery — ISO/IEC/IEEE 15288

[ISO/IEC/IEEE 15288:2023](https://www.iso.org/standard/81702.html) establishes a common framework of system life-cycle process descriptions. ISO says selected processes can be applied across life-cycle stages, iteratively and concurrently, and that the standard does not prescribe a specific life-cycle model, development method, or modelling technique.

**FED use.** Use a small vertical slice as the unit of delivery: one approved scenario, its minimum semantics and sources, one read-only result, and observable acceptance evidence. Iterate through the same analysis and validation loop as scope expands; maintain the shadow-operation comparison before increasing action authority.

## Proposed FED synthesis (not sourced fact)

The methods fit different concerns and should be used as a lightweight, traceable stack—not as eight parallel ceremonies.

| FED analysis question | Primary method | Persistent FED artefact | Exit evidence |
| --- | --- | --- | --- |
| Which operating problem and outcome matter? | ISO/IEC/IEEE 29148 | Approved scenario and acceptance criteria | Owner accepts scope, baseline, target, and constraints |
| Where does the work and exception occur? | BPMN or CMMN | Process/case model with FED intervention node | Users validate normal, exception, and escalation paths |
| What must remain true about business entities? | UML state/structure modelling | Object, relationship, state, and transition definitions | Domain owner validates terms and forbidden transitions |
| Which data definitions are reusable and governed? | ISO/IEC 11179 registration pattern | Versioned semantic asset and source mapping | Identity, owner, definition, status, and lineage are present |
| What decision is being supported or automated? | DMN | Decision service / decision table with inputs and output | Test cases cover rules, boundaries, and escalation |
| What risks constrain access or action? | NIST RMF | Risk/control/approval/monitoring record | Controls and authorization are tested before release |
| What qualities conflict in the design? | ATAM | Prioritized quality scenarios and trade-off decision | Material risks and mitigation are explicit |
| Does the smallest working capability meet its purpose? | ISO/IEC/IEEE 15288 | Vertical-slice validation and shadow-operation evidence | Acceptance criteria pass; observed gaps become owned changes |

### Suggested order for the first FED method pack

1. Run a requirements-and-scenario workshop; publish one bounded scenario.
2. Map its operating flow (BPMN/CMMN) and the relevant entity lifecycle (UML state model).
3. Register only the semantic assets and source mappings necessary for that slice.
4. Model any material recommendation or rule as a DMN-style decision service.
5. Evaluate risk/controls before permitting context access or write-back; use quality scenarios to resolve architecture trade-offs.
6. Release read-only first, validate it in shadow operation, then feed measured deviations into the next iteration.

## Deliberate boundaries

- BPMN/CMMN describe work coordination; DMN describes decision logic; UML state models describe allowed lifecycle transitions. FED should not force one notation to do all three jobs.
- A metadata registry pattern governs descriptions and identities; it is not a replacement for source-system data, an ontology graph, or access controls.
- NIST RMF is a security/privacy framework. Its control and authorization pattern is reusable, but FED should tailor it to its organisational and regulatory context.
- ISO/IEC/IEEE 15288 permits iterative tailoring; it should guide validation discipline, not introduce heavyweight phase gates for a small scenario.

## Research notes

- Sources are standards owners or the originating institutional authors: ISO, OMG, NIST, and Carnegie Mellon University’s Software Engineering Institute.
- The **Source facts** sections summarize what those sources state. The **FED use**, **Proposed FED synthesis**, and **Deliberate boundaries** sections are the author’s design synthesis for this repository.
- Accessed 2026-08-26. Some ISO normative text is paywalled; claims above are limited to the official public abstracts and catalogue descriptions.
