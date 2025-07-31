---
title: "No unobserved confounders"
parent: Assumptions
nav_order: 2
permalink: /nounobserved
categories:
- criteria
- assumptions
---

# No unobserved confounders

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | Method assumes no unobserved confounders. |
| `Recommended` | Best practice but not strictly enforced. |
| `Desirable` | Improves performance but not essential. |
| `Relaxes assumption` | Can tolerate some unmeasured confounding (e.g., DiD). |
| `Time-varying OR site-varying` | Assumes confounding is either time‐invariant and site-specific or time-varying but common to all sites. |

## Definition
Whether the method requires that all variables confounding the treatment-outcome relationship are observed and controlled or is designed to handle acknowledged / suspected unobserved confounders.

## Explanation
Unmeasured confounding can bias causal estimates when not accounted for at all. However, many methods do need this key assumption to reach effect estimations, be it explicitly or implicitly. A few other methods are designed to relax this strong hypothesis, e.g. relying on specific data structures (regression discontinuity design). This assumption is also called *causal sufficiency* especially in the causal discovery literature, or *conditional exchangeability*. When no unobserved confounders are assumed, a strongly advised verification is to lead a sensitivity analysis to test the result robustness. 

## Tools/rationale for helping assessment
1. From your field knowledge, list all variables that influence both exposure and outcome and draw a causal graph to check for potential strong but unavailable confounders. 
2. If you are confident that you have measured every major confounder, mark `Required`; if you aim to but may miss some, `Recommended`; if measurement would help but is not central, `Desirable`; if you lack key confounders, `Relaxes assumption`.  
3. Perform sensitivity analysis afterwards to challenge estimated effects against unobserved confounding. 


## Example
- In a study linking deforestation to species loss, an unmeasured “road proximity” confounder is identified after drawing a causal graph.  Since this data is available on the national data portal, it is added to the study and the assumption can hold: I can use a method requiring causal sufficiency.

- You have data on soil pH, moisture, elevation and NDVI → you believe no major confounders remain, so `Required`. If you lack soil pH, but it’s marginal, you mark `Recommended`. If, on the contrary many unknowns exist, you choose a design (e.g. DiD) that relaxes this assumption.
