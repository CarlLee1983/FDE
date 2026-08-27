#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <scenario.json>" >&2
  exit 64
fi

scenario_path="$1"
if [[ ! -f "$scenario_path" ]]; then
  echo "scenario not found: $scenario_path" >&2
  exit 66
fi

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$skill_dir/../../.." && pwd)"
schema_path="$repo_dir/schemas/fde-scenario.schema.json"

uvx check-jsonschema --check-metaschema "$schema_path"
uvx check-jsonschema --schemafile "$schema_path" "$scenario_path"
