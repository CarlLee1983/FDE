# 01 | Problem Framing and Feedback Loop

Back to the [chapter index](README.md).

## Diagram Definition

The diagram presents the delivery loop below:

```text
Business topic → FDE in the field → ontology modeling → application delivery → feedback and evolution
```

Business departments, leaders, and frontline experts contribute pain points, metrics, and processes. The output is dashboards, agents, workflows, and traceable delivery records. A management dashboard consolidates outcomes such as revenue, efficiency, and cost.

## Problems Addressed

| Problem | Direct consequence | Architectural response |
| --- | --- | --- |
| Different departments define the same term differently | Reports, processes, and AI outputs conflict | The ontology layer establishes a single semantic source of truth |
| Data and knowledge are split across systems, documents, and people | Applications lack the required business context | The connectivity layer continuously ingests multiple source types |
| AI cannot safely perform business actions | Outputs are not operational or carry excessive risk | Governed actions, permissions, and audit support applications |
| Project results remain with an individual team | Discovery and modeling are repeated; scale is limited | Results are written back and retained in the ontology |

## Value Chain Analysis

### From a topic to a testable problem

“Improve efficiency” is not directly deliverable. FDE must convert it into a specific workflow, user role, decision point, data set, and measurable outcome.

**Recommendation: use a business-topic card with the following fields.**

| Field | Purpose |
| --- | --- |
| Business goal | Revenue, efficiency, cost, quality, or risk to improve |
| Users and owners | Requester, daily users, process owner, and data owner |
| Scenario boundary | Organization, product, process start/end, and exceptions |
| Decision or action | What the user must decide or do after using the application |
| Measurement | Baseline, target, cadence, and evidence source |

### From a problem to an ontology

Ontology modeling is not a renaming exercise for database tables. It answers which objects, relationships, and actions exist in a scenario; who may use them; and under which conditions. This is the boundary that connects data engineering with business rules.

### From ontology to application

When dashboards, agents, and workflows share the same semantic assets, their measures, filters, and actions remain aligned. For example, an agent answering an order question should use the defined `Customer`, `Order`, and relationship between them, rather than inventing a separate prompt-level definition.

### From application back to assets

Exceptions, terminology, data gaps, and new workflow knowledge discovered during delivery should become ontology revision inputs. This feedback path is what makes application use evidence for the next round of governance and modeling.

## Traceability Chain

**Recommendation:** every delivery should be traceable through this chain:

```text
Business topic → scenario and metric → data source → ontology asset version
→ application version → execution / approval record → result metric → ontology revision
```

Without one of these links, results become hard to explain, reproduce, audit, or reuse.

## Success Conditions and Anti-Patterns

| Success condition | Anti-pattern |
| --- | --- |
| The problem has a user, a process node, and a measurement standard | “Build an AI” is itself the entire requirement |
| Ontology and application use the same business definitions | Dashboards, agents, and workflows each define their own terms |
| Results update operating work and ontology assets | A proof of concept ends without an owner or maintenance path |
| A small end-to-end scenario is validated before expansion | The team attempts to model the whole enterprise first |

## Questions to Resolve

1. What is the first business topic, process boundary, and target measure?
2. Who makes final definition decisions, and who maintains those definitions day to day?
3. Is the output advisory, human-approved, or automatically executable?
