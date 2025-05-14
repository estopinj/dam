---
title: Handles missing data
parent: Data compatibility
nav_order: 5
---

# Handles missing data

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Yes` | Built-in handling of missing values (e.g., likelihood‐based, imputation). |
| `Partially` | Limited capacity to handle missing data, e.g. by automatically discarding incomplete time series. |
| `No: requires prelim. correction` | Cannot function without complete data and therefore requires the data to be imputed before applying. |


## Definition
Whether the method can accommodate or adjust for missing values in the dataset.

## Explanation
Missing data are common in RS and ecological datasets; methods must either handle gaps or require imputation.

## Tools/rationale for helping assessment
Count the number of incomplete variables in the system relative to the total variable number, and the percentage of missing values per such variable. If the user estimates unreasonable to drop these variables, the next step is to specify how this aspect should be taken into account by the method: It is central, suggested methods should have built-in capacities (`Yes`), It is secondary, i.e. simple tools to leverage the data are enough (`Partially`), and finally externally: imputation of missing data should bedone with a preliminary algorithm.

## Example
Cloud cover masks ~30 % of my Landsat images. I need a method for handling such large data gaps with built-in capacities, so I select `Yes` (e.g. state‐space gap‐filling). 
