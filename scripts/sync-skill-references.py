#!/usr/bin/env python3
"""Synchronize canonical FDE references bundled with the portable Skill."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / ".agents" / "skills" / "fde-project-work"
MANIFEST = SKILL / "references" / "packaged-sources.json"


def main() -> int:
    check = sys.argv[1:] == ["--check"]
    if not check and sys.argv[1:]:
        print("usage: sync-skill-references.py [--check]", file=sys.stderr)
        return 64
    sources: dict[str, str] = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    for packaged, canonical in sources.items():
        destination = SKILL / "references" / packaged
        source = REPO / canonical
        if check:
            if not destination.is_file() or destination.read_bytes() != source.read_bytes():
                errors.append(f"{packaged} differs from {canonical}")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    if errors:
        print("Packaged Skill references are out of sync: " + "; ".join(errors), file=sys.stderr)
        return 1
    print("Packaged Skill references are synchronized" if check else "Packaged Skill references synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
