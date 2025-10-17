---
title: "STOC & land cover changes"
parent: Gallery
nav_order: 1
categories:
- gallery
---

# Impacts of abrupt land cover changes on French common birds

{: .note}
>Biospace25 presentation introducing the study context and first results available on [HAL](https://hal.science/hal-04947333).


Observed biodiversity changes can be hard to attribute to their pressures since they are often highly entangled and barely measured.
In this work, the objective is:
1. `Detection` To isolate abrupt landscape changes from a land cover annual dataset
2. `Attribution` To assess if the detected changes resulted in bird diversity metric shifts


*Below, we further introduce the data & objectives and showcase how **NaviDAM** could help throughout the study.*


## Introduction

- STOC presentation
<!-- TODO: Get the references right -->

## Detection of landscape changes
- [x] Download GLC_FCS30D ([Zhang et al. 2024](https://essd.copernicus.org/articles/16/1353/2024/)) data over French territory
    - Data downloaded from their [Zenodo repository [Version v1]](https://zenodo.org/records/8239305)
    - Land cover rasters and initial STOC data available on the UGA cloud [here](https://cloud.univ-grenoble-alpes.fr/s/rC5H7qxDQCnbkp3).
- [x] Extract STOC 2x2 kms survey square locations
- [x] Using [PyLandStats](https://pylandstats.readthedocs.io/en/latest/#) [1], compute landscape metrics on STOC squares (with help from their [gitHub notebooks](https://github.com/martibosch/pylandstats-notebooks/tree/main/notebooks)).
	- R equivalent package: [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/)
- [x] Define which metrics (See PyLandStats [Table S1](https://doi.org/10.1371/journal.pone.0225734.s002)) are ecologiccally sensitive to monitor for birds.
    - Initial list: `["number_of_patches", "largest_patch_index", "total_edge", "landscape_shape_index", "contagion", "shannon_diversity_index"]`
    - Look at edge metrics and class proportions for closed/open forest classes (forest [edge effect](https://en.wikipedia.org/wiki/Edge_effects))
- [x] Define abrupt change as a deviation superior to X standard deviation
    - [x] Identify resulting plots affected by landscape change and at which years


## Bird diversity metric shifts attribution
- [x] Identify relevant bird community metrics
    - Initial list: Alpha, Beta (turnover), Shannon diversity, Pielou index
    - [x] Adapt candidates with [Santini et al. (2017)](https://doi.org/10.1016/j.biocon.2016.08.024) "Assessing the suitability of diversity metrics to detect biodiversity change"
    - [ ] Work at the species abundance level: Total abundance by specialization group aggregates distinct species dynamics and is over-driven by dominant species.
- [ ] Gather and align covariate data:
    - [x] Bioclim
    - [x] PatriNat anthropogenic pressures
- [x] Identify relevant control groups with the synthetic control method [2,3]
    - Nice [introduction blog](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html) to the method
    - [ ] Continue testing SC variants like the Augmented SC method
- [ ] Measure if landscape change effects are significative after the identified change year.
    - [ ] Use [Reif et al. (2021)](https://doi.org/10.1016/j.ecolind.2021.107909) to identify test landscape changes and response types
    - [ ] Consider and test for lagged effects



## References

- [1] Bosch, Martí. "[PyLandStats: An open-source Pythonic library to compute landscape metrics.](https://doi.org/10.1371/journal.pone.0225734)" PLoS One 14.12 (2019): e0225734.
- [2] Fick, Stephen E., et al. "[Evaluating natural experiments in ecology: using synthetic controls in assessments of remotely sensed land treatments.](https://onlinelibrary.wiley.com/doi/abs/10.1002/eap.2264)" Ecological Applications 31.3 (2021): e02264.
- [3] Abadie, Alberto. "[Using synthetic controls: Feasibility, data requirements, and methodological aspects.](https://www.aeaweb.org/articles?id=10.1257/jel.20191450)" Journal of economic literature 59.2 (2021): 391-425.
- [4] Zhang, Xiao et al. "[GLC_FCS30D: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985.](https://essd.copernicus.org/articles/16/1353/2024/) " Earth System Science Data Discussions 2023 (2023): 1-32.