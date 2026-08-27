---
name: fde-project-work
description: Turn an operating problem into an evidence-grounded, implementable FDE operating solution, build its smallest governed slice, or assure its release gates. Use for process analysis and redesign, scenario shaping, intervention selection including AI-fit decisions, capability delivery, or evidence-based gate decisions; not for translation, static HTML/CSS, or routine Git and repository maintenance.
---

# FDE project work

Use this as the agent driver for FDE work whose answer or implementation depends on the project's scenario-to-action method, operating-process redesign, capability delivery, or assurance gates.

The default outcome for an open-ended FDE request is an implementable operating solution, not an inventory of documents or gates and not an AI feature by default. Scenario records, models, definitions, controls, and evidence are inputs that make the solution credible. The proposal must diagnose the current process, redesign the workflow before selecting technology, and show what the delivery team can build and verify first. Assess AI only after the target process is coherent; `no AI in the first slice` is a valid and often preferable result.

## Grounding

1. Locate the repository root and use the [source map](references/source-map.md) only as an index. Treat Traditional Chinese files as reading aids only.
2. Select the applicable mode from [task modes](references/task-modes.md), then load only its current English canonical sources. For an open-ended request such as “what should we do?” or “where could AI help?”, select **Operating solution shaping**. When a request spans modes, process them in dependency order. Read the schema directly whenever its active contract applies.
3. Keep repository proposals separate from facts about a target enterprise. Establish owners, authorities, baselines, targets, policies, permissions, integrations, and current acceptance only from supplied or inspected evidence. Label absent evidence `missing` and evidence that cannot be checked `unverifiable`.
4. Use examples only to show a record's shape. Do not promote their people, systems, values, or acceptance claims into real-world facts.
5. Analyse the whole current workflow before choosing an intervention. First remove unnecessary work; simplify handoffs; standardize definitions, ownership, and exception paths; repair evidence or data gaps; and use deterministic software for stable rules. Only then assess whether a remaining step benefits from AI because interpretation, language, synthesis, or bounded reasoning creates a defensible advantage. Assign every retained responsibility to deterministic software, an AI model, a human, or a governed system action.

When missing decisions materially change the operating diagnosis or solution, read [collaborative clarification](references/collaborative-clarification.md). Investigate available facts, then work through the decision frontier with accountable participants before relying on downstream assumptions.

## Agent delivery loop

For change, build, or end-to-end delivery requests, read [agent-delivery-loop](references/agent-delivery-loop.md) and drive the work until its completion or evidence boundary. Do not stop after describing the method when the requested artefacts can be safely produced or validated. For read, explanation, or review requests, use the selected mode's output contract without creating artefacts unless the user asks for them.

When a case slice produces learning that might change FDE core or be reused across scenarios, read [capability-return review](references/capability-return-review.md). Keep domain behaviour with the case and return only evidence-backed change candidates for accountable promotion.

When AI is justified for work whose method is not yet stable enough to specify, design a **governed capability-evolution loop** rather than a permanent prompt-bound task. Capture recommendations, human corrections, exceptions, and outcomes as evidence; use them to propose named process, semantic, decision, tool, model, or control changes. Promote repeated and accepted work into versioned, tested software only through an accountable owner and a replay or shadow comparison. The AI may then use the released capability and look for the next gap; it does not approve its own proposal, silently change policy, or publish production behavior.

## Control boundary

For an operating solution proposal, use the [solution proposal contract](references/solution-proposal.md). A gate gap limits the authority and claims of the proposal; it does not justify stopping at a gap list. Always return the highest safe proposed solution, its first buildable slice, and the concrete owner action or evidence needed next. Do not make model evaluation, model infrastructure, or AI interaction part of that slice unless the process analysis shows that the slice cannot deliver its intended outcome without them.

For a delivered read-only inquiry, the runtime output contract is:

`result + semantic-definition version + source evidence + freshness + access decision`

Report a component as `missing` or `unverifiable` when evidence does not establish it. A project guardrail or proposed safe scope is not a target-enterprise access decision; label it `proposed`, not `allowed` or `authorized`. Before a persistent write-back or a recommendation that would authorize one, read the current gate, authority-tier, and control sources and require the applicable evidence. When it is absent, bound the proposal to a `proposed` advisory, shadow, or read-only design and expose the gap; never infer permission to operate or the needed authority or control.

Use the [source map](references/source-map.md) for canonical paths and headings. Use [task modes](references/task-modes.md) for the mode-specific input, output, and stopping contracts.
