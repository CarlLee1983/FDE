# FDE Capability Enhancement Plan

This plan makes the capability enhancement of an FDE (Forward Deployed Engineer) the project objective. The ontology-driven FDE delivery architecture is a reference model that supplies design constraints and a vocabulary for the work.

## Capability Target

FDE delivery should progress from isolated answers or demonstrations to governed, reusable operating capabilities:

```text
Defined scenario → shared semantics → sourced context → decision support
→ controlled action → reusable enterprise capability
```

## Mapping the Reference Model to FDE Targets

| Reference-model concern | FDE capability to build or strengthen | First observable outcome |
| --- | --- | --- |
| Business topic and metrics | Scenario definition | A scenario has an owner, process node, baseline, target, and acceptance rule |
| Enterprise ontology | Semantic asset lifecycle | A released object/link/action definition has source, owner, version, and review cycle |
| System connectivity | Source ingestion and alignment | A permitted source is mapped to a semantic asset with freshness and lineage |
| Dashboards, agents, workflows | Evidence-aware decision support | A user can obtain a consistent answer or metric with cited evidence |
| Approval, dispatch, write-back | Controlled action execution | An approved, named action is validated, audited, and executed once |
| Feedback and evolution | Operating governance | Production feedback leads to an accountable asset or application revision |

## Maturity Model

| Level | FDE capability | Definition of done |
| --- | --- | --- |
| 1. Defined | Scenario registry | A scenario record has a clear owner, decision, source set, and measurable outcome |
| 2. Grounded | Semantic context | A permitted request resolves to versioned objects, links, data, and provenance |
| 3. Useful | Decision support | A dashboard or agent uses that context and agrees with the business definition |
| 4. Controlled | Action execution | An approved action meets preconditions, records an audit trail, and has failure handling |
| 5. Compounding | Reuse and governance | A second scenario reuses assets without creating a competing definition |

## First Concrete Capability: Scenario Registration

The first FDE artifact is a technology-neutral contract for a scenario registry:

- [Scenario record JSON Schema](schemas/fde-scenario.schema.json)
- [Illustrative scenario record](examples/order-exception-triage.scenario.json)

The registry is intentionally first because it connects product intent, operational ownership, ontology scope, data sources, and acceptance evidence before implementation complexity is introduced.

## Recommended Near-Term Work

1. Replace the illustrative scenario with the project's first real FDE business scenario.
2. Confirm its accountable business owner, source owner, and decision or action owner.
3. Define the minimum object, link, and action set required by the scenario.
4. Implement a read-only context-resolution path that returns evidence and access decisions.
5. Verify the result with a dashboard or agent before considering write-back.

## Guardrails

- An FDE is not required to ingest every enterprise source before delivering a useful capability.
- A system must prove semantic consistency, provenance, and access control before it gains write authority.
- Business definitions are owned and versioned assets; prompts or individual applications do not own them.
- An action must be explicit, approved at the correct level, and auditable; an agent must not improvise a persistent action.

For the detailed module design and vertical-slice plan, see [Capability Map and Implementation Strategy](docs/fde-ontology/07-capability-map-and-implementation-strategy.md).

For the methodology used to analyse and prepare each scenario, see [FDE Scenario-to-Action Method](FDE-Scenario-to-Action-Method.md).
