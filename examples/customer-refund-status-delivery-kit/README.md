# Customer refund-status proposal delivery kit

This synthetic example tests one FDE analysis-to-proposal delivery flow. It does not implement a customer-service or payment product and does not establish target-enterprise facts, permissions, integrations, acceptance, or value.

## Source of truth

[`artifacts/analysis-package.json`](artifacts/analysis-package.json) is the canonical, case-owned analysis package. The formal proposal, standalone HTML report, and browser-native decision presentation are views of that package; none of them may upgrade an evidence state.

Material values that must stay consistent across all views are recorded in `consistencyClaims` and checked by [`scripts/validate_delivery_kit.py`](scripts/validate_delivery_kit.py).

## Outputs

- [`artifacts/operating-solution-proposal.md`](artifacts/operating-solution-proposal.md) — reviewable proposal source.
- [`artifacts/customer-refund-status-proposal.docx`](artifacts/customer-refund-status-proposal.docx) — formal proposal document.
- [`index.html`](index.html) — standalone stakeholder report.
- [`presentation.html`](presentation.html) — required 10-slide, browser-native decision presentation with keyboard, fullscreen, and print controls.
- `artifacts/customer-refund-status-decision.pptx` — optional derivative. Its case-owned builder remains available, but PPTX is not a completion requirement.
- [`evidence/validation-report.json`](evidence/validation-report.json) — deterministic consistency and artifact status.

## Generate and validate

Generate the Markdown, report HTML, presentation HTML, and DOCX views:

```bash
python3 examples/customer-refund-status-delivery-kit/scripts/generate_views.py
```

Open `presentation.html` directly in a modern browser. Use Left/Right, Page Up/Page Down, Space, Home, and End to navigate; `F` toggles fullscreen and `P` opens printing. The PowerPoint builder is retained as an optional derivative and must still use the managed Presentations workspace runtime if invoked.

Run the complete example validation:

```bash
examples/customer-refund-status-delivery-kit/scripts/validate-example.sh
```

The complete validator requires the document, stakeholder report, and browser-native presentation to be current, consistent, and visually inspected. It does not require a PPTX.

## Evidence boundary

Every business fact and number is proposed synthetic. The scenario remains `proposed`; enterprise owner acceptance, source and access evidence, accepted baselines, and real shadow results are missing or unverifiable. The first slice is read-only, requires human confirmation, and performs no write-back.
