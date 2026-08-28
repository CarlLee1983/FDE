## What changed and why

<!-- One paragraph. Name the operating problem, decision, or defect this addresses. -->

## Boundary check

- [ ] This change stays inside the capability set in [`README.md`](../README.md) and the accepted decisions in [`docs/adr/`](../docs/adr/).
- [ ] No accepted ADR's `**Falsified if:**` condition is triggered, or an ADR is added/updated in this pull request.
- [ ] Traditional Chinese mirrors are updated, or the deferral is stated below.

## Verification

<!-- Paste real output. "Should pass" is not verification. Delete a command only if it does not apply. -->

```
uvx --with pytest pytest -q tests
```

```
scripts/build-pages.sh "$output_dir" && python3 scripts/validate-pages.py "$output_dir"
```

```
.agents/skills/fde-project-work/scripts/validate-scenario.sh <scenario.json>
```

## What this does not establish

<!-- For evaluation or example changes: state the limits. Repository behaviour is not target-enterprise acceptance, access, authority, production readiness, or value. Write "n/a" for tooling-only changes. -->
