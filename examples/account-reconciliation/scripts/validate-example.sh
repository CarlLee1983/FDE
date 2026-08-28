#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"
actual="$(mktemp)"
golden="$(mktemp)"
trap 'rm -f "$actual" "$golden"' EXIT

"$repo_dir/.agents/skills/fde-project-work/scripts/validate-scenario.sh" "$example_dir/scenario.json"
python3 -m unittest discover -s "$example_dir/tests" -p 'test_*.py'
python3 -c 'import json, sys; print(json.dumps(json.load(open(sys.argv[1])), indent=2, sort_keys=True))' "$example_dir/expected/read-only-result.json" > "$golden"
python3 "$example_dir/scripts/replay_account_reconciliation.py" > "$actual"
diff -u "$golden" "$actual"
echo "account-reconciliation validation: passed"
