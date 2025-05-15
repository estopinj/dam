---
title: Estimand
parent: Outcome
nav_order: 2
permalink: /estimand
---

# Estimand

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `ATT` | Average Treatment effect on the Treated: The mean effect for the units that actually received treatment. |
| `ATE` | Average Treatment Effect: The mean effect if the entire population were treated versus untreated. |
| `LATE` | Local Average Treatment Effect: The mean effect for units whose treatment status is affected by an instrument or cutoff. |
| `CATE` | Conditional ATE: The effect conditional on specific covariate values or subgroups. |
| `Mediation effects` | Decomposes the total effect into direct and indirect (mediated) components. |
| `Oriented link` | Identifies the existence and directions of associations (edges) in a causal graph without quantifying effect sizes. |
| `Risk ratios` | The ratio of outcome probabilities between treated and control groups (and derivatives). |
| `Maps & generalisations` | A model projection is the main method target, be it in space or time, rather than a causal effect. |
| `Others` | Any specialized causal or association measure not listed above. |


## Definition
The specific target quantity or causal parameter that the method seeks to estimate when precisely defined or more general quantities otherwise. 

## Explanation
Identifying the estimand clarifies what aspect of attribution or association the method recovers and for which subpopulation (e.g., all units, treated units only). This ensures alignment between your scientific question and the statistical target of inference.

## Tools/rationale for helping assessment
Sketch a simple DAG of your system to identify which causal parameter answers your question. For more materials on causal effects definitions, see [Igelström et al. (2022)](https://doi.org/10.1136/jech-2022-219267){:target="_blank"} *Defining causal effects* section, and [Lundberg et al. (2021)](https://www.jstor.org/stable/48632961){:target="_blank"}.

## Example
- A landscape ecologist studying selective logging chooses `ATT` to estimate the average canopy-loss effect on logged forest pixels only and uses `risk-ratios` for bird occupancy comparisons. 
- My DAG shows I care only about treated (disturbed) pixels’ biodiversity loss, so I pick `ATT`; I also want a spatial map of effects, so I note `Maps & generalisations` alongside. 