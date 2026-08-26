# 06 | Operating Governance and Adoption Roadmap

Back to the [chapter index](README.md).

## Diagram Definition

The architecture routes delivery results back to business systems and the ontology layer. It also connects ontology assets to periodic review, a review cycle, and accountable owners. Ontology and applications therefore require an operating model after project delivery.

## Governance Objects and Responsibilities

| Object | Main responsibility | Recurring activity |
| --- | --- | --- |
| Business definitions | Keep definitions aligned to real operations | Approve change, resolve metric disputes, authorize exceptions |
| Ontology assets | Maintain objects, links, actions, and lineage | Release versions, review assets, retire obsolete assets |
| Data sources | Keep data available, accurate, and compliant | Monitor sync, address quality issues, update access |
| AI applications | Keep outputs useful, safe, and operable | Review execution records, measure impact, tune operating flow |

## Recommended Adoption Roadmap

### Phase A: choose a high-value, narrow scenario

Choose a flow with obtainable data, a clear owner, and measurable value. The aim is to complete one usable loop, not to model the entire enterprise.

### Phase B: build a minimum ontology and trusted data path

Define core objects, links, actions, permissions, and sources so the first dashboard or agent can perform a specified task with traceable evidence.

### Phase C: shadow operation and controlled delivery

Run old and new approaches in parallel. Test definitions, data quality, usability, and exceptions. Keep high-impact actions human-approved until results are stable.

### Phase D: handover and assetization

Complete SOPs, accountability, review cycles, version management, and rollback. Add reusable model components to the enterprise ontology.

### Phase E: expand to adjacent scenarios

Reuse existing objects, links, and actions first, then add only what the new scenario needs. Prevent semantic forks by checking each expansion against the shared source of truth.

## Recommended Metric System

| Level | Examples | Purpose |
| --- | --- | --- |
| Business outcome | Revenue, cost, throughput time, error rate | Validate business value |
| Use and adoption | Active users, completion rate, human-intervention rate | Confirm incorporation into real work |
| Asset health | On-time review, data-quality exceptions, ontology reuse | Assess whether semantic assets remain viable |
| Risk control | Permission denials, approval overrides, write-back failures, rollbacks | Monitor safety and operating risk |

## Main Risks and Responses

| Risk | Early signal | Response |
| --- | --- | --- |
| Unresolved definition disputes | Users repeatedly report different figures for the same metric | Assign a business definition owner and resolve high-frequency disputes first |
| Insufficient data quality | Applications require frequent manual correction or results cannot be reproduced | Set release quality gates and an exception process |
| Excessive AI authority | An agent can update a critical system without audit | Layer permissions: recommend, approve, then limited automation |
| Unmaintained assets | SOPs change while ontology and applications retain old rules | Establish review cycles, owners, and retirement procedures |
| Demo-only proof of concept | A dashboard looks good but never affects work | Accept only against real decisions, actions, and result metrics |

## Expansion Decision Checklist

Before scaling, the team should be able to answer yes to the following:

1. Is there a validated first scenario with an accountable owner?
2. Can critical data, ontology assets, and metrics be traced to authoritative sources?
3. Do controlled actions have access controls, approval, audit, and failure handling?
4. Has shadow operation explained the old/new definition differences?
5. Is there an ongoing operating and review mechanism for the ontology, applications, and data sources?

## Closing Principle

The diagram’s message can be summarized as: ontology is the asset; applications are delivery containers. Applications can change by scenario, but shared enterprise understanding of objects, links, actions, and accountability should compound over time. Maturity is not the number of agents built—it is whether each delivery makes the next one faster, more trustworthy, and easier to govern.
