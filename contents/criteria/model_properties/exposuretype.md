---
title: "Exposure type"
parent: "Model properties"
nav_order: 2
permalink: /exposuretype
categories:
- criteria
- model_properties
---

# Exposure type

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Binary` |  Two‐level (treated vs control). |
| `Categorical` | Multiple distinct groups. |
| `Continuous / Time-varying` | Numeric variables fluctuating by site and/or in time. |
| `Compositional` | Parts of a whole (e.g., species proportions). |
| `Multivariate` | Multiple simultaneous exposures. |
| `Others` | Specialty types (e.g., network exposures). |


## Definition
The form of the treatment or exposure variable(s) that the method should accommodate. 

## Explanation
Some methods only handle binary treatments; others extend to multi‐level, continuous, time‐varying, or compositional exposures. for instance 

## Tools/rationale for helping assessment
Inspect how your exposure variable is defined: is it `binary` (presence/absence), `categorical` (habitat types), `continuous` (temperature), `compositional` (soil nutrients), or `multivariate`? 

## Example
I have continuous canopy‐height measurements as response variable and categorical land‐cover classes as treatment → I will choose a method supporting `Categorical` exposures, or possibly `Compositional` if I compute LC class proportions in buffers. 
