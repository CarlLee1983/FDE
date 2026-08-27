# Demo request

> **Synthetic demo only.** This request, its people, data, permissions, baselines, and outcomes are invented to demonstrate the FED method. It is not evidence of a real enterprise authorization or result.

A replenishment planner currently receives an alert only after stock falls below a fixed safety level. By then, supplier lead time and upcoming demand may already make a stockout difficult to avoid.

Design a proposed FED workflow that checks inventory pressure on a schedule, combines inventory, sales history, planned promotions, inbound supply, and supplier lead time, and gives the planner an explainable replenishment recommendation. In the exploratory phase, an AI assistant may synthesize permitted evidence and prepare a purchase-order draft for human review. It must not approve, submit, or write a purchase order by itself.

When repeated recommendations and human corrections reveal a stable method, move that method into a versioned, tested software tool. Keep the AI assistant in the workflow to use the tool, explain unusual cases, identify recurring gaps, and propose the next governed improvement.
