---
title: Causal Markov condition
parent: Assumptions
nav_order: 6
permalink: /markovcondition
---

# Causal Markov condition

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | Must hold exactly. |
| `Recommended` | Advisable if using graphs. |
| `Desirable` | Aids clarity. |
| `Relaxes assumption` | Some methods can handle approximate violations. |

## Definition
Whether the method assumes that each variable is independent of its non‐descendants given its parents in a causal graph (d‐separation). 

## Explanation
Fundamental for graphical causal inference: it ensures that the graph’s conditional independencies mirror the data causal structure. Methods based on DAGs rely on it; others may not. It is a key assumption for some causal discovery algorithms (e.g. constraint-based) but can seem irrelevant for many other methods parts of the navigator (`Inapplicable` can apply).

## Tools/rationale for helping assessment
1. Use domain expertise to enumerate all direct parent variables of each node in your causal graph. 
2. If you are confident that no hidden pathways exist once you condition on those parents, mark `Required`; if you believe the graph is mostly correct, `Recommended`; if important paths may be missing, `Desirable`; `Relaxes assumption` if you target a method focused to specifically study this assumption’s impact on results. 
3. Use partial‐correlation tests (e.g. with dagitty R package) to check if conditioning on parent variables blocks other associations. 

## Example
In my DAG, I test if vegetation index ⟂ precipitation ∣ temperature; a partial correlation (assuming linear relationships) p-value of 0.7 supports the Markov condition and don’t need a method relaxing this assumption. 
