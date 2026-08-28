# Account reconciliation reference request

Create a generic, workflow-first account-reconciliation example that can be replayed without enterprise systems or AI.

The example should first separate exact matching, human exception review, and accounting action. Its first slice must remain deterministic and read-only: match only unique bank and ledger entries with the same versioned reference, currency, integer minor-unit amount, and booking date; send every ambiguous, mismatched, or single-sided item to a human review queue; and fail closed when evidence, freshness, identity, access, or the declared contracts are invalid.

This repository request establishes only the shape of a common operating case. Target-enterprise process ownership, current workflow acceptance, sources, access, baseline, target, policy acceptance, and value evidence remain `missing` or `unverifiable`.
