#!/usr/bin/env python3
"""Replay the synthetic shipment-priority decision without persistent actions."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_INPUTS = ("shipmentId", "overdueHours", "serviceLevel", "temperatureControlled", "atRiskCustomerCommitment")
EXPECTED_BINDINGS = {
    "shipmentId": "Shipment.shipmentId", "overdueHours": "Shipment.overdueHours", "serviceLevel": "Shipment.serviceLevel",
    "temperatureControlled": "Shipment.temperatureControlled", "atRiskCustomerCommitment": "Shipment.atRiskCustomerCommitment",
}
EXPECTED_SERVICE_LEVELS = ["critical", "standard"]
EXPECTED_RULES = {
    "baseScore": [{"when": "overdueHours >= 48", "score": 50}, {"when": "overdueHours >= 24 and overdueHours < 48", "score": 30}, {"when": "overdueHours < 24", "score": 10}],
    "additions": [{"when": "serviceLevel == critical", "score": 25}, {"when": "temperatureControlled == true", "score": 20}, {"when": "atRiskCustomerCommitment == true", "score": 15}],
    "missingRequiredInput": "escalate without score", "tieBreakers": ["overdueHours descending", "shipmentId ascending"],
}
ALLOWED_DISPOSITIONS = {"accepted", "rejected", "needs-investigation"}
DISPOSITION_OUTCOMES = {
    "accepted": "Demo Logistics Coordinator follows up under the synthetic target workflow.",
    "rejected": "Demo Logistics Coordinator records the rejection rationale before choosing an alternative follow-up.",
    "needs-investigation": "Demo Logistics Coordinator investigates the shipment evidence before operational follow-up.",
}


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def empty_result() -> dict[str, list[dict[str, Any]]]:
    return {"recommendations": [], "escalations": []}


def expected_scope(value: Any, expected: str) -> bool:
    return value == expected


def allowed_service_levels(semantic_definitions: dict[str, Any]) -> set[str]:
    definitions = semantic_definitions.get("definitions")
    if not isinstance(definitions, list):
        return set()
    for definition in definitions:
        if isinstance(definition, dict) and definition.get("id") == "Shipment.serviceLevel":
            values = definition.get("allowedValues")
            if isinstance(values, list) and all(isinstance(value, str) for value in values):
                return set(values)
    return set()


def contract_failures(snapshot: dict[str, Any], semantics: dict[str, Any], decision: dict[str, Any], access: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    source_id = snapshot.get("sourceId")
    if not expected_scope(snapshot.get("scope"), "synthetic demo only"):
        failures.append("invalid snapshot scope")
    if not expected_scope(semantics.get("scope"), "synthetic demo only"):
        failures.append("invalid semantic scope")
    if not expected_scope(decision.get("scope"), "synthetic demo only; human review recommendation; no write-back"):
        failures.append("invalid decision scope")
    if not expected_scope(access.get("scope"), "synthetic demo sandbox only"):
        failures.append("invalid access scope")
    if semantics.get("registryId") != "demo-shipment-semantics" or semantics.get("version") != "1.0.0" or semantics.get("status") != "released":
        failures.append("semantic definition is not the supported released version")
    service_level_definition = next((definition for definition in semantics.get("definitions", []) if isinstance(definition, dict) and definition.get("id") == "Shipment.serviceLevel"), None) if isinstance(semantics.get("definitions"), list) else None
    if not isinstance(service_level_definition, dict) or service_level_definition.get("allowedValues") != EXPECTED_SERVICE_LEVELS:
        failures.append("semantic service-level values do not match the supported contract")
    source_definitions = semantics.get("sourceDefinitions")
    source_definition = source_definitions[0] if isinstance(source_definitions, list) and len(source_definitions) == 1 and isinstance(source_definitions[0], dict) else None
    if source_definition is None or source_definition.get("id") != source_id or source_definition.get("status") != "released":
        failures.append("snapshot source is not bound to the semantic contract")
    bindings = decision.get("inputBindings")
    binding_map = {binding.get("input"): binding.get("semanticId") for binding in bindings if isinstance(binding, dict)} if isinstance(bindings, list) else {}
    binding_sources = {binding.get("sourceId") for binding in bindings if isinstance(binding, dict)} if isinstance(bindings, list) else set()
    if tuple(decision.get("requiredInputs", [])) != REQUIRED_INPUTS or binding_map != EXPECTED_BINDINGS or binding_sources != {source_id}:
        failures.append("decision inputs are not bound to the supported semantic source contract")
    if decision.get("id") != "rank-delayed-shipment-for-review" or decision.get("version") != "1.0.0" or decision.get("rules") != EXPECTED_RULES:
        failures.append("decision rules do not match the supported synthetic contract")
    decision_output = decision.get("output") if isinstance(decision.get("output"), dict) else {}
    if decision_output.get("persistentActionAllowed") is not False or "no write-back" not in str(decision.get("scope")):
        failures.append("decision contract does not enforce the non-persistent boundary")
    if access.get("sourceId") != source_id:
        failures.append("access evidence is not bound to the snapshot source")
    if access.get("decisionId") != "demo-access-decision-001":
        failures.append("access decision is not the supported synthetic decision")
    freshness_policy = access.get("freshnessPolicy") if isinstance(access.get("freshnessPolicy"), dict) else {}
    if freshness_policy.get("maximumAgeMinutes") != 60:
        failures.append("freshness policy does not match the supported synthetic SLA")
    permissions = access.get("permissions") if isinstance(access.get("permissions"), dict) else {}
    if permissions.get("controlledExecution") != "denied":
        failures.append("controlled execution is not denied")
    return failures


def score_record(record: dict[str, Any]) -> tuple[int, list[str]]:
    overdue_hours = record["overdueHours"]
    if overdue_hours >= 48:
        score, reasons = 50, ["overdueHours >= 48"]
    elif overdue_hours >= 24:
        score, reasons = 30, ["overdueHours >= 24 and overdueHours < 48"]
    else:
        score, reasons = 10, ["overdueHours < 24"]
    if record["serviceLevel"] == "critical":
        score += 25
        reasons.append("serviceLevel == critical")
    if record["temperatureControlled"]:
        score += 20
        reasons.append("temperatureControlled == true")
    if record["atRiskCustomerCommitment"]:
        score += 15
        reasons.append("atRiskCustomerCommitment == true")
    return score, reasons


def record_failure(record: Any, service_levels: set[str]) -> tuple[Any, str | None]:
    if not isinstance(record, dict):
        return None, "record"
    shipment_id = record.get("shipmentId")
    for field in REQUIRED_INPUTS:
        if field not in record:
            return shipment_id, f"missing required input: {field}"
    if not isinstance(shipment_id, str) or not shipment_id.strip():
        return shipment_id, "invalid required input: shipmentId"
    overdue_hours = record["overdueHours"]
    if isinstance(overdue_hours, bool) or not isinstance(overdue_hours, (int, float)) or not math.isfinite(overdue_hours) or overdue_hours < 0:
        return shipment_id, "invalid required input: overdueHours"
    if not isinstance(record["serviceLevel"], str) or record["serviceLevel"] not in service_levels:
        return shipment_id, "invalid required input: serviceLevel"
    for field in ("temperatureControlled", "atRiskCustomerCommitment"):
        if not isinstance(record[field], bool):
            return shipment_id, f"invalid required input: {field}"
    return shipment_id, None


def disposition_records(dispositions: dict[str, str], recommendation_ids: set[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for shipment_id in sorted(dispositions):
        disposition = dispositions[shipment_id]
        if shipment_id not in recommendation_ids:
            raise ValueError(f"disposition shipment is not recommended: {shipment_id}")
        if disposition not in ALLOWED_DISPOSITIONS:
            raise ValueError(f"unsupported disposition: {disposition}")
        records.append({"shipmentId": shipment_id, "disposition": disposition, "nextAccountableOutcome": DISPOSITION_OUTCOMES[disposition]})
    return records


def replay(snapshot: dict[str, Any], semantic_definitions: dict[str, Any], decision_service: dict[str, Any], access_decision: dict[str, Any], *, as_of: str, dispositions: dict[str, str] | None = None) -> dict[str, Any]:
    """Return a deterministic, synthetic read-only recommendation result."""
    captured_at, captured, evaluated = snapshot.get("capturedAt"), parse_timestamp(snapshot.get("capturedAt")), parse_timestamp(as_of)
    freshness_policy = access_decision.get("freshnessPolicy") if isinstance(access_decision.get("freshnessPolicy"), dict) else {}
    permissions = access_decision.get("permissions") if isinstance(access_decision.get("permissions"), dict) else {}
    maximum_age = freshness_policy.get("maximumAgeMinutes")
    age_seconds = (evaluated - captured).total_seconds() if captured and evaluated else None
    freshness_status = "unverifiable"
    if isinstance(maximum_age, int) and maximum_age >= 0 and age_seconds is not None:
        freshness_status = "fresh" if 0 <= age_seconds <= maximum_age * 60 else "stale"
    source_id = snapshot.get("sourceId")
    access_summary = {"decisionId": access_decision.get("decisionId"), "query": permissions.get("query"), "recommendation": permissions.get("recommendation"), "controlledExecution": permissions.get("controlledExecution")}
    failures = contract_failures(snapshot, semantic_definitions, decision_service, access_decision)
    preconditions = list(failures)
    if freshness_status != "fresh":
        preconditions.append(f"freshness is {freshness_status}")
    if access_summary["query"] != "allowed" or access_summary["recommendation"] != "allowed":
        preconditions.append("access is not allowed")
    output: dict[str, Any] = {
        "scope": snapshot.get("scope"), "query": {"scenarioId": "shipment-delay-priority-demo", "asOf": as_of}, "result": empty_result(),
        "semanticDefinition": {"registryId": semantic_definitions.get("registryId"), "version": semantic_definitions.get("version"), "status": semantic_definitions.get("status")},
        "sourceEvidence": {"sourceId": source_id, "capturedAt": captured_at, "recordCount": len(snapshot.get("records", [])) if isinstance(snapshot.get("records"), list) else 0},
        "freshness": {"asOf": as_of, "ageMinutes": age_seconds / 60 if age_seconds is not None else None, "ageSeconds": age_seconds, "maximumAgeMinutes": maximum_age, "status": freshness_status},
        "accessDecision": access_summary, "contractFailures": failures, "preconditionFailures": preconditions,
        "persistentActionExecuted": False, "sessionDispositions": {"persistence": "none", "status": "not-requested", "records": []},
    }
    if preconditions:
        return output
    records = snapshot.get("records")
    if not isinstance(records, list):
        output["preconditionFailures"].append("snapshot records are invalid")
        return output
    service_levels = allowed_service_levels(semantic_definitions)
    recommendations, escalations = [], []
    for record in records:
        shipment_id, failure = record_failure(record, service_levels)
        if failure:
            escalations.append({"shipmentId": shipment_id, "reason": failure, "priorityScore": None})
            continue
        score, reasons = score_record(record)
        recommendations.append((record, score, reasons))
    recommendations.sort(key=lambda item: (-item[1], -item[0]["overdueHours"], item[0]["shipmentId"]))
    output["result"] = {"recommendations": [{"shipmentId": record["shipmentId"], "priorityScore": score, "reasons": reasons} for record, score, reasons in recommendations], "escalations": escalations}
    if dispositions:
        output["sessionDispositions"] = {"persistence": "none", "status": "recorded", "records": disposition_records(dispositions, {record["shipmentId"] for record, _, _ in recommendations})}
    return output


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def parse_dispositions(values: list[str]) -> dict[str, str]:
    dispositions: dict[str, str] = {}
    for value in values:
        shipment_id, separator, disposition = value.partition("=")
        if not separator or not shipment_id or not disposition:
            raise ValueError("disposition must be SHIPMENT_ID=accepted|rejected|needs-investigation")
        if shipment_id in dispositions:
            raise ValueError(f"duplicate disposition shipmentId: {shipment_id}")
        dispositions[shipment_id] = disposition
    return dispositions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--semantic-definitions", required=True, type=Path)
    parser.add_argument("--decision-service", required=True, type=Path)
    parser.add_argument("--access-decision", required=True, type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--disposition", action="append", default=[])
    args = parser.parse_args()
    try:
        dispositions = parse_dispositions(args.disposition)
        output = replay(load_json(args.snapshot), load_json(args.semantic_definitions), load_json(args.decision_service), load_json(args.access_decision), as_of=args.as_of, dispositions=dispositions)
        if dispositions and output["preconditionFailures"]:
            raise ValueError("cannot apply dispositions: " + "; ".join(output["preconditionFailures"]))
    except ValueError as error:
        parser.error(str(error))
    sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
