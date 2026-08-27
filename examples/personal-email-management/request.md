# Demo request

> **Synthetic demo only.** This request, its email content, users, permissions, baselines, and outcomes are invented to demonstrate the FDE method. It is not evidence that any mailbox provider or user has authorized access.

An individual receives work, personal, account, newsletter, receipt, and notification email in the same inbox. Important messages compete with bulk mail, and the person repeatedly scans the inbox to decide what needs a reply, what has a deadline, and what can wait.

Design a proposed FDE workflow that produces a daily inbox review and action list from permitted email metadata and content. The first slice must remain read-only with respect to the mailbox: it may group messages and show evidence. If it stores a user's review decision, that separate write must be explicitly authorized, auditable, idempotent, and removable under an accepted retention policy. It must not send, delete, archive, unsubscribe, or change mailbox state.

After the review workflow and deterministic baseline are validated, evaluate an AI shadow for thread summaries, action extraction, deadline detection, and reply drafts. Every AI output must link back to the source message, express uncertainty, abstain when evidence is insufficient, and remain subject to user confirmation.
