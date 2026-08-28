#!/usr/bin/env python3
"""Deterministic, read-only replay for the synthetic reconciliation example."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parents[1]
DEFAULT_AS_OF = "2026-08-28T09:15:00Z"
DEFAULT_ACTOR = "synthetic-reconciliation-operator"
DEFAULT_SCENARIO = "account-reconciliation-demo"
EXPECTED_FIELDS = ["transactionId", "reference", "referenceVersion", "amountMinor", "currency", "bookingDate"]
EXPECTED_RULE = "Within one immutable account/currency/closed-period snapshot, match exactly one bank record to exactly one ledger record only when reference, referenceVersion, integer amountMinor, currency, and bookingDate all match; never tie-break multiple candidates."


def load(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ValueError(f"object required: {path}")
    return value


def timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def iso_date(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None
    return value if parsed.strftime("%Y-%m-%d") == value else None


def valid_record(record: Any, currency: Any, period: Any) -> bool:
    valid_currency = isinstance(currency, str) and len(currency) == 3 and currency.isascii() and currency.isalpha() and currency.isupper()
    return (isinstance(record, dict) and all(isinstance(record.get(field), str) and record[field].strip() for field in ("transactionId", "reference", "referenceVersion", "bookingDate")) and type(record.get("amountMinor")) is int and record.get("currency") == currency and valid_currency and isinstance(period, str) and iso_date(record["bookingDate"]) is not None and record["bookingDate"][:7] == period)


def match_key(record: dict[str, Any]) -> tuple[str, str, int, str, str]:
    return (record["reference"], record["referenceVersion"], record["amountMinor"], record["currency"], record["bookingDate"])


def review_key(record: dict[str, Any]) -> tuple[str, str, str, str]:
    return (record["reference"], record["referenceVersion"], record["currency"], record["bookingDate"])


def replay(snapshot: dict[str, Any], semantics: dict[str, Any], decision: dict[str, Any], access: dict[str, Any], as_of: str, actor: str, scenario: str) -> dict[str, Any]:
    failures: list[str] = []
    captured = timestamp(snapshot.get("capturedAt"))
    query_time = timestamp(as_of)
    freshness_policy = mapping(access.get("freshnessPolicy"))
    maximum_age = freshness_policy.get("maximumAgeMinutes")
    age_seconds = None if not captured or not query_time else int((query_time - captured).total_seconds())
    freshness_status = "invalid" if age_seconds is None or age_seconds < 0 or type(maximum_age) is not int else ("fresh" if age_seconds <= maximum_age * 60 else "stale")
    freshness = {"asOf": as_of, "ageSeconds": age_seconds, "maximumAgeMinutes": maximum_age, "status": freshness_status}
    required_scope = "synthetic local example only"
    if snapshot.get("scope") != required_scope: failures.append("invalid snapshot scope")
    semantic_definitions = semantics.get("definitions") if isinstance(semantics.get("definitions"), list) else []
    semantic_ids = {item.get("id") for item in semantic_definitions if isinstance(item, dict) and isinstance(item.get("id"), str)}
    required_semantic_ids = {"BankTransaction", "InternalLedgerEntry", "ReconciliationExactMatch", *EXPECTED_FIELDS}
    if semantics.get("registryId") != "synthetic-account-reconciliation-semantics" or semantics.get("version") != "1.0.0" or semantics.get("status") != "proposed" or semantic_ids != required_semantic_ids: failures.append("semantic definition mismatch")
    expected_inputs = {"bank": EXPECTED_FIELDS, "ledger": EXPECTED_FIELDS}
    if decision.get("id") != "synthetic-bank-ledger-exact-reconciliation" or decision.get("version") != "1.0.0" or decision.get("status") != "proposed" or decision.get("inputs") != expected_inputs or decision.get("rule") != EXPECTED_RULE or decision.get("output") != {"type": "read-only reconciliation result", "writeBack": False}: failures.append("decision contract mismatch")
    expected_access_scope = "synthetic local fixture only; not target-enterprise access evidence"
    if access.get("scope") != expected_access_scope or access.get("decisionId") != "synthetic-local-reconciliation-access-001": failures.append("access decision contract mismatch")
    if snapshot.get("sourceId") != access.get("sourceId") or access.get("scenarioId") != scenario: failures.append("source or scenario mismatch")
    subject = mapping(access.get("subject"))
    if subject.get("id") != actor: failures.append("access subject mismatch")
    access_time = timestamp(access.get("evaluatedAt"))
    access_valid_until = timestamp(access.get("validUntil"))
    if not access_time or not access_valid_until or not query_time or access_time > query_time or query_time > access_valid_until or access.get("status") != "active": failures.append("access decision is invalid, inactive, or outside its validity window")
    permissions = mapping(access.get("permissions"))
    if permissions.get("query") != "allowed" or permissions.get("reconciliation") != "allowed" or permissions.get("writeBack") != "denied": failures.append("access not allowed")
    if freshness_status != "fresh": failures.append("source is stale or freshness is invalid")
    bank, ledger = snapshot.get("bankTransactions"), snapshot.get("ledgerEntries")
    currency, period = snapshot.get("currency"), snapshot.get("closedPeriod")
    if snapshot.get("immutable") is not True or not isinstance(snapshot.get("accountId"), str) or not snapshot["accountId"].strip() or not isinstance(currency, str) or not isinstance(period, str): failures.append("invalid immutable snapshot boundary")
    if not isinstance(bank, list) or not isinstance(ledger, list): failures.append("missing or conflicting sources")
    else:
        for source_name, records in (("bank", bank), ("ledger", ledger)):
            if not all(valid_record(record, currency, period) for record in records): failures.append(f"invalid {source_name} record")
            ids = [record.get("transactionId") for record in records if isinstance(record, dict) and isinstance(record.get("transactionId"), str)]
            if len(ids) != len(set(ids)): failures.append(f"duplicate {source_name} transactionId")
        totals = snapshot.get("controlTotals")
        actual_totals = {"bankRecordCount": len(bank), "bankAmountMinor": sum(record["amountMinor"] for record in bank if valid_record(record, currency, period)), "ledgerRecordCount": len(ledger), "ledgerAmountMinor": sum(record["amountMinor"] for record in ledger if valid_record(record, currency, period))}
        if totals != actual_totals: failures.append("source control totals mismatch")
    evidence = {"sourceId": snapshot.get("sourceId"), "capturedAt": snapshot.get("capturedAt"), "accountId": snapshot.get("accountId"), "currency": currency, "closedPeriod": period, "immutable": snapshot.get("immutable"), "controlTotals": snapshot.get("controlTotals")}
    access_out = {"decisionId": access.get("decisionId"), "scope": access.get("scope"), "evaluatedAt": access.get("evaluatedAt"), "validUntil": access.get("validUntil"), "status": access.get("status"), "subject": access.get("subject"), "scenarioId": access.get("scenarioId"), "sourceId": access.get("sourceId"), "query": permissions.get("query"), "reconciliation": permissions.get("reconciliation"), "writeBack": permissions.get("writeBack")}
    output = {"scope": required_scope, "query": {"scenarioId": scenario, "actor": actor, "asOf": as_of}, "result": {"exactMatches": [], "humanReviewQueue": []}, "semanticDefinitionVersion": {"registryId": semantics.get("registryId"), "version": semantics.get("version"), "status": semantics.get("status")}, "decisionServiceVersion": {"id": decision.get("id"), "version": decision.get("version"), "status": decision.get("status")}, "sourceEvidence": evidence, "freshness": freshness, "accessDecision": access_out, "contractFailures": sorted(set(failures)), "writeBack": False}
    if failures:
        return output
    bank_by_key: dict[tuple[str, str, int, str, str], list[dict[str, Any]]] = {}
    ledger_by_key: dict[tuple[str, str, int, str, str], list[dict[str, Any]]] = {}
    for record in bank: bank_by_key.setdefault(match_key(record), []).append(record)
    for record in ledger: ledger_by_key.setdefault(match_key(record), []).append(record)
    matched_bank_ids: set[str] = set()
    matched_ledger_ids: set[str] = set()
    for key in sorted(set(bank_by_key) & set(ledger_by_key)):
        bank_candidates, ledger_candidates = bank_by_key.get(key, []), ledger_by_key.get(key, [])
        if len(bank_candidates) == len(ledger_candidates) == 1:
            output["result"]["exactMatches"].append({"reference": key[0], "referenceVersion": key[1], "amountMinor": key[2], "currency": key[3], "bookingDate": key[4], "bankTransactionId": bank_candidates[0]["transactionId"], "ledgerTransactionId": ledger_candidates[0]["transactionId"]})
            matched_bank_ids.add(bank_candidates[0]["transactionId"])
            matched_ledger_ids.add(ledger_candidates[0]["transactionId"])
    review_groups: dict[tuple[str, str, str, str], dict[str, list[dict[str, Any]]]] = {}
    for side, records, matched_ids in (("bankCandidates", bank, matched_bank_ids), ("ledgerCandidates", ledger, matched_ledger_ids)):
        for record in records:
            if record["transactionId"] in matched_ids:
                continue
            review_groups.setdefault(review_key(record), {"bankCandidates": [], "ledgerCandidates": []})[side].append(record)
    for key in sorted(review_groups):
        candidates = review_groups[key]
        bank_candidates, ledger_candidates = candidates["bankCandidates"], candidates["ledgerCandidates"]
        if len(bank_candidates) > 1 or len(ledger_candidates) > 1:
            reason = "ambiguous-multiple-candidates-abstained"
        elif bank_candidates and ledger_candidates:
            reason = "amount-mismatch"
        else:
            reason = "unmatched"
        output["result"]["humanReviewQueue"].append({"reference": key[0], "referenceVersion": key[1], "currency": key[2], "bookingDate": key[3], "reason": reason, **candidates})
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", default=HERE / "evidence/reconciliation-snapshot.json")
    parser.add_argument("--semantic-definitions", default=HERE / "artifacts/semantic-definitions.json")
    parser.add_argument("--decision-service", default=HERE / "artifacts/decision-service.json")
    parser.add_argument("--access-decision", default=HERE / "evidence/local-access-decision.json")
    parser.add_argument("--as-of", default=DEFAULT_AS_OF)
    parser.add_argument("--actor", default=DEFAULT_ACTOR)
    parser.add_argument("--scenario", default=DEFAULT_SCENARIO)
    args = parser.parse_args()
    try:
        result = replay(load(args.snapshot), load(args.semantic_definitions), load(args.decision_service), load(args.access_decision), args.as_of, args.actor, args.scenario)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"replay failed closed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
