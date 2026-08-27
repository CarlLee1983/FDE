#!/usr/bin/env python3
"""Validate source integrity and cross-format consistency for this case."""

from __future__ import annotations

import html
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


EXAMPLE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_PATH = EXAMPLE_DIR / "artifacts" / "analysis-package.json"
SCENARIO_PATH = EXAMPLE_DIR / "scenario.json"
MARKDOWN_PATH = EXAMPLE_DIR / "artifacts" / "operating-solution-proposal.md"
HTML_PATH = EXAMPLE_DIR / "index.html"
PRESENTATION_HTML_PATH = EXAMPLE_DIR / "presentation.html"
DOCX_PATH = EXAMPLE_DIR / "artifacts" / "customer-refund-status-proposal.docx"
PPTX_PATH = EXAMPLE_DIR / "artifacts" / "customer-refund-status-decision.pptx"
VISUAL_QA_PATH = EXAMPLE_DIR / "evidence" / "visual-qa.json"
REPORT_PATH = EXAMPLE_DIR / "evidence" / "validation-report.json"


def extract_ooxml_text(path: Path, prefix: str, text_tag: str) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = sorted(name for name in archive.namelist() if name.startswith(prefix) and name.endswith(".xml"))
        for name in names:
            root = ElementTree.fromstring(archive.read(name))
            chunks.extend(node.text or "" for node in root.iter() if node.tag.endswith(text_tag))
    return " ".join(chunks)


def claim_fragments(display: str) -> list[str]:
    return [fragment.strip() for fragment in display.split("|")]


def audit_docx_layout(path: Path) -> tuple[bool, str]:
    """Check the fixed page and table geometry used by the proposal preset."""
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    attribute = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as archive:
        document = ElementTree.fromstring(archive.read("word/document.xml"))
        styles = ElementTree.fromstring(archive.read("word/styles.xml"))
        numbering = ElementTree.fromstring(archive.read("word/numbering.xml"))

    section = document.find(".//w:sectPr", namespace)
    page_size = section.find("w:pgSz", namespace) if section is not None else None
    margins = section.find("w:pgMar", namespace) if section is not None else None
    page_ok = (
        page_size is not None
        and page_size.get(attribute + "w") == "12240"
        and page_size.get(attribute + "h") == "15840"
        and margins is not None
        and all(margins.get(attribute + edge) == "1440" for edge in ("top", "right", "bottom", "left"))
    )

    style_ids = {style.get(attribute + "styleId") for style in styles.findall("w:style", namespace)}
    styles_ok = {"Normal", "Title", "Subtitle", "Heading1", "Heading2", "Heading3"}.issubset(style_ids)
    bullets_ok = numbering.find(".//w:numFmt[@w:val='bullet']", namespace) is not None

    table_errors: list[str] = []
    tables = document.findall(".//w:tbl", namespace)
    for index, table in enumerate(tables, 1):
        width = table.find("w:tblPr/w:tblW", namespace)
        indent = table.find("w:tblPr/w:tblInd", namespace)
        columns = table.findall("w:tblGrid/w:gridCol", namespace)
        grid_width = sum(int(column.get(attribute + "w", "0")) for column in columns)
        if width is None or width.get(attribute + "w") != "9360" or indent is None or indent.get(attribute + "w") != "120" or grid_width != 9360:
            table_errors.append(str(index))
    layout_ok = page_ok and styles_ok and bullets_ok and bool(tables) and not table_errors
    detail = (
        f"letter page and one-inch margins: {page_ok}; required styles: {styles_ok}; "
        f"real bullet numbering: {bullets_ok}; fixed-width tables: {len(tables) - len(table_errors)}/{len(tables)}"
    )
    return layout_ok, detail


def add_check(checks: list[dict], check_id: str, status: str, detail: str) -> None:
    checks.append({"id": check_id, "status": status, "detail": detail})


