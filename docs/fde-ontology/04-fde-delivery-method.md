# 04 | FDE Delivery Method

Back to the [chapter index](README.md).

## Diagram Definition

The diagram configures an FDE squad with three capabilities: business translator, data/ontology engineer, and application delivery engineer. Its delivery engine follows five stages: field diagnosis, ontology modeling, application assembly, parallel operation with definition alignment, and handover/assetization.

## Role Collaboration

| Role | Business responsibility | Delivery-artifact responsibility |
| --- | --- | --- |
| Business translator | Aligns requirements, terminology, flow, and metrics | Scenario definition, acceptance criteria, SOP collaboration |
| Data / ontology engineer | Validates data availability and business semantics | Objects, links, actions, lineage, and quality rules |
| Application delivery engineer | Enables adoption in the operating workflow | Dashboards, agents, workflows, launch, and training |

These roles collaborate rather than hand work off in isolation. The model must be grounded in the field; applications must understand semantic definitions and access constraints.

## Five-Stage Analysis

### 1. Field diagnosis

Identify the process node creating loss or risk, the actor making a decision, the required data and rules, and the measurable success condition. Outputs include the scenario statement, process map, data/knowledge needs, and baseline metric.

### 2. Ontology modeling

Map diagnosis results to objects, links, actions, and governance metadata. Model exception paths, state transitions, authoritative sources, and access rules—not only the happy path.

### 3. Application assembly

Build the needed dashboard, agent, or workflow. Dashboards support observation; agents support retrieval, reasoning, and recommendations; workflows perform controlled steps and system write-backs. Every output should identify its semantic and source basis.

### 4. Shadow operation

The diagram explicitly requires parallel old/new operation and definition alignment. The new capability can produce results or recommendations while the existing process remains authoritative. Compare differences, error sources, exceptions, and human intervention cost before expanding permissions.

### 5. Handover and assetization

Handover includes SOPs, training, and accountable owners. **Recommendation:** also include the asset inventory, exception procedure, change workflow, monitoring checklist, and recovery path.

**Evidence status.** This stage is derived from the supplied architecture diagram and is this project's synthesis. No primary source read in [the FDE primary-source record](../research/forward-deployed-engineer-sources.md) states an exit or handoff criterion for the role, so nothing here should be cited as established industry practice.

## Recommended Acceptance Gates

| Gate | Acceptance question |
| --- | --- |
| Business value | Did the defined metric improve in a reproducible way? |
| Semantic correctness | Do users accept the object, relationship, state, and metric definitions? |
| Data quality | Do critical records have known source, freshness, and exception handling? |
| Operational safety | Do write or dispatch actions have appropriate permission, approval, and audit? |
| Maintainability | Can accountable owners manage change, incident handling, and rollback? |

## Questions to Resolve

1. Who forms the first FDE squad, and who is the business decision-maker?
2. How long should shadow operation run, and what constitutes a pass?
3. Which actions remain advisory, which require approval, and which may write back automatically?
