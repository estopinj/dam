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

```js
Under development.
```

<!-- 2. Render Dropdowns for Each Criterion -->
<!-- Add this where you want the filters/results to appear -->
<div id="criteria-filters"></div>
<div id="filtered-methods"></div>


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


<!-- 1. Expose the Assessment Data as JSON -->
<!-- Add this to index.md -->
<script id="method-data" type="application/json">
  {{ site.data.method_assessments_clean | jsonify }}
</script>


<!-- 3. Add JavaScript for Interactivity -->
<script>
// filepath: index.md
// ...existing code...

document.addEventListener("DOMContentLoaded", function() {
  // 1. Load method data
  const methodData = JSON.parse(document.getElementById('method-data').textContent);

  // 2. Define the criteria you want dropdowns for (column names from your TSV)
  const criteria = [
    { key: "Objective", label: "Objective" },
    { key: "Estimand", label: "Estimand" },
    { key: "Validity", label: "Validity" },
    { key: "Type", label: "Data Type" },
    // Add more as needed, matching your TSV column headers
  ];

  // 3. Get unique options for each criterion
  const optionsByCriterion = {};
  criteria.forEach(criterion => {
    const opts = new Set();
    methodData.forEach(m => {
      if (m[criterion.key]) {
        m[criterion.key].split(",").forEach(val => opts.add(val.trim()));
      }
    });
    optionsByCriterion[criterion.key] = Array.from(opts).sort();
  });

  // 4. Render dropdowns
  const filtersDiv = document.getElementById("criteria-filters");
  criteria.forEach(criterion => {
    const label = document.createElement("label");
    label.textContent = criterion.label + ": ";
    const select = document.createElement("select");
    select.id = "filter-" + criterion.key;
    select.innerHTML = `<option value="">(Any)</option>` +
      optionsByCriterion[criterion.key].map(opt => `<option value="${opt}">${opt}</option>`).join("");
    label.appendChild(select);
    filtersDiv.appendChild(label);
    filtersDiv.appendChild(document.createElement("br"));
  });

  // 5. Filter and display methods
  function filterMethods() {
    let filtered = methodData;
    criteria.forEach(criterion => {
      const val = document.getElementById("filter-" + criterion.key).value;
      if (val) {
        filtered = filtered.filter(m =>
          m[criterion.key] && m[criterion.key].split(",").map(x => x.trim()).includes(val)
        );
      }
    });
    displayMethods(filtered);
  }

  // 6. Display filtered methods
  function displayMethods(methods) {
    const div = document.getElementById("filtered-methods");
    if (methods.length === 0) {
      div.innerHTML = "<p>No methods match your criteria.</p>";
      return;
    }
    div.innerHTML = "<ul>" + methods.map(m =>
      `<li><a href="/methods/${m["Method list"] | slugify}/">${m["Method list"]}</a></li>`
    ).join("") + "</ul>";
  }

  // 7. Attach event listeners
  criteria.forEach(criterion => {
    document.getElementById("filter-" + criterion.key).addEventListener("change", filterMethods);
  });

  // 8. Initial display
  displayMethods(methodData);
});

// Helper for slugifying (if needed)
function slugify(text) {
  return text.toString().toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]+/g, '');
}
</script>