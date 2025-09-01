---
title: Home
layout: home
nav_order: 1
description: "NaviDAM provides a criteria-based engine to allow users describing their case-study properties and identify a set of suited attribution methods."
permalink: /
---




# **NaviDAM** - A decision tool to help you navigate *Detection* and *Attribution* Methods


## Welcome !

NaviDAM is an interactive decision-support tool designed to help users explore, compare, and select appropriate detection and attribution methods based on the nature of their project.
{: .fs-6 .fw-300 }


- **Users are invited [below](#evaluate-needs) to qualify their _objective_, _data at hands_ and affordable _assumptions_ between others by assessing different <a href="{{ site.baseurl }}/criteria" target="_blank" rel="noopener noreferrer">criteria</a>**
- **[Suited methods](#candidate-methods) are described in more detail on <a href="{{ site.baseurl }}/methods" target="_blank" rel="noopener noreferrer">documentation pages</a>, allowing users to get started on their project using relevant resources**
- The <a href="{{ site.baseurl }}/practices" target="_blank" rel="noopener noreferrer">Good practices</a> and <a href="{{ site.baseurl }}/gallery" target="_blank" rel="noopener noreferrer">Gallery</a> panels respectively provide conceptual and general resources on attribution, causal inference & detection, and NaviDAM application examples [*ongoing work*]

*Check the [About page]({{ site.baseurl }}/about) for further information*


{: .note-title }
> Credits
> 
> This is a joint developpement of the <a href="https://obsgession.eu/" target="_blank" rel="noopener noreferrer">OBSGESSION</a> Horizon Europe project and of the <a href="https://www.fondationbiodiversite.fr/en/the-frb-in-action/programs-and-projects/le-cesab/impacts/" target="_blank" rel="noopener noreferrer">IMPACTS</a> research group.

{: .highlight-title}
> Status
> 
> This website is under active development.

<a id="evaluate-needs"></a>
## Evaluating your project's needs

Choose the [criteria]({{ site.baseurl }}/criteria) options in the dropdown lists that **best describe your project**. Criteria are adapted to each objective.

<script id="site-baseurl" type="application/json">
  "{{ site.baseurl }}"
</script>

<script id="cat-dicts" type="application/json">
  {{ site.data.cat_dicts | jsonify }}
</script>

<script id="criteria-mapping" type="application/json">
  {{ site.data.criteria_mapping | jsonify }}
</script>

<script id="method-data" type="application/json">
  {{ site.data.method_assessments_clean | jsonify }}
</script>

<script id="objective-criteria-map" type="application/json">
  {{ site.data.objective_criteria_map | jsonify }}
</script>

<div id="criteria-filters"></div>


<a id="suggested-methods"></a>
## *Candidate methods*

<div id="filtered-methods"></div>



## *Graph Explorer*

{: .new}
> A <a href="https://neo4j.com/docs/getting-started/graph-database/" target="_blank" rel="noopener noreferrer"><strong>Neo4j</strong></a> graph database is being developed to explore, vizualize and query the network of methods and criteria.

- Illustrative scheme highlighting some methods
![]({{ site.baseurl }}/assets/images/DAM_Scheme_greenHighlight.png){: width="75%" }




[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[Jekyll]: https://jekyllrb.com
[Bundler]: https://bundler.io/
[Markdown]: https://daringfireball.net/projects/markdown/
<!-- [**Neo4j**]: https://neo4j.com/docs/getting-started/graph-database/ -->