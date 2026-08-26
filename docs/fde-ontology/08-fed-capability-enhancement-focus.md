# 08 | FED Capability Enhancement Focus

Back to the [chapter index](README.md).

## Project Positioning

FED capability enhancement is the purpose of this project. The ontology-driven FDE architecture remains a reference model: it helps identify what FED can build and strengthen, but it is not assumed to be FED’s existing implementation or complete product definition.

The practical question is not “How do we recreate the diagram?” It is “Which capabilities would let FED deliver trusted, governed, and reusable outcomes in a real business scenario?”

## Capability Priorities

| Priority | Capability | Why it comes now |
| --- | --- | --- |
| P0 | Scenario registration | Establishes a measurable purpose and accountable owner before technology choices |
| P1 | Ontology asset lifecycle | Prevents each FED feature from defining business terms independently |
| P1 | Evidence-aware context resolution | Makes answers and metrics attributable to permitted sources |
| P2 | Decision support | Turns context into an operating dashboard or agent interaction |
| P3 | Controlled action execution | Adds operational effect only after read-only and advisory use is trusted |
| P4 | Cross-scenario reuse and governance | Converts delivery work into compounding FED capability |

P0 and P1 should form the first vertical slice. P2 and P3 should not be treated as independent products: they consume the same scenario, semantic assets, context, and access decisions.

## First Buildable Contract

The project now includes a JSON Schema for a FED scenario record at [schemas/fed-scenario.schema.json](../../schemas/fed-scenario.schema.json). The schema is technology-neutral and establishes the information FED must collect before building a scenario:

| Contract element | Capability it enables |
| --- | --- |
| Accountable owner | Definition approval, ongoing decisions, and acceptance |
| Process node and user role | A narrow and testable operating scope |
| Decision or action | A direct path from information to work |
| Baseline and target metric | Outcome measurement rather than demo evaluation |
| Ontology references | The minimum shared semantics to build or extend |
| Source references | Permission, freshness, and lineage decisions |
| Acceptance criteria | A verifiable release decision |

The included [illustrative record](../../examples/order-exception-triage.scenario.json) is intentionally generic. It demonstrates the contract shape only and must be replaced with FED’s first real scenario before implementation begins.

## Modules to Develop After the Contract Is Populated

The following modules are ordered by dependency. Their interfaces should remain small while their implementations absorb recurring complexity.

| Module | Interface purpose | Complexity kept inside the module |
| --- | --- | --- |
| Scenario Registry Module | Register and resolve an approved scenario | Validation, ownership checks, metric metadata, lifecycle state |
| Ontology Asset Module | Read released definitions and govern definition changes | Versioning, review, impact analysis, retirement |
| Context Resolution Module | Return permitted, sourced context for a scenario request | Source adapters, mappings, quality checks, access evaluation, lineage |
| Decision Support Module | Produce a metric, answer, or recommendation from context | Calculations, model use, formatting, uncertainty treatment |
| Action Execution Module | Prepare, approve, and execute named actions | Preconditions, idempotency, audit, retries, recovery |

## Next Acceptance Target

The immediate target is not autonomous action. It is one read-only inquiry for one approved scenario that returns:

```text
result + semantic definition version + source evidence + freshness status + access decision
```

This result is the first proof that FED can give a user an answer grounded in governed enterprise context. Once it is reliable, the exact same context can power a dashboard, a decision-support interaction, and eventually a controlled action.
