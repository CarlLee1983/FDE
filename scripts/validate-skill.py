#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/agent-delivery-loop.md",
    "references/capability-return-review.md",
    "references/collaborative-clarification.md",
    "references/packaged-sources.json",
    "references/solution-proposal.md",
    "references/source-map.md",
    "references/task-modes.md",
    "schemas/fde-scenario.schema.json",
    "scripts/validate-scenario.sh",
)
PACKAGED_SOURCES = {
    "canonical/CONTEXT.md": "CONTEXT.md",
    "canonical/adr/0001-operating-analysis-is-project-boundary.md": "docs/adr/0001-operating-analysis-is-project-boundary.md",
    "canonical/adr/0002-use-an-adaptive-analysis-core.md": "docs/adr/0002-use-an-adaptive-analysis-core.md",
    "canonical/adr/0003-separate-analysis-completion-from-assurance.md": "docs/adr/0003-separate-analysis-completion-from-assurance.md",
    "canonical/adr/0004-make-skill-behavior-canonical.md": "docs/adr/0004-make-skill-behavior-canonical.md",
    "canonical/adr/0005-recompute-only-on-dependency.md": "docs/adr/0005-recompute-only-on-dependency.md",
    "canonical/FDE-Capability-Enhancement-Plan.md": "FDE-Capability-Enhancement-Plan.md",
    "canonical/FDE-Scenario-to-Action-Method.md": "FDE-Scenario-to-Action-Method.md",
    "canonical/docs/fde-ontology/05-platform-capabilities-and-application-operations.md": "docs/fde-ontology/05-platform-capabilities-and-application-operations.md",
    "canonical/docs/fde-ontology/07-capability-map-and-implementation-strategy.md": "docs/fde-ontology/07-capability-map-and-implementation-strategy.md",
    "canonical/docs/fde-ontology/08-fde-capability-enhancement-focus.md": "docs/fde-ontology/08-fde-capability-enhancement-focus.md",
    "canonical/schemas/fde-scenario.example.json": "schemas/fde-scenario.example.json",
}
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def main() -> int:
    arguments = sys.argv[1:]
    if len(arguments) not in (1, 3) or (len(arguments) == 3 and arguments[1] != "--source-root"):
        print("usage: validate-skill.py <skill-directory> [--source-root <repository>]", file=sys.stderr)
        return 64

    skill_dir = Path(arguments[0]).resolve()
    source_root = Path(arguments[2]).resolve() if len(arguments) == 3 else None
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

    if source_root:
        canonical_schema = source_root / "schemas" / "fde-scenario.schema.json"
        packaged_schema = skill_dir / "schemas" / "fde-scenario.schema.json"
        if packaged_schema.is_file() and canonical_schema.is_file():
            if packaged_schema.read_bytes() != canonical_schema.read_bytes():
                errors.append("packaged scenario schema differs from canonical schema")

        manifest = skill_dir / "references" / "packaged-sources.json"
        if manifest.is_file():
            sources = json.loads(manifest.read_text(encoding="utf-8"))
            if sources != PACKAGED_SOURCES:
                errors.append("packaged source manifest is incomplete or unexpected")
            for packaged, canonical in PACKAGED_SOURCES.items():
                packaged_file = skill_dir / "references" / packaged
                canonical_file = source_root / canonical
                if (
                    not canonical_file.is_file()
                    or not packaged_file.is_file()
                    or packaged_file.read_bytes() != canonical_file.read_bytes()
                ):
                    errors.append(f"packaged reference differs: {packaged} <- {canonical}")

    references_dir = skill_dir / "references"
    for reference in [skill_dir / "SKILL.md", *references_dir.glob("*.md")]:
        for target in LINK.findall(reference.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (reference.parent / target).resolve()
            try:
                resolved.relative_to(skill_dir)
            except ValueError:
                errors.append(f"{reference.relative_to(skill_dir)} -> {target} escapes the Skill package")
                continue
            if not resolved.exists():
                errors.append(f"{reference.relative_to(skill_dir)} -> {target} is missing")

    if errors:
        print("Skill validation failed: " + ", ".join(errors), file=sys.stderr)
        return 1

    references = sum(1 for _ in (skill_dir / "references").glob("*.md"))
    scripts = sum(1 for _ in (skill_dir / "scripts").glob("*"))
    print(f"Skill validation passed: fde-project-work ({references} references, {scripts} script)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
