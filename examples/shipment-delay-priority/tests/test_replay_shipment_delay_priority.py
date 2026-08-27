"""Public CLI replay-contract tests for the synthetic shipment-delay example."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

EXAMPLE = Path(__file__).resolve().parents[1]
SCRIPT = EXAMPLE / "scripts" / "replay_shipment_delay_priority.py"
AS_OF = "2026-08-25T09:00:00Z"


def load_json(relative_path: str):
    return json.loads((EXAMPLE / relative_path).read_text(encoding="utf-8"))


class ShipmentReplayCliTests(unittest.TestCase):
    def inputs(self):
        return {"snapshot": load_json("evidence/shipments.json"), "semantics": load_json("artifacts/semantic-definitions.json"), "decision": load_json("artifacts/decision-service.json"), "access": load_json("evidence/access-decision.json")}

    def invoke(self, inputs=None, *extra):
        inputs = inputs or self.inputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = {}
            for name, value in inputs.items():
                path = root / f"{name}.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                paths[name] = path
            command = [sys.executable, str(SCRIPT), "--snapshot", str(paths["snapshot"]), "--semantic-definitions", str(paths["semantics"]), "--decision-service", str(paths["decision"]), "--access-decision", str(paths["access"]), "--as-of", AS_OF, *extra]
            completed = subprocess.run(command, text=True, capture_output=True)
        return completed, json.loads(completed.stdout) if completed.stdout else None

    def test_normal_fixture_replays_expected_read_only_contract(self):
        completed, result = self.invoke()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result, load_json("expected/read-only-result.json"))

    def test_boundary_scores_and_tie_breakers_are_deterministic(self):
        inputs = self.inputs()
        inputs["snapshot"]["records"] = [
            {"shipmentId": "TIE-B", "overdueHours": 24, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
            {"shipmentId": "TIE-A", "overdueHours": 24, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
            {"shipmentId": "BOUNDARY-48", "overdueHours": 48, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
        ]
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual([item["shipmentId"] for item in result["result"]["recommendations"]], ["BOUNDARY-48", "TIE-A", "TIE-B"])
        self.assertEqual([item["priorityScore"] for item in result["result"]["recommendations"]], [50, 30, 30])

    def test_missing_required_field_escalates_without_scoring(self):
        completed, result = self.invoke()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["result"]["escalations"], [{"shipmentId": "SHP-1004", "reason": "missing required input: overdueHours", "priorityScore": None}])

    def test_freshness_uses_full_duration_at_and_after_the_boundary(self):
        inputs = self.inputs()
        inputs["snapshot"]["capturedAt"] = "2026-08-25T08:00:00Z"
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["freshness"], {"asOf": AS_OF, "ageMinutes": 60, "ageSeconds": 3600, "maximumAgeMinutes": 60, "status": "fresh"})
        inputs["snapshot"]["capturedAt"] = "2026-08-25T07:59:59Z"
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["freshness"]["status"], "stale")
        self.assertEqual(result["freshness"]["ageSeconds"], 3601)
        self.assertEqual(result["result"], {"recommendations": [], "escalations": []})

    def test_access_denied_returns_no_recommendation(self):
        inputs = self.inputs()
        inputs["access"]["permissions"]["recommendation"] = "denied"
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["result"], {"recommendations": [], "escalations": []})
        self.assertEqual(result["accessDecision"]["recommendation"], "denied")

    def test_invalid_required_facts_use_named_escalations(self):
        cases = {"shipmentId": "", "overdueHours": float("inf"), "serviceLevel": "express", "temperatureControlled": "true", "atRiskCustomerCommitment": 1}
        for field, value in cases.items():
            with self.subTest(field=field):
                inputs = self.inputs()
                inputs["snapshot"]["records"] = [{"shipmentId": "SHP-INVALID", "overdueHours": 24, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False}]
                inputs["snapshot"]["records"][0][field] = value
                completed, result = self.invoke(inputs)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                escalation = result["result"]["escalations"][0]
                self.assertEqual(escalation["reason"], f"invalid required input: {field}")
                self.assertIsNone(escalation["priorityScore"])

    def test_scope_and_contract_drift_fail_closed(self):
        inputs = self.inputs()
        inputs["snapshot"]["scope"] = "enterprise production export"
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["result"], {"recommendations": [], "escalations": []})
        self.assertIn("invalid snapshot scope", result["contractFailures"])
        self.assertEqual(result["scope"], "enterprise production export")
        inputs = self.inputs()
        inputs["decision"]["rules"]["baseScore"][0]["score"] = 999
        completed, result = self.invoke(inputs)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("decision rules do not match the supported synthetic contract", result["contractFailures"])
        self.assertEqual(result["result"], {"recommendations": [], "escalations": []})

    def test_semantic_allowed_values_must_match_the_released_contract_exactly(self):
        for values in (["critical"], ["critical", "standard", "express"], ["critical", "standard", "standard"]):
            with self.subTest(values=values):
                inputs = self.inputs()
                service_level = next(definition for definition in inputs["semantics"]["definitions"] if definition["id"] == "Shipment.serviceLevel")
                service_level["allowedValues"] = values
                completed, result = self.invoke(inputs)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn("semantic service-level values do not match the supported contract", result["contractFailures"])
                self.assertEqual(result["result"], {"recommendations": [], "escalations": []})

    def test_access_decision_and_sla_drift_fail_closed(self):
        for field, value, failure in (("decisionId", "other-decision", "access decision is not the supported synthetic decision"), ("maximumAgeMinutes", 61, "freshness policy does not match the supported synthetic SLA")):
            with self.subTest(field=field):
                inputs = self.inputs()
                if field == "maximumAgeMinutes":
                    inputs["access"]["freshnessPolicy"][field] = value
                else:
                    inputs["access"][field] = value
                completed, result = self.invoke(inputs)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(failure, result["contractFailures"])
                self.assertEqual(result["result"], {"recommendations": [], "escalations": []})

    def test_disposition_precondition_is_not_silently_discarded(self):
        inputs = self.inputs()
        inputs["snapshot"]["capturedAt"] = "2026-08-25T07:59:59Z"
        completed, result = self.invoke(inputs, "--disposition", "SHP-1001=accepted")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIsNone(result)
        self.assertIn("cannot apply dispositions", completed.stderr)

    def test_duplicate_disposition_is_rejected_instead_of_last_write_wins(self):
        completed, result = self.invoke(None, "--disposition", "SHP-1001=accepted", "--disposition", "SHP-1001=rejected")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIsNone(result)
        self.assertIn("duplicate disposition shipmentId: SHP-1001", completed.stderr)

    def test_disposition_is_session_local_and_has_accountable_outcome(self):
        completed, result = self.invoke(None, "--disposition", "SHP-1001=needs-investigation", "--disposition", "SHP-1002=accepted", "--disposition", "SHP-1003=rejected")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(result["sessionDispositions"]["persistence"], "none")
        self.assertEqual(result["sessionDispositions"]["records"][0], {"shipmentId": "SHP-1001", "disposition": "needs-investigation", "nextAccountableOutcome": "Demo Logistics Coordinator investigates the shipment evidence before operational follow-up."})

    def test_one_command_validator_asserts_the_synthetic_gate_boundary(self):
        environment = os.environ | {"SHIPMENT_VALIDATOR_CHILD": "1"}
        completed = subprocess.run([str(EXAMPLE / "scripts" / "validate-example.sh")], check=True, text=True, capture_output=True, env=environment)
        self.assertIn("shipment-delay-priority validation: passed", completed.stdout)


if __name__ == "__main__":
    unittest.main()
