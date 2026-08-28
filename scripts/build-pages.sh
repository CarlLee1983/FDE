#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <output-directory>" >&2
  exit 64
fi

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
output_dir="$1"

if [[ "$output_dir" == -* ]]; then
  echo "output directory must not start with '-': $output_dir" >&2
  exit 64
fi

if [[ -L "$output_dir" ]]; then
  echo "output directory must not be a symlink: $output_dir" >&2
  exit 65
fi

if [[ -e "$output_dir" && ! -d "$output_dir" ]]; then
  echo "output path must be a directory: $output_dir" >&2
  exit 65
fi

if [[ -d "$output_dir" ]] && [[ -n "$(find "$output_dir" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
  echo "output directory must be absent or empty: $output_dir" >&2
  exit 73
fi

mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd -P)"
if [[ "$output_dir" == "/" || "$output_dir" == "$repo_dir" || "$output_dir" == "$repo_dir/.git" || "$output_dir" == "$repo_dir/.git/"* ]]; then
  echo "refusing unsafe output directory: $output_dir" >&2
  exit 64
fi

required_sources=(
  "site/index.html"
  "site/tokens.css"
  "examples/README.zh-TW.md"
)
for relative_path in "${required_sources[@]}"; do
  source_path="$repo_dir/$relative_path"
  if [[ ! -f "$source_path" || -L "$source_path" ]]; then
    echo "required publish source must be a regular non-symlink file: $relative_path" >&2
    exit 65
  fi
  if ! git -C "$repo_dir" ls-files --error-unmatch -- "$relative_path" >/dev/null 2>&1; then
    echo "required publish source must be tracked: $relative_path" >&2
    exit 65
  fi
done

cp "$repo_dir/site/index.html" "$output_dir/index.html"
cp "$repo_dir/site/tokens.css" "$output_dir/tokens.css"

file_list="$(mktemp)"
trap 'rm -f "$file_list"' EXIT
git -C "$repo_dir" ls-files --cached -- \
  '*.md' \
  'examples/**' \
  'schemas/**' \
  'docs/**' \
  'site/zh-TW/**' \
  '.agents/skills/fde-project-work/**' > "$file_list"

while IFS= read -r relative_path; do
  if [[ "$relative_path" == -* || "$relative_path" == *$'\n'* || -L "$repo_dir/$relative_path" ]]; then
    echo "refusing unsafe publish path: $relative_path" >&2
    exit 65
  fi
done < "$file_list"

tar -C "$repo_dir" -cf - -T "$file_list" | tar -C "$output_dir" -xf -
touch "$output_dir/.nojekyll"

echo "GitHub Pages artifact built at $output_dir"
