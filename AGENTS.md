# Agent entry

Read in this order and treat nothing else as a rule source:

1. `CONTEXT.md` — canonical project language.
2. `docs/adr/` — accepted decisions; each ends with a `**Falsified if:**` condition that names the files it depends on.
3. `.agents/skills/fde-project-work/SKILL.md` — runtime analysis behaviour (also exposed at `.claude/skills/fde-project-work`).
4. `README.md` — project entry point and source hierarchy.

`.agents/skills/fde-project-work/references/source-map.md` locates every supporting document; open supporting material only for the branch you are on. Supporting documents, examples, and translations cannot expand the capability boundary.

Verify before claiming: `make verify`.
