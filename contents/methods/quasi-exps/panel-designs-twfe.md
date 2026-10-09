---
layout: method
title: "Panel designs, TWFE"
parent: "Quasi-experiments"
date: 2025-11-18
author: Romain Goury, reviewed by Mickaël Hedde
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Adjusted methods (Backdoor C.)]({{ site.baseurl }}/adjusted).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Two-Way Fixed Effects (TWFE) models are a generalisation of
difference-in-difference (DID) models, such as those described by {% cite angrist2009 --style _bibliography/narrative %}.
They use added ‘fixed effects’ to control for several dimensions of
confounding. Generally, they are used to account for multiple groups and
time periods by including unit and time fixed effects (although these
fixed effects may consider other variables). The "unit" fixed effect
controls for all confounding variables that are time-invariant and only
vary spatially (e.g. topographic variables), while the 'time' fixed
effect controls for all confounding variables that vary over time, but
not in space. By adding both unit and time fixed effects, the model estimates
the average causal effect of predictor variation within units and years
on the outcome. In other words, TWFE captures anomalies in both the
explanatory and response variables, so these models focus more strongly on
individuals with a lot of variation over time and/or space.

Methodologically, TWFE comes with the strong assumption of effect (or
treatment) homogeneity, i.e. that the treatment effect does not vary
across units or over time, which might not always be the case in
ecological scenarios. In contrast to mixed-effects models with
unit/year random intercepts, TWFE do not assume no correlation between
fixed effects and predictor variables, which could
be relevant with strong climatic gradients across study areas.

- **No dynamic treatment effects:** The model requires that the
  treatment effect does not evolve over time.

- **No unit-level differences:** The treatment effect must be constant
  across all units.

- **Linear additive effects:** TWFE assumes that the underlying
  data-generating process is captured by additive fixed effects plus a
  constant treatment effect {% cite imaikim2021 --style _bibliography/narrative %}.

What happens to our data when we apply OWFE/TWFE models?

*Fig. 1:* *This plot shows how the effect of X on Y changes according to
the applied model. The left panel shows the raw data,* *simply
regressing x~Y.* *The middle panel illustrates the OWFE* *adding* *a
'unit' fixed effect. The X and Y values both correspond to anomalies
with a mean value of 0. and the right panel represents the TWFE, adding
both ‘unit’ and ‘year’ fixed effects (right panel).* *represents the
anomalies of the OWFE, centring the data at 0 and effectively removing
the trends present in both the X and Y values.*

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}
A variant of the method uses only single fixed effect, i.e. for time or
unit (one-way fixed effect, OWFE). This model makes the same assumptions
as the TWFE, but we keep the temporal trajectories (anomaly, trends) in
the data.

## Further online resources

{: .no_toc }
[https://bookdown.org/mike/data_analysis/sec-two-way-fixed-effects.html#ref-goodman2021difference](https://bookdown.org/mike/data_analysis/sec-two-way-fixed-effects.html#ref-goodman2021difference)

[https://theeffectbook.net/ch-FixedEffects.html?panelset_001=r-code#how-does-it-work](https://theeffectbook.net/ch-FixedEffects.html?panelset_001=r-code#how-does-it-work)

## Reference articles

### Method
{: .no_toc }

- {% cite dee2023 --style _bibliography/narrative_full %}

- {% cite dudney2025 --style _bibliography/narrative_full %}

- {% cite angrist2009 --style _bibliography/narrative_full %}

- {% cite imaikim2021 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite dee2023 --style _bibliography/narrative_full %}

- {% cite dudney2021 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }

#### R
{: .no_toc }
> [Https://lrberge.github.io/fixest/index.html](https://lrberge.github.io/fixest/index.html)

### Code Cells
{: .no_toc }
```r
library(tidyverse)
library(modelsummary)
library(fixest)

gm <- causaldata::gapminder

twfe <- feols(
  lifeExp ~ log(gdpPercap) | country + year,
  data = gm
)

msummary(twfe, stars = c("*" = .1, "**" = .05, "***" = .01))
```

## Assessment table
