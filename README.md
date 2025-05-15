# Detection & Attribution Modelling Framework


## Objective
- The Detection Attribution Modeling Framework ([DAM]) serves the goal to orient users looking methods for detecting and disentangling the drivers of observed biodiversity change.
It **situates methods**, both *widespread* methods used in ecological studies and approaches inherited from *causal inference* or econometrics, against an ordered set of [criteria].

- The different [criteria] invite users to precisely qualify what they are looking for and what they have at hands to narrow down and suggest detection and/or attribution [methods] and tools suited to their study.



## Website structure

The DAM framework is implemented in this collaborative website and is organized around a dynamical method scheme on the landing page:

1. [Landing page]:
    - Briefly description of the framework
    - Invite users to fill in [criteria] in default order
        - Criteria default to `Unevaluated`, including all options and therefore not filtering the set of suggested methods
   
    - Method scheme
        - Gets refined with criteria assessment
        <!-- ![Illustrative scheme highlighting some methods](/assets/images/DAM_Scheme_greenHighlight.png) -->
        <img src="https://estopinj.github.io/dam/assets/images/DAM_Scheme_greenHighlight.png" width="350" />


2. The sidebar provides access to different panels grouping resource pages logically.
Its exploration in regards with the landing page is key for good use of the framework.

    1. [Good practices] panel
        
        This panel provides general resources that aim to help conceptualising and applying attribution methods. Here are page examples that fit this category:
        - Getting started 
        - Causal diagrams
        <!-- - Review articles -->
        - Compare multiple methods etc.


    1. [Criteria] panel

        This panel provides information on every criterion used to subset detection & attribution methods when using the framework. Pages follow a common documentation structure: *Definition*, *Explanation*, *Tools/rationale for helping assessment* and *Example*.

        <!-- ![criteria list](/assets/images/DAM_criteria.png) -->
         <img src="https://estopinj.github.io/dam/assets/images/DAM_criteria.png" width="220" />

    1. [Methods] panel

        This panel provides information on every method listed in the framework. The methods are described along a common documentation structure: *Description & principle*, *Reference articles*, *Implementation packages* and the *Assessment table* reflecting how the method is filtered against criteria evaluation.


    1. [Gallery] panel

        This final panel illustrates how the DAM can be used with examples, from the question + data at hands, to the criteria assessment and the method application. Examples include:
        - STOC + synthetic controls 
        - Other T3.2 applications and project’s voluntary studies 





## Building and previewing your site locally

Assuming [Jekyll] and [Bundler] are installed on your computer:

1.  Change your working directory to the root directory of your site.

2.  Run `bundle install`.

3.  Run `bundle exec jekyll serve` to build your site and preview it at `localhost:4000`.

    The built site is stored in the directory `_site`.



## Licensing and Attribution

This repository is licensed under the [MIT License]. You are generally free to reuse or extend upon this code as you see fit; just include the original copy of the license (which is preserved when you "make a template").

The deployment GitHub Actions workflow is heavily based on GitHub's mixed-party [starter workflows]. A copy of their MIT License is available in [actions/starter-workflows].

----


[Bundler]: https://bundler.io/
[Jekyll]: https://jekyllrb.com
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[MIT License]: https://en.wikipedia.org/wiki/MIT_License
[actions/starter-workflows]: https://github.com/actions/starter-workflows/blob/main/LICENSE


[DAM]: https://estopinj.github.io/dam/
[criteria]: https://estopinj.github.io/dam/criteria
[methods]: https://estopinj.github.io/dam/methods
[Landing page]: https://estopinj.github.io/dam/
[Good practices]: https://estopinj.github.io/dam/practices
[Gallery]: https://estopinj.github.io/dam/gallery


