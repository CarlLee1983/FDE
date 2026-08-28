# Contributing

This repository is an FDE operating-analysis skill: documents, a skill definition, schemas, worked cases, and a small amount of Python tooling. Contributions are welcome within that boundary.

## Read first

Read [../AGENTS.md](../AGENTS.md) before proposing a change. It names the four rule sources — [`CONTEXT.md`](../CONTEXT.md) for canonical language, [`docs/adr/`](../docs/adr/) for accepted decisions, the skill definition for runtime behaviour, and [`README.md`](../README.md) for the source hierarchy. Supporting documents, examples, and translations cannot expand the capability boundary; a change that needs a wider boundary needs an ADR first, not a larger pull request.

## Verify before claiming

Run all three locally and paste the output in the pull request:

```bash
uvx --with pytest pytest -q tests
.agents/skills/fde-project-work/scripts/validate-scenario.sh <scenario.json>
output_dir="$(mktemp -d)/site"
scripts/build-pages.sh "$output_dir"
python3 scripts/validate-pages.py "$output_dir"
```

The scenario validator applies only when you touch a `scenario.json` or [`schemas/`](../schemas/). The Pages build applies to any change under a published path — every tracked `*.md`, plus `examples/`, `schemas/`, `docs/`, `site/zh-TW/`, and the skill directory. `scripts/build-pages.sh` publishes only tracked files, so a new file must be `git add`ed before it will validate.

## Conventions

Commits follow conventional commits: `<type>: [ <scope> ] <subject>`, with types `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`.

A decision that is hard to reverse, surprising without context, or the result of a real trade-off gets an ADR in [`docs/adr/`](../docs/adr/), closed with a `**Falsified if:**` condition naming the files it depends on in backticks. That condition is the boundary list, so the backticks are load-bearing.

English is the primary language for root documents; `docs/zh-TW/` and `*.zh-TW.md` hold Traditional Chinese mirrors. Update a translation in the same pull request as the document it mirrors, or say explicitly that it is deferred. Files under `.github/` are English only.

## Scope of a good pull request

Prefer one concern per pull request. New evaluation evidence belongs in [`docs/evaluations/`](../docs/evaluations/) and must state what it does and does not establish — repository behaviour is not target-enterprise acceptance, authority, production readiness, or value. Additional synthetic example files are not progress by themselves; a new case should come from a real operating problem or a specific failure you observed.
