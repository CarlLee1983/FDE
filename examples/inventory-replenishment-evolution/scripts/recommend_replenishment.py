#!/usr/bin/env python3
"""Produce deterministic, read-only replenishment candidates from one snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_SOURCES = {
    "inventory-snapshot",
    "demand-snapshot",
    "supplier-policy",
}
SUPPORTED_SEMANTIC_VERSION = "inventory-replenishment-semantics@0.1.0"
SUPPORTED_POLICY_VERSION = "synthetic-replenishment-policy@0.1.0"
SUPPORTED_ACCESS_DECISION = {
    "decision": "allowed",
    "decisionId": "synthetic-local-read-only@0.1.0",
    "scope": "local fixture replay only",
    "evidenceStatus": "synthetic",
    "enterpriseAuthorization": False,
}
MAX_QUANTITY = 9_007_199_254_740_991
REQUIRED_ITEM_FIELDS = (
    "sku",
    "onHand",
    "reserved",
    "dailyDemand",
    "safetyStock",
    "leadTime",
    "inboundBeforeArrival",
    "minOrderQty",
    "packSize",
)


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def ceil_to_pack(quantity: int, pack_size: int) -> int:
    return ((quantity + pack_size - 1) // pack_size) * pack_size


def item_error(item: Any) -> str | None:
    if not isinstance(item, dict):
        return "invalid-item"
    for field in REQUIRED_ITEM_FIELDS:
        if field not in item:
            return f"missing-{field}"
    if not isinstance(item["sku"], str) or not item["sku"].strip():
        return "invalid-sku"
    for field in REQUIRED_ITEM_FIELDS[1:]:
        value = item[field]
        if isinstance(value, bool) or not isinstance(value, int):
            return f"invalid-{field}"
        if value < 0 or value > MAX_QUANTITY:
            return f"invalid-{field}"
    if item["minOrderQty"] == 0 or item["packSize"] == 0:
        return "invalid-order-constraint"
    return None


def assess_freshness(snapshot: dict[str, Any], as_of: datetime | None) -> tuple[dict[str, Any], list[str]]:
    by_id: dict[str, list[dict[str, Any]]] = {}
    source_evidence = snapshot.get("sourceEvidence", [])
    if not isinstance(source_evidence, list):
        source_evidence = []
    for source in source_evidence:
        if isinstance(source, dict) and isinstance(source.get("sourceId"), str):
            by_id.setdefault(source["sourceId"], []).append(source)
    records: list[dict[str, Any]] = []
    issues: list[str] = []
    for source_id in sorted(REQUIRED_SOURCES):
        matches = by_id.get(source_id, [])
        if not matches:
            records.append({"sourceId": source_id, "status": "missing"})
            issues.append(f"missing-source:{source_id}")
            continue
        if len(matches) != 1:
            records.append({"sourceId": source_id, "status": "conflicting"})
            issues.append(f"conflicting-source:{source_id}")
            continue
        source = matches[0]
        observed_at = parse_timestamp(source.get("observedAt"))
        fresh_until = parse_timestamp(source.get("freshUntil"))
        if as_of is None or observed_at is None or fresh_until is None or observed_at > fresh_until:
            status = "unverifiable"
        elif observed_at <= as_of <= fresh_until:
            status = "fresh"
        else:
            status = "stale"
        records.append({
            "sourceId": source_id,
            "observedAt": source.get("observedAt"),
            "freshUntil": source.get("freshUntil"),
            "status": status,
        })
        if status != "fresh":
            issues.append(f"{status}-source:{source_id}")
    statuses = {record["status"] for record in records}
    overall = "fresh" if statuses == {"fresh"} else "unverifiable" if "unverifiable" in statuses else "unacceptable"
    return {"status": overall, "evaluatedAt": snapshot.get("asOf"), "sources": records}, issues


def abstained(snapshot: dict[str, Any], reasons: list[str], freshness: dict[str, Any]) -> dict[str, Any]:
    return {
        "asOf": snapshot.get("asOf"),
        "result": {"status": "abstained", "reasonCodes": reasons, "items": []},
        "semanticDefinitionVersion": snapshot.get("semanticDefinitionVersion"),
        "sourceEvidence": snapshot.get("sourceEvidence", []),
        "freshness": freshness,
        "accessDecision": snapshot.get("accessDecision"),
        "policy": snapshot.get("policy"),
        "writeBack": {"permitted": False, "attempted": False, "reason": "read-only-synthetic-local-tool"},
    }


def recommend(snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        return abstained({}, ["invalid-snapshot"], {"status": "unverifiable", "evaluatedAt": None, "sources": []})
    raw_as_of = snapshot.get("asOf")
    as_of = parse_timestamp(raw_as_of) if isinstance(raw_as_of, str) and raw_as_of.endswith("Z") else None
    freshness, source_issues = assess_freshness(snapshot, as_of)
    if as_of is None:
        return abstained(snapshot, ["invalid-asOf"], freshness)
    if snapshot.get("semanticDefinitionVersion") != SUPPORTED_SEMANTIC_VERSION:
        return abstained(snapshot, ["unsupported-semantic-definition-version"], freshness)
    policy = snapshot.get("policy")
    if not isinstance(policy, dict) or policy.get("policyVersion") != SUPPORTED_POLICY_VERSION:
        return abstained(snapshot, ["unsupported-policy-version"], freshness)
    review_period = policy.get("reviewPeriod")
    if not isinstance(review_period, dict):
        return abstained(snapshot, ["invalid-review-period"], freshness)
    review_start = parse_date(review_period.get("start"))
    review_end = parse_date(review_period.get("end"))
    if review_start is None or review_end is None or review_start > review_end or not review_start <= as_of.date() <= review_end:
        return abstained(snapshot, ["invalid-review-period"], freshness)
    access = snapshot.get("accessDecision")
    if access != SUPPORTED_ACCESS_DECISION:
        return abstained(snapshot, ["access-not-allowed"], freshness)
    if source_issues:
        return abstained(snapshot, source_issues, freshness)
    items = snapshot.get("items")
    if not isinstance(items, list):
        return abstained(snapshot, ["invalid-items"], freshness)
    skus = [item.get("sku") for item in items if isinstance(item, dict) and isinstance(item.get("sku"), str)]
    duplicate_skus = sorted({sku for sku in skus if skus.count(sku) > 1})
    if duplicate_skus:
        return abstained(snapshot, [f"duplicate-sku:{sku}" for sku in duplicate_skus], freshness)

    results: list[dict[str, Any]] = []
    for item in items:
        error = item_error(item)
        if error:
            results.append({"sku": item.get("sku") if isinstance(item, dict) else None, "status": "abstained", "reasonCodes": [error]})
            continue
        projected = item["onHand"] - item["reserved"] + item["inboundBeforeArrival"] - item["dailyDemand"] * item["leadTime"]
        shortfall = item["safetyStock"] - projected
        if abs(projected) > MAX_QUANTITY or shortfall > MAX_QUANTITY:
            results.append({"sku": item["sku"], "status": "abstained", "reasonCodes": ["calculation-out-of-range"]})
            continue
        uncertainty = {
            "status": "unassessed",
            "factors": ["demand-variability", "supplier-lead-time-variability", "inbound-reliability"],
            "decisionUse": "human-review-required",
        }
        if shortfall <= 0:
            results.append({"sku": item["sku"], "status": "no-candidate", "projectedStockAtArrival": projected, "uncertainty": uncertainty, "reasonCodes": ["safety-stock-met-at-arrival"]})
            continue
        requested = max(shortfall, item["minOrderQty"])
        quantity = ceil_to_pack(requested, item["packSize"])
        if quantity > MAX_QUANTITY:
            results.append({"sku": item["sku"], "status": "abstained", "reasonCodes": ["calculation-out-of-range"]})
            continue
        results.append({
            "sku": item["sku"],
            "status": "candidate",
            "projectedStockAtArrival": projected,
            "safetyStock": item["safetyStock"],
            "shortfall": shortfall,
            "quantity": quantity,
            "uncertainty": uncertainty,
            "reasonCodes": ["projected-stock-below-safety-stock", "rounded-to-min-order-and-pack-size"],
        })
    has_candidates = any(result["status"] == "candidate" for result in results)
    has_abstentions = any(result["status"] == "abstained" for result in results)
    status = "candidates" if has_candidates else "no-candidates"
    if has_abstentions:
        status += "-with-abstentions"
    return {
        "asOf": snapshot["asOf"],
        "result": {"status": status, "reasonCodes": [], "items": results},
        "semanticDefinitionVersion": snapshot["semanticDefinitionVersion"],
        "sourceEvidence": snapshot["sourceEvidence"],
        "freshness": freshness,
        "accessDecision": access,
        "policy": policy,
        "writeBack": {"permitted": False, "attempted": False, "reason": "read-only-synthetic-local-tool"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="local synthetic snapshot JSON")
    parser.add_argument("--output", type=Path, help="write result JSON to this local path")
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"cannot read snapshot: {error}")
    output = json.dumps(recommend(snapshot), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
