---
title: Well-defined treatment
parent: Assumptions
nav_order: 4
permalink: /definedtreatment
---

# Well-defined treatment

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | Treatment must be precisely specified. |
| `Recommended` | Best-practice but no strict definitions necessary. |
| `Desirable` | Improves clarity and reproducibility. |
| `Relaxes assumption` | Handles fuzzy or continuous dose‐response exposures. |

## Definition
Whether the method requires a clear, unambiguous definition of the treatment or exposure condition. It is, with the no interference assumption, part of the *SUTVA* condition (Stable Unit Treatment Value Assumption). 

## Explanation
Ambiguity or variability in what constitutes “treatment” undermines interpretation of causal effects. Multiple versions of the supposedly same treatment level result in averaging their possibly distinct causal effects. Methods differ in how strictly they need a crisp treatment delineation. This assumption is also named *consistency*.

## Tools/rationale for helping assessment
1. Inspect your treatment variable’s values for ambiguity in definition or levels. Is it an exact binary decision, an ordered category, a continuous dose, or inherently fuzzy over time?
2. If you have a crisp on/off label (e.g. clearcut vs intact), mark `Required`. If ideally crisp but some ambiguity remains, `Recommended`. If clarity helps but is not mandatory, `Desirable`. If exposure is continuous or inherently fuzzy (e.g. percent canopy cover change), and/or you want to specifically study the impact of relaxing this assumption, `Relaxes assumption`. 

## Example
- `Required`: You code “deforestation” as exactly zero vs. >90 % canopy loss—no ambiguity. 
- `Recommended`: For selective logging you use >30 % canopy loss, acknowledging minor misclassification. 
- `Desirable`: You have a continuous % cover as treatment, but cut it into low/med/high levels to recover categorical treatment.
- `Relaxes assumption`: You use a continuous logging‐intensity index (0–1) and accept fuzziness. 
