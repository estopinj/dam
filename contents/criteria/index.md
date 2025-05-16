---
title: Criteria
nav_order: 3
permalink: /criteria
---

# Criteria

- This panel provides information on every criterion used to subset detection & attribution [methods]({{ site.baseurl }}/methods) when using the framework.
- Criteria are grouped in five descriptive categories: *Outcome*, *Data Compatibility*, *Assumptions*, *Model Properties*, and *Packages*.
{: .fs-6 .fw-300 }

They capture: 
- What a method aims to do
- Which data structures it requires or supports
- Under which foundational assumptions it remains valid
- How it behaves in terms of flexibility, scale, and feature support
- Where and how it can be implemented in practice

{: .note }
Criterion pages follow a common documentation format: ***Definition***, ***Explanation***, ***Tools/rationale for helping assessment*** and ***Example***.


## Common criterion options

Every criterion has the four base options to ease the assessment process: `Unevaluated`, `Don't know`, `Inapplicable`, and `Indifferent`. They are described below:


|  **Option**        | **Usage**                  | **Description**                  |
|:------------------:|:--------------------------:|---------------------------------|
| `Unevaluated`      | Default when starting the criteria assessment | When selected, the criterion applies no filtering on the suggested method set. Users should consider every criterion of the framework, and, only when deemed necessary, select one of the next two options `Don't know` or `Inapplicable`. |
| `Don't know`       | User don't know which option to pick | When the user judges not being able to rightly assess the method against a criterion (lack of documentation, understanding, unsure), this option avoids subsetting methods by the corresponding criterion. |
| `Inapplicable`     | Criterion cannot be applied because of incompatible paradigms | Because the framework ambitions to be large and to include methods from different fields relying on heterogeneous assumptions, a criterion can be irrelevant to a case study. Methods indeed rely on implicit / explicit modelling paradigms that are not all focused on the same aspects and are not fully compatible with each other. |
| `Indifferent`      | All options are satisfying | Users can estimate that all options of a criterion are satisfying. The corresponding criterion has therefore been evaluated but should not filter the suggested method set. |

{: .warning}
> `Don't know` allows to reach the end of the assessment more easily but should be picked only when necessary since it will result in a larger and less informative set of suitable methods.
> 
> {: .note}
> **? signs** redirecting to the criterion page should allow the user to apply criteria in most cases.
> 
> {: .note}
> When the criterion is understood but seems irrelevant to the question at hand, `Inapplicable` should be preferred.
  