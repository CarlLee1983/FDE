#!/usr/bin/env python3
"""Read a synthetic refund-status fixture and emit an evidence-backed result."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED_SEMANTIC_DEFINITION_VERSION = "refund-status/v1"


class ReadOnlyError(Exception):
    """A fail-closed error which is safe to serialize to the caller."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def parse_timestamp(value: str) -> datetime:
    """Parse the fixture's ISO-8601 timestamp as an offset-aware UTC time."""
    if not isinstance(value, str):
        raise ReadOnlyError("invalid_fixture", "Fixture timestamp must be an ISO-8601 string.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as error:
        raise ReadOnlyError("invalid_fixture", "Fixture contains an invalid timestamp.") from error
    if parsed.tzinfo is None:
        raise ReadOnlyError("invalid_fixture", "Fixture timestamp must include a timezone.")
    return parsed.astimezone(timezone.utc)


def read_fixture(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReadOnlyError("invalid_fixture", "Fixture cannot be read as JSON.") from error
    if not isinstance(data, dict):
        raise ReadOnlyError("invalid_fixture", "Fixture root must be a JSON object.")
    return data


def lookup(refund_case_id: str, fixture_path: Path, as_of: str) -> dict[str, Any]:
    """Return only a current, authorized result from the supported semantic contract."""
    fixture = read_fixture(fixture_path)
    version = fixture.get("semanticDefinitionVersion")
    if version != SUPPORTED_SEMANTIC_DEFINITION_VERSION:
        raise ReadOnlyError(
            "unsupported_semantic_definition",
            "Fixture semantic definition version is not supported.",
        )

    as_of_time = parse_timestamp(as_of)
    source_evidence = fixture.get("sourceEvidence")
    if not isinstance(source_evidence, dict):
        raise ReadOnlyError("invalid_fixture", "Fixture lacks valid source evidence.")
    source_kind = source_evidence.get("kind")
    source_id = source_evidence.get("sourceId")
    if not (
        isinstance(source_kind, str)
        and source_kind.strip()
        and isinstance(source_id, str)
        and source_id.strip()
    ):
        raise ReadOnlyError(
            "invalid_source_evidence",
            "Fixture source evidence requires non-empty kind and sourceId values.",
        )
    observed_at = parse_timestamp(source_evidence.get("observedAt"))
    expires_at = parse_timestamp(fixture.get("expiresAt"))
    if not observed_at <= as_of_time <= expires_at:
        raise ReadOnlyError(
            "evidence_outside_freshness_window",
            "Fixture evidence is not current for the requested as-of time.",
        )

    records = fixture.get("records")
    if not isinstance(records, list):
        raise ReadOnlyError("invalid_fixture", "Fixture records must be a JSON array.")
    record = next(
        (item for item in records if isinstance(item, dict) and item.get("refundCaseId") == refund_case_id),
        None,
    )
    if record is None:
        raise ReadOnlyError("refund_case_not_found", "No matching refund case exists in this fixture.")
    if record.get("accessAllowed") is not True:
        raise ReadOnlyError("access_denied", "Access to this refund case is denied.")

    result = record.get("result")
    if not isinstance(result, dict):
        raise ReadOnlyError("invalid_fixture", "Fixture lacks a valid result or source evidence.")

    return {
        "result": result,
        "semanticDefinitionVersion": version,
        "sourceEvidence": source_evidence,
        "freshness": {
            "observedAt": observed_at.isoformat().replace("+00:00", "Z"),
            "asOf": as_of_time.isoformat().replace("+00:00", "Z"),
            "expiresAt": expires_at.isoformat().replace("+00:00", "Z"),
            "status": "fresh",
        },
        "accessDecision": {
            "allowed": True,
            "policy": "synthetic-fixture-access/v1",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read a synthetic refund-status fixture.")
    parser.add_argument("refund_case_id", help="De-identified refund case ID")
    parser.add_argument("fixture", type=Path, help="Path to a local JSON fixture")
    parser.add_argument(
        "--as-of",
        default="2026-08-28T00:00:00Z",
        help="ISO-8601 evaluation time (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    try:
        print(json.dumps(lookup(args.refund_case_id, args.fixture, args.as_of), sort_keys=True))
    except ReadOnlyError as error:
        print(json.dumps({"error": {"code": error.code, "message": error.message}}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
