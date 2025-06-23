---
layout: method
title: Synthetic controls
parent: Quasi-experiments
nav_order: 1
date: 2025-06-23
author: Joaquim Estopinan
# assessor: Mr. Smith
---

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

The synthetic control (SC) method originates from the early 2000s, with its first introduction in the influential {% cite abadie2003 --style _bibliography/narrative %} article. It consists in combining a selection of control sites to best mimick the treatment site's counterfactual, based on the pre-intervention similarity of their respective outcome and covariates. It is an effect estimation method shifting the `causal sufficiency` (no unobserved confounders) to the `good pre-intervention fit` assumption and still without  time-varying unobserved confoundinfing after the intervention.

### Major variants
{: .no_toc }
{: .d-inline-block }

The success of this method has also led to numerous variants. We can cite:
- *Augmented SC* from {% cite ben-michael2020 --style _bibliography/narrative %}: Relaxes constraints on the synthetic control combination to improve pre-treatment fit
- *Generalized SC* from {% cite xu2016 --style _bibliography/narrative %}: Relaxes the parallel trend assumption and unifies the SC method with linear fixed effects models under a common framework
- 


### Further online resources
{: .no_toc }

References to useful online resources to get started, e.g. [explanation blogs](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html){:target="_blank"}

 

## Reference articles
### Method
{: .no_toc }
- An updated review paper positioning the method by its original author: {% cite abadie2021  --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- A

#### Without RS data (Ecology domain)
{: .no_toc }
{: .d-inline-block }
optional
{: .label}

- B

## R / Python Packages 
- Name of packages, link to official pages 
- Short note on usage & documentation _(optional)_

### Code Cells
{: .no_toc }
{: .d-inline-block }
optional
{: .label}

Template code cells or GitHub Gist links. 









<!-- For referencement in toc before automatic table -->
## Assessment table

