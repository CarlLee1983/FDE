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
schema_path="$skill_dir/schemas/fde-scenario.schema.json"

if ! command -v uv >/dev/null 2>&1; then
  echo "required tool not found: uv" >&2
  exit 69
fi

uv tool run --from 'check-jsonschema==0.38.0' check-jsonschema --check-metaschema "$schema_path"
uv tool run --from 'check-jsonschema==0.38.0' check-jsonschema --schemafile "$schema_path" "$scenario_path"
