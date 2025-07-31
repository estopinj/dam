---
title: "Number of variables"
parent: "Model properties"
nav_order: 3
permalink: /variablenumber
categories:
- criteria
- model_properties
---

# Number of variables

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Univariate` | Models a single variable (exposure or response). |
| `Bivariate` | Handles exactly two variables in conjunction (e.g., one exposure and one outcome). |
| `Multivariate` | Simultaneously models multiple variables (e.g., several exposures or multivariate responses) when predictors are fewer than observations. |
| `High-dimensional (p≫n`) | Designed for contexts where the number of variables (*p*) greatly exceeds the number of observations (*n*), requiring techniques for variable selection, regularization, or dimension reduction. |


## Definition
The total number of distinct variables -either exposures or response variables- that the method should handle simultaneously. 

## Explanation
Some methods are designed to analyze a single variable at a time (univariate), while others can jointly handle two variables (bivariate), multiple variables (multivariate), or very large sets of variables including many exposures or response metrics (high‑dimensional). This criterion ensures you select a method compatible with the complexity of your variable set. 

## Tools/rationale for helping assessment
1. Count how many exposures, responses and covariates you wish to include simultaneously. 
2. If *p*≫*n*, consider `High‐dimensional`; if exactly one, `Univariate` etc. 

## Example
I plan to model 4 spectral indices and 2 vegetation metrics simultaneously (total 6 variables) → I select `Multivariate`. 
