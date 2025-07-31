---
title: "Propagates uncertainty"
parent: "Model properties"
nav_order: 5
permalink: /uncertainty
categories:
- criteria
- model_properties
---

# Propagates uncertainty

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Inherent capacity` | Fully incorporates input and parameter uncertainty into output intervals. |
| `Model-specific tools` | Specialized extensions or package functions (e.g., bootstrap routines, sandwich variance estimators, delta method) are available to propagate uncertainty for that method. |
| `Needs model-agnostic propagation` | Requires external, generic workflows (e.g., Monte Carlo simulation, bootstrap wrappers) to track and quantify uncertainty across model outputs. |


## Definition
The method’s built-in ability to carry the quantified uncertainty of inputs (e.g., measurement error, parameter estimation variance) through the analysis to produce valid confidence or credible intervals on outputs. 

## Explanation
Proper uncertainty propagation prevents overconfident conclusions by ensuring that input errors and model uncertainties are reflected in the final inference. Some methods do this inherently; others require external tools or custom workflows. Methods lacking this aspect provide point estimates without a realistic appraisal of their reliability. 

## Tools/rationale for helping assessment
1. Decide if you require your RS measurement error (e.g. ±σ per pixel) to flow into your final effect estimates. 
2. If you need full integration with no extra coding, choose `Inherent capacity`; if availability via method‐specific additional routines suits you (e.g. bootstrap), choose `Model-specific tools`; if you plan a separate Monte Carlo wrapper, choose `Needs model-agnostic propagation`. 

## Example
Your LiDAR canopy‐height σ is 0.3 m/pixel and you want those errors to propagate in your biomass estimate’s CI: *i)* with no time-consuming coding efforts: you pick `Inherent capacity`; *ii)* you are ok with some additional dedicated function calls and parameter tweaking: `Model-specific tools`. 
