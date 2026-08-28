#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

"$repo_dir/.agents/skills/fde-project-work/scripts/validate-scenario.sh" "$example_dir/scenario.json"

echo "third-party-api-change-monitoring validation: passed"
