# FDE Operating Analysis

Project website: [static landing page](index.html) · [case index](examples/README.zh-TW.md)

This project strengthens an FDE (Forward Deployed Engineer) as an **operating-analysis skill**. It turns a bounded operating problem into an evidence-bounded operating solution and next accountable action. It is not an enterprise application platform, delivery toolkit, or default implementation roadmap.

## Default Outcome

The default output is the smallest sufficient five-part operating solution:

1. Operating problem and outcome.
2. Current-work diagnosis.
3. Technology-neutral target workflow.
4. Intervention and AI-fit decision, with evidence limits.
5. Next accountable action.

The skill first redesigns work, responsibility, definitions, and evidence flow. Its core intervention principle is **穩定規則交給軟體，語言負擔才考慮 AI。** Stable rules, calculations, controls, and repeatable state transitions belong in deterministic software; AI is considered only for retained language-heavy work where it adds evidence-backed value. `No AI` is a valid outcome.

## Capability Set

The project's closed capability set is:

1. Operating problem framing.
2. Workflow diagnosis and redesign.
3. Intervention selection and AI-fit.
4. Operating solution formation.
5. Optional delivery and assurance assistance, only when explicitly requested.

## Source Hierarchy

[CONTEXT.md](CONTEXT.md) defines canonical project language, accepted [ADRs](docs/adr/) govern hard-to-reverse decisions, and the [FDE operating-analysis skill](.agents/skills/fde-project-work/SKILL.md) governs runtime analysis behavior. The README is the entry point; supporting material cannot independently expand this boundary.

The [FDE Scenario-to-Action Method](FDE-Scenario-to-Action-Method.md) provides the full-depth reference method when a case needs deeper modelling, assurance, or delivery support. The [FDE Capability Enhancement Plan](FDE-Capability-Enhancement-Plan.md) explains how analysis quality is validated across cases.

The [FDE reference study](docs/fde-ontology/README.md) and its capability materials are supporting reference. Scenario registration, semantic definition, context resolution, decision support, and controlled action are **solution patterns** that may be selected for a case; they are not project modules or a mandatory roadmap.

Generic cases may use clearly labelled reference hypotheses. They demonstrate reasoning, not target-enterprise facts, acceptance, authority, value, or implementation progress. Models, schemas, artefacts, gates, research, and executable validation are optional and proportional to uncertainty, risk, authority, persistence, or an explicit request.

## Validation Evidence

The [evaluation contract and recorded runs](docs/evaluations/README.md) provide bounded evidence for the skill's four task modes: operating analysis, scenario preparation, capability build, and assurance. The records include varied and failure-seeking forward evaluations, a proposed schema-valid scenario package, a tested local read-only slice, and a persistent-write gate review.

This evidence establishes repository behaviour only. It does not establish target-enterprise facts, acceptance, access, authority, production readiness, or value.

Continue project evaluation when a new independent operating case, observed response failure, explicit structured/build/assurance request, or cross-case promotion candidate creates a decision to test. Otherwise use the skill on the next real operating problem or stop; additional synthetic files are not progress by themselves.

## GitHub Pages

The repository includes a static project site and a Pages deployment workflow. Build and validate the exact artifact locally with:

```bash
output_dir="$(mktemp -d)"
scripts/build-pages.sh "$output_dir"
python3 scripts/validate-pages.py "$output_dir"
```

The workflow publishes only after the repository owner enables GitHub Pages with **GitHub Actions** as its source. A successful repository build proves the static artifact and its local links; it does not establish target-enterprise acceptance, access, authority, production readiness, or value.
