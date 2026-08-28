# Task modes

Choose the mode that matches the user's request. **Operating analysis** is the default. The other modes require an explicit proposal, structured-record, implementation, or assurance outcome; they do not activate merely because an analysis mentions a possible system.

Across modes, distinguish target-enterprise facts from reference hypotheses and classify material claims as `evidenced`, `proposed`, `missing`, or `unverifiable`.

## Operating analysis — default

Use for a case, operating problem, workflow question, solution exploration, or AI-fit question.

Follow the core analysis flow in `SKILL.md`. Return the minimum operating solution:

1. operating problem and outcome;
2. current-work diagnosis;
3. target workflow;
4. intervention and AI-fit decision with evidence limits;
5. next accountable action.

Use narrative, a small table, or a diagram only when it makes the decision clearer. Do not create repository artefacts unless requested. A generic case may remain useful with explicit reference hypotheses and a validation path.

**Completion:** the user can make the next decision without an unstated material assumption. This does not imply enterprise acceptance, implementation readiness, or gate passage.

## Solution proposal — explicit document outcome

Use when the user asks to propose, prepare a proposal, or turn the completed analysis into a proposal.

Read [operating solution](solution-proposal.md). Persist an editable Markdown source and a standalone, responsive, print-ready HTML communication document in the requested repository location, or beside the case material when no location is specified. Keep their claims and status aligned. Include the five-part minimum contract, evidence states and restrictions, the validation design, the decision requested from the accountable owner, and an acceptance record that can be completed without rewriting the proposal. Use visual hierarchy and workflow presentation to make the HTML suitable for stakeholder review; keep evidence limits prominent. A chat response may summarize and link the files, but does not replace them.

Keep unsupported enterprise claims `proposed`, `missing`, or `unverifiable`. Owner acceptance changes proposal status only; measured operating results and control evidence require their own validation.

**Completion:** both proposal files exist, communicate the same material claims, contain no unstated material assumption, identify the decision and accountable owner, and the HTML works at desktop and mobile widths and in print. This does not imply acceptance or demonstrated value.

## Scenario preparation — explicit structured outcome

Use when the user asks to create, complete, or review a scenario record or preparation package.

Read the current scenario schema and the relevant framing sections of the method. Produce only the record and unresolved evidence or decisions needed for its stated purpose. Schema validity proves structure only. Keep the record `proposed` when real ownership, baseline, target, source, semantic, or acceptance evidence is absent.

**Completion:** the requested preparation artefact is structurally valid where applicable, evidence states are visible, and the next owner decision is explicit.

## Capability build — explicit implementation request

Use only when the user asks to build or change a working capability. Require an accepted solution boundary and direct evidence for any source, identity, permission, integration, or authority claim the slice uses.

Read [the delivery loop](agent-delivery-loop.md) and only the implementation references needed by the slice. Deliver the smallest coherent end-to-end change with proportionate tests, documentation, evidence limits, and rollback or operating notes. For a read-only result, preserve:

```text
result + semantic-definition version + source evidence + freshness + access decision
```

**Completion:** the explicit acceptance criteria pass and unsupported integrations, permissions, or effects remain outside the implementation.

## Assurance — explicit or authority-bearing conclusion

Use when the user requests a gate/control review, or when a recommendation depends on real access, release, increased authority, persistent action, or demonstrated value.

Read only the applicable method gate and control sources. Return `passed`, `missing`, and `unverifiable` evidence with the restriction caused by each gap. Verify source, freshness, access, and semantic version for read-only results; require authorization, audit, idempotency, and recovery evidence for persistent effects.

**Completion:** the allowed claim or next action is clear. Assurance gaps do not invalidate a separate generic operating analysis.
