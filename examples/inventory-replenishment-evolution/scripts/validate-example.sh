#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

"$repo_dir/.agents/skills/fde-project-work/scripts/validate-scenario.sh" "$example_dir/scenario.json"
python3 -m unittest discover -s "$example_dir/tests" -p 'test_*.py'

actual_output="$(mktemp)"
trap 'rm -f "$actual_output"' EXIT
python3 "$example_dir/scripts/recommend_replenishment.py" "$example_dir/fixtures/replenishment-snapshot.json" --output "$actual_output"
diff -u "$example_dir/expected/replenishment-result.json" "$actual_output"

python3 - "$example_dir/scripts/recommend_replenishment.py" "$example_dir/fixtures/stale-replenishment-snapshot.json" <<'PY'
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("recommend_replenishment", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
snapshot = json.load(open(sys.argv[2], encoding="utf-8"))
result = module.recommend(snapshot)
assert result["result"]["status"] == "abstained"
assert result["freshness"]["status"] == "unacceptable"
assert result["writeBack"] == {"permitted": False, "attempted": False, "reason": "read-only-synthetic-local-tool"}
PY

echo "inventory-replenishment-evolution validation: passed"
