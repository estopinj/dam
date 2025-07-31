---
title: "Handles huge datasets"
parent: "Data compatibility"
nav_order: 4
permalink: /bigdata
categories:
- criteria
- data
---

#     Handles huge datasets (*n*)

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes` | Scales smoothly to arbitrarily large *n* without fundamental changes. |
| `Most do` | Works for large *n* with most method declinations but may need optimization. |
| `Most don't` | Only a few variants or implementations of the method can handle large *n*. |
| `No` | Breaks down or becomes computationally infeasible when *n* grows. |


## Definition
The method’s scalability to very large datasets, indicating if it remains computationally and statistically tractable as sample size n grows. 

## Explanation
Big‑data settings present both opportunity and challenge for detection and attribution: scalable algorithms can leverage high resolution or massive sensor networks, but some methods become infeasible or lose interpretability at scale. Knowing which methods handle large *n* informs decisions about algorithmic implementations and resource needs. 

## Tools/rationale for helping assessment
Depending on the number of samples available in the case study, the user estimates if this aspect is important to consider when filtering methods. 

## Example
A biogeographer wants to process 3 million 10 m Sentinel-2 pixels; only a distributed causal random-forest implementation would complete in hours, whereas a full Bayesian SEM fails beyond ~10 000 pixels, so `Yes` is selected. 
