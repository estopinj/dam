---
title: About
layout: about
nav_order: 2
description: "The DAM Navigator is an interactive decision-support tool designed to help researchers explore, compare, and select appropriate detection and attribution modelling methods based on their data, assumptions, and goals."
---

## Table of Contents
{: .no_toc .text-delta }
1. TOC
{:toc}


## Objective
- The Detection Attribution Modeling (DAM) Navigator serves the goal to orient users looking methods for detecting and disentangling the drivers of observed biodiversity change.
It **situates methods**, both *widespread* methods used in ecological studies and approaches inherited from *causal inference* or econometrics, against an ordered set of [criteria]({{ site.baseurl }}/criteria).

- The different [criteria]({{ site.baseurl }}/criteria) invite users to precisely qualify what they are looking for and what they have at hands to narrow down and suggest detection and/or attribution [methods]({{ site.baseurl }}/methods) and tools suited to their study.



## Website structure

The DAM Navigator is implemented in this collaborative website and is organized around a dynamical method scheme on the landing page:

1. [Landing page]({{ site.baseurl }}/):
    - Brief description of the navigator
    - Invite users to fill in [criteria]({{ site.baseurl }}/criteria) in default order
        - Criteria default to `Unevaluated`, including all options and therefore not filtering the set of suggested methods

        {: .highlight}
        Incomplete assessments are reported in outputs.
    
        {: .note-title }
        > **?** signs
        > 
        > Along each criterion, a **?** sign redirects to the description page in the [criteria]({{ site.baseurl }}/criteria) panel.

   
    - Method scheme
        - Gets refined/colored with criteria assessment 
            - _see feasibility_ - Is refined **each time** a criterion is informed _vs._ updated **on click only**
        - Retained methods on the scheme can be clicked on to redirect to their page in method panel 
            - _see feasibility_ - Corresponding methods are highlighted in method left bar panel 
        - Exportable outputs: refined scheme `.png`, criteria assessment + methods `.csv`, suited method list `.txt`



{: .important-title}
> The sidebar
>
> The sidebar provides access to different panels grouping resource pages logically.
> Its exploration in regards with the landing page is key for good use of the navigator.

{:style="counter-reset:none"}
1. [Good practices panel]({{ site.baseurl }}/practices)
    
    This panel provides general resources that aim to help conceptualising and applying attribution methods. Here are page examples that fit this category:
    - Getting started 
    - Causal diagrams
    <!-- - Review articles -->
    - Compare multiple methods etc.


1. [Criteria panel ]({{ site.baseurl }}/criteria)

    This panel provides information on every criterion used to subset detection & attribution methods when using the navigator. Pages follow a common documentation structure: *Definition*, *Explanation*, *Tools/rationale for helping assessment* and *Example*.


1. [Method panel]({{ site.baseurl }}/methods)

    This panel provides information on every method listed in the navigator. The methods are described along a common documentation structure: *Description & principle*, *Reference articles*, *Implementation packages* and the *Assessment table* reflecting how the method is filtered against criteria evaluation.


1. [DAM Gallery]({{ site.baseurl }}/gallery)

    This final panel illustrates how the DAM can be used with examples, from the question + data at hands, to the criteria assessment and the method application. Examples include:
    - STOC + synthetic controls 
    - Other T3.2 applications and project’s voluntary studies 



## Contact

XXXX