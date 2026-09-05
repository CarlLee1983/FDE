# Agent delivery loop

Use this loop when the user asks the agent to prepare, build, improve, or carry an FDE scenario through its next safe delivery stage. The loop turns the method pack into working artefacts; it does not grant enterprise authority.

## 1. Establish the delivery contract

Name the operating outcome, current boundary, selected task mode, relevant constraints, expected artefacts, and observable acceptance checks. Infer repository conventions and facts from inspected evidence. Ask only when a missing choice would materially change the solution or authorize a consequential action.

Completion criterion: the next safe outcome and the evidence that will prove it are explicit.

## 2. Build the evidence ledger

Classify every material enterprise claim as `evidenced`, `proposed`, `missing`, or `unverifiable`. Record the source and freshness of evidenced claims and the delivery restriction caused by each gap. Examples and project guardrails establish shape or proposed scope, not enterprise acceptance.

Completion criterion: every owner, authority, baseline, target, source, definition, permission, integration, and acceptance claim used by the slice has a status.

## 3. Advance the smallest coherent artefact set

Follow the selected mode in [task-modes](task-modes.md). Reuse an existing scenario workspace when one exists; otherwise place new artefacts together using the repository's current example shape. Keep only artefacts needed for the next gate:

- Scenario preparation: scenario record plus unresolved evidence and owner decisions.
- Operating solution shaping: current/target flow, operating solution proposal, first vertical slice, validation and rollout boundary.
- Capability build: working slice, tests, evidence boundary, operating instructions, and rollback path.
- Assurance: gate result with `passed`, `missing`, and `unverifiable` evidence.

Keep code, definitions, tests, evidence, and operating documentation coherent within the slice. Do not manufacture placeholder enterprise facts merely to make a schema pass; keep an incomplete preparation package or mark the field's evidence status outside the scenario record until an owner supplies it.

Completion criterion: the artefact set answers the selected mode's output contract and remains useful at the evidenced authority level.

## 4. Validate deterministically

For every scenario record, change to the installed Skill directory (the directory that contains this file's `SKILL.md`) and run:

```bash
./scripts/validate-scenario.sh <scenario.json>
```

This works for both `.agents/skills/fde-project-work/` (Codex) and `.claude/skills/fde-project-work/` (Claude Code); it does not require the other host's installation.

Run any narrower example or slice-specific checks, then the repository's proportionate required checks. Inspect generated output and the final diff; a schema pass proves structure only. For read-only results, also verify result, semantic-definition version, source evidence, freshness, and access decision. For controlled action, require direct authorization, audit, idempotency, and recovery evidence.

Completion criterion: relevant checks have actual results and semantic or authority gaps remain visible.

## 5. Decide the gate and continue safely

Compare the evidence with the current gate in the canonical method. A failed or incomplete gate bounds the next action; it does not erase useful work. Continue with proposed design, read-only implementation, fixture validation, or another lower-authority outcome when that outcome remains within scope and is independently useful. Stop before an unsupported integration, release, permission increase, or persistent write-back.

Completion criterion: the highest safe completed outcome, gate result, deferred work, and exact next accountable owner action are explicit.

## Handoff

Report artefacts changed, checks passed or failed, evidence restrictions, rollback or operational implications when applicable, and the next owner decision. Describe synthetic evidence as synthetic and proposed behaviour as proposed. When the slice produced a reuse or core-change claim, complete the [capability-return review](capability-return-review.md) before presenting it as a project capability.
