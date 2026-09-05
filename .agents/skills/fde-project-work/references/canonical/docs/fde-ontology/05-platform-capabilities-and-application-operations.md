# 05 | Platform Capabilities and Application Operations

Back to the [chapter index](README.md).

## Diagram Definition

The platform foundation contains four capabilities: data governance and real-time synchronization; model and agent orchestration; permission governance and audit; and version management and rollback. It supports the enterprise ontology and FDE delivery engine; it does not replace either.

## Capability Breakdown

| Capability | Problem addressed | Minimum verifiable outcome |
| --- | --- | --- |
| Data governance and synchronization | Applications use stale, incorrect, or untraceable data | Observable sync status, source, and freshness |
| Model and agent orchestration | Models, prompts, tools, and task flows are scattered | Configurable agent tasks, tool boundaries, and execution records |
| Access control and audit | Users or agents access data/actions beyond their remit | Queryable identity, asset, action, and audit records |
| Versioning and rollback | Ontology or application changes disrupt operations | Identifiable versions, comparable changes, and a known good recovery point |

## Application Forms and Control Boundaries

| Application form | Typical use | Risks to control |
| --- | --- | --- |
| Dashboard | Exposes operating and management metrics | Definition consistency, freshness, and source drill-down |
| Agent | Queries, summarizes, reasons, or recommends | Tool permissions, source context, unsupported claims, and unexplained recommendations |
| Workflow | Dispatches, approves, notifies, or writes to systems | Preconditions, human approval, idempotency, and failure compensation |

The diagram includes approval, dispatch, and system write-back actions. **Recommendation:** operate with three permission tiers: read-only query, recommendation, and controlled execution. Approval and audit requirements should increase as an action approaches an external or persistent effect.

## Typical Runtime Path

```text
User or workflow trigger
→ obtain permitted ontology context and data
→ agent / rule / workflow evaluates the request
→ display result, propose action, or request approval
→ execute controlled action
→ record input, evidence, output, and outcome
→ write back to business system and update relevant ontology state
```

On failure, accountable operators need enough evidence to distinguish a data issue, rule issue, system issue, or access issue and to run compensation or rollback.

## Interface Principle

**Recommendation:** applications should consume business objects, links, and actions through the ontology boundary rather than directly depend on source-system internal field names. This confines source-system changes to the connectivity and mapping layer and reduces cascading application changes.

## Questions to Resolve

1. Which systems are readable today, and which systems permit write-back?
2. Are there existing identity, authorization, audit, or workflow platforms to reuse?
3. Which high-impact actions require human approval or dual control?
