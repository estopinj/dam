# Detection & Attribution Modelling Navigator

[![DOI](https://zenodo.org/badge/974315324.svg)](https://doi.org/10.5281/zenodo.22675343)


## Objective
- The Detection Attribution Modeling ([DAM]) Navigator serves the goal to orient users looking methods for detecting and disentangling the drivers of observed biodiversity change.
It **situates methods**, both *widespread* methods used in ecological studies and approaches inherited from *causal inference* or econometrics, against an ordered set of [criteria].

- The different [criteria] invite users to precisely qualify what they are looking for and what they have at hands to narrow down and suggest detection and/or attribution [methods] and tools suited to their study.



## Website structure

NaviDAM is implemented in this collaborative website and is organized around a dynamical method filtering tool on the *Home* page:

1. [Home]:
    - Brief description of the project
    - User input invite: Evaluate their project's needs
        - Criteria default to `Any`, including all options and therefore not filtering the set of suggested methods
   

2. The sidebar provides access to different panels grouping resource pages logically.
Its exploration in regards with the home page is key for robust use of the navigator.

    1. [Criteria] panel

        This panel provides information on every criterion used to subset detection & attribution methods when using the navigator. Pages follow a common documentation structure: *Definition*, *Explanation*, *Tools/rationale for helping assessment* and *Example*.

    1. [Methods] panel

        This panel provides information on every method listed in the navigator. The methods are described along a common documentation structure: *Description & principle*, *Reference articles*, *Implementation* and the *Assessment table* reflecting how the method is filtered against criteria evaluation.

    1. [Good practices] panel
        
        This panel provides general resources that aim to help conceptualising and applying attribution methods. Here are page examples that fit this category:
        - A primer on causal graphs
        - Beyond method selection
        - NavviDAM usage diagram
        <!-- - Review articles -->

    1. [Examples] panel

        This final panel illustrates how NaviDAM can be used with examples, from the question + data at hands, to the criteria assessment and the method application. Examples include:
        - STOC + synthetic controls 


## Building and previewing your site locally

Assuming [Jekyll] and [Bundler] are installed on your computer:
1.  Change your working directory to the root directory of your site.
2.  Run `bundle install`.
3.  Run `bundle exec jekyll serve` to build your site and preview it at `localhost:4000`.
    The built site is stored in the directory `_site`.


## Licensing and Attribution

The original NaviDAM source code is distributed under the [GNU General Public License v3.0 or later][GPLv3].

The original documentation and scientific text are distributed under the [Creative Commons Attribution 4.0 International License][CC BY 4.0].

These licenses apply only to original project material. Third-party components and externally sourced content retain their own licenses and attributions. See [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) for details.

The deployment GitHub Actions workflow is heavily based on GitHub's mixed-party [starter workflows]. A copy of their MIT License is available in [actions/starter-workflows].

----


[Bundler]: https://bundler.io/
[Jekyll]: https://jekyllrb.com
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[GPLv3]: https://www.gnu.org/licenses/gpl-3.0.html
[CC BY 4.0]: https://creativecommons.org/licenses/by/4.0/
[actions/starter-workflows]: https://github.com/actions/starter-workflows/blob/main/LICENSE


[DAM]: https://estopinj.github.io/dam/
[criteria]: https://estopinj.github.io/dam/criteria
[methods]: https://estopinj.github.io/dam/methods
[Landing page]: https://estopinj.github.io/dam/
[Good practices]: https://estopinj.github.io/dam/practices
[Examples]: https://estopinj.github.io/dam/examples


