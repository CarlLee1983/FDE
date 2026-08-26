---
name: fed-project-work
description: Route FED scenario preparation, governed capability design or build, and gate-based assurance in this repository. Use for work that needs the current FED method, canonical scenario schema, or evidence-based gate decisions; not for translation, static HTML/CSS, or routine Git and repository maintenance.
---

# FED project work

Use this as a thin router for FED work whose answer or implementation depends on the project's scenario-to-action method, capability design, or assurance gates.

## Grounding

1. Locate the repository root and use the [source map](references/source-map.md) only as an index. Treat Traditional Chinese files as reading aids only.
2. Select the applicable mode from [task modes](references/task-modes.md), then load only its current English canonical sources. When a request genuinely spans modes, process them in dependency order and stop at the first unmet gate. Read the schema directly whenever its active contract applies.
3. Keep repository proposals separate from facts about a target enterprise. Establish owners, authorities, baselines, targets, policies, permissions, integrations, and current acceptance only from supplied or inspected evidence. Label absent evidence `missing` and evidence that cannot be checked `unverifiable`.
4. Use examples only to show a record's shape. Do not promote their people, systems, values, or acceptance claims into real-world facts.

## Control boundary

For a read-only inquiry, the output contract is:

`result + semantic-definition version + source evidence + freshness + access decision`

Report a component as `missing` or `unverifiable` when evidence does not establish it. A project guardrail or proposed safe scope is not a target-enterprise access decision; label it as a proposal rather than `allowed` or `authorized`. Before a persistent write-back or a recommendation that would authorize one, read the current gate, authority-tier, and control sources and require the applicable evidence. When it is absent, stop at an advisory or design outcome and expose the gap; never infer the needed authority or control.

Use the [source map](references/source-map.md) for canonical paths and headings. Use [task modes](references/task-modes.md) for the mode-specific input, output, and stopping contracts.
