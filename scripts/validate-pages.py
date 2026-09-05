#!/usr/bin/env python3
from __future__ import annotations

import sys
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link" and values.get("href"):
            self.resources.append(values["href"] or "")
        if tag in {"img", "script", "source", "video", "audio", "iframe"} and values.get("src"):
            self.resources.append(values["src"] or "")
        if tag == "video" and values.get("poster"):
            self.resources.append(values["poster"] or "")
        if tag == "object" and values.get("data"):
            self.resources.append(values["data"] or "")
        if values.get("srcset"):
            self.resources.extend(
                candidate.strip().split(maxsplit=1)[0]
                for candidate in (values["srcset"] or "").split(",")
                if candidate.strip()
            )


def parse(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def within(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def local_target(root: Path, source: Path, href: str) -> tuple[Path | None, str]:
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith(("mailto:", "data:")):
        return None, parts.fragment
    target = ((source.parent / unquote(parts.path)).resolve() if parts.path else source.resolve())
    if not within(root, target):
        raise ValueError(f"target escapes artifact root: {href}")
    return target, parts.fragment


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate-pages.py <artifact-directory>", file=sys.stderr)
        return 64

    root = Path(sys.argv[1]).resolve()
    required = [
        root / "index.html",
        root / "tokens.css",
        root / ".nojekyll",
        root / "examples" / "README.zh-TW.md",
        root / "examples" / "third-party-api-change-monitoring" / "index.html",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        print("missing required Pages files: " + ", ".join(missing), file=sys.stderr)
        return 1

    errors: list[str] = []
    html_files = sorted(root.rglob("*.html"))
    parsed = {path: parse(path) for path in html_files}
    for source, document in parsed.items():
        for href in document.links + document.resources:
            try:
                target, fragment = local_target(root, source, href)
            except ValueError as error:
                errors.append(f"{source.relative_to(root)} -> {error}")
                continue
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{source.relative_to(root)} -> missing {href}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_document = parsed.get(target) or parse(target)
                if fragment not in target_document.ids:
                    errors.append(f"{source.relative_to(root)} -> missing fragment {href}")

    markdown_link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for source in sorted(root.rglob("*.md")):
        if source.is_relative_to(root / ".agents" / "skills" / "fde-project-work"):
            # The portable Skill has its own validator: snapshots retain their
            # canonical repository links and are not Pages documentation.
            continue
        for href in markdown_link.findall(source.read_text(encoding="utf-8")):
            href = href.strip().split(maxsplit=1)[0].strip("<>")
            try:
                target, _ = local_target(root, source, href)
            except ValueError as error:
                errors.append(f"{source.relative_to(root)} -> {error}")
                continue
            if target is None or not urlsplit(href).path:
                continue
            if not target.exists():
                errors.append(f"{source.relative_to(root)} -> missing {href}")

    css_url = re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)")
    css_import = re.compile(r"@import\s+(['\"])([^'\"]+)\1")
    for source in sorted(root.rglob("*.css")):
        content = source.read_text(encoding="utf-8")
        references = [href for _, href in css_url.findall(content)]
        references.extend(href for _, href in css_import.findall(content))
        for href in references:
            try:
                target, _ = local_target(root, source, href.strip())
            except ValueError as error:
                errors.append(f"{source.relative_to(root)} -> {error}")
                continue
            if target is not None and not target.exists():
                errors.append(f"{source.relative_to(root)} -> missing {href}")

    if errors:
        print("Pages link validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    markdown_count = sum(1 for _ in root.rglob("*.md"))
    print(f"Pages validation passed: {len(html_files)} HTML and {markdown_count} Markdown files, all local links resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
