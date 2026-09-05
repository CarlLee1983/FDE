# FDE Project Work Skill operating guide

`fde-project-work` is a portable operating-analysis Skill for Codex and Claude Code. It turns a bounded operating problem into an evidence-bounded operating solution and next accountable action. It is not an enterprise platform, a default build request, or evidence of enterprise acceptance, authority, production readiness, or value.

The installed copy is self-contained: it carries the required method snapshots, scenario schema, and validator. It never treats a target repository's `README.md`, `CONTEXT.md`, or `docs/` as FDE guidance.

## Install and invoke

From an FDE checkout, install into the root of another Git repository:

```bash
scripts/install-skill.sh --target /path/to/project --agent codex
scripts/install-skill.sh --target /path/to/project --agent claude
scripts/install-skill.sh --target /path/to/project --agent both
```

Start the chosen host in `/path/to/project`. In Codex, use `$fde-project-work`; in Claude Code, use `/fde-project-work`. State the operating problem, desired outcome, and any explicit request for a proposal, scenario record, build, or assurance review.

The installer writes only one or both of these directories and refuses to overwrite an existing Skill:

```text
.agents/skills/fde-project-work/  # Codex
.claude/skills/fde-project-work/  # Claude Code
```

See the [Quick Start](quickstart.md) for a disposable-repository walkthrough, update, and removal steps.

## Choose the mode

Operating analysis is the default. Its complete result has five parts:

1. Operating problem and outcome.
2. Current-work diagnosis.
3. Technology-neutral target workflow.
4. Intervention and AI-fit decision with evidence limits.
5. Next accountable action.

Only an explicit request activates another mode:

| Request | Mode | Read next |
| --- | --- | --- |
| Proposal or stakeholder document | Solution proposal | `references/solution-proposal.md` |
| Scenario record or preparation package | Scenario preparation | `references/task-modes.md` and the packaged schema |
| Build or change a working capability | Capability build | `references/agent-delivery-loop.md` and only the needed method references |
| Gate, control, authority, release, or persistent-action review | Assurance | the applicable method gate and control references |

Stable rules, calculations, controls, and repeatable transitions belong in deterministic software. Consider AI only for retained language-heavy work when evidence shows value over the non-AI workflow. Missing enterprise evidence remains `missing`, `proposed`, or `unverifiable`; it is never invented.

## Validate a scenario

`uv` is required. Change to the installed Skill directory, then run the same command for either host:

```bash
./scripts/validate-scenario.sh /path/to/scenario.json
```

A successful command proves the schema and record structure only. It does not prove enterprise approval, source access, authority, or value.

## Package layout and maintenance

```text
fde-project-work/
├── SKILL.md
├── references/
│   ├── source-map.md
│   ├── packaged-sources.json
│   └── canonical/             # synchronized required method snapshots
├── schemas/fde-scenario.schema.json
└── scripts/validate-scenario.sh
```

Read `references/source-map.md` only as needed for the active branch. It identifies local packaged references; large examples, translations, and rationale are fixed-version optional reading.

FDE maintainers must synchronize a changed canonical source listed in `packaged-sources.json` before release:

```bash
python3 scripts/sync-skill-references.py
python3 scripts/sync-skill-references.py --check
make verify
```

`make verify` rejects missing package files, links that escape the Skill, canonical/package drift, and an incomplete snapshot manifest.
