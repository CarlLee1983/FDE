#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

python3 - "$example_dir" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

example = Path(sys.argv[1])
authorization = json.loads((example / "evidence/shadow-rehearsal-authorization.json").read_text(encoding="utf-8"))
result = json.loads((example / "evidence/shadow-rehearsal-result.json").read_text(encoding="utf-8"))
required_artifacts = (
    "scripts/replay_shipment_delay_priority.py",
    "evidence/shipments.json",
    "artifacts/semantic-definitions.json",
    "artifacts/decision-service.json",
    "evidence/access-decision.json",
    "expected/read-only-result.json",
)
expected_command = [
    "python3", "scripts/replay_shipment_delay_priority.py",
    "--snapshot", "evidence/shipments.json",
    "--semantic-definitions", "artifacts/semantic-definitions.json",
    "--decision-service", "artifacts/decision-service.json",
    "--access-decision", "evidence/access-decision.json",
    "--as-of", "2026-08-25T09:00:00Z",
    "--disposition", "SHP-1001=needs-investigation",
    "--disposition", "SHP-1002=accepted",
    "--disposition", "SHP-1003=rejected",
]
assert tuple(authorization["artifactDigests"]) == required_artifacts, "rehearsal artifact allowlist drift"
actual_digests = {relative: "sha256:" + hashlib.sha256((example / relative).read_bytes()).hexdigest() for relative in required_artifacts}
assert authorization["artifactDigests"] == actual_digests == result["artifactDigests"], "rehearsal artifact content drift"
assert authorization["replayPlan"]["command"] == expected_command, "rehearsal command allowlist drift"
PY

"$repo_dir/.agents/skills/fde-project-work/scripts/validate-scenario.sh" "$example_dir/scenario.json"

if [[ "${SHIPMENT_VALIDATOR_CHILD:-}" != "1" ]]; then
  python3 -m unittest discover -s "$example_dir/tests" -p 'test_*.py'
fi

actual_output="$(mktemp)"
trap 'rm -f "$actual_output"' EXIT
python3 "$example_dir/scripts/replay_shipment_delay_priority.py" \
  --snapshot "$example_dir/evidence/shipments.json" \
  --semantic-definitions "$example_dir/artifacts/semantic-definitions.json" \
  --decision-service "$example_dir/artifacts/decision-service.json" \
  --access-decision "$example_dir/evidence/access-decision.json" \
  --as-of '2026-08-25T09:00:00Z' >"$actual_output"
python3 - "$example_dir/expected/read-only-result.json" "$actual_output" <<'PY'
import json
import sys

expected = json.load(open(sys.argv[1], encoding="utf-8"))
actual = json.load(open(sys.argv[2], encoding="utf-8"))
assert actual == expected, "normal replay differs from the read-only contract"
PY

python3 - "$example_dir" <<'PY'
import importlib.util
import hashlib
import json
import subprocess
import sys
from pathlib import Path

example = Path(sys.argv[1])
script = example / "scripts" / "replay_shipment_delay_priority.py"
spec = importlib.util.spec_from_file_location("shipment_replay", script)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

def read(relative):
    return json.loads((example / relative).read_text(encoding="utf-8"))

def inputs():
    return (read("evidence/shipments.json"), read("artifacts/semantic-definitions.json"), read("artifacts/decision-service.json"), read("evidence/access-decision.json"))

snapshot, semantics, decision, access = inputs()
normal = module.replay(snapshot, semantics, decision, access, as_of="2026-08-25T09:00:00Z")
required_output = {"result", "semanticDefinition", "sourceEvidence", "freshness", "accessDecision"}
assert required_output <= normal.keys()
assert normal["freshness"]["status"] == "fresh"
assert normal["persistentActionExecuted"] is False

