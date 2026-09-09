---
status: accepted
---

# Recompute only what the new information depends on

New information arriving after a conclusion triggers a recompute only when it changes a fact, rule, or assumption that conclusion depends on. Information under a different market, product line, amount band, role, system, or time window with no such dependency leaves the conclusion, its target workflow, and its controls unchanged, and creates no recompute task and no new open decision. A cross-scope comparison, a control simplification, an approval matrix, or a wider process may be offered as an option carrying its reason and cost; it never becomes a work requirement. When the case's own scope is not stated, it is asked about rather than assumed to be a global rule.

The trade-off is deliberate. Recomputing eagerly looks more thorough and is the behaviour a later reader is likely to restore: one market's observation appears to justify revisiting every market. It is not free. Each unnecessary recompute converts a bounded case into a wider redesign the user did not request, reopens settled controls on the strength of an out-of-scope observation, and puts work on an accountable owner's list that no evidence supports. Under-expanding is recoverable — the user asks for the comparison, and the analysis expands on request. Over-expanding is not visibly wrong, so it is not caught.

The same separation applies to who is asked what. Facts reachable from supplied material, repository sources, or safely inspectable systems are investigated, not handed back as questions; facts out of reach — missing data, missing access, or something only on-site experience can confirm — are requested as evidence from a role that holds them; policy change, scope trade-offs, and authorization go to the accountable role. Asking a knowledgeable role for a fact is not asking for a decision.

**Falsified if:** `.agents/skills/fde-project-work/references/collaborative-clarification.md` or `.agents/skills/fde-project-work/SKILL.md` requires recomputing a conclusion that the new information's scope does not touch, turns a cross-scope comparison or control change into a required task or an open decision the user must close, assumes an unstated scope is global, or states that people may be asked only for decisions.
