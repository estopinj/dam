---
title: Parametric nature
parent: Model properties
nav_order: 6
permalink: /parametric
---

# Parametric nature

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Parametric` | All functional relationships are specified by a finite set of parameters. |
| `Semi-parametric` | Combines parametric and non‑parametric elements. |
| `Non-parametric` | No fixed form, often data‑driven. |
| `Rule-based` | Deterministic rules define relationships. |

## Definition
The level of assumed functional specification in the method’s core structure. 

## Explanation
Parametric methods impose strong structural assumptions that simplify estimation but risk misspecification, while non‑parametric approaches adapt to data but require larger sample sizes. Semi‑parametric methods strike a compromise by combining parametric core components with flexible adjustments.

## Tools/rationale for helping assessment
1. Think whether you trust a specific functional form (e.g. logistic growth) or need flexibility depending on your system’s knowledge. 
2. If theory prescribes a form, `Parametric`; if you want a mixture, `Semi-parametric`; if you want entirely data‐driven, `Non-parametric`; if you want to set decision rules, `Rule-based`.

## Example
Population growth is known logistic from past studies → `Parametric`. If you combine logistic with spline corrections, Semi-parametric. If you choose a random forest, `Non-parametric`. If you use an expert‐system of rules (“if NDVI>0.7 then high habitat”), `Rule-based`. 

 
