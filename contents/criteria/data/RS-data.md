---
title: "RS-data proven"
parent: "Data compatibility"
nav_order: 6
permalink: /rsdata
categories:
- criteria
- data
---

# Remote sensing data proven

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes` | Extensively demonstrated on RS datasets in published studies. | 
| `Few applications` | Some exploratory uses but not widespread. |
| `No` | No known successful RS applications with biodiversity data. |


## Definition
Whether the method has already been successfully applied to remote‑sensing datasets for a biodiversity study. 

## Explanation
Remote‑sensing (RS) data carry unique error structures such as atmospheric interference and spatial dependencies. Methods validated on RS applications provide confidence that they can accommodate these challenges, whereas untested methods may yield unreliable results when confronted with satellite or Imaging Spectroscopy (IS) imagery.

## Tools/rationale for helping assessment
Regarding the final analyses I have in mind, do I need the eventual suggested methods to be already proven on RS data, e.g. to help discuss/compare my results with the literature? Decide how much prior RS literature support you need to feel confident in method performance on your problem. 
1. If you need direct comparability to published studies, require `Yes` (many prior RS uses). 
2. If you are comfortable pioneering with only a few limited precedents, choose `Few applications`. 
3. If you are ok with any method - from well-established with RS data to models with no referenced RS applications - rule out any with `No`. 

## Example
- `Yes`: You plan to benchmark canopy-loss attribution against 10 published DiD studies on tropical forests, so you target a method established to deal well with RS data.
- `Few applications`: You target a method for studying pollution impacts on coral-bleaching RS-detected patterns and accept using methods with few prior RS-data usages to explore possibilities.
