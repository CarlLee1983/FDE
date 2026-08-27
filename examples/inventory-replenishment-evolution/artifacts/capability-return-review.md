# Inventory replenishment capability-return review

## Source case and evidence boundary

- Case: `inventory-replenishment-evolution-demo`, status `proposed`.
- Capability: deterministic local replenishment baseline using `inventory-replenishment-semantics@0.1.0` and `synthetic-replenishment-policy@0.1.0`.
- Direct evidence: `scripts/recommend_replenishment.py`, 16 unit tests, fixed fixtures, golden replay, scenario validation, and `scripts/validate-example.sh`.
- Validation result: `scripts/validate-example.sh` passed on 2026-08-27, including all 16 unit tests, scenario validation, and golden replay.
- Evidence boundary: synthetic/local-only. There is no enterprise owner acceptance, source authorization, shadow result, production result, or write-back authority.

## Observations and ownership

| Observed behaviour | Direct case evidence | Classification | Decision |
| --- | --- | --- | --- |
| Project stock at arrival and round a replenishment quantity by safety stock, minimum order quantity, and pack size | `artifacts/replenishment-decision-contract.md`; candidate, boundary, inbound, and rounding tests | `case-specific` | `retain-in-case` |
| Use only inbound quantity established to arrive before the assessed arrival date | Decision contract and confirmed-inbound test | `case-specific` | `retain-in-case` |
| Return semantic version, source evidence, freshness, access decision, and a fail-closed no-write result | Golden result and read-only replay test; canonical read-only output contract | `existing-core-invariant` | `retain-in-case` as an implementation of the invariant |
| Require the inventory, demand, and supplier-policy sources and compute freshness by bracketing the snapshot time between each source's observation and expiry | `assess_freshness`; stale, malformed-time, and missing-source paths | `case-specific` | `retain-in-case`; the core requires freshness disclosure but does not own this source set or freshness policy |
| Reject duplicate required-source records and duplicate SKU identity before producing recommendations | Duplicate-source and duplicate-SKU tests | `proposed-candidate` | `candidate-only`; recurrence evidence is `missing` |
| Pin the inventory semantic, policy, synthetic access, and UTC review-period contracts | Unsupported-version, access, and UTC-offset tests | `case-specific` | `retain-in-case` as this case's implementation of core version and access invariants |
| Expose unassessed uncertainty | Golden result and replay test; canonical decision-support validation rule | `existing-core-invariant` | `retain-in-case` as an implementation of the invariant |
| Require human review of every valid inventory result | Decision contract and golden result | `case-specific` | `retain-in-case`; the core requires uncertainty disclosure but does not prescribe this decision policy for every case |
| Separate whole-snapshot abstention from item-level abstention | Access, freshness, invalid-item, and partial-result tests | `proposed-candidate` | `candidate-only`; recurrence evidence is `missing` |
| Use bounded integer arithmetic for domain quantities | Fractional, non-finite, out-of-range, and derived-overflow tests | `case-specific` | `retain-in-case` until another domain demonstrates the same numeric contract |

## Candidate Interfaces

### Unambiguous identity validation

```text
validateUniqueIdentity(records, identityDefinition) -> valid | conflicting identities
```

The case shows that ambiguous item or required-source identity must fail closed, but no second runnable scenario currently demonstrates the same Interface or repeated Implementation complexity. The seam and promotion evidence are `missing`.

### Scoped abstention

```text
classifyEvidenceFailure(failure, decisionScope) -> whole-result | item-result abstention
```

The case has useful failure scopes, but their semantics may depend on each decision's risk and partial-result policy. A second scenario and an accountable shared contract are `missing`; premature extraction could conceal domain authority.

## Promotion decision

Overall result: `candidate-only`.

No behaviour from this case is promoted into FDE core. Domain calculations remain with the inventory case. Existing FDE invariants remain owned by their canonical sources. The two proposed candidates lack a second independent runnable scenario, replay equivalence, an accepted shared Interface, shared version ownership, and cross-case rollback evidence.

## Validation and rollback

The inventory case can replay its fixtures and pin or revert its own capability version independently. A real version owner, release acceptance, and rollback owner are `missing`; the synthetic scenario names no accountable post-engagement operating owner. Cross-case replay and rollback are also `missing` because no shared Module exists. Promotion must not make a future shared Module a prerequisite for rolling back this case.

## Next accountable action

The FDE delivery owner should name the repository capability-version and rollback owner, then complete a second runnable case and its capability-return review. Completion means the named owner accepts the case release/rollback responsibility, the review shows whether identity ambiguity or abstention scope recurs with the same domain-neutral Interface, and both case evaluation sets replay equivalently. Until then, both observations remain proposed candidates and all implementation stays case-owned.
