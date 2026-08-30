#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
mode="${1:-verify}"
uv_bin="${UV:-uv}"

case "$mode" in
  test|scenarios|pages|verify) ;;
  *)
    echo "usage: $0 [test|scenarios|pages]" >&2
    exit 64
    ;;
esac

for tool in git find mktemp tar "$uv_bin"; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "required tool not found: $tool" >&2
    [[ "$tool" == "$uv_bin" ]] && echo "install uv from https://docs.astral.sh/uv/ and try again" >&2
    exit 69
  fi
done

temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/fde-verify.XXXXXX")"
trap 'rm -rf -- "$temp_dir"' EXIT
mkdir "$temp_dir/tmp"
export TMPDIR="$temp_dir/tmp"
export UV_PROJECT_ENVIRONMENT="$temp_dir/venv"
unset VIRTUAL_ENV

test_count=""
scenario_count=""
pages_result=""
skill_result=""

run_tests() {
  local root_report="$temp_dir/root-tests.xml"
  local example_report="$temp_dir/example-tests.xml"
  local reports=("$root_report")
  local example_tests=()

  "$uv_bin" run --frozen pytest -q --junitxml="$root_report" "$repo_dir/tests"

  while IFS= read -r -d '' test_file; do
    example_tests+=("$test_file")
  done < <(find "$repo_dir/examples" -type f -path '*/tests/*' -name 'test_*.py' -print0)

  if ((${#example_tests[@]})); then
    "$uv_bin" run --frozen pytest -q --junitxml="$example_report" "${example_tests[@]}"
    reports+=("$example_report")
  fi

  test_count="$("$uv_bin" run --frozen python - "${reports[@]}" <<'PY'
import sys
import xml.etree.ElementTree as ET

passed = 0
for report in sys.argv[1:]:
    for case in ET.parse(report).iter("testcase"):
        if not any(case.find(result) is not None for result in ("failure", "error", "skipped")):
            passed += 1
print(passed)
PY
)"
  echo "Tests passed: $test_count"
}

run_scenarios() {
  local schema="$repo_dir/schemas/fde-scenario.schema.json"
  local scenarios=()
  local scenario_path

  while IFS= read -r -d '' scenario; do
    scenario_path="$repo_dir/$scenario"
    if [[ ! -f "$scenario_path" || -L "$scenario_path" ]]; then
      echo "tracked scenario must be a regular non-symlink file: $scenario" >&2
      return 1
    fi
    scenarios+=("$scenario_path")
  done < <(git -C "$repo_dir" ls-files -z -- 'examples/**/scenario.json')

  if ((${#scenarios[@]})); then
    "$uv_bin" run --frozen check-jsonschema --schemafile "$schema" "${scenarios[@]}"
  fi
  "$uv_bin" run --frozen check-jsonschema --check-metaschema "$schema"
  scenario_count="${#scenarios[@]}"
  echo "Scenarios passed: $scenario_count tracked records; schema metaschema passed"
}

run_pages() {
  local artifact="$temp_dir/pages"
  "$repo_dir/scripts/build-pages.sh" "$artifact"
  pages_result="$("$uv_bin" run --frozen python "$repo_dir/scripts/validate-pages.py" "$artifact")"
  echo "$pages_result"
}

run_skill() {
  skill_result="$("$uv_bin" run --frozen python "$repo_dir/scripts/validate-skill.py" "$repo_dir/.agents/skills/fde-project-work" "$repo_dir/schemas/fde-scenario.schema.json")"
  echo "$skill_result"
}

case "$mode" in
  test)
    run_tests
    ;;
  scenarios)
    run_scenarios
    ;;
  pages)
    run_pages
    ;;
  verify)
    run_tests
    run_scenarios
    run_pages
    run_skill
    echo "Verification passed: $test_count tests; $scenario_count tracked scenarios; Pages and Skill valid"
    ;;
esac
