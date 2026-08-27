# Synthetic request: customer refund-status inquiry

This case exists to validate FDE analysis-to-proposal delivery. It is not a target-enterprise engagement and does not establish any real owner, source, permission, baseline, target, integration, or acceptance result.

Every business fact and number in this request is **proposed synthetic**.

- Operating outcome: reduce handling time for customer refund-status inquiries.
- Primary user: customer-service representative.
- Included scope: refund-status inquiry only.
- Excluded scope: refund approval, compensation, payment disputes, direct AI-to-customer responses, and write-back.
- Proposed current flow: receive inquiry, find order, open payment system, inspect refund state, compose response, and escalate exceptions to finance.
- Proposed average handling-time baseline and target: 8 minutes to 3 minutes.
- Quality guardrail: incorrect refund-status responses must not increase.
- Proposed process owner and acceptance owner: customer-service operations lead.
- Proposed semantic and exception owner: finance refund owner.
- Diagnosis hypothesis: cross-system lookup and manual state interpretation are the main delays, not prose composition.
- Supported normalized states: refund not initiated, refund processing, and refund completed.
- Every other state escalates to finance.
- First slice: a read-only refund summary showing source evidence, retrieval time, normalized status, and a response template for human confirmation.
- AI-fit: not needed for the first slice. Retrieval, state mapping, access checks, and exception rules are deterministic.
- Abstain or escalate for missing records, conflicting states, stale data, failed or rejected refunds, payment disputes, or insufficient access.
- Proposed validation: de-identified historical shadow replay; complete mapping for the three supported states; abstention for every missing, conflicting, stale, prohibited, or unauthorized case; average simulated handling time no more than 3 minutes; evidence, retrieval time, and semantic version shown for every result; and acceptance by both named owner roles.
