# 03 | Data Integration and Knowledge Governance

Back to the [chapter index](README.md).

## Diagram Definition

The diagram names three source categories: business-system data (ERP, CRM, MES, IoT); enterprise material (documents, spreadsheets, SOPs, and expert experience); and external domain knowledge (industry, policy, competitors). These sources enter through APIs, data views, file synchronization, or MCP and are collected, cleaned, and aligned before entering the ontology.

## Ingestion Is More Than Importing

The goal is not centralized storage; it is data that can be used with trusted business meaning. Every source should be evaluated across four dimensions.

| Dimension | Key question | Recommended control |
| --- | --- | --- |
| Connectivity | Can it be retrieved reliably? | Define synchronization mode, cadence, failure retry, and monitoring |
| Semantics | What do the fields or document contents mean? | Map them to defined objects, links, and actions |
| Quality | Is the data complete, correct, and timely? | Set quality rules, exception queues, and accountable owners |
| Access | Who may read, edit, or use the data for AI? | Apply least-privilege access to data and ontology assets |

## Recommended Ingestion Lifecycle

```text
Inventory source → confirm ownership and purpose → connect and collect → clean / standardize
→ align semantics → validate quality → publish ontology asset → synchronize and review continuously
```

Standardization commonly includes codes, timestamps, units, status values, organization names, and keys. The crucial question is whether a record truly represents the ontology object or relationship it is mapped to.

## Knowledge Sources Need Their Own Controls

| Source type | Additional information to confirm |
| --- | --- |
| SOP or policy document | Scope, version, effective date, approver, and replacement status |
| Spreadsheet or report | Metric definition, editor, refresh cadence, and formula basis |
| Expert experience | Conditions of use, exceptions, supporting evidence, and ability to become an explicit rule |
| External knowledge | Source, publication date, license, and precedence when it conflicts with internal rules |

**Recommendation:** do not directly convert unverified interview content into an automatically executable action rule. Label it as candidate knowledge until the accountable business owner validates it.

## Lineage and Evidence

The diagram explicitly includes permissions and lineage. A user should be able to trace any answer, metric, or action through:

```text
Source system / document → extraction time → cleaning and transformation rule → ontology asset version
→ application or agent usage record → output or write-back outcome
```

This chain enables data-dispute resolution, compliance review, and outcome investigation.

## Questions to Resolve

1. What are the first sources to ingest, and who owns each one?
2. Which data or documents contain personal, confidential, or restricted information?
3. What quality gate, review cadence, and exception process apply before an asset is made available to applications?
