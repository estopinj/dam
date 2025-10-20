---
title: "STOC & land cover changes"
parent: Gallery
nav_order: 1
categories:
- gallery
---

# Impacts of abrupt land cover changes on French common birds
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


{: .note}
>Biospace25 presentation introducing the study context and first results available on [HAL](https://hal.science/hal-04947333).

Observed biodiversity changes can be hard to attribute to their pressures since they are often highly entangled and barely measured.

*In this [Gallery]({{ site.baseurl }}/gallery) page, we showcase how **NaviDAM** can be used to guide method selection (with the [filtering motor]({{ site.baseurl }}/#user-input)) after introducing the [**data**]({{ site.baseurl }}/data) & [**objectives**]({{ site.baseurl }}/objective).*
{: .fs-6 .fw-300 }


# Data

## Temporal Monitoring of Common Birds | STOC

STOC is a standardized count protocol of common birds in France, with data available on the study period **2001-2019** (protocol change in 2001). Partipant observers focus on 2x2 km squares monitored according to an annual random draw, see [Figure 1](#fig1).

![]({{ site.baseurl }}/assets/images/STOC_1.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig1"></a>
  <a href="#fig1">Figure 1</a>: STOC coverage in mainland France. <em>Source:</em> {% cite fontaine2020 --style _bibliography/narrative %}
</div>

This survey enables studying the evolution of specialization groups of birds through time:

![]({{ site.baseurl }}/assets/images/STOC_2.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig2"></a>
  <a href="#fig2">Figure 2</a>: 75 species are used to construct indicators based on their specialized habitats.
  <em>Source:</em> {% cite fontaine2020 --style _bibliography/narrative %}
</div>


## Annual land cover products | GLC_FCS30D

The annual land cover data products originate from {% cite zhang2024  --style _bibliography/narrative %}. It has a 30-meter resolution as based on Landsat imagery, 35 land-cover categoties spanning from 1985 to 2022 (every 5 years before 2000, annual after), see [Figure 3](#fig3). The tiles were downloaded from the project's [Zenodo](https://doi.org/10.5281/zenodo.8239305) and merged as annual mosaics over France using GDAL command lines.

![]({{ site.baseurl }}/assets/images/GLC_figure.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig3"></a>
  <a href="#fig3">Figure 3</a>: The overview of the GLC_FCS30D dataset during 1985 to 2022.
  <em>Source:</em> {% cite liu2023 --style _bibliography/narrative %}
</div>


## Intersection | STOC ∩ GLC_FCS30D

We extracted land cover data on the 2x2-km squares matching the STOC survey squares, see the example STOC squares on [Figure 4](#fig4). It results in short **time-series** as illustrated [Figure 5](#fig5).

![]({{ site.baseurl }}/assets/images/stoc_locations_example.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig4"></a>
  <a href="#fig4">Figure 4</a>: Example STOC observation squares used to intersect the land cover products.
</div>



![]({{ site.baseurl }}/assets/images/100163.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/100865.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/100972.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/101058.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig5"></a>
  <a href="#fig5">Figure 5</a>: Example land cover time-series of STOC observation squares.
</div>



# Objectives

The objective of this work is twofold: 
1. `Detection` To identify STOC monitoring squares that have been affected by abrupt landscape changes. To achieve this, we compute landscape metrics on the annual land cover squares and **detect** extreme deviations from the mean annual change.
2. `Effect estimation` To test if the detected landscape changes result in bird diversity metric shifts. If we succeed in estimating significant effects, we could therefore confidently **attribute** or not the diversity shifts to the land cover changes.


# Detection of abrupt landscape changes

- Using [PyLandStats](https://pylandstats.readthedocs.io/en/latest/#) {% cite bosch2019 %}, we computed landscape metrics on STOC squares (with help from their [gitHub notebooks](https://github.com/martibosch/pylandstats-notebooks/tree/main/notebooks)). The R equivalent package is [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/).


- Then, we tested several landscape metrics assumed to be ecologically relevant for bird populations (e.g. according to the [forest edge effect](https://en.wikipedia.org/wiki/Edge_effects)): `["number_of_patches", "largest_patch_index", "total_edge", "landscape_shape_index", "contagion", "shannon_diversity_index"]`.
- We also computed several bird community metrics: `Alpha, Beta (turnover), Shannon diversity, Pielou index`.

- However, we plan to further exploit {% cite reif2021 santini2017 %} to better guide tests on:
    *i)* which bird populations, monitored with 
    *ii)* which diversity metric, are sensitive to
    *iii)* which landscape changes.

> Abrupt changes were defined as a deviation superior to X standard deviation to the average annual change. It allowed **detecting** plots affected by landscape change and at which years.

<!-- NaviDAM REF -->


# Bird diversity metric shifts attribution

According to the synthetic control requirements, we gathered and aligned covariate data (bioclimatic variables, PatriNat anthropogenic pressures) on our treated sites and donor pools to then best identify suited controls.
  



<!-- Add References section here -->
<div class="references-section">
  <h2>References</h2>
  {% bibliography --cited_in_order %}
</div>