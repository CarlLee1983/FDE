#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

"$repo_dir/.agents/skills/fde-project-work/scripts/validate-scenario.sh" "$example_dir/scenario.json"
python3 "$example_dir/scripts/generate_views.py" --check
python3 "$example_dir/scripts/validate_delivery_kit.py"
