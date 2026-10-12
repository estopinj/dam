---
layout: method
title: "Linear path method"
parent: "Adjusted methods (Backdoor C.)"
date: 2025-11-18
author: Tamara Münkemüller, CNRS
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

A linear path model is a series of linear regressions. It describes the
directed dependencies among a set of variables and this way allows, for
example, to disentangle direct from indirect effects. The path model can
be represented with a path diagram to visualise the complex system of
relations. A linear path model holds the same assumptions as linear
regressions, including linear, additive and causal associations and
independence of residuals. In addition, the model needs to be recursive
and without feedback loops. Or in other words a variable cannot be the
cause and the effects of another variable. A rule of thumb for required
sample size is 20 times the number of parameters estimated, which with
increasing model complexity can quickly become a limitation.

When confronting linear path models to data one can evaluate different
performance indicators. On the one hand these include indices of overall
model fit that can help to judge if the overall assumed causal
relationships are supported by the data. On the other hand, these
include indices of the importance of specific paths or pathways
(combinations of paths) that can help to judge which are the best
supported links in the model.

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}
Linear path models are a special case of structural equation models
(SEM). SEMs can in addition include latent variables and structures that
are not directly observed but estimated based on data. In ecology,
piecewise SEMs are regularly used. Here, the overall causal path model
is broken down into pieces and separate component models that can be
more flexibly adapted to data specificity and the approach may require
lower sample sizes.

## Further online resources

{: .no_toc }
[https://www.regorz-statistik.de/blog/semblog.html](https://www.regorz-statistik.de/blog/semblog.html)

## Reference articles

### Method
{: .no_toc }

- {% cite doi1023072389745 --style _bibliography/narrative_full %}

- {% cite doi101186s1371701600633 --style _bibliography/narrative_full %}

- {% cite doi101016jpedobi201503002 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite doi1010882752664xad87f9 --style _bibliography/narrative_full %}

- {% cite doi101111ejss12446 --style _bibliography/narrative_full %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite doi1011111365243513393 --style _bibliography/narrative_full %}

- {% cite doi101111geb70093 --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }
- Semopy

- [https://www.datacamp.com/tutorial/structural-equation-modeling](https://www.datacamp.com/tutorial/structural-equation-modeling)

#### R
{: .no_toc }
- lavaan (for analysis)

- sem

- semPlot (for plotting)

- [https://stats.oarc.ucla.edu/r/seminars/rsem/](https://stats.oarc.ucla.edu/r/seminars/rsem/)

### Code Cells
{: .no_toc }

## Assessment table
