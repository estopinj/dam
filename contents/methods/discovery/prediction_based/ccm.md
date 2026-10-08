---
layout: method
title: "CCM"
parent: "Prediction-based approaches"
date: 2025-09-17
author: Miriam Beck, FRB-CESAB, Montpellier, France, reviewed by Colin Fontaine
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Alternative paradigms]({{ site.baseurl }}/alternative).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Convergent Cross-Mapping (CCM) is a nonlinear, data-driven,
equation-free method used to infer causality between time series in
complex systems ({% cite sugihara2012 --style _bibliography/narrative %}). Rooted in the framework of
Empirical Dynamical Modeling (EDM), it builds on the principle that in a
deterministic dynamic system, each variable is influenced by the
underlying system's state and therefore carries embedded information
about other variables it interacts with. Thus, according to Takens'
Theorem the full dynamics of a system can be reconstructed from
time-delayed observations of a single variable through state-space
embedding. This reconstruction yields what is referred to as a shadow
manifold: a geometrical representation of the system’s attractor
reconstructed from a single observed variable, using delay
coordinates. For a time series X(t), its shadow manifold M<sub>X</sub>
is constructed using delay coordinates:

M<sub>X</sub>(t)={X(t),X(t−τ),X(t−2τ),...,X(t−(E−1)τ)}

where τ is the time delay and E is the embedding dimension. The manifold
M<sub>X</sub>​ approximates the true system attractor, preserving its
topological properties under suitable conditions.

Within this framework, if a variable X causally influences variable Y,
then the shadow manifold reconstructed from Y (denoted M<sub>Y</sub>)
will contain information about X. CCM tests this by attempting to
reconstruct (or "cross-map") the values of X using delay coordinates of
Y, with nearest neighbors in the shadow manifold reconstructed from Y
having to correspond to close values of X, using time indices to make
the correspondence. This procedure is based on the assumption that
nearby points in the reconstructed manifold correspond to nearby states
of the full dynamical system. Therefore, if M<sub>Y</sub>​ is a valid
reconstruction of the system attractor and X is dynamically coupled to
Y, then similar states in M<sub>Y</sub> should correspond to similar
values of X. If such reconstruction improves as the length of the time
series used to construct the manifold increases, which refers to the
“convergence” criteria of CCM, we will conclude that X is a causal
driver of Y.

A strength of this approach is that it allows for asymmetric inference:
the fact that M<sub>Y</sub> can reconstruct X, and therefore that X
causes Y, does not imply that the reverse is true. CCM also allows for
the detection of bidirectional causality (X ↔ Y), though extensions of
the method (e.g., {% cite ye2015 --style _bibliography/narrative %}) are needed to differentiate true
feedback from spurious correlations due to shared drivers or strong
coupling.

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}
Several variants are available to deal with common challenges arising from
ecological data: **Multispatial CCM** combines spatially replicated
observations via bootstrapping, enabling to work with shorter time
series ({% cite clark2015 --style _bibliography/narrative %}), implemented in R/Python package fastEDM,\
**Baysian versions of EDM** rely on (Deep) Gaussian Processes (GP)
regressions (e.g. GP-CCM), combining short time series in a hierarchical
model structure to increase forecast precision, addressing cases of
short time series or noisy data ({% cite munch2017 --style _bibliography/narrative %},
{% cite feng2019 --style _bibliography/narrative %},
{% cite ghouse2021 --style _bibliography/narrative %}).\
**Partial Cross-Mapping** integrates partial correlation to distinguish
direct from indirect causal links ({% cite leng2020 --style _bibliography/narrative %}); a multi-variate
variant is in development ({% cite zhang2025 --style _bibliography/narrative %}).

## Further online resources

{: .no_toc }
The rEDM package documentations provide walk through examples across
methods and workflows in EDM, including S-Map and highlighting its
integration in EDM workflow
(https://ha0ye.github.io/rEDM/articles/rEDM.html)

## Reference articles

### Method
{: .no_toc }

- {% cite sugihara2012 --style _bibliography/narrative_full %}

- {% cite clark2015 --style _bibliography/narrative_full %}

- {% cite feng2019 --style _bibliography/narrative_full %}

- {% cite ghouse2021 --style _bibliography/narrative_full %}

- {% cite leng2020 --style _bibliography/narrative_full %}

- {% cite munch2017 --style _bibliography/narrative_full %}

- {% cite ye2015 --style _bibliography/narrative_full %}

- {% cite zhang2025 --style _bibliography/narrative_full %}

- {% cite wang2021 --style _bibliography/narrative_full %}

- {% cite tsonis2015 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite diaz2022 --style _bibliography/narrative_full %}

- {% cite wang2018 --style _bibliography/narrative_full %}

- {% cite rigal2023 --style _bibliography/narrative_full %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite matsuzaki2018 --style _bibliography/narrative_full %}

- {% cite wang2020 --style _bibliography/narrative_full %}

- {% cite ye2019functional --style _bibliography/narrative_full %}

## Implementation

#### Python
{: .no_toc }
- pyEDM (https://pypi.org/project/pyEDM/,
  https://sugiharalab.github.io/EDM_Documentation/)

- fastEDM (https://edm-developers.github.io/fastEDM-python/)

#### R
{: .no_toc }
- rEDM (https://ha0ye.github.io/rEDM/articles/rEDM.html)

- fastEDM (https://github.com/EDM-Developers/fastEDM-r) allow to process
  panel data (‘multispatial EDM’)

### Code Cells
{: .no_toc }

## Assessment table
