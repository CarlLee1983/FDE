#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/agent-delivery-loop.md",
    "references/capability-return-review.md",
    "references/collaborative-clarification.md",
    "references/solution-proposal.md",
    "references/source-map.md",
    "references/task-modes.md",
    "schemas/fde-scenario.schema.json",
    "scripts/validate-scenario.sh",
)


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: validate-skill.py <skill-directory> [canonical-schema]", file=sys.stderr)
        return 64

    skill_dir = Path(sys.argv[1])
    errors = [
        path
        for path in REQUIRED_FILES
        if not (skill_dir / path).is_file() or (skill_dir / path).is_symlink()
    ]
    skill_file = skill_dir / "SKILL.md"
    if skill_file.is_file():
        lines = skill_file.read_text(encoding="utf-8").splitlines()
        try:
            closing = lines.index("---", 1) if lines and lines[0] == "---" else -1
        except ValueError:
            closing = -1
        frontmatter = {}
        if closing > 0:
            frontmatter = {
                key.strip(): value.strip()
                for key, value in (line.split(":", 1) for line in lines[1:closing] if ":" in line)
            }
        if frontmatter.get("name", "").strip() != "fde-project-work":
            errors.append("SKILL.md frontmatter name")
        if not frontmatter.get("description", "").strip():
            errors.append("SKILL.md frontmatter description")

    if len(sys.argv) == 3:
        canonical_schema = Path(sys.argv[2])
        packaged_schema = skill_dir / "schemas" / "fde-scenario.schema.json"
        if packaged_schema.is_file() and canonical_schema.is_file():
            if packaged_schema.read_bytes() != canonical_schema.read_bytes():
                errors.append("packaged scenario schema differs from canonical schema")

    if errors:
        print("Skill validation failed: " + ", ".join(errors), file=sys.stderr)
        return 1

    references = sum(1 for _ in (skill_dir / "references").glob("*.md"))
    scripts = sum(1 for _ in (skill_dir / "scripts").glob("*"))
    print(f"Skill validation passed: fde-project-work ({references} references, {scripts} script)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
