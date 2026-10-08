---
layout: method
title: "Generalized Dissimilarity Models (GDMs)"
parent: "Alternative paradigms"
date: 2025-11-19
author: Pierre Gaüzère, CNRS
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

{% if page.category_note != '' %}
{: .note }
This method also belongs to [Ecology-guided Modelling]({{ site.baseurl }}/ecology-guided).
{% endif %}

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Generalized Dissimilarity Model (GDM) are statistical models that relate
the dissimilarity (i.e., beta-diversity) between pairs of biological
communities (or genetic samples) to the geographic distance and the
differences in environmental variables between the sites where they were
sampled. GDM is an additive regression model, with the particularity of
using the site-pairs differences instead of using individual sites
values. The central idea is that the biological dissimilarity between
two locations is a function of both the geographical distance between
them and the environmental differences.

Figure from [({% cite mokany2022 --style _bibliography/narrative %}](https://paperpile.com/c/HziGHr/hgxv). Conceptual depiction of
the model fitting procedure of generalized dissimilarity modelling
(GDM). To best represent the observed dissimilarity (*dij*) between
sites *i* and *j*, GDM uses I-spline basis functions to transform each
of the predictor variables (e.g., *f*(Pred. A)), so that summed absolute
difference in the transformed predictor values, combined with the model
intercept (*b*) provide a predicted ecological distance (η). The
negative exponential link function ensures predicted dissimilarities
increase and saturate with increases in the predicted ecological
distance

The model transforms the observed biological dissimilarity (e.g., using
Jaccard or Bray-Curtis dissimilarity) into a measure that is linearly
related to the predicted total dissimilarity. This transformation allows
the model to work effectively across different scales of dissimilarity.

To handle the non-linear nature of ecological dissimilarity, GDM employs
a mathematical transformation to linearize the relationship between the
observed dissimilarity and the environmental/geographic distances.
Hence, the model works directly with the additive effects of the
predictor variables, allowing for easier interpretation. For each
environmental variable (e.g., elevation, rainfall), the GDM fits a
non-negative, monotonic I-spline function. The slope of the I-spline
curve shows the rate at which biological communities change along that
specific environmental gradient. A steep slope indicates a rapid, strong
biological boundary (high turnover). The maximum height of the I-spline
indicates the total amount of biological change uniquely explained by
that variable, quantifying its relative importance as an ecological
driver. GDM can be used for detection purposes to identify which
environmental factors (e.g., climate change indicators, human impacts)
are significantly structuring the communities, and for attribution as it
quantifies the amount of biological turnover uniquely attributed to each
predictor. For instance, the model can tell you that 60% of the
community change is due to temperature differences, 30% is due to soil
type, and the remaining 10% is purely due to geographic isolation.

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}
Many variants exist, but most important are:

- extensions to phylogenetic and/or functional dissimilarity, or even
  Multifaceted Biodiversity Modelling (MBM) that model taxonomic,
  functional and phylogenetic at the same time.

- extension to genetic dissimilarity into a single species to model
  genetic isolation and divergence (“landscape genetics”)

- adaptation to decomposition of dissimilarity into nestedness and
  turnover components

## Further online resources

{: .no_toc }
- Mokany, K., Ware, C., Woolley, S. N. C., Ferrier, S., &
  Fitzpatrick, M. C. (2022). A working guide to harnessing generalized
  dissimilarity modelling for biodiversity analysis and conservation
  assessment. Global Ecology and Biogeography: A Journal of
  Macroecology, 31(4), 802–821.

- R Package gdm tutorial : https://mfitzpatrick.al.umces.edu/gdm/

## Reference articles

### Method
{: .no_toc }

- {% cite mokany2022 --style _bibliography/narrative_full %}

- {% cite talluto2018 --style _bibliography/narrative_full %}

- {% cite leitao2017 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite leitao2015 --style _bibliography/narrative_full %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite ferrier2007 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }

#### R
{: .no_toc }
- gdm ([CRAN - Package
  gdm](https://cran.r-project.org/package=gdm) or [GitHub -
  fitzLab-AL/gdm](https://github.com/fitzLab-AL/gdm)). Performs
  standard GDM, handles predictions and environmental transformations.

- sgdm ([GitHub -
  sparsegdm/sgdm_package](https://github.com/sparsegdm/sgdm_package)).
  An extension designed for high-dimensional datasets (e.g.,
  hyperspectral remote sensing, time-series data).Uses a sparse
  canonical correlation analysis component to reduce the large number of
  predictor variables, making GDM applicable to remote sensing/genomics
  data. Requires gdm and other packages.

### Code Cells
{: .no_toc }

## Assessment table
