# Deterministic replenishment decision contract

**Status:** `proposed` baseline sub-slice, synthetic/local-only. This contract has no enterprise access or approval evidence and does not complete the proposal's planner-feedback workflow.

## Input snapshot

The JSON input is one fixed-time snapshot. It requires `asOf`, `semanticDefinitionVersion`, an `accessDecision`, `sourceEvidence`, `policy`, and `items`.

- `asOf` must be an ISO 8601 UTC timestamp ending in `Z`; the UTC calendar date is used for review-period membership.
- `semanticDefinitionVersion` must be `inventory-replenishment-semantics@0.1.0`.
- `accessDecision` must exactly match the built-in synthetic local replay profile. It explicitly states `enterpriseAuthorization: false`; any other value causes a whole-snapshot abstention.
- Required sources are `inventory-snapshot`, `demand-snapshot`, and `supplier-policy`. Each needs an `observedAt` and `freshUntil` time that brackets `asOf`.
- `policy` must name the implemented `synthetic-replenishment-policy@0.1.0` and carries a `reviewPeriod`. It is echoed in every result to make the replay decision traceable.
- Each item has a snapshot-unique `sku` plus non-negative integer `onHand`, `reserved`, `dailyDemand`, `safetyStock`, `leadTime`, `inboundBeforeArrival`, `minOrderQty`, and `packSize`. A duplicate SKU abstains the whole snapshot because item identity becomes ambiguous. `inboundBeforeArrival` includes only quantities whose arrival before the assessed replenishment arrival has already been established by the synthetic source.

## Rule

For a valid item, the deterministic baseline is:

```text
projectedStockAtArrival = onHand - reserved + inboundBeforeArrival - (dailyDemand * leadTime)
shortfall = safetyStock - projectedStockAtArrival
```

Only `shortfall > 0` creates a candidate. Its quantity is `max(shortfall, minOrderQty)`, rounded up to the next `packSize`. Equality with safety stock does not create a candidate. Invalid item data abstains only that item; invalid access, a stale/missing required source, or invalid snapshot-wide metadata abstains the entire result.

## Output and authority boundary

Every result includes `result`, `semanticDefinitionVersion`, `sourceEvidence`, `freshness`, `accessDecision`, `policy`, and `writeBack`. Each valid item states that demand, supplier-lead-time, and inbound uncertainty are unassessed and human review is required. `writeBack.permitted` and `writeBack.attempted` are always `false`. This local program does not connect to, create, modify, approve, or submit a purchase order or any external record.
