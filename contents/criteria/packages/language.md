---
title: Language
parent: Packages
nav_order: 1
permalink: /language
---

# Programing language

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `R` | Robust, community‑driven libraries in R. |
| `Python` | Well‑supported Python packages. |
| `GIS` | Implementations within GIS software (e.g., ArcGIS, QGIS). |
| `Others` | Other languages (MATLAB, Java, Stata, etc.). |
| `None` | No known packaged code exists, e.g. only developer scripts. |


## Definition
The primary programming environment(s) in which mature, maintained implementations of the method are available (e.g., R, Python, GIS software).

## Explanation
Availability in your preferred language affects ease of use, access to community support, and integration with existing workflows. Methods supported by multiple well‑maintained libraries reduce barriers to adoption and encourage reproducibility.

## Tools/rationale for helping assessment
Depends on *i)* your coding preferences, *ii)* your target audience and *iii)* your result dissemination plan: do you target high reproducibility standards with packaged code or are ok with versioned code only? 

## Example
Your group is R‐centric and has already developed CRAN packages for DiD & SEM → you select `R` for enhanced uptake and continuity. If instead you plan to code your pipeline in Google Earth Engine (JS/Python) or OpenEO (supports both R and Python, but bigger Python community), you should choose `Python`. 
