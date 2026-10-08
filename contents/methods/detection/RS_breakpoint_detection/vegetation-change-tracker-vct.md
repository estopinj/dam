---
layout: method
title: "Vegetation Change Tracker (VCT)"
parent: "RS breakpoint detection"
date: 2026-04-28
author: Lori Giagnacovo, VITO
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Vegetation change tracker (VCT) is a change detection algorithm for
mapping forest change using LTSS (Landsat Time Series Stacks). This
algorithm is similar to LandTrendr in that changes are detected through
simultaneous analysis of all images in an LTSS. But the mechanisms based
on which changes are detected are different. The VCT is based on the
spectral–temporal characteristics of land cover and forest change
processes. It consists of two major steps. In the first step, each image
in an LTSS is analyzed to create masks and to calculate spectral indices
that are measures of forest likelihood. Once this step is complete for
all images in that LTSS, the derived indices and masks are analyzed in a
time series analysis step to map disturbances. Based on these
distinctive temporal profiles of different land cover and forest change
processes (by the time series of the derived indices), decision rules
are used to identify persisting land cover types and to detect
disturbances in a sequence of steps

It should be noted that because VCT uses the spectral–temporal
information as recorded in an LTSS to detect forest disturbance, the
detected disturbances are not necessarily limited to those defined in
forestry or ecology. In VCT a disturbance refers to any event that can
result in significant reduction or removal of forest canopy cover and
woody biomass, including harvest, selective logging, tree reduction for
fuel treatment or other purposes, and damages due to fire, storm, insect
or diseases, although, not all of these events can be detected reliably
by the current version of the VCT.

## Major variants

{: .no_toc }
{: .d-inline-block }
optional
{: .label}

## Further online resources

{: .no_toc }
## Reference articles

### Method
{: .no_toc }

- {% cite huang2009 --style _bibliography/narrative_full %}

- {% cite huang2009 --style _bibliography/narrative_full %}

- {% cite huang2010 --style _bibliography/narrative_full %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite li2009 --style _bibliography/narrative_full %}

- {% cite masek2013 --style _bibliography/narrative_full %}

- {% cite zhao2015 --style _bibliography/narrative_full %}

- {% cite kauffman2016 --style _bibliography/narrative_full %}

- {% cite diao2020 --style _bibliography/narrative_full %}

#### Without RS data (Ecology domain)
{: .no_toc }

## Implementation

#### Python
{: .no_toc }
- Use earthengine-api Python wrapper to call for
  ee.Algorithms.TemporalSegmentation.VCT from GEE

#### R
{: .no_toc }
- Use rgee R wrapper to call for
  ee\$Algorithms\$TemporalSegmentation\$VCT(...)

### Code Cells
{: .no_toc }
<https://developers.google.com/earth-engine/apidocs/ee-algorithms-temporalsegmentation-vct>

## Assessment table
