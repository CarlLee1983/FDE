# FDE Skill Evaluation Contract

Use this contract for forward evaluations of `fde-project-work`. It tests the skill's response behaviour against a generic operating case; it does not test whether the case supplies target-enterprise evidence.

**Score the response behaviour, not the completeness of the case input.** Input gaps are case conditions that the response must expose and handle.

## Run

1. Record the repository revision, skill blob, case input, evaluator identity, and evaluator instruction.
2. Ask the evaluator to read the skill in full and return its five-part minimum operating solution.
3. Score the response against every criterion below and cite the response evidence for each decision.
4. Preserve the evaluator's original score. If adjudication changes it, record both scores and the reason.
5. Classify the result as a runtime defect, evaluation-contract defect, case-specific limitation, or no defect.

## Score the response

Assess whether the response:

1. bounds the user, workflow location, operating outcome, and decision;
2. accounts for normal, exception, escalation, and rework paths;
3. redesigns work before selecting technology;
4. compares proportionate interventions and treats AI as optional;
5. preserves evidence, authority, and value boundaries;
6. leaves an accountable owner with an observable next action.

Missing enterprise evidence is not a failure when the response exposes the gap, restricts its claim or action, and gives an accountable validation path. A response fails when it invents the missing fact, ignores a material gap, or cannot form a safe next decision because of it.

## Complete

A run is complete when every criterion has a decision and response citation, every score difference is adjudicated, provenance limits are explicit, and any proposed runtime change is tied to a reproducible response failure.

## Recorded runs

- [Operating-analysis forward evaluation](2026-08-28-p0-forward-evaluation.md) — varied, failure-seeking, and evaluator-contract repeat cases.
- [Scenario-preparation mode](2026-08-28-scenario-preparation-mode.md) — proposed schema-valid record with visible evidence gaps and an owner decision frontier.
- [Conditional delivery and assurance](2026-08-28-p2-conditional-modes.md) — tested local read-only build and persistent-write gate review.
- [New-evidence reconciliation](2026-09-09-new-evidence-reconciliation.md) — baseline and post-change runs on information arriving after a conclusion, scope-separated coexistence, and an ordinary analysis control case. Round 2 re-adjudicates case B for scope over-reach, tests fact verification against a knowing role, verifies an in-place partial update of a case document by file diff, and adds an independent adjudicator over all its answers. Round 3 re-adjudicates case B3 for task completion — an analysis the user explicitly asked for that was returned as an option — and re-runs it with two regressions covering information without a request and a system change requested after the analysis. A blind adjudicator over round 3 disagreed on one of thirteen conditions, recorded there as a FAIL. The report closes with the batch status across engineering verification, behaviour evaluation, and real-world application, and with two limitations carried forward: evidence fields left untagged in one answer, and a completion level overstated in another.

## Continue or stop

Run another evaluation only when there is a new independent operating case, an observed response or scoring failure, an explicit task-mode request that lacks coverage, or repeated cross-case evidence that may justify a core candidate. State the hypothesis and observable failure before adding the case.

When none applies, evaluation is complete for the current evidence. Use the skill on a real operating problem or stop; do not add synthetic cases to increase file or case counts.

## Real-case trial

**Status: not started.** No real enterprise case has been run. Until one is, do not fabricate enterprise facts and do not add further synthetic cases in place of a trial.

Run a trial as ordinary use, not as a new process. It needs no new tooling and no fixed document bundle.

1. The user brings one real operating problem with a stated scope.
2. The skill returns the five-part minimum operating solution.
3. The user adds a new fact, a contradicting one, or an explicit request to extend the analysis.
4. Check that the response did what was asked, revised only what depends on the new information, and kept its evidence and authority limits.
5. Keep what is needed to re-read the run — input, response, skill revision, user feedback — under the access and retention rules that apply to the case material. Real case content does not enter this repository unless those rules allow it.

What to watch for, all of them observed from the response itself:

- an important piece of evidence used without its time, version, or scope;
- an evidence-incomplete proposal described as executable, approved, or ready for release;
- asking again about work the user already assigned;
- the case scope widened by the response rather than by the user;
- a next step too vague for the accountable owner to act on.

A trial that reproduces one of these is the evidence a further change needs. A trial that does not is the first real-world support this skill has.
