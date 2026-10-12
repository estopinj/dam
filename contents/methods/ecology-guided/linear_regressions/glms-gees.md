---
layout: method
title: "GLMs, GEEs"
parent: "Linear regressions & extensions"
date: 2025-09-29
author: Jussi Mäkinen, Finnish Environment Research Institute
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

GLMs are statistical models, which build a statistical association
between a non-Gaussian distributed (commonly binary, positive integer or
multinomial) response variable and explanatory variables. A linear
predictor which is a linear combination of explanatory variables is
scaled with a link function (such as the inverse of logit or exponent)
to correspond to the response variable. Model parameters are estimated
with maximum likelihood procedure.

GEEs differ from GLMs by that they are not considered as models but as
estimation technique. A GEE is used for building a statistical
association between a non-Gaussian response variable and explanatory
variables. In comparison to a GLM, GEE does not compute a likelihood of
data but computes an empirical estimate of standard deviation and
covariance of linear weights of the predictor. The advantage of GEEs is
that when the response variable is multivariate (longitudinal or a
collection of different responses), GEE avoids computing a full joint
distribution of the responses but computes only the empirical covariance
of the responses. Due to the lack of likelihood, GEEs cannot be applied
for model testing and comparison.

## Major variants
{: .no_toc }
{: .d-inline-block }
optional
{: .label}
GLMs can be used for many different applications with different variants
of the linear predictor.

## Further online resources
{: .no_toc }
GLM: <https://online.stat.psu.edu/stat504/lesson/6/6.1>,
<https://medium.com/@sahin.samia/a-comprehensive-introduction-to-generalized-linear-models-fd773d460c1d>

GEEs: <https://online.stat.psu.edu/stat504/lesson/12/12.1>

## Reference articles

### Method
{: .no_toc }

- {% cite myers1997 --style _bibliography/narrative_full %}

- {% cite mcculloch2000 --style _bibliography/narrative_full %}

- {% cite ballinger2004 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

- {% cite guisan2002generalized --style _bibliography/narrative_full %}

- {% cite miller2002 --style _bibliography/narrative_full %}

- {% cite hawkes2021 --style _bibliography/narrative_full %}

- {% cite lieske2009 --style _bibliography/narrative_full %}

- {% cite pirotta2014 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }
- GLM and GEE: statsmodels-package

#### R
{: .no_toc }
- GLM: stats-package

- GEE: geepack-package

## Assessment table
