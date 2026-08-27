# FDE Practice and Adoption Field Note

**Purpose.** Record useful practice signals from informal external articles without treating them as enterprise evidence or approved project requirements.

**Reviewed:** 2026-08-27

## Sources reviewed

- Adrian Punk, [最近大火的 AI 岗位，FDE 到底是干嘛的？普通人怎么上车？](https://x.com/AdrianPunk115/status/2083090241683128626)
- 阿哲 Phil, [零基础怎么做 FDE？附能力路径与经验分享](https://x.com/Formulasearch/status/2084158215596486804)
- 小樹, [純乾貨！零基礎小白怎麼開始做 FDE？拆解觀猹課程](https://x.com/AmberTreelet/status/2088890051862430040)
- Miles Ma, [昨天在深圳做完 FDE 路演，我更確定：企業真正缺的不是模型](https://x.com/miles_mazy/status/2087516591244361755)

## Relevant practice signals

The article describes an FDE as an engineer who enters a real operating environment, clarifies the business problem, builds production-grade integrations and controls, follows the capability into use, and remains accountable for adoption and business results. The following signals are consistent with this project's current direction:

- A request is only a starting point; delivery is judged by an operating result.
- Current work, exceptions, data, permissions, recovery, and success measures must be understood before implementation.
- A demonstration is not a production capability. Integration, access control, evaluation, observability, human review, and failure handling remain delivery responsibilities.
- Post-release evidence should include whether users continue using the capability, accept its recommendations, correct it, reject it, or return to the previous workflow.
- Repeated field learning should become reusable product or capability assets rather than project-specific rework.
- Delivery authority and operating incentives matter: a nominal owner who cannot change the workflow, allocate attention, or accept the outcome cannot sustain the intervention.
- A successful FDE engagement should reduce dependence on the individual FDE by leaving a maintained workflow, explicit definitions and controls, reusable assets, and people who can continue operating it.
- Evaluation should begin with the delivery contract and representative operating cases, not after a polished demonstration is complete.
- Failures should be diagnosed at the responsible layer—process, source, semantic definition, access, tool or integration, model, or human decision—before selecting a remedy.
- Delivery has two connected loops: platform or product capabilities move into the field, while validated field learning returns as reviewable capability-change candidates.
- Evidence types must not impersonate one another. A requirement, calculation, simulation, measurement, supplier declaration, and certification support different claims and decisions.
- AI may help propose, implement, and review work, but accountable humans retain authorization, fact acceptance, release, and production responsibility.

These points reinforce, rather than replace, the repository's scenario-to-action method, read-before-write guardrail, and governed capability-evolution loop.

## Project feedback

### Already covered

- The scenario record requires an owner, process node, users, decision or action, baseline, target, sources, and acceptance criteria.
- `Frame -> Map Work` requires process diagnosis and redesign before technology selection.
- The first accepted capability is a trusted read-only inquiry with semantic version, source evidence, freshness, and access decision.
- Persistent actions remain named, authorized, auditable, idempotent, and recoverable.
- Cross-scenario reuse and governed change are explicit maturity goals.

### Useful addition

Adoption evidence should be made explicit in the first real scenario and pilot. In addition to the operating outcome, the team should record:

- usage frequency and sustained use;
- recommendation acceptance, correction, rejection, and override reasons;
- exceptions requiring human intervention;
- abandonment and fallback to the previous workflow;
- whether observed deviations should change the process, semantic assets, decision logic, controls, or application.

Use the existing `metrics` and `acceptanceCriteria` fields for the first scenario. Promote adoption concepts into the scenario schema only after a real scenario shows that they are stable and reusable.

The second article adds an organizational test that adoption measures alone do not cover. Before delivery, scenario framing should establish:

- whether the process owner has the authority and incentive to accept the target workflow;
- which affected roles must approve or cooperate with the change;
- which role owns operation and maintenance after the FDE engagement;
- what reusable process, semantic, decision, tool, or control asset the engagement is expected to leave behind.

An assigned name or title does not prove these conditions. Until direct enterprise evidence establishes them, record them as `missing` or `proposed` and keep the delivery boundary correspondingly narrow.

The third article adds useful delivery detail. Before building the first slice, prepare a small, versioned evaluation set that covers:

- normal cases with sufficient evidence;
- incomplete evidence that requires clarification or abstention;
- conflicting rules or sources that require escalation;
- boundary and prohibited cases;
- representative historical failures when they exist.

For each failed case, preserve enough execution evidence to distinguish a workflow defect from a source, semantic, authorization, integration, model, or human-decision problem. The correction may belong in the process, definition, decision logic, control, tool interface, evaluation set, or model behavior; a prompt change is not the default remedy.

The article also suggests preferring stable system interfaces over UI automation. Record this as an integration-selection hypothesis rather than a fixed architecture rule: use an evidenced, authorized API or structured tool interface when it is the simplest reliable seam; treat UI automation as a fallback whose brittleness, observability, permission, and recovery requirements must be tested in the real scenario.

The fourth article sharpens the completion boundary. A field deployment should close two distinct loops:

1. **Operating handoff.** Leave the target organization with a supportable workflow, source and semantic definitions, controls, evaluation evidence, operating instructions, known failure boundaries, and a named maintenance owner.
2. **Capability return.** Submit de-identified field learning as explicit process, semantic, decision, tool, evaluation, model, or control change candidates for accountable review, versioning, release, and maintenance.

A customer-specific workaround is not automatically a reusable asset. Promotion requires the repository's existing tests: repeated and accepted work, a specifiable contract, replay or shadow evidence, accountable acceptance, and a versioned, observable, reversible release path.

The article proposes a useful evidence vocabulary: `requirement`, `calculated`, `simulated`, `measured`, `supplier-declared`, and `certified`. Treat this as a proposed classification vocabulary, not a universal ranking. The important rule is provenance integrity: preserve the source, method, conditions, assumptions, freshness, and reviewer needed to reproduce or recheck a claim, and never upgrade its evidence type without new evidence and accountable review.

### Proposed pilot default

For planning, use a small time-bounded pilot with real users as a proposed default: one accepted scenario, a narrow read-only or advisory slice, a small group of affected users, and enough repeated use to observe adoption and fallback behavior. The article suggests three to five users for two weeks; those numbers are a starting hypothesis, not a project requirement. The accountable process owner must accept the actual cohort, duration, baseline, thresholds, and expansion decision.

## Evidence ledger

| Statement | Status | Evidence and restriction |
| --- | --- | --- |
| The reviewed articles advocate production delivery, real-user use, outcome measurement, and reusable field learning | `evidenced` | Directly stated in the linked articles; useful as external practice signals only |
| These themes align with the repository method and guardrails | `evidenced` | `FDE-Scenario-to-Action-Method.md` and `FDE-Capability-Enhancement-Plan.md` |
| Adoption measures should be recorded in the first real scenario | `proposed` | Project design decision recorded by this note; requires confirmation through scenario work |
| Process-change authority, incentives, and post-engagement maintenance ownership should be checked explicitly | `proposed` | Supported by the second article's failure analysis and consistent with the repository's accountable-owner model; requires target-enterprise evidence |
| A representative evaluation set and failure-layer diagnosis should precede implementation | `proposed` | Supported by the third article and consistent with the repository's decision tests, validation strategy, and capability-evolution loop |
| Stable APIs or structured tool interfaces should always be preferred over UI automation | `proposed` | Useful default hypothesis, but the simplest reliable seam depends on evidenced target-system constraints, permissions, and failure modes |
| A field deployment should complete both an operating handoff and a governed capability-return loop | `proposed` | Supported by the fourth article and directly aligned with the repository's compounding maturity target |
| Requirement, calculated, simulated, measured, supplier-declared, and certified should become the project's evidence taxonomy | `proposed` | Useful vocabulary from the fourth article; requires comparison with real scenario evidence and existing provenance contracts before schema adoption |
| AI cannot transfer authorization or accountability from the named human owner | `evidenced` | Established by the repository control boundary; AI may propose, implement, or review but cannot approve its own facts, scope, authority, or release |
| Three to five users for two weeks is the correct pilot design | `unverifiable` | Article recommendation; depends on the real workflow, frequency, risk, and owner decision |
| The articles' market-growth, investment, hiring, policy, salary, or career claims are accurate | `unverifiable` | Not independently researched for this note and not used as project evidence |
| A target enterprise has approved users, sources, permissions, baseline, target, or acceptance criteria | `missing` | No real scenario evidence supplied; implementation and authority remain bounded accordingly |

## Next accountable action

The FDE delivery owner should nominate the first real operating scenario and bring its process owner and affected users into scenario framing. Completion means the scenario record identifies the workflow, accountable owners, baseline and target, sources, acceptance criteria, proposed adoption evidence, process-change authority, post-engagement maintenance owner, and expected operating-handoff and capability-return outputs; the accountable roles must then accept or correct the pilot boundary before delivery begins.
