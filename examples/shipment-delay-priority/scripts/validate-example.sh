#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

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
import json
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
gate_review = (example / "expected/gate-review.md").read_text(encoding="utf-8")
assert scenario["id"] == approval["scenarioId"] and approval["scope"].startswith("synthetic")  # G1
assert semantics["status"] == "released" and {binding["input"] for binding in decision["inputBindings"]} == set(decision["requiredInputs"]) and process["scope"].startswith("synthetic")  # G2
assert normal["accessDecision"]["query"] == "allowed" and normal["accessDecision"]["recommendation"] == "allowed"  # G3
case_ids = {case["caseId"] for case in report["testCases"]}
assert report["status"] == "passed" and {"boundary-24-hours", "boundary-48-hours", "tie-breakers", "escalation-missing-overdue"} <= case_ids  # G4
assert access["permissions"]["controlledExecution"] == "denied" and normal["persistentActionExecuted"] is False  # G5 missing
for gate, conclusion in (("G1", "passed"), ("G2", "passed"), ("G3", "passed"), ("G4", "passed"), ("G5", "missing"), ("G6", "unverifiable")):
    assert f"| {gate} | {conclusion} |" in gate_review, f"{gate} must remain {conclusion} in the synthetic gate review"
PY

echo "shipment-delay-priority validation: passed"
