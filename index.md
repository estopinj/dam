---
title: Home
layout: home
nav_order: 1
description: "NaviDAM provides a criteria-based engine to allow users describing their case-study properties and identify a set of suited attribution methods."
permalink: /
---

# **Detection & Attribution Modelling navigator**


## Welcome
This website provides access to the Detection & Attribution Modelling (DAM) navigator called **NaviDAM**, a guide suggesting you methods suited to your project.
{: .fs-6 .fw-300 }


- Different [criteria]({{ site.baseurl }}/criteria) below invite users to precisely qualify _objective_, _data at hands_ and affordable _assumptions_ between others to **narrow down** and **suggest detection & attribution methods** suited to their study.
- [Methods]({{ site.baseurl }}/methods) are further describe with dedicated pages to allow users jump start their project from the relevant ressources.

{: .important-title }
_This is a developpement of the OBSGESSION Horizon Europe project._

{: .highlight-title}
> Status
> {: .d-inline-block }
> DEV (V0)
> {: .label .label-green }
> 
> This website is under active development.


# Evaluating your project's needs

- This is in this section that users evaluate their project against the different [criteria]({{ site.baseurl }}/criteria) of the navigator.

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

<div id="criteria-filters"></div>


## Results 


### List of methods

<div id="filtered-methods"></div>



### NaviDAM Graph Explorer

- Illustrative scheme highlighting some methods
![]({{ site.baseurl }}/assets/images/DAM_Scheme_greenHighlight.png){: width="75%" }




[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[Jekyll]: https://jekyllrb.com
[Bundler]: https://bundler.io/
[Markdown]: https://daringfireball.net/projects/markdown/