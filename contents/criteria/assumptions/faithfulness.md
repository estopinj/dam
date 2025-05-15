---
title: Faithfulness
parent: Assumptions
nav_order: 7
permalink: /faithfulness
---

# Faithfulness

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | No independencies beyond graph structure. |
| `Recommended` | Likely no independencies beyond graph structure. |
| `Desirable` | Desirable but not verified per se. |
| `Relaxes assumption` | Allows near‐faithfulness or weak dependencies. |

## Definition
Whether the method assumes that all and only the independencies entailed by the causal graph appear in the data (no coincidental cancelation of paths). 

## Explanation
Ensures that observed independence relations in the data reflect the true graph rather than coincidences. Like the Causal Markov Condition, it is a key assumption for many causal‐discovery algorithms. Even for methods outside the causal discovery realm and not relying on causal graphs, this assumption is often done implicitly. 

## Tools/rationale for helping assessment
Based on your system knowledge and ecological theory, reflect on your ecosystem’s complexity and whether causal effects are unlikely to exactly cancel: 
1. Draw a causal diagram of your system, identifying all hypothesized pathways from exposure to outcome. 
2. Use domain knowledge to ask whether any two or more pathways could perfectly offset each other in magnitude and direction. 
3. If no plausible cancellation mechanisms exist, you can assume faithfulness holds (`Required`); if offsetting effects are possible, faithfulness may be invalid: Minor cancellations possible, `Recommended`; if complex interactions may cancel, `Desirable`; if you cannot assume any and/or want to specifically study this assumption’s influence on results, `Relaxes assumption`. 

## Example
In a study of fire frequency → grassland productivity, ecologists know that fire consistently enhances nutrient availability and thus productivity - there is no plausible mechanism that would reduce productivity by the same amount to cancel the increase. Therefore, they conclude faithfulness is valid.
