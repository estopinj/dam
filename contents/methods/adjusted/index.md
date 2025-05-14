---
title: Adjusted methods
nav_order: 4
parent: Methods
permalink: /adjusted
---

# Adjusted methods (Backdoor criterion)

 - A set of approaches used to control for confounding and isolate the causal effect of an exposure on an outcome.
 - Based on the backdoor criterion, these methods require a valid adjustment set to block non-causal paths.
 - The key premise is that the causal graph is known or assumed.
 - These methods rely on adjusting for confounding variables using conditioning sets.
{: .fs-6 .fw-300 }

**Overlap:**
Widely overlaps with Causal ML (which builds upon these), Causal Discovery (which may infer the graph), and Quasi-Experiments (when combined with temporal or spatial structure)

**Key feature:**
Control for confounding through observed covariates

**Usage:**
Widely used when experimental data is unavailable but good covariate data exists