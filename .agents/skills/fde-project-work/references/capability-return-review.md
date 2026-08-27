# Capability-return review

Use this output contract after a case slice reveals learning that might be reused or change FDE core. Read `Capability Ownership and Return` in the canonical implementation strategy before deciding ownership or promotion.

## Review contract

1. **Source case and evidence boundary.** Identify the case, capability version, direct runtime or operating evidence, validation result, and whether evidence is synthetic, shadow, or production.
2. **Observed behaviour.** Name each behaviour precisely and cite the case artefact, test, correction, exception, or outcome that exposed it.
3. **Ownership classification.** Assign exactly one status:
   - `case-specific`: domain behaviour retained and versioned with the case;
   - `existing-core-invariant`: behaviour already required by a canonical FDE source; the case tests but does not redefine it;
   - `proposed-candidate`: possibly reusable non-domain complexity awaiting the canonical promotion criteria;
   - `rejected-generalization`: similarity is superficial, authority-changing, or would expose domain complexity through a shared Interface.
4. **Candidate Interface.** For each `proposed-candidate`, state the smallest domain-neutral Interface, the repeated Implementation complexity it would hide, and the independent scenarios or adapters that establish a real seam. Mark absent recurrence evidence `missing`.
5. **Promotion decision.** Return `retain-in-case`, `candidate-only`, `promote`, or `reject`, citing every applicable canonical promotion criterion. A case author or agent cannot approve its own promotion.
6. **Validation and rollback.** Name the replay sets, expected equivalence, version owner, release evidence, and independent rollback for every affected case. Mark unavailable evidence explicitly.
7. **Next accountable action.** Name the owner role, required evidence or second scenario, and observable completion criterion.

## Completion criterion

Every observed behaviour has one owner and one promotion status. No case-specific term or rule enters FDE core, and no candidate is described as shared capability before all canonical promotion criteria pass.
