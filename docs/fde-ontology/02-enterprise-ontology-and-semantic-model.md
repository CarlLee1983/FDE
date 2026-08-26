# 02 | Enterprise Ontology and Semantic Model

Back to the [chapter index](README.md).

## Diagram Definition

The enterprise ontology layer is the “single semantic source of truth.” It contains the following elements.

| Element | Diagram examples | Purpose |
| --- | --- | --- |
| Objects | Customer, order, equipment, work order | Represent business entities |
| Links | Customer—order—production line—supplier | Represent business connections between entities |
| Actions | Approval, work dispatch, write-back to a system | Represent actions that may be executed or recorded |
| Permissions and lineage | Permission, owner, data source | Make assets governable and auditable |

## Why an Ontology Is a Semantic Boundary, Not a Database Schema

Database schemas serve storage and transactions. An ontology serves business meaning and cross-system relationships. One customer may appear in a CRM, ERP, service log, and document. The ontology defines when these records represent the same customer, which source is authoritative, who may access it, and how it links to orders or work orders.

Source-system structures can change. Stable enterprise concepts such as customer, order, and dispatch should remain understandable and governable across those changes.

## Minimum Viable Model

**Recommendation:** begin with the smallest complete set required by one scenario, not a full enterprise model.

```text
Objects: Customer, Order, Work Order, Equipment
Links: Customer owns Order; Order triggers Work Order; Work Order uses Equipment
Actions: Query Order, Create Work Order, Dispatch, Approve, Write Back
```

Every element should answer a business question or support an action. Defer elements without a current consumer.

## Asset Specifications

### Objects

| Field | Description |
| --- | --- |
| Name and business definition | Plain-language scope and explicit exclusions |
| Identity rule | Unique key, cross-system mapping, and deduplication rule |
| Key attributes | Status, time, monetary, or classification data required by the scenario |
| Authoritative source | The system or process with final write authority |
| Quality rules | Completeness, validity, freshness, and exception handling |

### Links

| Field | Description |
| --- | --- |
| Relationship name | Business verb, for example, “Customer places Order” |
| Start and end | The two object types connected |
| Cardinality and validity | One-to-one, one-to-many, or many-to-many, plus effective dates |
| Evidence source | System, document, or human-confirmation source |
| Constraints | Invalid combinations, prerequisites, and exceptions |

### Actions

| Field | Description |
| --- | --- |
| Action name and intent | For example, dispatch creates an accountable assignment |
| Trigger | Person, system, workflow, or agent |
| Input and preconditions | Required objects, permissions, state, and approval conditions |
| Effect | Records created, changed, notified, or written back |
| Audit record | Caller, time, input, output, outcome, and failure reason |

## Versioning and Compatibility

The diagram includes version management and rollback. **Recommendation:** treat ontology definitions as versioned assets: propose and scope a change, test it in a shadow environment, obtain owner approval, then release it with a known rollback point. A change to an order state or customer definition may require every dependent dashboard, agent, and workflow to be revalidated.

## Questions to Resolve

1. Which objects, links, and actions are essential to the first scenario?
2. What are the authoritative sources and identity rules for the core objects?
3. Are there existing data dictionaries, master data, or process definitions that can serve as initial evidence?
