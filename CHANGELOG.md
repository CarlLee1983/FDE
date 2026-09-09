# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). While the major version is `0`, the capability boundary and the scenario schema may change in a minor release.

## [Unreleased]

### Changed

- Collaborative clarification now covers reconciling information that arrives after a conclusion exists — preserving the prior conclusion, bounding the new information's source, time, version, and scope, separating what must be recomputed from what still holds, and naming the work that can continue while a decision waits.
- Decision-changing unknowns now return with the decision they affect, a verification method, an accountable role, a closure condition, and the analysis to recompute, ordered by decision impact, dependency, then verification cost.
- `SKILL.md` triggers that reconciliation without adding an artefact or gate to an analysis that has no conflicting evidence.

## [0.2.2] - 2026-09-05

### Changed

- Consolidated the Codex and Claude Code portable-Skill operating instructions in English and Traditional Chinese, including installation, invocation, scenario validation, update, removal, and package maintenance.
- Updated the project site and contribution guide to describe self-contained Skill copies and synchronized reference snapshots.

## [0.2.1] - 2026-09-05

### Fixed

- Installed Codex and Claude Code Skills now include the required local FDE method references and use host-independent scenario-validator instructions.
- Skill verification now rejects missing packaged references and canonical/package drift; the synchronized snapshots are regenerated with `scripts/sync-skill-references.py`.

## [0.2.0] - 2026-08-30

### Added

- A frozen `make verify` chain covering root and example tests, tracked scenario records, schema metaschema, Pages content and links, and Skill structure.
- A safe `install-skill.sh` entry point for independent Codex and Claude Code repository copies, with installer integration tests.
- Five-minute Quick Starts in English and Traditional Chinese.

### Changed

- Pull requests now run full repository verification; Pages deployment remains limited to successful non-PR runs on `main`.
- English and Traditional Chinese entry points now link installation and verification while keeping enterprise architecture, schemas, models, assurance, and implementation conditional.
- GitHub Pages Actions were updated to `actions/checkout` v7, `actions/configure-pages` v6, and `actions/deploy-pages` v5.

## [0.1.0] - 2026-08-28

First tagged version. It marks the point where the project boundary, the skill's runtime behaviour, and the validation tooling were all stated and verifiable in one place.

### Added

- The FDE operating-analysis skill at `.agents/skills/fde-project-work/`, exposed to Claude Code at `.claude/skills/fde-project-work`, with its four task modes: operating analysis, scenario preparation, capability build, and assurance.
- [`CONTEXT.md`](CONTEXT.md) as the canonical project language, and [`AGENTS.md`](AGENTS.md) as the single agent entry naming the four rule sources.
- Four accepted decisions in [`docs/adr/`](docs/adr/), each closed with a `**Falsified if:**` condition naming the files it depends on.
- The scenario schema and its example in [`schemas/`](schemas/), with `validate-scenario.sh` for executable validation.
- Eight worked cases in [`examples/`](examples/), each with a `request.md` and a `scenario.json`.
- The bounded evaluation contract and recorded runs in [`docs/evaluations/`](docs/evaluations/), including forward and failure-seeking evaluations, a schema-valid scenario package, a tested read-only slice, and a persistent-write gate review.
- The FDE reference study in [`docs/fde-ontology/`](docs/fde-ontology/), the full-depth [Scenario-to-Action Method](FDE-Scenario-to-Action-Method.md), and Traditional Chinese mirrors under [`docs/zh-TW/`](docs/zh-TW/).
- A static project site under `site/`, built by `scripts/build-pages.sh`, link-checked by `scripts/validate-pages.py`, and deployed by the `pages.yml` workflow.
- MIT licensing, and the community documents under `.github/`: contributing guide, code of conduct, security policy, issue forms, pull request template, code owners, and a monthly Actions dependency update.

### Notes

This version establishes repository behaviour only. It does not establish target-enterprise facts, acceptance, access, authority, production readiness, or value.

[Unreleased]: https://github.com/CarlLee1983/FDE/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/CarlLee1983/FDE/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/CarlLee1983/FDE/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/CarlLee1983/FDE/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/CarlLee1983/FDE/releases/tag/v0.1.0
