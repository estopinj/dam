---
title: Objective
parent: Outcome
nav_order: 1
---

# Objective

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Effect estimation` | Quantifies the numerical magnitude of causal effects. |
| `Causal relationship(s)` | Identifies the presence or direction of causal links without providing numeric estimates.  |
| `Predictive task + interpretability` | Builds models that optimize the forecast of outcomes while remaining understandable to domain experts. |
| `Detection` | Identifies changes or anomalies without looking for attributing causes - at least in a first step. |
| `Significance and robustness tests` | Evaluates statistical significance and sensitivity of findings. |
| `Scenario projection` | Simulates future or counterfactual scenarios under different assumptions.  |


## Definition
The primary goal or purpose a user seeks to answer, and the assessed methods are designed to achieve. Some methods can satisfy various objectives depending on settings. 

## Explanation
Clearly stating the objective helps determine whether a method is suited to your research question. Whether you need quantitative attribution of effects, qualitative discovery of causal relationships, predictive performance with interpretability, or robust scenario forecasting between others. This framework assumes users to have clearly identified what they want to achieve to be properly used. If the objective is not well defined yet or exploratory, we advise testing different options successively to reach suggested methods in each case.

## Tools/rationale for helping assessment
If your study objective does not align with any of the suggested options but you believe it is relevant for a detection and attribution framework, please raise an issue on the subject. It may also be a vocabulary/convention distinction not accounted for in the framework. Write down your precise research question (e.g. “What is the attributable loss of canopy cover due to drought?”). In most cases, a clearly defined DA study objective should find a close match with the suggested options. An option would be to review recent papers in your field to see how authors formulate similar goals / which methods they choose. 

## Example
- A landscape ecologist wants to detect the first appearance of deforestation in satellite imagery - so they choose the `Detection` option rather than an attribution-oriented objective. 
- *I want to quantify how much mangrove area was lost during the 2023 El Niño*, I therefore choose `Effect estimation` and rule out pure detection or scenario tools. 
