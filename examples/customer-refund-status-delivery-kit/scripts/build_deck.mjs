#!/usr/bin/env node
/** Build the case-owned decision deck from artifacts/analysis-package.json.
 *
 * Requires the managed Presentations workspace runtime. This source is kept
 * case-owned and deliberately does not implement a generic proposal renderer.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const exampleDir = path.resolve(scriptDir, "..");
const analysisPath = path.join(exampleDir, "artifacts", "analysis-package.json");
const finalPptx = process.env.FINAL_PPTX || path.join(exampleDir, "artifacts", "customer-refund-status-decision.pptx");
const qaDir = process.env.PPTX_QA_DIR || path.join(exampleDir, ".deck-qa");
const data = JSON.parse(await fs.readFile(analysisPath, "utf8"));
const claims = new Map(data.consistencyClaims.map((item) => [item.id, item.display]));

const W = 1280;
const H = 720;
const INK = "#000000";
const MUTED = "#5F6E80";
const PANEL = "#EDEDED";
const LINE = "#B8BCC4";
const ACCENT = "#6DCBF4";
const ACCENT_STRONG = "#3D8DFF";
const AMBER = "#9A5B00";
const AMBER_SOFT = "#FFF4D6";
const RED_SOFT = "#FFEDF1";
const FONT = "Helvetica Neue";

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

function addText(slide, text, position, options = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    name: options.name || undefined,
    position,
    fill: options.fill || "none",
    line: options.line || { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = {
    fontSize: options.fontSize || 22,
    typeface: FONT,
    color: options.color || INK,
    bold: options.bold || false,
    alignment: options.alignment || "left",
    verticalAlignment: options.verticalAlignment || "top",
  };
  return box;
}

function addRect(slide, position, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry || "rect",
    name: options.name || undefined,
    position,
    fill: options.fill || "none",
    line: options.line || { style: "solid", fill: LINE, width: 1 },
    borderRadius: options.borderRadius,
  });
}

function sourceNotes(claimIds) {
  const claimLines = claimIds.map((id) => `- ${id}: ${claims.get(id)}`).join("\n");
  return `[Sources]\n- Canonical case source: artifacts/analysis-package.json\n${claimLines}\n- Evidence boundary: proposed synthetic; no enterprise authority implied.`;
}

function addChrome(slide, page, claimIds) {
  addText(slide, claims.get("C1"), { left: 42, top: 28, width: 270, height: 24 }, { fontSize: 16, bold: true, color: AMBER });
  addText(slide, String(page).padStart(2, "0"), { left: 1180, top: 660, width: 58, height: 24 }, { fontSize: 16, color: MUTED, alignment: "right" });
  slide.speakerNotes.textFrame.setText(sourceNotes(claimIds));
  slide.speakerNotes.setVisible(true);
}

function addTitle(slide, title, page, claimIds) {
  addChrome(slide, page, claimIds);
  addText(slide, title, { left: 42, top: 72, width: 1196, height: 100 }, { fontSize: 48, bold: true, name: `slide-${page}-title` });
}

function styleTable(table, rows, columns, headerFill = PANEL) {
  table.borders.assign({ style: "solid", fill: "#D7DEE8", width: 1 });
  table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: columns }).assign({
    fill: headerFill,
    textStyle: { fontSize: 21, bold: true, color: "#102A43", typeface: FONT },
    margins: { top: 8, right: 10, bottom: 8, left: 10 },
  });
  if (rows > 1) {
    table.cells.block({ row: 1, column: 0, rowCount: rows - 1, columnCount: columns }).assign({
      textStyle: { fontSize: 19, color: INK, typeface: FONT },
      margins: { top: 8, right: 10, bottom: 8, left: 10 },
    });
  }
}

// 1 — sparse cover, based on Codex Grid slide-01.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addChrome(slide, 1, ["C1", "C2", "C3", "C5", "C6"]);
  addText(slide, "FDE OPERATING SOLUTION", { left: 42, top: 76, width: 500, height: 48 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.title, { left: 42, top: 178, width: 1030, height: 250 }, { fontSize: 80, bold: true, verticalAlignment: "bottom", name: "cover-title" });
  addText(slide, `${data.firstSlice.name} · ${claims.get("C6")}`, { left: 42, top: 496, width: 760, height: 92 }, { fontSize: 32, color: MUTED });
  addText(slide, `${claims.get("C2")} · ${claims.get("C3")}`, { left: 42, top: 610, width: 900, height: 30 }, { fontSize: 20, color: MUTED });
}

// 2 — decision and decision basis, based on Codex Grid slide-05.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "The next decision is a bounded shadow replay", 2, ["C1", "C3", "C7", "C8"]);
  addText(slide, "DECISION", { left: 42, top: 206, width: 560, height: 34 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.communication.decision, { left: 42, top: 250, width: 560, height: 260 }, { fontSize: 32, bold: true });
  addText(slide, "WHY NOW", { left: 656, top: 206, width: 560, height: 34 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.communication.centralTakeaway, { left: 656, top: 250, width: 560, height: 260 }, { fontSize: 30 });
  addText(slide, `Owners: ${data.nextAccountableAction.owners.join(" · ")}`, { left: 42, top: 596, width: 1000, height: 34 }, { fontSize: 22, color: MUTED });
}

// 3 — proposed diagnosis, two-column layout.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "The likely delays happen before anyone writes the response", 3, ["C1", "C2"]);
  addText(slide, "CURRENT WORK", { left: 42, top: 198, width: 520, height: 32 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.currentProcess.normalFlow.map((step, index) => `${index + 1}  ${step}`).join("\n"), { left: 42, top: 244, width: 540, height: 320 }, { fontSize: 28 });
  addRect(slide, { left: 628, top: 196, width: 570, height: 350 }, { fill: PANEL, line: { style: "solid", fill: "none", width: 0 } });
  addText(slide, "DIAGNOSIS HYPOTHESIS", { left: 666, top: 230, width: 490, height: 32 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.diagnosis.map((item) => item.issue).join("\n"), { left: 666, top: 284, width: 490, height: 220 }, { fontSize: 30, bold: true });
  addText(slide, `${data.classification.label}—not observed enterprise evidence`, { left: 666, top: 506, width: 490, height: 28 }, { fontSize: 19, color: AMBER });
}

// 4 — simple process sequence, based on Codex Grid slide-17. Connectors first.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "The target flow standardizes evidence before human confirmation", 4, ["C2", "C6", "C7", "C8"]);
  addRect(slide, { left: 100, top: 350, width: 1060, height: 2 }, { geometry: "straightConnector1", line: { style: "solid", fill: INK, width: 2 } });
  const steps = data.targetProcess.steps;
  const xs = [100, 345, 590, 835, 1080];
  for (let i = 0; i < steps.length; i += 1) {
    addRect(slide, { left: xs[i], top: 337, width: 28, height: 28 }, { geometry: "ellipse", fill: i === 4 ? AMBER_SOFT : ACCENT, line: { style: "solid", fill: INK, width: 1 } });
  }
  for (let i = 0; i < steps.length; i += 1) {
    addText(slide, steps[i].name.toUpperCase(), { left: xs[i] - 8, top: 278, width: 180, height: 32 }, { fontSize: 21, bold: true, color: i === 4 ? AMBER : ACCENT_STRONG });
    addText(slide, steps[i].description, { left: xs[i] - 8, top: 396, width: 194, height: 142 }, { fontSize: 20 });
    addText(slide, steps[i].owner, { left: xs[i] - 8, top: 552, width: 194, height: 52 }, { fontSize: 17, color: MUTED });
  }
}

// 5 — intervention evidence table, based on Codex Grid slide-14.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "Stable work stays deterministic; accountable judgment stays human", 5, ["C5", "C6"]);
  addText(slide, "Each retained need receives the simplest sufficient intervention.", { left: 42, top: 156, width: 1040, height: 38 }, { fontSize: 22, color: MUTED });
  const values = [["Need", "Selected intervention", "Responsibility"], ...data.interventions.map((item) => [item.need, item.selection, item.owner])];
  const table = slide.tables.add({ rows: values.length, columns: 3, left: 42, top: 220, width: 1196, height: 390, columnWidths: [300, 430, 466], values });
  styleTable(table, values.length, 3);
}

// 6 — sparse message slide.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#102A43";
  addText(slide, claims.get("C1"), { left: 42, top: 36, width: 300, height: 28 }, { fontSize: 16, bold: true, color: "#FFD078" });
  addText(slide, claims.get("C5"), { left: 42, top: 180, width: 1120, height: 180 }, { fontSize: 64, bold: true, color: "#FFFFFF" });
  addText(slide, data.aiFit.rationale, { left: 42, top: 420, width: 1080, height: 100 }, { fontSize: 27, color: "#FFFFFF" });
  addText(slide, data.aiFit.futureBoundary, { left: 42, top: 548, width: 1080, height: 70 }, { fontSize: 19, color: "#FFFFFF" });
  addText(slide, "06", { left: 1180, top: 660, width: 58, height: 24 }, { fontSize: 16, color: "#FFFFFF", alignment: "right" });
  slide.speakerNotes.textFrame.setText(sourceNotes(["C1", "C5"]));
  slide.speakerNotes.setVisible(true);
}

// 7 — supported states and abstention boundary, table layout.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "Only three states are supported; everything unsafe abstains", 7, ["C4", "C8"]);
  const states = data.semanticContract.supportedStates.map((item) => item.normalizedState);
  const values = [["Supported state", "Route"], ...data.semanticContract.supportedStates.map((item) => [item.normalizedState, item.route]), ["All other or unsafe states", data.targetProcess.exceptionOutcome]];
  const table = slide.tables.add({ rows: values.length, columns: 2, left: 42, top: 198, width: 700, height: 350, columnWidths: [330, 370], values });
  styleTable(table, values.length, 2);
  addRect(slide, { left: 786, top: 198, width: 412, height: 350 }, { fill: RED_SOFT, line: { style: "solid", fill: "none", width: 0 } });
  addText(slide, "ABSTAIN ON", { left: 820, top: 230, width: 330, height: 30 }, { fontSize: 24, bold: true, color: "#B4233D" });
  addText(slide, data.semanticContract.abstentionCases.join("\n"), { left: 820, top: 280, width: 330, height: 230 }, { fontSize: 22 });
  addText(slide, states.join(" | "), { left: 42, top: 580, width: 1000, height: 28 }, { fontSize: 18, color: MUTED });
}

// 8 — slice and authority, two-column layout.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "The first slice is useful without integration or write authority", 8, ["C2", "C5", "C6"]);
  addText(slide, "RETURNS", { left: 42, top: 194, width: 540, height: 32 }, { fontSize: 24, bold: true, color: ACCENT_STRONG });
  addText(slide, data.firstSlice.requiredResultFields.join("\n"), { left: 42, top: 246, width: 540, height: 310 }, { fontSize: 25 });
  addText(slide, "DEFERS", { left: 656, top: 194, width: 540, height: 32 }, { fontSize: 24, bold: true, color: AMBER });
  addText(slide, data.firstSlice.deferred.join("\n"), { left: 656, top: 246, width: 540, height: 300 }, { fontSize: 25 });
  addText(slide, `${data.authority.writeBack.display} · ${data.authority.customerResponse} · Enterprise access decision: ${data.authority.accessDecision}`, { left: 42, top: 594, width: 1120, height: 34 }, { fontSize: 22, bold: true, color: "#B4233D" });
}

// 9 — validation table.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addTitle(slide, "Shadow evidence must pass every hard gate before a pilot", 9, ["C3", "C4", "C6"]);
  const rows = data.validation.thresholds.map((item) => [item.id, item.criterion, item.threshold]);
  const values = [["ID", "Criterion", "Proposed hard gate"], ...rows];
  const table = slide.tables.add({ rows: values.length, columns: 3, left: 42, top: 184, width: 1196, height: 440, columnWidths: [80, 280, 836], values });
  styleTable(table, values.length, 3);
}

// 10 — decision close, based on a sparse process/close layout.
{
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
  addChrome(slide, 10, ["C1", "C6", "C7", "C8"]);
  addText(slide, data.nextAccountableAction.action, { left: 42, top: 104, width: 1120, height: 170 }, { fontSize: 45, bold: true });
  addRect(slide, { left: 42, top: 318, width: 1156, height: 1 }, { geometry: "straightConnector1", line: { style: "solid", fill: LINE, width: 1 } });
  addText(slide, data.nextAccountableAction.requiredInputs.map((item, index) => `${index + 1}  ${item}`).join("\n"), { left: 42, top: 350, width: 1120, height: 220 }, { fontSize: 23 });
  addText(slide, data.nextAccountableAction.completionCriterion, { left: 42, top: 590, width: 1120, height: 55 }, { fontSize: 23, bold: true, color: ACCENT_STRONG });
}

await fs.mkdir(path.dirname(finalPptx), { recursive: true });
await fs.mkdir(qaDir, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  const png = await presentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(qaDir, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(qaDir, `${stem}.layout.json`), await layout.text());
}
const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(qaDir, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(finalPptx);
console.log(finalPptx);
