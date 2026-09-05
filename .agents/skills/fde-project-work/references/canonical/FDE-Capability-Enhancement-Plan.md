# FDE Capability Enhancement Plan

This plan improves an FDE (Forward Deployed Engineer) as an **operating-analysis skill**. The objective is not to build an ontology platform or a fixed delivery sequence. It is to reliably form evidence-bounded operating solutions that let an accountable person decide what to do next.

## Capability Target

The project has a closed set of five capabilities:

| Capability | Observable case outcome |
| --- | --- |
| Operating problem framing | A vague request becomes a bounded problem with a user, workflow location, outcome, and decision. |
| Workflow diagnosis and redesign | The analysis explains normal, exception, escalation, and rework paths, then proposes a simpler target workflow before selecting technology. |
| Intervention selection and AI-fit | The analysis compares process, responsibility, information, deterministic software, human judgment, AI assistance, and governed action, then selects the simplest sufficient intervention. |
| Operating solution formation | A user receives a usable five-part operating solution with explicit evidence limits and a next accountable action. |
| Optional delivery and assurance assistance | When explicitly requested, the skill helps plan, review, validate, or hand off an implementation without treating that work as the default outcome. |

## Default Case Output

Every ordinary case should reach the minimum sufficient operating solution:

1. Problem and outcome.
2. Current-work diagnosis.
3. Target workflow.
4. Intervention and AI-fit decision, including evidence limits.
5. Next accountable action.

Depth is proportional. Detailed models, research, gate reviews, schemas, replays, or executable validation are added only when material uncertainty, risk, authority, persistent action, value claims, or an explicit request requires them. Generic cases may use labelled reference hypotheses; they do not establish enterprise facts, approval, access, or value.

## Case-Based Validation

Progress is measured through varied operating cases, not by document count, schema count, code volume, or runnable examples. A case is strong when it:

1. Frames the right operating problem and outcome.
2. Accounts for the whole current workflow, including exceptions and rework.
3. Redesigns the work before proposing technology.
4. Selects a proportionate intervention and treats AI as optional.
5. Preserves evidence, authority, and value boundaries.
6. Leaves an accountable person with a concrete next action.

Examples and validation artefacts can test this reasoning, but remain evidence aids rather than capability milestones or implementation progress.

## Supporting Solution Patterns

The ontology-driven FDE reference model remains useful as a vocabulary and source of solution patterns. A case may need scenario registration, semantic definition, context resolution, decision support, controlled action, or governance. These patterns are selected for their fit to the target workflow; they are not a project roadmap or modules that must be built.

When a case explicitly requests delivery, a narrow read-only inquiry or other governed slice can be a valid first implementation. Persistent actions, release claims, access increases, and value claims require the relevant evidence and approval. In their absence, the output remains a proposed advisory, shadow, or read-only design.

For detailed pattern and module reference, see [Capability Map and Implementation Strategy](docs/fde-ontology/07-capability-map-and-implementation-strategy.md). For the full-depth method used only when a case needs it, see [FDE Scenario-to-Action Method](FDE-Scenario-to-Action-Method.md).
