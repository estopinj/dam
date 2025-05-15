---
title: Required TS length
parent: Data compatibility
nav_order: 2
permalink: /tslength
---

# Required time-series length

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Handles ≤ 10` | Designed to work reliably even with less than ten time points. |
| `≥ 10` | Requires at least ten observations. |
| `≥ 100` | Needs at least one hundred observations for stable estimation. |


## Definition
The minimum number of time points or temporal observations needed for the method to perform reliably, for example at least 10 or 100 time steps. 

## Explanation
Time‑series length requirements prevent methods from over‑fitting or producing spurious patterns when there are too few observations. Methods designed for short series emphasize robustness and parsimony, whereas those needing long series can capture complex dynamics but risk over‑parameterization if data are scarce.

## Tools/rationale for helping assessment
Compare time-series length (or smallest time-series length in case of panel data) against thresholds. 

## Example
A phenologist with only 8 years of NDVI data marks `≤ 10` and opts for a short series changepoint detector rather than models needing `≥ 100` observations. 
