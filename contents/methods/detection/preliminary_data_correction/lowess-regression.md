---
layout: method
title: "Lowess Regression"
parent: "Preliminary data correction"
date: 2026-04-28
author: Lori Giagnacovo, VITO
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Versatile tools]({{ site.baseurl }}/tools).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Local regression or local polynomial regression, also known as moving
regression, is a generalization of the moving average and [polynomial
regression](https://en.wikipedia.org/wiki/Polynomial_regression). Its
most common methods, initially developed
for [scatterplot](https://en.wikipedia.org/wiki/Scatterplot_smoothing)
smoothing, are LOESS (locally estimated scatterplot smoothing)
and LOWESS (locally weighted scatterplot smoothing). A smoothing
function is a function that attempts to capture general patterns in
stressor-response relationships while reducing the noise and it makes
minimal assumptions about the relationship among variables. LOESS and
LoWESS are two strongly
related [non-parametric](https://en.wikipedia.org/wiki/Non-parametric_regression)
regression methods that combine multiple regression models in
a [*k*-nearest-neighbor](https://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm)-based
meta-model. It fits simple models to localized subsets of data to build
up a function that describes the deterministic part of the variation in
the data, point by point. The data analyst is not required to specify a
global function of any form to fit a model to the data, only to fit
segments of the data. Local regression is therefore quite
computation-heavy.

The result of a local regression application is a line through the
moving central tendency of the stressor-response relationship. The
method is essentially used to visually assess the relationship between
two variables and is especially useful for large datasets, where trends
can be hard to visualize.

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}
/ (Lowess and Loess are both regression models of the Local Regression
family)

## Further online resources

{: .no_toc }
## Reference articles

### Method
{: .no_toc }

- {% cite cleveland1979 --style _bibliography/narrative_full %}

- {% cite cleveland1988 --style _bibliography/narrative_full %}

- NIST/SEMATECH e-Handbook of Statistical Methods, 4.1.4.4. Loess (aka
  Lowess)
  <http://www.itl.nist.gov/div898/handbook/pmd/section1/pmd144.htm>

- {% cite jacoby2000 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite moreno2014 --style _bibliography/narrative_full %}

- {% cite cai2017 --style _bibliography/narrative_full %}

- {% cite georganos2018 --style _bibliography/narrative_full %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite rojo2017 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }
- loess, <https://pypi.org/project/loess/>

- <https://towardsdatascience.com/lowess-regression-in-python-how-to-discover-clear-patterns-in-your-data-f26e523d7a35/>

#### R
{: .no_toc }
- loess() function in stats package,
  <https://r-statistics.co/Loess-Regression-With-R.html>

- lowess() function in stats package,
  <https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/lowess>

### Code Cells
{: .no_toc }
<https://github.com/Open-EO/openeo-community-examples/blob/main/python/StatisticalDataFill/StatisticalDataFill.ipynb>

## Assessment table
