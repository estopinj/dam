---
title: "Handles lag effects"
parent: "Model properties"
nav_order: 4
permalink: /lags
categories:
- criteria
- model_properties
---

# Handles lag effects

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes` | Explicit support for lagged terms. |
| `Possible` | Options to handle lag effects can be set up by users. |
| `No` | Totally ignores temporal lags. |


## Definition
Whether the method can explicitly incorporate lagged influences of exposures on responses. 

## Explanation
Lag structures are critical in time‐series or ecological processes where effects manifest after delays. Some methods natively include lags; others ignore them. 

## Tools/rationale for helping assessment
1. Based on the system's known ecology and envisioned study plan, decide if effects are only tested to be immediate or can also be delayed (and by how much / which time step). 
2. If you want to allow and test for lag effects, mark `Yes`; if you suspect some lag and plan as an option to study them, but it is not central to the study, `Possible`; if you only want to test for immediate effects, `No`. 

## Example
You know tree‐mortality follows drought with a ~1‐year delay and it is the focus of your study → `Yes`. If you only suspect a lag but it isn’t your priority to test it, `Possible`. If you study instantaneous spectral changes only (e.g. chlorophyll), `No`. 
