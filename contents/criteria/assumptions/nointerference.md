---
title: "No interference"
parent: Assumptions
nav_order: 3
permalink: /nointerference
categories:
- criteria
- assumptions
---

# No interference

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Required` | Assumes strict no‐spillover. |
| `Recommended` | Best if spillovers are minimal. |
| `Desirable` | Improves validity but can be relaxed. |
| `Relaxes assumption` | Explicitly allows and models interference (e.g., network models). |
| `Not required` | Interference is irrelevant or explicitly allowed. |

## Definition
Whether the method assumes each unit’s treatment does not affect any other unit’s outcome. It is, with the well-defined treatments assumption, part of the *SUTVA* condition (Stable Unit Treatment Value Assumption). 

## Explanation
Interference (spillover) violates independence. Most causal methods assume no interference; some advanced approaches model networks or spatial spillovers explicitly. 

## Tools/rationale for helping assessment
1. Plot spatial coordinates of units and test for interference in untreated units next to treated ones vs. remote controls. 
2. Compute Moran’s I on treatment indicator to detect clustering/spillover. 
3. From your study design: If units are truly isolated, mark `Required`; if only minor spillover possible, `Recommended`; if some spillover but manageable, `Desirable`; if you expect substantial interference and/or want to specifically study the impact of relaxing this assumption, `Relaxes assumption`. 

## Example
- Moran’s I on burned vs. unburned patches =0.3 (p<0.01) ↦ strong spatial spillover. I choose a method that relaxes no‐interference or explicitly models spatial networks. 

- Logging in one forest patch decreases bird richness in adjacent patches (p<0.01), violating the assumption; thus, the method must relax no-interference or explicitly model spillovers. 

- Your 1 km² forest plots are >50 km apart (birds don’t travel far) → `Required`. If plots are 5 km apart (some movement), Recommended. If plots are adjacent, `Desirable`. If there is a continuous landscape with high connectivity, you pick a spatial model that relaxes no‐interference. 


