#!/usr/bin/env python3
"""Generate case-owned proposal views from the canonical analysis package.

This is deliberately specific to the synthetic customer-refund delivery kit. It
is not a generic FDE renderer and does not promote refund behaviour into core.
"""

from __future__ import annotations

import argparse
import html
import json
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


EXAMPLE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_PATH = EXAMPLE_DIR / "artifacts" / "analysis-package.json"
MARKDOWN_PATH = EXAMPLE_DIR / "artifacts" / "operating-solution-proposal.md"
HTML_PATH = EXAMPLE_DIR / "index.html"
PRESENTATION_HTML_PATH = EXAMPLE_DIR / "presentation.html"
DOCX_PATH = EXAMPLE_DIR / "artifacts" / "customer-refund-status-proposal.docx"


def load_analysis() -> dict:
    with ANALYSIS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    separator = ["---"] * len(headers)
    rendered = ["| " + " | ".join(headers) + " |", "| " + " | ".join(separator) + " |"]
    rendered.extend("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(rendered)


def build_markdown(data: dict) -> str:
    outcome = data["operatingOutcome"]
    current = data["currentProcess"]
    target = data["targetProcess"]
    evidence_rows = [
        [item["claimId"], item["statement"], f'`{item["status"]}`', item["source"], item["restriction"]]
        for item in data["evidenceLedger"]
    ]
    validation_rows = [
        [item["id"], item["criterion"], item["threshold"], item["failureEffect"]]
        for item in data["validation"]["thresholds"]
    ]
    state_rows = [
        [item["normalizedState"], item["meaning"], item["route"]]
        for item in data["semanticContract"]["supportedStates"]
    ]
    intervention_rows = [
        [item["need"], item["selection"], item["owner"], item["reason"]]
        for item in data["interventions"]
    ]
    seam_rows = [
        [item["seam"], f'`{item["status"]}`', item["restriction"]]
        for item in data["firstSlice"]["capabilitySeams"]
    ]

    sections = [
        f"# Proposed operating solution: {data['title']}",
        f"> **{data['classification']['label']}.** {data['classification']['statement']}",
        "## Decision requested",
        data["communication"]["decision"],
        f"**Recommendation:** {data['communication']['centralTakeaway']}",
        "## Operating outcome and scope",
        (
            f"For the **{outcome['user']}** at **{outcome['processNode']}**, the proposed change is to "
            f"{outcome['decisionOrAction'].lower()} The synthetic handling-time hypothesis is "
            f"**{outcome['baseline']['display']} to {outcome['target']['display']}**; "
            f"**{outcome['qualityGuardrail']['display'].lower()}**."
        ),
        "### Included",
        bullet_lines(data["scope"]["included"]),
        "### Excluded",
        bullet_lines(data["scope"]["excluded"]),
        "## Current-process diagnosis",
        "The proposed current normal flow is:",
        "```text\n" + " → ".join(current["normalFlow"]) + "\n```",
        "The proposed exception path is:",
        "```text\n" + " → ".join(current["exceptionFlow"]) + "\n```",
        markdown_table(
            ["Diagnosis hypothesis", "Operational effect", "Evidence status"],
            [[item["issue"], item["effect"], f'`{item["evidenceState"]}`'] for item in data["diagnosis"]],
        ),
        "These are synthetic hypotheses to confirm or correct with the process owner and affected users. They are not findings from observed enterprise work.",
        "## Process redesign before technology",
        "\n".join(f"{index}. **{item['action']}.** {item['change']}" for index, item in enumerate(data["processRedesign"], 1)),
        "## Technology-neutral target flow",
        "```text\n" + "\n  → ".join(f"{step['name']} — {step['description']}" for step in target["steps"]) + "\n```",
        f"**Normal outcome:** {target['normalOutcome']}",
        f"**Exception outcome:** {target['exceptionOutcome']}",
        f"**Human override:** {target['humanOverride']}",
        "## Process-readiness decision",
        (
            "The as-is path, target flow, handoffs, exception ownership, baseline, and semantic contract have not been accepted by accountable target-enterprise participants. "
            "The process therefore remains `proposed`. This package supports a decision about preparing a shadow replay; it does not authorize implementation or pilot use."
        ),
        "## Intervention selection",
        markdown_table(["Retained need", "Selected intervention", "Responsibility", "Why sufficient"], intervention_rows),
        "## AI-fit decision",
        f"**{data['aiFit']['display']}.** {data['aiFit']['rationale']}",
        data["aiFit"]["futureBoundary"],
        "## Semantic and exception contract",
        f"Proposed semantic version: `{data['semanticContract']['version']}`. Proposed owner: **{data['semanticContract']['owner']}**.",
        markdown_table(["Normalized state", "Meaning", "Route"], state_rows),
        "Every other or unsafe case abstains and escalates:",
        bullet_lines(data["semanticContract"]["abstentionCases"]),
        "## First buildable vertical slice",
        f"**{data['firstSlice']['name']}.** {data['firstSlice']['userVisibleOutcome']}",
        "Every returned result must expose:",
        bullet_lines(data["firstSlice"]["requiredResultFields"]),
        "Capability and integration seams remain case-owned and proposed:",
        markdown_table(["Case seam", "Status", "Restriction"], seam_rows),
        "Explicitly deferred:",
        bullet_lines(data["firstSlice"]["deferred"]),
        "## Authority and controls",
        f"**Proposed application form:** {data['authority']['proposedApplicationForm']}.",
        f"**Authority boundary:** {data['authority']['writeBack']['display']}; {data['authority']['customerResponse'].lower()}.",
        f"**Enterprise access decision:** `{data['authority']['accessDecision']}`. {data['authority']['restriction']}",
        "## Validation, rollout, and rollback",
        f"Proposed method: **{data['validation']['method']}**.",
        "Entry criteria:",
        bullet_lines(data["validation"]["entryCriteria"]),
        markdown_table(["ID", "Criterion", "Proposed threshold", "Failure effect"], validation_rows),
        f"**Rollback:** {data['validation']['rollback']}",
        "## Evidence ledger",
        markdown_table(["ID", "Statement", "Status", "Source", "Delivery restriction"], evidence_rows),
        "## Next accountable action",
        data["nextAccountableAction"]["action"],
        f"**Owner roles:** {' and '.join(data['nextAccountableAction']['owners'])}.",
        "Required inputs:",
        bullet_lines(data["nextAccountableAction"]["requiredInputs"]),
        f"**Observable completion:** {data['nextAccountableAction']['completionCriterion']}",
        "## Cross-format consistency anchors",
        "These anchors are generated from the canonical package and checked deterministically across the document, HTML, and decision deck:",
        bullet_lines([f"{claim['id']} — {claim['label']}: {claim['display']}" for claim in data["consistencyClaims"]]),
    ]
    return "\n\n".join(sections) + "\n"


def status_class(status: str) -> str:
    return status if status in {"evidenced", "proposed", "missing", "unverifiable"} else "missing"


def badge(status: str) -> str:
    safe = html.escape(status)
    return f'<span class="badge {status_class(status)}">{safe}</span>'


def html_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def html_table(headers: list[str], rows: list[list[str]], statuses: list[str] | None = None) -> str:
    head = "".join(f"<th scope=\"col\">{html.escape(cell)}</th>" for cell in headers)
    body_rows = []
    for index, row in enumerate(rows):
        cells = []
        for cell_index, cell in enumerate(row):
            if statuses and cell_index == len(row) - 1:
                cells.append(f"<td>{badge(statuses[index])}</td>")
            else:
                cells.append(f"<td>{html.escape(str(cell))}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def build_html(data: dict) -> str:
    outcome = data["operatingOutcome"]
    current = data["currentProcess"]
    target = data["targetProcess"]
    state_rows = [[s["normalizedState"], s["meaning"], s["route"]] for s in data["semanticContract"]["supportedStates"]]
    validation_rows = [[v["id"], v["criterion"], v["threshold"], v["failureEffect"]] for v in data["validation"]["thresholds"]]
    evidence_rows = [[e["claimId"], e["statement"], e["source"], e["restriction"], e["status"]] for e in data["evidenceLedger"]]
    evidence_statuses = [e["status"] for e in data["evidenceLedger"]]
    consistency = "".join(
        f'<li data-claim-id="{html.escape(c["id"])}"><strong>{html.escape(c["label"])}</strong><span>{html.escape(c["display"])}</span></li>'
        for c in data["consistencyClaims"]
    )
    current_steps = "".join(f'<li><span>{i:02}</span>{html.escape(step)}</li>' for i, step in enumerate(current["normalFlow"], 1))
    target_steps = "".join(
        f'<li><div><span>{i:02}</span><strong>{html.escape(step["name"])}</strong></div><p>{html.escape(step["description"])}</p><small>{html.escape(step["owner"])}</small></li>'
        for i, step in enumerate(target["steps"], 1)
    )
    diagnosis_cards = "".join(
        f'<article class="diagnosis-card"><div>{badge(item["evidenceState"])}</div><h3>{html.escape(item["issue"])}</h3><p>{html.escape(item["effect"])}</p></article>'
        for item in data["diagnosis"]
    )
    redesign = "".join(
        f'<li><span>{i}</span><div><strong>{html.escape(item["action"])}</strong><p>{html.escape(item["change"])}</p></div></li>'
        for i, item in enumerate(data["processRedesign"], 1)
    )
    owners = "".join(
        f'<article><h3>{html.escape(owner["role"])}</h3>{badge(owner["evidenceState"])}{html_list(owner["responsibilities"])}<p class="muted">Enterprise contact: {html.escape(owner["enterpriseContact"])}</p></article>'
        for owner in data["owners"]
    )
    interventions = "".join(
        f'<article><p class="kicker">{html.escape(item["need"])}</p><h3>{html.escape(item["selection"])}</h3><p>{html.escape(item["reason"])}</p><small>{html.escape(item["owner"])}</small></article>'
        for item in data["interventions"]
    )
    thresholds = html_table(["ID", "Criterion", "Proposed threshold", "Failure effect"], validation_rows)
    states = html_table(["Supported normalized state", "Meaning", "Route"], state_rows)
    ledger = html_table(["ID", "Statement", "Source", "Restriction", "Status"], evidence_rows, evidence_statuses)
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(data["classification"]["label"])} FDE operating solution: {html.escape(data["title"])}.">
  <title>{html.escape(data["title"])} — FDE proposal</title>
  <style>
    :root {{ color-scheme: light; --page:#f3f5f8; --surface:#fff; --ink:#132238; --muted:#5f6e80; --line:#d9e0e8; --navy:#102a43; --blue:#0b7285; --blue-soft:#e7f5f7; --green:#087f5b; --green-soft:#e7f7f0; --amber:#9a5b00; --amber-soft:#fff4d6; --red:#b4233d; --red-soft:#ffedf1; --purple:#6741a7; --purple-soft:#f0ebfa; --shadow:0 18px 48px rgba(27,43,65,.09); --radius:20px; --sans:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; }}
    html[data-theme="dark"] {{ color-scheme:dark; --page:#08121e; --surface:#0e1d2d; --ink:#eff5fb; --muted:#a8b6c5; --line:#293c51; --navy:#eff5fb; --blue:#62d3e6; --blue-soft:#113846; --green:#66ddb2; --green-soft:#10392f; --amber:#ffd078; --amber-soft:#3b2d10; --red:#ff8ba0; --red-soft:#421b27; --purple:#c0a7ff; --purple-soft:#30264d; --shadow:0 22px 54px rgba(0,0,0,.3); }}
    * {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }} body {{ margin:0; background:var(--page); color:var(--ink); font-family:var(--sans); line-height:1.65; }} a {{ color:var(--blue); }} button {{ font:inherit; }}
    .topbar {{ position:sticky; top:0; z-index:20; border-bottom:1px solid var(--line); background:color-mix(in srgb,var(--surface) 92%,transparent); backdrop-filter:blur(14px); }}
    .topbar-inner {{ width:min(1180px,calc(100% - 32px)); min-height:60px; margin:auto; display:flex; align-items:center; justify-content:space-between; gap:20px; }}
    .brand {{ display:flex; gap:10px; align-items:center; font-weight:800; color:var(--ink); text-decoration:none; }} .brand-mark {{ display:inline-block; width:11px; height:11px; border-radius:50%; background:var(--blue); box-shadow:0 0 0 5px var(--blue-soft); font-size:0; }}
    .actions {{ display:flex; gap:8px; }} .actions button {{ border:1px solid var(--line); border-radius:10px; background:var(--surface); color:var(--ink); padding:7px 11px; cursor:pointer; }}
    .hero {{ border-bottom:1px solid var(--line); background:radial-gradient(circle at 85% 15%,color-mix(in srgb,var(--blue) 17%,transparent),transparent 30rem),var(--surface); }}
    .hero-inner {{ width:min(1180px,calc(100% - 32px)); margin:auto; padding:72px 0 58px; }} .eyebrow,.kicker {{ color:var(--blue); font-size:.76rem; font-weight:850; letter-spacing:.12em; text-transform:uppercase; }}
    h1 {{ max-width:900px; margin:10px 0 0; color:var(--navy); font-size:clamp(2.5rem,6vw,5.2rem); line-height:1.02; letter-spacing:-.052em; }} .lede {{ max-width:790px; color:var(--muted); font-size:1.2rem; }}
    .notice {{ max-width:920px; margin-top:26px; border-left:5px solid var(--amber); border-radius:12px; background:var(--amber-soft); color:var(--amber); padding:16px 18px; font-weight:700; }}
    .metric-strip {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:1px; margin-top:40px; border:1px solid var(--line); border-radius:18px; overflow:hidden; background:var(--line); box-shadow:var(--shadow); }} .metric {{ background:var(--surface); padding:22px; }} .metric span {{ display:block; color:var(--muted); font-size:.76rem; font-weight:800; text-transform:uppercase; letter-spacing:.09em; }} .metric strong {{ display:block; margin-top:7px; color:var(--navy); font-size:1.28rem; line-height:1.25; }}
    .page {{ width:min(1180px,calc(100% - 32px)); margin:auto; display:grid; grid-template-columns:245px minmax(0,1fr); gap:42px; padding:42px 0 90px; }} nav {{ align-self:start; position:sticky; top:90px; }} nav a {{ display:block; border-left:2px solid var(--line); padding:7px 13px; color:var(--muted); text-decoration:none; font-size:.9rem; }} nav a:hover {{ border-color:var(--blue); color:var(--ink); }}
    main {{ min-width:0; }} section {{ scroll-margin-top:90px; margin-bottom:62px; }} h2 {{ margin:0 0 18px; color:var(--navy); font-size:clamp(1.65rem,3vw,2.35rem); letter-spacing:-.025em; }} h3 {{ color:var(--navy); }} .section-lead {{ max-width:800px; color:var(--muted); font-size:1.05rem; }}
    .decision {{ border:1px solid color-mix(in srgb,var(--blue) 28%,var(--line)); border-radius:var(--radius); background:linear-gradient(140deg,var(--blue-soft),var(--surface)); padding:28px; box-shadow:var(--shadow); }} .decision strong {{ display:block; margin-top:12px; font-size:1.2rem; }}
    .flow-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }} .flow-card {{ border:1px solid var(--line); border-radius:var(--radius); background:var(--surface); padding:24px; }} .flow {{ list-style:none; margin:22px 0 0; padding:0; }} .flow li {{ display:grid; grid-template-columns:38px 1fr; gap:12px; align-items:start; position:relative; padding:0 0 20px; }} .flow li:not(:last-child)::after {{ content:""; position:absolute; left:14px; top:29px; bottom:3px; width:1px; background:var(--line); }} .flow li span {{ display:grid; place-items:center; width:29px; height:29px; border-radius:50%; background:var(--blue-soft); color:var(--blue); font-size:.72rem; font-weight:850; }}
    .target-flow {{ list-style:none; margin:22px 0 0; padding:0; display:grid; gap:12px; }} .target-flow li {{ border-left:4px solid var(--blue); border-radius:0 14px 14px 0; background:var(--surface); padding:15px 17px; }} .target-flow li div {{ display:flex; align-items:center; gap:10px; }} .target-flow li div span {{ color:var(--blue); font-weight:850; }} .target-flow li p {{ margin:6px 0; }} .target-flow small,.muted {{ color:var(--muted); }}
    .card-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }} .diagnosis-card,.card-grid>article,.interventions>article {{ border:1px solid var(--line); border-radius:16px; background:var(--surface); padding:20px; }} .diagnosis-card h3,.card-grid h3,.interventions h3 {{ margin:10px 0 6px; }} .diagnosis-card p,.interventions p {{ margin:0; }}
    .redesign {{ list-style:none; padding:0; display:grid; gap:12px; }} .redesign li {{ display:grid; grid-template-columns:42px 1fr; gap:14px; border-bottom:1px solid var(--line); padding:15px 0; }} .redesign li>span {{ color:var(--blue); font-size:1.5rem; font-weight:850; }} .redesign p {{ margin:4px 0; color:var(--muted); }}
    .ai {{ border-radius:var(--radius); background:var(--navy); color:white; padding:30px; }} .ai h2,.ai strong {{ color:white; }} .ai p {{ max-width:820px; }}
    .badge {{ display:inline-flex; border-radius:999px; padding:3px 9px; font-size:.72rem; font-weight:850; letter-spacing:.04em; text-transform:uppercase; }} .badge.evidenced {{ background:var(--green-soft); color:var(--green); }} .badge.proposed {{ background:var(--amber-soft); color:var(--amber); }} .badge.missing {{ background:var(--red-soft); color:var(--red); }} .badge.unverifiable {{ background:var(--purple-soft); color:var(--purple); }}
    .table-wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:16px; background:var(--surface); }} table {{ width:100%; border-collapse:collapse; font-size:.9rem; }} th,td {{ padding:13px 14px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }} th {{ color:var(--muted); font-size:.72rem; letter-spacing:.07em; text-transform:uppercase; }} tr:last-child td {{ border-bottom:0; }}
    .interventions {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }} .interventions small {{ display:block; margin-top:14px; color:var(--muted); }}
    .anchor-list {{ list-style:none; padding:0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }} .anchor-list li {{ display:flex; justify-content:space-between; gap:18px; border-bottom:1px solid var(--line); padding:10px 0; }} .anchor-list span {{ text-align:right; font-weight:750; }}
    footer {{ border-top:1px solid var(--line); background:var(--surface); }} footer>div {{ width:min(1180px,calc(100% - 32px)); margin:auto; padding:30px 0; color:var(--muted); }}
    @media (max-width:900px) {{ .page {{ grid-template-columns:1fr; }} nav {{ display:none; }} .metric-strip,.flow-grid,.card-grid,.interventions,.anchor-list {{ grid-template-columns:1fr 1fr; }} }}
    @media (max-width:620px) {{ .metric-strip,.flow-grid,.card-grid,.interventions,.anchor-list {{ grid-template-columns:1fr; }} h1 {{ font-size:2.35rem; overflow-wrap:anywhere; }} .anchor-list li {{ display:block; }} .anchor-list span {{ display:block; margin-top:4px; text-align:left; overflow-wrap:anywhere; }} .actions button:first-child {{ display:none; }} }}
    @media print {{ .topbar,nav {{ display:none!important; }} body {{ background:#fff; }} .page {{ display:block; width:auto; padding:24px 0; }} .hero-inner,main,footer>div {{ width:auto; margin:0 34px; }} section {{ break-inside:avoid; }} .ai {{ background:#102a43!important; print-color-adjust:exact; }} }}
  </style>
</head>
<body>
  <header class="topbar"><div class="topbar-inner"><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true">brand</span>FDE proposal delivery kit</a><div class="actions"><button type="button" onclick="window.print()">Print</button><button id="theme" type="button" aria-label="Toggle color theme">Dark theme</button></div></div></header>
  <section class="hero" id="top"><div class="hero-inner"><p class="eyebrow">Decision brief · {html.escape(data["classification"]["label"])}</p><h1>{html.escape(data["title"])}</h1><p class="lede">{html.escape(data["subtitle"])}</p><div class="notice">{html.escape(data["classification"]["statement"])}</div><div class="metric-strip"><div class="metric"><span>Scope</span><strong>{html.escape(data["scope"]["included"][0])}</strong></div><div class="metric"><span>Handling-time hypothesis</span><strong>{outcome["baseline"]["display"]} to {outcome["target"]["display"]}</strong></div><div class="metric"><span>AI-fit</span><strong>{html.escape(data["aiFit"]["decision"].capitalize())}</strong></div><div class="metric"><span>Authority</span><strong>{html.escape(data["authority"]["writeBack"]["display"])}</strong></div></div></div></section>
  <div class="page"><nav aria-label="Proposal sections"><p class="kicker">Contents</p><a href="#decision">Decision</a><a href="#diagnosis">Diagnosis</a><a href="#redesign">Redesign</a><a href="#target">Target flow</a><a href="#intervention">Interventions</a><a href="#semantics">Semantics</a><a href="#slice">First slice</a><a href="#validation">Validation</a><a href="#ledger">Evidence ledger</a><a href="#next">Next action</a></nav><main>
    <section id="decision"><div class="decision"><p class="kicker">Decision requested</p><h2>{html.escape(data["communication"]["decision"])}</h2><strong>{html.escape(data["communication"]["centralTakeaway"])}</strong></div></section>
    <section id="diagnosis"><p class="kicker">Current process</p><h2>The delay is likely in evidence assembly and state interpretation</h2><p class="section-lead">These are proposed synthetic hypotheses, not observations of enterprise work.</p><div class="flow-grid"><article class="flow-card"><h3>Normal path</h3><ol class="flow">{current_steps}</ol></article><article class="flow-card"><h3>Exception path</h3><ol class="flow">{"".join(f'<li><span>{i:02}</span>{html.escape(step)}</li>' for i,step in enumerate(current["exceptionFlow"],1))}</ol></article></div><div class="card-grid" style="margin-top:18px">{diagnosis_cards}</div></section>
    <section id="redesign"><p class="kicker">Before technology</p><h2>Remove repeated work and standardize the control boundary</h2><ol class="redesign">{redesign}</ol><div class="card-grid">{owners}</div></section>
    <section id="target"><p class="kicker">Technology-neutral target</p><h2>Retrieve, control, normalize, then let a human confirm</h2><ol class="target-flow">{target_steps}</ol><p><strong>Normal:</strong> {html.escape(target["normalOutcome"])}</p><p><strong>Exception:</strong> {html.escape(target["exceptionOutcome"])}</p><p><strong>Override:</strong> {html.escape(target["humanOverride"])}</p></section>
    <section id="intervention"><p class="kicker">Simplest sufficient choices</p><h2>Deterministic software handles stable rules; humans retain judgment</h2><div class="interventions">{interventions}</div></section>
    <section class="ai"><p class="kicker">AI decision</p><h2>{html.escape(data["aiFit"]["display"])}</h2><p>{html.escape(data["aiFit"]["rationale"])}</p><p>{html.escape(data["aiFit"]["futureBoundary"])}</p></section>
    <section id="semantics"><p class="kicker">Versioned meaning</p><h2>Only three refund states are supported</h2><p>Proposed version <strong>{html.escape(data["semanticContract"]["version"])}</strong>, owned by <strong>{html.escape(data["semanticContract"]["owner"])}</strong> {badge(data["semanticContract"]["evidenceState"])}</p>{states}<h3>Everything else abstains and routes to finance</h3>{html_list(data["semanticContract"]["abstentionCases"])}</section>
    <section id="slice"><p class="kicker">First buildable slice</p><h2>{html.escape(data["firstSlice"]["name"])}</h2><p class="section-lead">{html.escape(data["firstSlice"]["userVisibleOutcome"])}</p><div class="flow-grid"><article class="flow-card"><h3>Every result exposes</h3>{html_list(data["firstSlice"]["requiredResultFields"])}</article><article class="flow-card"><h3>Explicitly deferred</h3>{html_list(data["firstSlice"]["deferred"])}</article></div><p><strong>Authority:</strong> {html.escape(data["authority"]["writeBack"]["display"])}; {html.escape(data["authority"]["customerResponse"])}. Enterprise access decision: <code>{html.escape(data["authority"]["accessDecision"])}</code>.</p></section>
    <section id="validation"><p class="kicker">Shadow before pilot</p><h2>{html.escape(data["validation"]["method"])}</h2><h3>Entry criteria</h3>{html_list(data["validation"]["entryCriteria"])}{thresholds}<p><strong>Rollback:</strong> {html.escape(data["validation"]["rollback"])}</p></section>
    <section id="ledger"><p class="kicker">Evidence boundary</p><h2>Polish does not upgrade evidence</h2><p class="section-lead">Each target-enterprise gap restricts delivery or authority explicitly.</p>{ledger}</section>
    <section id="next"><div class="decision"><p class="kicker">Next accountable action</p><h2>{html.escape(data["nextAccountableAction"]["action"])}</h2><p><strong>Owners:</strong> {html.escape(" and ".join(data["nextAccountableAction"]["owners"]))}</p><p><strong>Observable completion:</strong> {html.escape(data["nextAccountableAction"]["completionCriterion"])}</p></div><h3>Cross-format consistency anchors</h3><ul class="anchor-list">{consistency}</ul></section>
  </main></div>
  <footer><div>Canonical source: <code>artifacts/analysis-package.json</code> · Case-owned synthetic proposal · No enterprise authority implied.</div></footer>
  <script>const root=document.documentElement;const button=document.getElementById('theme');button.addEventListener('click',()=>{{const dark=root.dataset.theme==='dark';root.dataset.theme=dark?'light':'dark';button.textContent=dark?'Dark theme':'Light theme';}});</script>
</body>
</html>
'''


def build_presentation_html(data: dict) -> str:
    """Build a browser-native decision deck from the canonical case package."""
    claims = {item["id"]: item["display"] for item in data["consistencyClaims"]}
    classification = data["classification"]

    def source_line(*claim_ids: str) -> str:
        anchors = " · ".join(f'{claim_id}: {claims[claim_id]}' for claim_id in claim_ids)
        return f'<footer><span>artifacts/analysis-package.json</span><span>{html.escape(anchors)}</span></footer>'

    current_flow = "".join(
        f'<li><span>{index:02}</span><strong>{html.escape(step)}</strong></li>'
        for index, step in enumerate(data["currentProcess"]["normalFlow"], 1)
    )
    diagnosis = "".join(
        f'<article class="card"><small>{html.escape(item["evidenceState"])}</small><h3>{html.escape(item["issue"])}</h3><p>{html.escape(item["effect"])}</p></article>'
        for item in data["diagnosis"]
    )
    target_steps = "".join(
        f'<li><span>{index:02}</span><div><h3>{html.escape(step["name"])}</h3><p>{html.escape(step["description"])}</p><small>{html.escape(step["owner"])}</small></div></li>'
        for index, step in enumerate(data["targetProcess"]["steps"], 1)
    )
    interventions = "".join(
        f'<article class="card"><small>{html.escape(item["need"])}</small><h3>{html.escape(item["selection"])}</h3><p>{html.escape(item["reason"])}</p><strong>{html.escape(item["owner"])}</strong></article>'
        for item in data["interventions"]
    )
    states = "".join(
        f'<article class="state"><small>SUPPORTED</small><h3>{html.escape(item["normalizedState"])}</h3><p>{html.escape(item["meaning"])}</p><strong>{html.escape(item["route"])}</strong></article>'
        for item in data["semanticContract"]["supportedStates"]
    )
    abstentions = "".join(f'<li>{html.escape(item)}</li>' for item in data["semanticContract"]["abstentionCases"])
    result_fields = "".join(f'<li>{html.escape(item)}</li>' for item in data["firstSlice"]["requiredResultFields"])
    deferred = "".join(f'<li>{html.escape(item)}</li>' for item in data["firstSlice"]["deferred"])
    thresholds = "".join(
        f'<article class="gate"><span>{html.escape(item["id"])}</span><div><h3>{html.escape(item["criterion"])}</h3><p>{html.escape(item["threshold"])}</p></div></article>'
        for item in data["validation"]["thresholds"]
    )
    required_inputs = "".join(
        f'<li><span>{index:02}</span>{html.escape(item)}</li>'
        for index, item in enumerate(data["nextAccountableAction"]["requiredInputs"], 1)
    )
    owner_line = " · ".join(data["nextAccountableAction"]["owners"])

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Browser-native decision presentation for {html.escape(data["title"])}">
  <title>{html.escape(data["title"])} — Decision presentation</title>
  <style>
    :root {{ color-scheme:dark; --navy:#07131f; --surface:#10263a; --panel:#16334b; --ink:#f7fbff; --muted:#a8bfd0; --line:#345068; --accent:#69d2e7; --accent2:#62a8ff; --amber:#ffd078; --red:#ff91a4; font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; }}
    * {{ box-sizing:border-box; }} html,body {{ margin:0; min-height:100%; background:var(--navy); color:var(--ink); }} body {{ overflow:hidden; }} button {{ font:inherit; }}
    .deck {{ position:fixed; inset:0; background:radial-gradient(circle at 85% 0%,#153f59 0,transparent 32rem),var(--navy); }}
    .slide {{ position:absolute; inset:0; display:none; grid-template-rows:auto 1fr auto; gap:clamp(20px,3vh,34px); overflow:auto; padding:clamp(30px,5vh,58px) clamp(38px,7vw,110px) 88px; }}
    .slide.active {{ display:grid; animation:enter .28s ease-out; }} @keyframes enter {{ from {{ opacity:0; transform:translateX(22px); }} to {{ opacity:1; transform:none; }} }}
    .slide-head {{ display:flex; align-items:center; justify-content:space-between; gap:20px; color:var(--accent); font-size:clamp(.72rem,1.2vw,.95rem); font-weight:850; letter-spacing:.13em; text-transform:uppercase; }}
    .evidence {{ color:var(--amber); }} .content {{ align-self:center; width:100%; max-width:1500px; margin:auto; }}
    h1,h2,h3,p {{ margin-top:0; }} h1 {{ max-width:1180px; margin-bottom:26px; font-size:clamp(3.2rem,7vw,7rem); line-height:.94; letter-spacing:-.055em; }} h2 {{ max-width:1220px; margin-bottom:28px; font-size:clamp(2.3rem,5vw,4.9rem); line-height:1.02; letter-spacing:-.04em; }} h3 {{ margin-bottom:9px; font-size:clamp(1rem,1.65vw,1.35rem); }} p,li {{ color:var(--muted); font-size:clamp(.94rem,1.45vw,1.24rem); line-height:1.48; }}
    .lede {{ max-width:930px; font-size:clamp(1.2rem,2.2vw,1.75rem); }} .decision {{ max-width:1180px; font-size:clamp(1.65rem,3.3vw,3rem); line-height:1.2; font-weight:760; }}
    .chips {{ display:flex; flex-wrap:wrap; gap:11px; margin-top:35px; }} .chip {{ border:1px solid var(--line); border-radius:999px; background:#0c2031; padding:10px 16px; color:var(--ink); font-weight:760; }}
    .accent-box {{ border-left:7px solid var(--accent); border-radius:0 18px 18px 0; background:linear-gradient(120deg,#123149,#0d2233); padding:clamp(22px,3vw,40px); }}
    .grid {{ display:grid; gap:16px; }} .grid.two {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .grid.three {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .grid.four {{ grid-template-columns:repeat(4,minmax(0,1fr)); }}
    .card,.state,.gate {{ border:1px solid var(--line); border-radius:18px; background:linear-gradient(145deg,var(--surface),#0c2031); padding:clamp(18px,2vw,28px); }} .card small,.state small {{ display:block; margin-bottom:14px; color:var(--accent); font-weight:850; letter-spacing:.09em; text-transform:uppercase; }} .card p,.state p {{ margin-bottom:14px; }} .card strong,.state strong {{ color:var(--ink); font-size:.9rem; }}
    .flow {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; margin:34px 0 0; padding:0; list-style:none; }} .flow li {{ position:relative; border-top:2px solid var(--line); padding:22px 8px 0 0; }} .flow span,.timeline span,.action-list span {{ display:block; margin-bottom:8px; color:var(--accent); font-weight:850; }}
    .timeline {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:14px; margin:0; padding:0; list-style:none; }} .timeline li {{ border-top:5px solid var(--accent2); border-radius:8px 8px 16px 16px; background:var(--surface); padding:20px; }} .timeline p {{ font-size:clamp(.82rem,1.2vw,1.05rem); }} .timeline small {{ color:var(--accent); }}
    .ai {{ max-width:1250px; }} .ai h2 {{ color:var(--accent); }} .ai p {{ max-width:1060px; font-size:clamp(1.1rem,2vw,1.55rem); }}
    .split {{ display:grid; grid-template-columns:1.2fr .8fr; gap:28px; }} .compact {{ columns:2; gap:30px; margin:0; padding-left:20px; }} .compact li {{ break-inside:avoid; margin-bottom:9px; }}
    .plain-list {{ margin:0; padding-left:22px; }} .plain-list li {{ margin-bottom:8px; }} .authority {{ margin-top:20px; color:var(--red); font-weight:850; }}
    .gates {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }} .gate {{ display:flex; gap:14px; }} .gate>span {{ color:var(--accent); font-size:1.35rem; font-weight:900; }} .gate p {{ margin-bottom:0; font-size:clamp(.8rem,1.15vw,1rem); }}
    .action-list {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px 30px; margin:28px 0; padding:0; list-style:none; }} .action-list li {{ border-bottom:1px solid var(--line); padding:10px 0 14px; }}
    footer {{ display:flex; justify-content:space-between; gap:24px; border-top:1px solid var(--line); padding-top:13px; color:var(--muted); font-size:clamp(.64rem,.9vw,.78rem); }} footer span:last-child {{ text-align:right; }}
    .controls {{ position:fixed; z-index:30; right:22px; bottom:18px; display:flex; align-items:center; gap:8px; border:1px solid var(--line); border-radius:14px; background:rgba(7,19,31,.9); padding:7px; backdrop-filter:blur(14px); }} .controls button {{ display:grid; place-items:center; min-width:38px; height:34px; border:0; border-radius:9px; background:var(--surface); color:var(--ink); cursor:pointer; }} .controls button:hover,.controls button:focus-visible {{ outline:2px solid var(--accent); }} #counter {{ min-width:58px; text-align:center; color:var(--muted); font-variant-numeric:tabular-nums; }}
    .progress {{ position:fixed; z-index:31; left:0; bottom:0; width:100%; height:4px; background:#0b1c2a; }} .progress i {{ display:block; width:10%; height:100%; background:linear-gradient(90deg,var(--accent),var(--accent2)); transition:width .2s ease; }}
    .help {{ position:fixed; z-index:29; left:22px; bottom:23px; color:var(--muted); font-size:.75rem; }}
    @media (max-height:800px) and (min-width:801px) {{
      .slide {{ gap:12px; padding:24px 54px 62px; }} h1 {{ margin-bottom:18px; }} h2 {{ margin-bottom:18px; font-size:clamp(2.2rem,4.2vw,3.8rem); }} p,li {{ font-size:.9rem; line-height:1.34; }}
      .card,.state,.gate {{ padding:15px; }} .grid {{ gap:11px; }} .card small,.state small {{ margin-bottom:8px; }} .card p,.state p {{ margin-bottom:8px; }}
      .flow {{ gap:9px; margin-top:18px; }} .flow li {{ padding-top:12px; }} .timeline {{ gap:9px; }} .timeline li {{ padding:14px; }} footer {{ padding-top:8px; }} .controls {{ bottom:12px; }}
      #slide-2 .decision {{ font-size:2rem; }} #slide-2 .accent-box {{ padding:24px; }}
      #slide-3 .grid {{ margin-top:14px!important; }} #slide-3 .card h3 {{ font-size:1rem; }} #slide-3 .card p {{ font-size:.78rem; }}
      #slide-7 .compact li {{ margin-bottom:5px; font-size:.8rem; }}
      #slide-8 .lede {{ margin-bottom:12px; font-size:1.05rem; }} #slide-8 .plain-list li {{ margin-bottom:3px; font-size:.78rem; }} #slide-8 .authority {{ margin-top:9px; font-size:.78rem; }}
      #slide-9 .gate p {{ font-size:.75rem; }} #slide-9 .authority {{ margin-top:9px; font-size:.76rem; }}
      #slide-10 h2 {{ max-width:1180px; margin-bottom:10px; font-size:2.65rem; }} #slide-10 .action-list {{ grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; margin:12px 0; }} #slide-10 .action-list li {{ padding:7px 0; font-size:.72rem; }} #slide-10 .accent-box {{ padding:17px; font-size:.82rem; }} #slide-10 .accent-box p {{ font-size:.72rem; }}
    }}
    @media (max-width:800px) {{ .slide {{ padding:26px 24px 82px; }} .grid.three,.grid.four,.flow,.timeline,.gates {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .split,.grid.two {{ grid-template-columns:1fr; }} .content {{ align-self:start; }} footer {{ display:block; }} footer span {{ display:block; margin-top:3px; text-align:left!important; }} .help {{ display:none; }} }}
    @media print {{
      @page {{ size:13.333in 7.5in; margin:0; }} body {{ overflow:visible; background:white; }} .deck {{ position:static; }}
      .slide,.slide.active {{ position:relative; display:grid; width:13.333in; height:7.5in; gap:12px; overflow:hidden; padding:24px 54px 28px; break-after:page; page-break-after:always; animation:none; }}
      h1 {{ margin-bottom:18px; }} h2 {{ margin-bottom:18px; font-size:3.8rem; }} p,li {{ font-size:.9rem; line-height:1.34; }} .card,.state,.gate {{ padding:15px; }} .grid {{ gap:11px; }} .card small,.state small {{ margin-bottom:8px; }} .card p,.state p {{ margin-bottom:8px; }}
      .flow {{ gap:9px; margin-top:18px; }} .flow li {{ padding-top:12px; }} .timeline {{ gap:9px; }} .timeline li {{ padding:14px; }} footer {{ padding-top:8px; }}
      #slide-2 .decision {{ font-size:2rem; }} #slide-2 .accent-box {{ padding:24px; }} #slide-3 .grid {{ margin-top:14px!important; }} #slide-3 .card h3 {{ font-size:1rem; }} #slide-3 .card p {{ font-size:.78rem; }}
      #slide-7 .compact li {{ margin-bottom:5px; font-size:.8rem; }} #slide-8 .lede {{ margin-bottom:12px; font-size:1.05rem; }} #slide-8 .plain-list li {{ margin-bottom:3px; font-size:.78rem; }} #slide-8 .authority {{ margin-top:9px; font-size:.78rem; }}
      #slide-9 .gate p {{ font-size:.75rem; }} #slide-9 .authority {{ margin-top:9px; font-size:.76rem; }} #slide-10 h2 {{ max-width:1180px; margin-bottom:10px; font-size:2.65rem; }} #slide-10 .action-list {{ grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; margin:12px 0; }} #slide-10 .action-list li {{ padding:7px 0; font-size:.72rem; }} #slide-10 .accent-box {{ padding:17px; font-size:.82rem; }} #slide-10 .accent-box p {{ font-size:.72rem; }}
      .controls,.progress,.help {{ display:none; }}
    }}
  </style>
</head>
<body>
  <main class="deck" aria-live="polite">
    <section class="slide active" id="slide-1" data-slide="1">
      <div class="slide-head"><span>FDE operating solution</span><span class="evidence">{html.escape(classification["label"])}</span></div>
      <div class="content"><h1>{html.escape(data["title"])}</h1><p class="lede">{html.escape(data["subtitle"])}</p><div class="chips"><span class="chip">{html.escape(claims["C2"])}</span><span class="chip">{html.escape(claims["C3"])}</span><span class="chip">{html.escape(claims["C5"])}</span><span class="chip">{html.escape(claims["C6"])}</span></div></div>
      {source_line("C1", "C2", "C3", "C5", "C6")}
    </section>
    <section class="slide" id="slide-2" data-slide="2">
      <div class="slide-head"><span>Decision</span><span class="evidence">{html.escape(classification["label"])}</span></div>
      <div class="content"><h2>The next decision is a bounded shadow replay</h2><div class="accent-box"><p class="decision">{html.escape(data["communication"]["decision"])}</p><p>{html.escape(data["communication"]["centralTakeaway"])}</p></div><div class="chips"><span class="chip">{html.escape(owner_line)}</span></div></div>
      {source_line("C1", "C3", "C7", "C8")}
    </section>
    <section class="slide" id="slide-3" data-slide="3">
      <div class="slide-head"><span>Proposed diagnosis</span><span class="evidence">Not observed enterprise evidence</span></div>
      <div class="content"><h2>The likely delays happen before anyone writes the response</h2><ol class="flow">{current_flow}</ol><div class="grid four" style="margin-top:28px">{diagnosis}</div></div>
      {source_line("C1", "C2")}
    </section>
    <section class="slide" id="slide-4" data-slide="4">
      <div class="slide-head"><span>Target workflow</span><span class="evidence">Process before technology</span></div>
      <div class="content"><h2>Standardize evidence before human confirmation</h2><ol class="timeline">{target_steps}</ol><p class="authority">{html.escape(data["targetProcess"]["exceptionOutcome"])}</p></div>
      {source_line("C2", "C6", "C7", "C8")}
    </section>
    <section class="slide" id="slide-5" data-slide="5">
      <div class="slide-head"><span>Intervention selection</span><span class="evidence">Simplest sufficient choice</span></div>
      <div class="content"><h2>Stable work stays deterministic; accountable judgment stays human</h2><div class="grid four">{interventions}</div></div>
      {source_line("C5", "C6")}
    </section>
    <section class="slide" id="slide-6" data-slide="6">
      <div class="slide-head"><span>AI decision</span><span class="evidence">{html.escape(classification["label"])}</span></div>
      <div class="content ai"><h2>{html.escape(data["aiFit"]["display"])}</h2><p>{html.escape(data["aiFit"]["rationale"])}</p><p>{html.escape(data["aiFit"]["futureBoundary"])}</p></div>
      {source_line("C1", "C5")}
    </section>
    <section class="slide" id="slide-7" data-slide="7">
      <div class="slide-head"><span>Semantic contract</span><span class="evidence">Version {html.escape(data["semanticContract"]["version"])}</span></div>
      <div class="content"><h2>Only three refund states are supported</h2><div class="grid three">{states}</div><h3 style="margin-top:24px">Everything else abstains and routes to finance</h3><ul class="compact">{abstentions}</ul></div>
      {source_line("C4", "C8")}
    </section>
    <section class="slide" id="slide-8" data-slide="8">
      <div class="slide-head"><span>First buildable slice</span><span class="evidence">Human confirmation required</span></div>
      <div class="content"><h2>{html.escape(data["firstSlice"]["name"])}</h2><p class="lede">{html.escape(data["firstSlice"]["userVisibleOutcome"])}</p><div class="split"><div class="card"><h3>Every result exposes</h3><ul class="plain-list">{result_fields}</ul></div><div class="card"><h3>Explicitly deferred</h3><ul class="plain-list">{deferred}</ul></div></div><p class="authority">{html.escape(data["authority"]["writeBack"]["display"])} · {html.escape(data["authority"]["customerResponse"])} · Enterprise access decision: {html.escape(data["authority"]["accessDecision"])}</p></div>
      {source_line("C2", "C5", "C6")}
    </section>
    <section class="slide" id="slide-9" data-slide="9">
      <div class="slide-head"><span>Validation gate</span><span class="evidence">Shadow before pilot</span></div>
      <div class="content"><h2>{html.escape(data["validation"]["method"])}</h2><div class="gates">{thresholds}</div><p class="authority">Rollback: {html.escape(data["validation"]["rollback"])}</p></div>
      {source_line("C3", "C4", "C6")}
    </section>
    <section class="slide" id="slide-10" data-slide="10">
      <div class="slide-head"><span>Next accountable action</span><span class="evidence">Not a pilot authorization</span></div>
      <div class="content"><h2>{html.escape(data["nextAccountableAction"]["action"])}</h2><ol class="action-list">{required_inputs}</ol><div class="accent-box"><strong>{html.escape(data["nextAccountableAction"]["completionCriterion"])}</strong><p style="margin:9px 0 0">Owners: {html.escape(owner_line)}</p></div></div>
      {source_line("C1", "C6", "C7", "C8")}
    </section>
  </main>
  <div class="help">← → / Space · Home / End · F fullscreen · P print</div>
  <div class="controls" aria-label="Presentation controls"><button id="prev" type="button" aria-label="Previous slide">←</button><span id="counter">1 / 10</span><button id="next" type="button" aria-label="Next slide">→</button><button id="full" type="button" aria-label="Toggle fullscreen">⛶</button></div>
  <div class="progress" aria-hidden="true"><i id="progress"></i></div>
  <script>
    const slides=[...document.querySelectorAll('.slide')]; let current=0;
    const counter=document.getElementById('counter'); const progress=document.getElementById('progress');
    function show(index,updateHash=true){{ current=Math.max(0,Math.min(slides.length-1,index)); slides.forEach((slide,i)=>{{slide.classList.toggle('active',i===current);slide.setAttribute('aria-hidden',i===current?'false':'true');}}); counter.textContent=`${{current+1}} / ${{slides.length}}`; progress.style.width=`${{((current+1)/slides.length)*100}}%`; if(updateHash) history.replaceState(null,'',`#slide-${{current+1}}`); }}
    document.getElementById('prev').addEventListener('click',()=>show(current-1)); document.getElementById('next').addEventListener('click',()=>show(current+1));
    document.getElementById('full').addEventListener('click',()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen());
    document.addEventListener('keydown',event=>{{ if(['ArrowRight','PageDown',' '].includes(event.key)){{event.preventDefault();show(current+1);}} if(['ArrowLeft','PageUp'].includes(event.key)){{event.preventDefault();show(current-1);}} if(event.key==='Home')show(0); if(event.key==='End')show(slides.length-1); if(event.key.toLowerCase()==='f')document.getElementById('full').click(); if(event.key.toLowerCase()==='p')window.print(); }});
    const initial=Number(location.hash.replace('#slide-','')); show(Number.isInteger(initial)&&initial>0?initial-1:0,false);
  </script>
</body>
</html>
'''


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def w_text(text: str, *, bold: bool = False, italic: bool = False, color: str | None = None, size: int | None = None) -> str:
    props = ["<w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\"/>"]
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    preserve = ' xml:space="preserve"' if text.startswith(" ") or text.endswith(" ") else ""
    return f'<w:r><w:rPr>{"".join(props)}</w:rPr><w:t{preserve}>{xml_escape(text)}</w:t></w:r>'


def w_paragraph(text: str = "", *, style: str | None = None, align: str | None = None, bullet: bool = False, keep_next: bool = False, shade: str | None = None, border: str | None = None, runs: list[str] | None = None) -> str:
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    if bullet:
        props.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
        props.append('<w:jc w:val="left"/>')
    if keep_next:
        props.append("<w:keepNext/>")
    if shade:
        props.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    if border:
        props.append(f'<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="{border}"/></w:pBdr>')
    content = "".join(runs) if runs is not None else w_text(text)
    return f'<w:p><w:pPr>{"".join(props)}</w:pPr>{content}</w:p>'


def w_cell(text: str, width: int, *, header: bool = False) -> str:
    fill = '<w:shd w:val="clear" w:color="auto" w:fill="F4F6F9"/>' if header else ""
    runs = [w_text(text, bold=header, color="1F4D78" if header else None)]
    return (
        f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{fill}'
        '<w:tcMar><w:top w:w="80" w:type="dxa"/><w:start w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:end w:w="120" w:type="dxa"/></w:tcMar></w:tcPr>'
        + w_paragraph(runs=runs, align="left")
        + "</w:tc>"
    )


def w_table(headers: list[str], rows: list[list[str]], widths: list[int]) -> str:
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in widths)
    table_props = (
        '<w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblInd w:w="120" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:color="D7DEE8"/><w:left w:val="single" w:sz="4" w:color="D7DEE8"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="D7DEE8"/><w:right w:val="single" w:sz="4" w:color="D7DEE8"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="D7DEE8"/><w:insideV w:val="single" w:sz="4" w:color="D7DEE8"/>'
        '</w:tblBorders></w:tblPr>'
    )
    header_row = '<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(w_cell(cell, widths[i], header=True) for i, cell in enumerate(headers)) + "</w:tr>"
    body = "".join('<w:tr>' + "".join(w_cell(str(cell), widths[i]) for i, cell in enumerate(row)) + "</w:tr>" for row in rows)
    return f'<w:tbl>{table_props}<w:tblGrid>{grid}</w:tblGrid>{header_row}{body}</w:tbl>'


def docx_document_xml(data: dict) -> str:
    outcome = data["operatingOutcome"]
    body: list[str] = []
    body.append(w_paragraph("PROPOSED OPERATING SOLUTION", align="center", runs=[w_text("PROPOSED OPERATING SOLUTION", bold=True, color="0B7285", size=20)]))
    body.append(w_paragraph(data["title"], align="center", runs=[w_text(data["title"], bold=True, color="102A43", size=48)]))
    body.append(w_paragraph(data["subtitle"], align="center", runs=[w_text(data["subtitle"], italic=True, color="5F6E80", size=26)]))
    body.append(w_paragraph(data["classification"]["label"], align="center", shade="FFF4D6", runs=[w_text(data["classification"]["label"], bold=True, color="9A5B00", size=22)]))
    body.append(w_paragraph(data["classification"]["statement"], shade="FFF4D6", border="9A5B00"))
    body.append(w_paragraph("Decision requested", style="Heading1", keep_next=True))
    body.append(w_paragraph(data["communication"]["decision"], shade="E7F5F7", border="0B7285", runs=[w_text(data["communication"]["decision"], bold=True, color="102A43")]))
    body.append(w_paragraph(data["communication"]["centralTakeaway"]))
    body.append(w_paragraph("Operating outcome and scope", style="Heading1", keep_next=True))
    body.append(w_paragraph(f"For the {outcome['user']} at {outcome['processNode']}, the proposed change is to {outcome['decisionOrAction'].lower()} The synthetic handling-time hypothesis is {outcome['baseline']['display']} to {outcome['target']['display']}; {outcome['qualityGuardrail']['display'].lower()}."))
    body.append(w_table(["Boundary", "Proposal"], [["Included", "; ".join(data["scope"]["included"])], ["Excluded", "; ".join(data["scope"]["excluded"])]], [1800, 7560]))
    body.append(w_paragraph("Current-process diagnosis", style="Heading1", keep_next=True))
    body.append(w_paragraph("Proposed normal flow", style="Heading2", keep_next=True))
    body.append(w_paragraph(" → ".join(data["currentProcess"]["normalFlow"]), shade="F4F6F9"))
    body.append(w_paragraph("Proposed exception flow", style="Heading2", keep_next=True))
    body.append(w_paragraph(" → ".join(data["currentProcess"]["exceptionFlow"]), shade="F4F6F9"))
    for item in data["diagnosis"]:
        body.append(w_paragraph(item["issue"], style="Heading3", keep_next=True))
        body.append(w_paragraph(f"{item['effect']} Evidence status: {item['evidenceState']}."))
    body.append(w_paragraph("These are synthetic hypotheses to confirm or correct with the process owner and affected users. They are not findings from observed enterprise work.", shade="FFF4D6", border="9A5B00"))
    body.append(w_paragraph("Process redesign before technology", style="Heading1", keep_next=True))
    for item in data["processRedesign"]:
        body.append(w_paragraph(runs=[w_text(item["action"] + ". ", bold=True), w_text(item["change"])], bullet=True))
    body.append(w_paragraph("Technology-neutral target flow", style="Heading1", keep_next=True))
    for index, step in enumerate(data["targetProcess"]["steps"], 1):
        body.append(w_paragraph(runs=[w_text(f"{index}. {step['name']} — ", bold=True, color="0B7285"), w_text(step["description"] + f" Owner: {step['owner']}.")]))
    body.append(w_paragraph(f"Normal outcome: {data['targetProcess']['normalOutcome']}"))
    body.append(w_paragraph(f"Exception outcome: {data['targetProcess']['exceptionOutcome']}"))
    body.append(w_paragraph(f"Human override: {data['targetProcess']['humanOverride']}"))
    body.append(w_paragraph("Process-readiness decision", style="Heading1", keep_next=True))
    body.append(w_paragraph("The as-is path, target flow, handoffs, exception ownership, baseline, and semantic contract have not been accepted by accountable target-enterprise participants. The process remains proposed. This package supports preparation for a shadow-replay decision; it does not authorize implementation or pilot use.", shade="FFEDF1", border="B4233D"))
    body.append(w_paragraph("Intervention selection", style="Heading1", keep_next=True))
    body.append(w_table(["Need", "Selection", "Responsibility", "Why sufficient"], [[i["need"], i["selection"], i["owner"], i["reason"]] for i in data["interventions"]], [1800, 2100, 2400, 3060]))
    body.append(w_paragraph("AI-fit decision", style="Heading1", keep_next=True))
    body.append(w_paragraph(data["aiFit"]["display"], shade="102A43", border="0B7285", runs=[w_text(data["aiFit"]["display"], bold=True, color="FFFFFF", size=26)]))
    body.append(w_paragraph(data["aiFit"]["rationale"]))
    body.append(w_paragraph(data["aiFit"]["futureBoundary"]))
    body.append(w_paragraph("Semantic and exception contract", style="Heading1", keep_next=True))
    body.append(w_paragraph(f"Proposed semantic version: {data['semanticContract']['version']}. Proposed owner: {data['semanticContract']['owner']}. Evidence status: {data['semanticContract']['evidenceState']}."))
    body.append(w_table(["Normalized state", "Meaning", "Route"], [[s["normalizedState"], s["meaning"], s["route"]] for s in data["semanticContract"]["supportedStates"]], [2200, 3580, 3580]))
    body.append(w_paragraph("Abstain and escalate on", style="Heading2", keep_next=True))
    for case in data["semanticContract"]["abstentionCases"]:
        body.append(w_paragraph(case, bullet=True))
    body.append(w_paragraph("First buildable vertical slice", style="Heading1", keep_next=True))
    body.append(w_paragraph(data["firstSlice"]["name"], style="Heading2", keep_next=True))
    body.append(w_paragraph(data["firstSlice"]["userVisibleOutcome"]))
    body.append(w_paragraph("Every returned result must expose", style="Heading2", keep_next=True))
    for item in data["firstSlice"]["requiredResultFields"]:
        body.append(w_paragraph(item, bullet=True))
    body.append(w_paragraph("Case-owned capability and integration seams", style="Heading2", keep_next=True))
    body.append(w_table(["Seam", "Status", "Restriction"], [[s["seam"], s["status"], s["restriction"]] for s in data["firstSlice"]["capabilitySeams"]], [2600, 1300, 5460]))
    body.append(w_paragraph("Explicitly deferred", style="Heading2", keep_next=True))
    for item in data["firstSlice"]["deferred"]:
        body.append(w_paragraph(item, bullet=True))
    body.append(w_paragraph("Authority and controls", style="Heading1", keep_next=True))
    body.append(w_paragraph(f"Proposed application form: {data['authority']['proposedApplicationForm']}. Proposed tier: {data['authority']['proposedTier']}."))
    body.append(w_paragraph(f"{data['authority']['writeBack']['display']}; {data['authority']['customerResponse'].lower()}. Enterprise access decision: {data['authority']['accessDecision']}.", shade="FFEDF1", border="B4233D"))
    body.append(w_paragraph(data["authority"]["restriction"]))
    body.append(w_paragraph("Validation, rollout, and rollback", style="Heading1", keep_next=True))
    body.append(w_paragraph(f"Proposed method: {data['validation']['method']}."))
    body.append(w_paragraph("Entry criteria", style="Heading2", keep_next=True))
    for item in data["validation"]["entryCriteria"]:
        body.append(w_paragraph(item, bullet=True))
    body.append(w_table(["ID", "Criterion", "Proposed threshold", "Failure effect"], [[v["id"], v["criterion"], v["threshold"], v["failureEffect"]] for v in data["validation"]["thresholds"]], [600, 1900, 4800, 2060]))
    body.append(w_paragraph(f"Rollback: {data['validation']['rollback']}", shade="F4F6F9"))
    body.append(w_paragraph("Evidence ledger", style="Heading1", keep_next=True))
    for item in data["evidenceLedger"]:
        body.append(w_paragraph(f"{item['claimId']} — {item['status']}", style="Heading3", keep_next=True))
        body.append(w_paragraph(item["statement"]))
        body.append(w_paragraph(runs=[w_text("Source: ", bold=True), w_text(item["source"]), w_text("  Restriction: ", bold=True), w_text(item["restriction"])], shade="F4F6F9"))
    body.append(w_paragraph("Next accountable action", style="Heading1", keep_next=True))
    body.append(w_paragraph(data["nextAccountableAction"]["action"], shade="E7F5F7", border="0B7285", runs=[w_text(data["nextAccountableAction"]["action"], bold=True, color="102A43")]))
    body.append(w_paragraph("Owners: " + " and ".join(data["nextAccountableAction"]["owners"])))
    body.append(w_paragraph("Required inputs", style="Heading2", keep_next=True))
    for item in data["nextAccountableAction"]["requiredInputs"]:
        body.append(w_paragraph(item, bullet=True))
    body.append(w_paragraph("Observable completion: " + data["nextAccountableAction"]["completionCriterion"]))
    section = (
        '<w:sectPr><w:headerReference w:type="default" r:id="rId1"/><w:footerReference w:type="default" r:id="rId2"/>'
        '<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708"/>'
        '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
    )
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + f'<w:document xmlns:w="{W_NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{"".join(body)}{section}</w:body></w:document>'


def styles_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="172033"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="320" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="160" w:line="320" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="172033"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="160"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="102A43"/><w:sz w:val="48"/><w:szCs w:val="48"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="160"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:i/><w:color w:val="5F6E80"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="200"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="1F4D78"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
</w:styles>'''


def numbering_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{W_NS}"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="540"/></w:tabs><w:ind w:left="540" w:hanging="279"/><w:spacing w:after="80" w:line="290" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''


def build_docx(data: dict, destination: Path) -> None:
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    document_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'''
    header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr xmlns:w="{W_NS}"><w:p><w:pPr><w:spacing w:after="0"/><w:jc w:val="left"/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="6" w:color="D7DEE8"/></w:pBdr></w:pPr>{w_text("FDE PROPOSAL  |  CUSTOMER REFUND STATUS", bold=True, color="5F6E80", size=16)}</w:p></w:hdr>'''
    footer = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="{W_NS}"><w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="0"/></w:pPr>{w_text("Proposed synthetic  |  Page ", color="5F6E80", size=16)}<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'''
    core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Customer Refund-Status Inquiry — Proposed Operating Solution</dc:title><dc:subject>Synthetic FDE proposal delivery kit</dc:subject><dc:creator>FDE Capability Enhancement example</dc:creator><cp:keywords>proposed synthetic; read-only; no write-back; AI not needed</cp:keywords><dc:description>Generated from artifacts/analysis-package.json</dc:description><cp:revision>1</cp:revision><dcterms:created xsi:type="dcterms:W3CDTF">2026-08-27T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-08-27T00:00:00Z</dcterms:modified></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>FDE case-owned generator</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>1.0</AppVersion></Properties>'''
    parts = {
        "[Content_Types].xml": content_types,
        "_rels/.rels": root_rels,
        "word/document.xml": docx_document_xml(data),
        "word/_rels/document.xml.rels": document_rels,
        "word/styles.xml": styles_xml(),
        "word/numbering.xml": numbering_xml(),
        "word/header1.xml": header,
        "word/footer1.xml": footer,
        "docProps/core.xml": core,
        "docProps/app.xml": app,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(parts.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content.encode("utf-8"))


def generate(destination_root: Path) -> tuple[Path, Path, Path, Path]:
    data = load_analysis()
    markdown_path = destination_root / "artifacts" / MARKDOWN_PATH.name
    html_path = destination_root / HTML_PATH.name
    presentation_html_path = destination_root / PRESENTATION_HTML_PATH.name
    docx_path = destination_root / "artifacts" / DOCX_PATH.name
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(build_markdown(data), encoding="utf-8")
    html_path.write_text(build_html(data), encoding="utf-8")
    presentation_html_path.write_text(build_presentation_html(data), encoding="utf-8")
    build_docx(data, docx_path)
    return markdown_path, html_path, presentation_html_path, docx_path


def check_generated() -> int:
    with tempfile.TemporaryDirectory(prefix="refund-delivery-kit-") as temp_dir:
        temp_root = Path(temp_dir)
        generated = generate(temp_root)
        expected = (MARKDOWN_PATH, HTML_PATH, PRESENTATION_HTML_PATH, DOCX_PATH)
        differences = [str(target.relative_to(EXAMPLE_DIR)) for target, source in zip(expected, generated) if not target.exists() or target.read_bytes() != source.read_bytes()]
    if differences:
        print("generated views are stale or missing:")
        for difference in differences:
            print(f"- {difference}")
        return 1
    print("generated views: current")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when committed generated views differ from canonical analysis.")
    args = parser.parse_args()
    if args.check:
        return check_generated()
    paths = generate(EXAMPLE_DIR)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
