#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 --target <repository> --agent <codex|claude|both>" >&2
}

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
source_skill="$repo_dir/.agents/skills/fde-project-work"
target=""
agent=""

for tool in git find mktemp cp mv; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "required tool not found: $tool" >&2
    exit 69
  fi
done

while (($#)); do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { usage; exit 64; }
      target="$2"
      shift 2
      ;;
    --agent)
      [[ $# -ge 2 ]] || { usage; exit 64; }
      agent="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown option: $1" >&2
      usage
      exit 64
      ;;
  esac
done

[[ -n "$target" && -n "$agent" ]] || { usage; exit 64; }
case "$agent" in
  codex|claude|both) ;;
  *)
    echo "agent must be codex, claude, or both: $agent" >&2
    exit 64
    ;;
esac

if [[ ! -d "$target" ]]; then
  echo "target must be an existing repository directory: $target" >&2
  exit 66
fi
target="$(cd "$target" && pwd -P)"
user_home="$(cd "${HOME:?HOME is required}" && pwd -P)"

if [[ "$target" == "/" || "$target" == "$user_home" || "$target" == "$repo_dir" ]]; then
  echo "refusing unsafe target: $target" >&2
  exit 64
fi

git_root="$(git -C "$target" rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$git_root" ]]; then
  echo "target must be a Git repository: $target" >&2
  exit 65
fi
git_root="$(cd "$git_root" && pwd -P)"
if [[ "$target" != "$git_root" ]]; then
  echo "target must be the repository root: $git_root" >&2
  exit 64
fi

if [[ -n "$(find "$source_skill" -type l -print -quit)" ]]; then
  echo "source Skill must not contain symlinks" >&2
  exit 65
fi

destinations=()
[[ "$agent" == "codex" || "$agent" == "both" ]] && destinations+=("$target/.agents/skills/fde-project-work")
[[ "$agent" == "claude" || "$agent" == "both" ]] && destinations+=("$target/.claude/skills/fde-project-work")

for destination in "${destinations[@]}"; do
  parent="$(dirname "$destination")"
  ancestor="$(dirname "$parent")"
  if [[ -L "$ancestor" || -L "$parent" || -e "$destination" || -L "$destination" ]]; then
    if [[ -e "$destination" || -L "$destination" ]]; then
      echo "Skill already exists: $destination" >&2
      echo "review and remove only that Skill directory before reinstalling an update" >&2
    else
      echo "refusing symlinked Skill destination: $destination" >&2
    fi
    exit 73
  fi
done

staging=()
cleanup() {
  for path in "${staging[@]}"; do
    [[ -d "$path" ]] && rm -rf -- "$path"
  done
  :
}
trap cleanup EXIT

for destination in "${destinations[@]}"; do
  parent="$(dirname "$destination")"
  mkdir -p "$parent"
  canonical_parent="$(cd "$parent" && pwd -P)"
  if [[ "$canonical_parent" != "$target/"* ]]; then
    echo "refusing Skill destination outside target repository: $destination" >&2
    exit 64
  fi
  stage="$(mktemp -d "$parent/.fde-project-work.XXXXXX")"
  staging+=("$stage")
  cp -R "$source_skill/." "$stage/"
done

for index in "${!destinations[@]}"; do
  mv "${staging[$index]}" "${destinations[$index]}"
  staging[$index]=""
  echo "Installed fde-project-work at ${destinations[$index]}"
done

echo "Next: Use \$fde-project-work to analyze an operating problem."
