---
status: accepted
---

# Operating analysis is the project boundary

This project is an FDE operating-analysis skill: it helps clarify operating scenarios, diagnose and redesign workflows, select the simplest sufficient intervention, and form evidence-bounded recommendations and next actions. Its default outcome is an operating solution and actionable decision, not an artefact package or application; implementation happens only when separately requested. Runnable components and enterprise-platform modules were considered as alternative project centres, but they would make implementation activity—not analysis quality—the default measure of progress.

The boundary is closed in two directions.

**Capability set.** The project has five capabilities: operating-problem framing, workflow diagnosis and redesign, intervention selection and AI-fit, operating-solution formation, and optional delivery or assurance assistance when separately requested. Scenario registries, ontology assets, context resolution, decision support, controlled action, and governance are solution patterns used when a case needs them, not modules this project must build. Expanding the set requires another explicit decision.

**Analysis depth.** The default operating solution contains only the problem and outcome, current-work diagnosis, target workflow, intervention and AI-fit decision with evidence limits, and next accountable action. Analysis expands into models, gates, research, or executable validation only when material uncertainty, risk, authority, persistence, or an explicit request justifies it.

Cases teach, stress-test, and validate the method without automatically becoming core capability. Code, schemas, and runnable examples remain optional validation artefacts used only when an analysis claim needs them; adding implementation to them is not project progress by default. Project improvement is evaluated through varied cases that test analysis quality and decision usefulness, not by counting documents, schemas, code, gates, or runnable examples.

**Falsified if:** the default outcome in `README.md` (Default Outcome) or `.agents/skills/fde-project-work/SKILL.md` becomes an artefact package, runnable component, or implementation instead of an operating solution and next action; the Capability Set in `README.md` or `CONTEXT.md` lists more than the five capabilities; `FDE-Capability-Enhancement-Plan.md` schedules scenario registry, ontology, context resolution, decision support, controlled action, or governance as project modules; `.agents/skills/fde-project-work/SKILL.md` expands the default operating solution beyond five parts; or `docs/evaluations/README.md` scores by document, schema, code, gate, or example count.
