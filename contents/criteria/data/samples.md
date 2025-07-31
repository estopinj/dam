---
title: "Handles few samples"
parent: "Data compatibility"
nav_order: 3
permalink: /fewsamples
categories:
- criteria
- data
---

# Handles few samples

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes CT design` | 1 Control vs 1 Treatment design or self‑controlled designs that work with very small *n*. |
| `Yes ≤ 10` | Can handle 10 samples or less reliably. |
| `10 to 100` | Requires between ten and one hundred samples. |
| `No` | Fails or produces unstable estimates when *n* is small. |


## Definition
Whether the method remains effective when the total number of units / observation sites (*n*) is small. 

## Explanation
In contexts with limited data (like rare events or expensive field observations), you need methods that do not break down under a few samples. Some designs can still produce valid inference, whereas many machine‑learning approaches require large samples to avoid over‑fitting.

## Tools/rationale for helping assessment
Compare directly against threshold rough estimates.

## Example
An ecologist with just 6 camera-trap sites finds standard GAMs unstable, so they choose a Control Treatment design proven for very small *n*.
