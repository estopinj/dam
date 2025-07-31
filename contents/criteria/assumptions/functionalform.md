---
title: "Functional form"
parent: Assumptions
nav_order: 1
permalink: /funform
categories:
- criteria
- assumptions
---

# Functional form

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Linear` | Assumes straight‐line relationships between predictors and outcomes. |
| `Quadratic` | Incorporates second‐degree terms to capture simple non‑linearity. |
| `Non-linear` | Allows arbitrary shape; may use kernels or neural networks. |
| `Additivity` | Effects sum without interaction terms. |
| `Assumption-free` | No explicit functional form assumed. |
| `Rule-based` | Uses decision or logic rules. |
| `Log-linear` | Models on a logarithmic scale. |

## Definition
The mathematical flexibility of the model’s structure, ranging from strictly linear or quadratic relationships to fully non‑parametric, additive, or rule‑based formulations. 

## Explanation
Choosing an appropriate functional form balances bias and interpretability: simpler linear forms offer transparency but may miss curvature, whereas flexible non‑parametric or rule‑based models capture complex patterns at the cost of more demanding data and potential over‑fitting. 

## Tools/rationale for helping assessment
1. List your mechanistic or theoretical expectations: do you expect a straight‐line, simple curvature, additive effects, or entirely unknown shape? 
2. Match explicitly your belief to the best option available 

## Example
You know from field experiments that tree‐growth response to sunlight saturates (levels off). You therefore expect a `non-linear` form over a strictly linear one, based on that a priori assumption. 
