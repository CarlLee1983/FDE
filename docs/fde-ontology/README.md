# Ontology-Driven FDE Enterprise Delivery: Chapter Study

This document set decomposes the source architecture diagram into independently readable topics. Statements explicitly present in the diagram are labeled **Diagram definition**. Implementation guidance inferred from it is labeled **Recommendation**, so the two are not conflated.

## Reading Map

| Chapter | Research question | Key outcome |
| --- | --- | --- |
| [01. Problem Framing and Feedback Loop](01-problem-framing-and-feedback-loop.md) | Why pair ontology with FDE instead of building isolated AI applications? | Value chain, feedback loop, and success conditions |
| [02. Enterprise Ontology and Semantic Model](02-enterprise-ontology-and-semantic-model.md) | What makes up a single semantic source of truth? | Objects, links, actions, and asset specifications |
| [03. Data Integration and Knowledge Governance](03-data-integration-and-knowledge-governance.md) | How do data, documents, and experience become trustworthy ontology assets? | Ingestion lifecycle, quality controls, and lineage |
| [04. FDE Delivery Method](04-fde-delivery-method.md) | How does an embedded delivery team turn a pain point into a running capability? | Five phases, roles, and acceptance criteria |
| [05. Platform Capabilities and Application Operations](05-platform-capabilities-and-application-operations.md) | What does a platform need to run AI applications safely? | Governance, orchestration, runtime, and write-back controls |
| [06. Operating Governance and Adoption Roadmap](06-operating-governance-and-adoption-roadmap.md) | How does one-off delivery become a continuously evolving operating model? | Governance, metrics, risks, and rollout order |
| [07. Capability Map and Implementation Strategy](07-capability-map-and-implementation-strategy.md) | Which capabilities should be built or strengthened first? | Module seams, vertical slices, and validation criteria |
| [08. FDE Capability Enhancement Focus](08-fde-capability-enhancement-focus.md) | How is the reference model applied to the FDE capability goal? | Capability targets, maturity sequence, and the first buildable contract |
| [09. FDE Scenario-to-Action Method](09-fde-scenario-to-action-method.md) | How should FDE analyse and prepare a capability before delivery? | A lightweight composition of established system-analysis methods |

## Shared Terms

| Term | Meaning in this document set |
| --- | --- |
| FDE | Forward Deployed Engineer: an engineer embedded in a concrete business setting who translates operating problems into working capabilities. |
| Ontology | A semantic model for enterprise objects, links, actions, and their governance metadata. |
| Single semantic source of truth | One shared definition for a business concept across data, processes, analytics, and AI applications. |
| Business application | A dashboard, agent, or workflow, as shown in the diagram. |
| Ontology asset | A defined, governed, traceable object, link, or action that can be reused. |

## Source and Scope

- The primary source is the user-provided architecture diagram, *Ontology-Driven FDE Enterprise Delivery Architecture*.
- The diagram is not treated as evidence of an already implemented system, nor does this documentation assume a specific vendor, database, or model provider.
- Rollout sequencing, acceptance gates, data-quality controls, and security controls are recommendations. They need to be validated against the target enterprise before implementation.
