---
title: Home
layout: home
nav_order: 1
description: "The DAM Navigator provides a criteria-based engine to allow users describing their case-study properties and identify a set of suited attribution methods."
permalink: /
---

# **Detection & Attribution Modelling navigator**


## Welcome
This website provides access to the Detection & Attribution Modelling (DAM) navigator, a guide suggesting you methods suited to your project.
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

```js
Under development.
```

![]({{ site.baseurl }}/assets/images/DAM_criteria.png){: width="35%" }


## Results

- Illustrative scheme highlighting some methods
![]({{ site.baseurl }}/assets/images/DAM_Scheme_greenHighlight.png){: width="75%" }




- Mermaid scheme example

```mermaid
graph TD;
    accTitle: the diamond pattern
    accDescr: a graph with four nodes: A points to B and C, while B and C both point to D
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
[Mermaid](https://mermaid.js.org/){:target="_blank"} will eventually be used to allow representing an interactive method scheme updated by the user's evaluation of the criteria.



[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[Jekyll]: https://jekyllrb.com
[Bundler]: https://bundler.io/
[Markdown]: https://daringfireball.net/projects/markdown/