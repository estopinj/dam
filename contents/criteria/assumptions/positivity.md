---
title: "Common support"
parent: Assumptions
nav_order: 5
permalink: /positivity
categories:
- criteria
- assumptions
---

# Common support (positivity)

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | Strict overlap needed for valid comparison. |
| `Recommended` | Strongly advised. |
| `Desirable` | Improves precision. |
| `Relaxes assumption` | Methods can tolerate some lack of overlap (e.g., regularization). |

## Definition
The method requires overlap in the covariate distributions of the treated and control units, which is also known as the *positivity* assumption.

## Explanation
Lack of overlap (regions with only treated or only control units) forces models to extrapolate beyond data, risking bias. Some methods strictly require common support; others can tolerate limited gaps.

## Tools/rationale for helping assessment
1. Tabulate key covariates (e.g. canopy cover, slope) by treatment group / compute propensity scores; check if ranges overlap. 
2. If there’s overlap across the full range, mark `Required`; if minor gaps, `Recommended`; if some extrapolation but acceptable, `Desirable`; if severe gaps, `Relaxes assumption` to specifically study this assumption’s influence or try limiting the study scope to recover overlapping covariate range. 

## Example
After matching on slope and elevation, treated and control plots overlap only in slope ∈ [5,25°], so I restrict analysis to that band and mark `Required`. 
