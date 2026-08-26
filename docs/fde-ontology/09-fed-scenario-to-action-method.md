# 09 | FED Scenario-to-Action Method

Back to the [chapter index](README.md).

The project-level [FED Scenario-to-Action Method](../../FED-Scenario-to-Action-Method.md) is the working methodology for turning a business scenario into a governed FED capability.

## Why a Method Pack

The FDE architecture describes layers and delivery flow but does not by itself prescribe how to analyse a problem, distinguish process from decision logic, govern semantic assets, or evaluate automation risk. FED therefore uses a lightweight method pack composed from established system-analysis methods.

| FED concern | Method used | Result |
| --- | --- | --- |
| Bounded business outcome | Requirements engineering | An approved scenario and acceptance criteria |
| Process versus exception work | BPMN / CMMN | A process or case model with a specific intervention node |
| Entities, relationships, and lifecycle | UML structure/state modelling | Separate structure and state definitions |
| Reusable semantics and source mapping | ISO/IEC 11179 registration pattern | Governed semantic assets with identity and lineage |
| Decision or rule logic | DMN | A named, testable decision service |
| Access, actions, and monitoring | NIST RMF | Proportionate controls and authorization evidence |
| Architecture trade-offs | SEI ATAM | Quality scenarios and explicit accepted risks |
| Iterative validation | ISO/IEC/IEEE 15288 | A small vertical slice and feedback loop |

Official-source research, direct links, and the limits of this synthesis are documented in [System-Analysis Methods That Can Inform FED](../research/system-analysis-methods.md).

## Resulting FED Method

```text
Frame → Map Work → Model Meaning → Specify Decision → Assure Control → Prove and Evolve
```

The method prevents common failure modes:

- building an agent before defining the operating outcome;
- treating a workflow as the sole representation of business meaning;
- hiding policy decisions inside prompts or UI behavior;
- enabling write-back before evidence, access, and recovery are trustworthy;
- treating a delivered capability as complete without feedback, ownership, and reuse.

Use the full [method document](../../FED-Scenario-to-Action-Method.md) when preparing the first real FED scenario.
