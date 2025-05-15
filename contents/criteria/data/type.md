---
title: Data type
parent: Data compatibility
nav_order: 1
---

# Data type

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Spatial only (cross-sectional)` | Uses a single time point - or a collapsed period - across spatial units. |
| `Time-series (one sample)` | Analyzes repeated measurements over time for a single unit. |
| `Panel data (many samples)` | Combines cross‑sectional and time‑series variation across multiple units. |


## Definition
The data structure(s) that the method can appropriately handle, such as spatial cross‑sectional measurements, single‑unit time‑series, or multi‑unit panel data.

## Explanation
Matching the method to your data’s form is crucial: some approaches require only a snapshot in space, others demand temporal repetition for a single unit, and still others exploit variation across many sampled units over time. Choosing an incompatible method can invalidate results or leave valuable structure unused.

## Tools/rationale for helping assessment
- Draw a causal graph to make sure no relevant to the system and easily available variable has not been forgotten. 
- Inspect your data: Do you have only one timestamp per pixel (cross-sectional), a single‐site time‐series, or many sites over time? 
- Use visualization helpers like a covariate alignment graph to ensure good comprehension of the data structure. 
- Prototype eventually the chosen method from the suggested set on a small subset of your data to confirm compatibility. 

## Example
A researcher has 10 years’ annual species richness from 30 protected areas - that’s `panel data` - so they exclude methods dealing only with a single‐site time-series or a single time point. 
