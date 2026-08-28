# P2 synthetic read-only refund-status slice

This isolated Python standard-library CLI demonstrates a **proposed** read-only
refund-status result contract. It accepts a de-identified `refundCaseId`, a
local JSON fixture path, and an optional evaluation time. It supports only
`refund-status/v1`.

## Run

From this directory:

```bash
python3 refund_status_cli.py case_synth_001 fixtures/valid.json
python3 refund_status_cli.py case_synth_001 fixtures/valid.json --as-of 2026-08-28T12:00:00Z
```

On success, stdout is JSON with exactly these contract elements:

```text
result + semanticDefinitionVersion + sourceEvidence + freshness + accessDecision
```

Freshness is valid only within the inclusive bracket
`observedAt <= asOf <= expiresAt`; the success `freshness` object displays all
three timestamps and a `fresh` status. For a missing ID, an as-of outside that
bracket, denied record, or unsupported semantic version, the CLI exits nonzero
and writes a structured `error` object without `result`.

## Test

```bash
python3 -m unittest -v test_refund_status_cli.py
```

## Synthetic evidence boundary

All fixtures are local, synthetic, and de-identified. They demonstrate data
shape and fail-closed behaviour only; they are not production data, a live
integration, authorization evidence, or evidence of enterprise acceptance.
Successful output also requires synthetic source identity: `sourceEvidence.kind`
and `sourceEvidence.sourceId` must both be non-empty strings. Missing, empty, or
malformed source identity fails closed without a result.
The CLI performs no production access, writes, refunds, updates, or
notifications.

## Rollback

Disable use of this slice, or delete this isolated directory. It has no runtime
dependency, persistent state, production integration, write path, or
notification path to unwind.