def main() -> int:
    data = json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    visual_qa = json.loads(VISUAL_QA_PATH.read_text(encoding="utf-8")) if VISUAL_QA_PATH.exists() else {}
    checks: list[dict] = []

    generated = subprocess.run(
        [sys.executable, str(EXAMPLE_DIR / "scripts" / "generate_views.py"), "--check"],
        cwd=EXAMPLE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    add_check(checks, "generated-views-current", "passed" if generated.returncode == 0 else "failed", (generated.stdout + generated.stderr).strip())

    required_ledger_statuses = {"evidenced", "proposed", "missing", "unverifiable"}
    ledger_statuses = {item["status"] for item in data["evidenceLedger"]}
    add_check(
        checks,
        "evidence-state-coverage",
        "passed" if ledger_statuses == required_ledger_statuses else "failed",
        f"ledger statuses: {sorted(ledger_statuses)}",
    )

    canonical_ok = (
        scenario["status"] == "proposed"
        and data["classification"]["evidenceState"] == "proposed"
        and data["operatingOutcome"]["baseline"]["display"] == "8 minutes"
        and data["operatingOutcome"]["target"]["display"] == "3 minutes"
        and data["aiFit"]["decision"] == "not needed"
        and data["authority"]["writeBack"]["permitted"] is False
        and len(data["semanticContract"]["supportedStates"]) == 3
    )
    add_check(checks, "canonical-contract", "passed" if canonical_ok else "failed", "scope, metrics, supported states, AI-fit, and authority checked")

    expected_claims = {
        "C1": data["classification"]["label"],
        "C2": data["scope"]["included"][0],
        "C3": f'{data["operatingOutcome"]["baseline"]["display"]} to {data["operatingOutcome"]["target"]["display"]}',
        "C4": " | ".join(item["normalizedState"] for item in data["semanticContract"]["supportedStates"]),
        "C5": data["aiFit"]["display"],
        "C6": data["authority"]["writeBack"]["display"],
        "C7": data["owners"][0]["role"],
        "C8": data["semanticContract"]["owner"],
    }
    claim_values = {item["id"]: item["display"] for item in data["consistencyClaims"]}
    claims_ok = claim_values == expected_claims
    add_check(
        checks,
        "consistency-claim-anchors",
        "passed" if claims_ok else "failed",
        "consistency claims match their canonical fields" if claims_ok else f"expected {expected_claims!r}; found {claim_values!r}",
    )

    texts: dict[str, str] = {
        "markdown": MARKDOWN_PATH.read_text(encoding="utf-8"),
        "html": html.unescape(HTML_PATH.read_text(encoding="utf-8")),
        "presentation_html": html.unescape(PRESENTATION_HTML_PATH.read_text(encoding="utf-8")),
    }
    presentation_source = PRESENTATION_HTML_PATH.read_text(encoding="utf-8")
    slide_count = presentation_source.count('class="slide') - presentation_source.count('class="slide-head')
    presentation_contract_ok = (
        slide_count == 10
        and "ArrowRight" in presentation_source
        and "requestFullscreen" in presentation_source
        and "@media print" in presentation_source
        and "artifacts/analysis-package.json" in presentation_source
    )
    add_check(
        checks,
        "presentation-html-contract",
        "passed" if presentation_contract_ok else "failed",
        f"slides: {slide_count}; keyboard, fullscreen, print, and canonical-source controls checked",
    )
    if DOCX_PATH.exists():
        try:
            texts["docx"] = extract_ooxml_text(DOCX_PATH, "word/", "}t")
            add_check(checks, "docx-structure", "passed", "OOXML package opened and Word text extracted")
            layout_ok, layout_detail = audit_docx_layout(DOCX_PATH)
            add_check(checks, "docx-layout-contract", "passed" if layout_ok else "failed", layout_detail)
        except (zipfile.BadZipFile, ElementTree.ParseError) as error:
            add_check(checks, "docx-structure", "failed", str(error))
    else:
        add_check(checks, "docx-structure", "failed", "DOCX output missing")

    if PPTX_PATH.exists():
        try:
            slide_text = extract_ooxml_text(PPTX_PATH, "ppt/slides/", "}t")
            notes_text = extract_ooxml_text(PPTX_PATH, "ppt/notesSlides/", "}t")
            texts["pptx"] = slide_text + " " + notes_text
            add_check(checks, "pptx-structure", "passed", "OOXML package opened; slide and notes text extracted")
        except (zipfile.BadZipFile, ElementTree.ParseError) as error:
            add_check(checks, "pptx-structure", "failed", str(error))
    else:
        add_check(checks, "pptx-optional", "passed", "PPTX output not produced; presentation.html is the required decision-deck view")

    format_map = {"docx": "docx", "html": "html", "presentationHtml": "presentation_html"}
    for claim in data["consistencyClaims"]:
        for required_format in claim["requiredIn"]:
            text_key = format_map[required_format]
            if text_key not in texts:
                add_check(checks, f'{claim["id"]}-{required_format}', "blocked", f'{required_format} output unavailable')
                continue
            missing = [fragment for fragment in claim_fragments(claim["display"]) if fragment not in texts[text_key]]
            add_check(
                checks,
                f'{claim["id"]}-{required_format}',
                "passed" if not missing else "failed",
                f'{claim["label"]}: {"all fragments present" if not missing else "missing " + repr(missing)}',
            )

    if "pptx" in texts:
        notes_ok = "[Sources]" in texts["pptx"] and "artifacts/analysis-package.json" in texts["pptx"]
        add_check(checks, "pptx-source-notes", "passed" if notes_ok else "failed", "speaker-note source blocks checked")

    acceptable_visual_statuses = {
        "docx": {"passed", "supplemental-pass"},
        "html": {"passed"},
        "presentationHtml": {"passed"},
    }
    for artifact, acceptable in acceptable_visual_statuses.items():
        record = visual_qa.get(artifact, {})
        status = record.get("status", "missing")
        check_status = "passed" if status in acceptable else "failed" if status == "failed" else "blocked"
        add_check(
            checks,
            f"visual-qa-{artifact}",
            check_status,
            f'{status}: {record.get("result", "no visual QA result recorded")}',
        )

    statuses = {check["status"] for check in checks}
    overall = "failed" if "failed" in statuses else "blocked" if "blocked" in statuses else "passed"
    report = {
        "caseId": data["caseId"],
        "overall": overall,
        "evidenceBoundary": data["classification"],
        "canonicalSource": "artifacts/analysis-package.json",
        "checks": checks,
        "visualQa": visual_qa,
        "restrictions": [
            "Schema and cross-format checks do not establish enterprise acceptance or authority.",
            *[
                f'{artifact.upper()} visual QA remains {visual_qa.get(artifact, {}).get("status", "missing")}: '
                f'{visual_qa.get(artifact, {}).get("restriction", "no restriction recorded")}'
                for artifact, acceptable in acceptable_visual_statuses.items()
                if visual_qa.get(artifact, {}).get("status", "missing") not in acceptable
            ],
            "PPTX is an optional derivative; presentation.html is the required decision presentation.",
            "No authority increase follows from presentation generation or visual quality.",
        ],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"delivery-kit validation: {overall}")
    for check in checks:
        if check["status"] != "passed":
            print(f'- {check["status"]}: {check["id"]} — {check["detail"]}')
    return 0 if overall == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