snapshot, semantics, decision, access = inputs()
snapshot["records"] = [
    {"shipmentId": "TIE-B", "overdueHours": 24, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
    {"shipmentId": "TIE-A", "overdueHours": 24, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
    {"shipmentId": "BOUNDARY-48", "overdueHours": 48, "serviceLevel": "standard", "temperatureControlled": False, "atRiskCustomerCommitment": False},
]
tied = module.replay(snapshot, semantics, decision, access, as_of="2026-08-25T09:00:00Z")
assert [item["shipmentId"] for item in tied["result"]["recommendations"]] == ["BOUNDARY-48", "TIE-A", "TIE-B"]

snapshot, semantics, decision, access = inputs()
snapshot["capturedAt"] = "2026-08-25T07:59:00Z"
assert module.replay(snapshot, semantics, decision, access, as_of="2026-08-25T09:00:00Z")["result"] == {"recommendations": [], "escalations": []}

snapshot, semantics, decision, access = inputs()
access["permissions"]["recommendation"] = "denied"
assert module.replay(snapshot, semantics, decision, access, as_of="2026-08-25T09:00:00Z")["result"] == {"recommendations": [], "escalations": []}

scenario = read("scenario.json")
approval = read("evidence/scenario-approval.json")
process = read("evidence/process-validation.json")
report = read("evidence/decision-test-report.json")
rehearsal_authorization = read("evidence/shadow-rehearsal-authorization.json")
rehearsal_result = read("evidence/shadow-rehearsal-result.json")
gate_review = (example / "expected/gate-review.md").read_text(encoding="utf-8")
assert scenario["id"] == approval["scenarioId"] and approval["scope"].startswith("synthetic")  # G1
assert semantics["status"] == "released" and {binding["input"] for binding in decision["inputBindings"]} == set(decision["requiredInputs"]) and process["scope"].startswith("synthetic")  # G2
assert normal["accessDecision"]["query"] == "allowed" and normal["accessDecision"]["recommendation"] == "allowed"  # G3
case_ids = {case["caseId"] for case in report["testCases"]}
assert report["status"] == "passed" and {"boundary-24-hours", "boundary-48-hours", "tie-breakers", "escalation-missing-overdue"} <= case_ids  # G4
assert access["permissions"]["controlledExecution"] == "denied" and normal["persistentActionExecuted"] is False  # G5 missing
assert rehearsal_authorization["decision"] == "authorized" and rehearsal_authorization["scope"]["kind"] == "synthetic-example-only"
assert rehearsal_authorization["scope"]["scenarioId"] == scenario["id"] and rehearsal_authorization["scope"]["accessDecisionId"] == access["decisionId"]
assert rehearsal_authorization["scope"]["semanticRegistryId"] == semantics["registryId"] and rehearsal_authorization["scope"]["semanticVersion"] == semantics["version"]
assert rehearsal_authorization["scope"]["sourceId"] == snapshot["sourceId"] and rehearsal_authorization["scope"]["sourceCapturedAt"] == snapshot["capturedAt"]
assert rehearsal_authorization["grant"]["persistence"].startswith("no human disposition")
assert rehearsal_authorization["grant"]["controlledExecution"] == "denied" and rehearsal_authorization["grant"]["externalSideEffects"] == "denied"
event_boundary = rehearsal_authorization["eventBoundary"]
assert event_boundary["authorizationMode"] == "documentary-event-scope; not a runtime token" and event_boundary["runtimeEnforcedSingleUse"] is False
assert event_boundary["newEventRequiresNewAuthorization"] is True and event_boundary["invalidatedOnBindingDrift"] is True
assert event_boundary["consumedByEvidenceId"] == rehearsal_result["evidenceId"] and event_boundary["eventId"] == rehearsal_result["eventId"]
assert rehearsal_authorization["replayPlan"]["workingDirectory"] == "example-root"
expected_rehearsal_command = [
    "python3", "scripts/replay_shipment_delay_priority.py",
    "--snapshot", "evidence/shipments.json",
    "--semantic-definitions", "artifacts/semantic-definitions.json",
    "--decision-service", "artifacts/decision-service.json",
    "--access-decision", "evidence/access-decision.json",
    "--as-of", "2026-08-25T09:00:00Z",
    "--disposition", "SHP-1001=needs-investigation",
    "--disposition", "SHP-1002=accepted",
    "--disposition", "SHP-1003=rejected",
]
assert rehearsal_authorization["replayPlan"]["command"] == expected_rehearsal_command
actual_digests = {relative: "sha256:" + hashlib.sha256((example / relative).read_bytes()).hexdigest() for relative in rehearsal_authorization["artifactDigests"]}
assert rehearsal_authorization["artifactDigests"] == actual_digests == rehearsal_result["artifactDigests"]
completed = subprocess.run([sys.executable, *expected_rehearsal_command[1:]], cwd=example, text=True, capture_output=True)
assert completed.returncode == 0, completed.stderr
shadow = json.loads(completed.stdout)
expected = read("expected/read-only-result.json")
normalized_shadow = dict(shadow)
normalized_shadow["sessionDispositions"] = expected["sessionDispositions"]
assert normalized_shadow == expected
observations = rehearsal_result["observations"]
assert rehearsal_result["authorizationId"] == rehearsal_authorization["authorizationId"] and rehearsal_result["status"] == "passed"
assert rehearsal_result["bindings"] == {key: rehearsal_authorization["scope"][key] for key in ("scenarioId", "semanticRegistryId", "semanticVersion", "sourceId", "sourceCapturedAt", "accessDecisionId")}
assert observations["readOnlyOutputContractComplete"] is True and required_output <= shadow.keys()
assert observations["recommendationCount"] == len(shadow["result"]["recommendations"])
assert observations["recommendationScoresInOrder"] == [item["priorityScore"] for item in shadow["result"]["recommendations"]]
assert observations["escalationCount"] == len(shadow["result"]["escalations"])
assert set(observations["seededDispositionCoverage"]) == {item["disposition"] for item in shadow["sessionDispositions"]["records"]}
assert observations["sessionDispositionPersistence"] == shadow["sessionDispositions"]["persistence"] == "none"
assert observations["persistentActionExecuted"] is shadow["persistentActionExecuted"] is False
assert observations["contractFailureCount"] == len(shadow["contractFailures"]) == 0
assert observations["preconditionFailureCount"] == len(shadow["preconditionFailures"]) == 0
assert rehearsal_result["evaluatedAsOf"] == "2026-08-25T09:00:00Z"
assert rehearsal_result["execution"] == {"interface": "scripts/replay_shipment_delay_priority.py", "planSource": "evidence/shadow-rehearsal-authorization.json#replayPlan", "workingDirectory": "example-root", "exitCode": 0, "deviations": []}
assert rehearsal_result["gateImpact"]["G5"] == "missing" and rehearsal_result["gateImpact"]["G6"] == "unverifiable"
for gate, conclusion in (("G1", "passed"), ("G2", "passed"), ("G3", "passed"), ("G4", "passed"), ("G5", "missing"), ("G6", "unverifiable")):
    assert f"| {gate} | {conclusion} |" in gate_review, f"{gate} must remain {conclusion} in the synthetic gate review"
PY

echo "shipment-delay-priority validation: passed"
