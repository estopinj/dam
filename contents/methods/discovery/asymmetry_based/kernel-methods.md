---
layout: method
title: "Kernel methods"
parent: "Asymmetry-based"
date: 2025-09-29
author: Jussi Mäkinen, Finnish Environment Research Institute
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Kernel methods are used for smoothing a response variable value in
relation to explanatory variables. The relationship can be non-linear
and highly complex. Thus, kernel methods differ from conventional
statistical models, which commonly fit simple relationships between
variables. The core idea of kernel methods is that they simplify a
complex response between variables by mapping the data to a
higher-dimensional space where a response appears more simple, even
linear. A kernel function is used to map the data to this
higher-dimensional space which simplifies the computation between the
original and higher-dimensional space. Kernel methods can be
non-parametric or semi-parametric depending on how kernel function is
defined.

## Major variants
{: .no_toc }
{: .d-inline-block }
optional
{: .label}
Common variants are support vector machines, Gaussian processes, kernel
density estimator and principal component analysis (PCA).

## Reference articles

### Method
{: .no_toc }

- {% cite muller2018 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

- {% cite mountrakis2011 --style _bibliography/narrative_full %}

- {% cite fieberg2007 --style _bibliography/narrative_full %}

- {% cite wang2025 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }
- scikit-learn-package

- commonly python is preferred over R in kernel methods which are
  applied in machine learning

#### R
{: .no_toc }
- caret- and tidymodels-package

## Assessment table
