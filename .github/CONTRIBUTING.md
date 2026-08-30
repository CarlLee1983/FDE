# Contributing

This repository is an FDE operating-analysis skill: documents, a skill definition, schemas, worked cases, and a small amount of Python tooling. Contributions are welcome within that boundary.

## Read first

Read [../AGENTS.md](../AGENTS.md) before proposing a change. It names the four rule sources — [`CONTEXT.md`](../CONTEXT.md) for canonical language, [`docs/adr/`](../docs/adr/) for accepted decisions, the skill definition for runtime behaviour, and [`README.md`](../README.md) for the source hierarchy. Supporting documents, examples, and translations cannot expand the capability boundary; a change that needs a wider boundary needs an ADR first, not a larger pull request.

## Verify before claiming

Install Git, Make, and [uv](https://docs.astral.sh/uv/). Dependencies are pinned in `pyproject.toml` and `uv.lock`; run the same frozen verification chain used by CI and paste its summary in the pull request:

```bash
make verify
```

The component targets are `make test`, `make validate-scenarios`, and `make validate-pages`; they are useful while iterating but do not replace the final `make verify`. Scenario release validation discovers only Git-tracked `examples/**/scenario.json`. The Pages build likewise publishes only tracked files, so a new scenario or published file must be `git add`ed before it is included. Untracked scenarios are deliberately excluded rather than treated as release evidence.

## Repository settings

The repository owner must separately protect `main`, require pull requests, require the `verify` status check, and block merges while required checks are failing. Workflow code cannot assert that these GitHub settings are enabled.

## Conventions

Commits follow conventional commits: `<type>: [ <scope> ] <subject>`, with types `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`.

A decision that is hard to reverse, surprising without context, or the result of a real trade-off gets an ADR in [`docs/adr/`](../docs/adr/), closed with a `**Falsified if:**` condition naming the files it depends on in backticks. That condition is the boundary list, so the backticks are load-bearing.

English is the primary language for root documents; `docs/zh-TW/` and `*.zh-TW.md` hold Traditional Chinese mirrors. Update a translation in the same pull request as the document it mirrors, or say explicitly that it is deferred. Files under `.github/` are English only.

## Scope of a good pull request

Prefer one concern per pull request. New evaluation evidence belongs in [`docs/evaluations/`](../docs/evaluations/) and must state what it does and does not establish — repository behaviour is not target-enterprise acceptance, authority, production readiness, or value. Additional synthetic example files are not progress by themselves; a new case should come from a real operating problem or a specific failure you observed.
