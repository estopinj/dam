---
title: Contributing
layout: about
nav_order: 7
permalink: /contributing/
description: "Describe how to contribute to NaviDAM"
categories:
- contributing
---

<!-- Logos (absolute URLs so they render both on GitHub and on the Jekyll site) -->
<div class="logo-row">
  <img src="https://estopinj.github.io/dam/assets/images/logos/Obsgession_text_logo.png" alt="Obsgession" style="width:250px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/logo-FRB-Cesab-anglais_cropped.png" alt="FRB Cesab" style="width:175px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/Logo_cnrs.png" alt="CNRS" style="width:60px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/logo-leca.png" alt="LECA" style="width:150px; margin:0 18px; vertical-align:middle;">
</div>
--------------------------------

# Contributing to NaviDAM

NaviDAM is a collaborative effort. Method suggestions depend directly on the quality and number of method assessments: the more complete and accurate the assessments, the more useful the guidance.

All contributions are welcome. No coding skills are required for most contributions.

Please follow the [Code of Conduct](https://github.com/estopinj/dam/blob/main/CODE_OF_CONDUCT.md) in all interactions.

## At a glance

| Goal | How |
|------|-----|
| New assessment or revision of an existing assessment | [Method assessment issue](#1-assess-a-method-new-or-revision) |
| New documentation page or completion of an existing one | [Method documentation issue](#2-document-a-method-new-or-completion) |
| Revision of an existing [documentation page](https://estopinj.github.io/dam/methods) | [Pull request](#3-revise-an-existing-documentation-page) |
| Brand-new method from scratch (assess + document) | [Both issues, in order](#4-add-a-brand-new-method-from-scratch) |
| Revise or add a [Good practices](https://estopinj.github.io/dam/practices) or [Examples](https://estopinj.github.io/dam/examples) page | [Pull request](#5-good-practices-and-examples-pages) |

Go to **Issues > New issue** and choose the matching template: <https://github.com/estopinj/dam/issues/new/choose>.

## 1. Assess a method (new or revision)

Use the **Method assessment** issue template for both cases. Assessments position [methods](https://estopinj.github.io/dam/methods) against the [criteria](https://estopinj.github.io/dam/criteria).

- **New assessment:** choose `Is the method already assessed in NaviDAM? > No`, give the method name, and fill in the criteria.
- **Revision:** choose `Is the method already assessed in NaviDAM? > Yes`, give the exact existing method name, and fill in the full form with suggested values. Only differing criteria are proposed as changes for maintainer review.

What happens next: a pull request is opened automatically. New rows are added directly; revisions are listed as old → new suggestions to accept or reject.

## 2. Document a method (new or completion)

Use the **Method documentation** issue template for both cases. Documentation fills the [methods](https://estopinj.github.io/dam/methods) pages (description, references, implementation).

- **New page:** choose `Is the method already documented in NaviDAM? > No`. A page is created from the submission.
- **Completion:** choose `Yes`, give the exact page title, and fill in only the sections to add. Placeholders are replaced on first contribution; later contributions are appended.

### What methods need help?

See the pending list of methods waiting to be assessed or documented (auto-generated from the assessment table; file to be added at `contents/methods/pending.md`).

If unsure where to start, pick a method from that list and follow sections 1–2.

## 3. Revise an existing documentation page

Revisions of existing [documentation pages](https://estopinj.github.io/dam/methods) are made via pull requests, not issues.

From the website:

1. Scroll to the bottom and click **Edit this page on GitHub**.
2. Click the pencil icon to edit the `.md` file:

   <svg width="32" height="32" viewBox="0 0 16 16" style="vertical-align:middle; border:1px solid #d0d7de; border-radius:6px; padding:4px; background:#f6f8fa;" role="img" aria-label="GitHub pencil icon to edit a file"><rect width="16" height="16" rx="3" fill="#f6f8fa" stroke="#d0d7de"></rect><path fill="#24292f" d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.757l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064l6.286-6.286Zm2.262-3.199-1.086-1.086a.25.25 0 0 0-.354 0L10.925 3.05l1.44 1.44 1.086-1.086a.25.25 0 0 0 0-.354Z"></path></svg>
3. Propose changes on a new `doc/<short-topic>` branch (e.g. `doc/synthetic-controls-refs`), then open a pull request against `main` with a clear title (e.g. `docs: clarify assumptions on Synthetic controls`).

For assessment corrections, use the **Method assessment** issue template instead (see section 1).

## 4. Add a brand-new method from scratch

Fully positioning a new method requires two steps, in order:

1. **Assess it** with the **Method assessment** issue template.
2. **Document it** with the **Method documentation** issue template.

Assessment first ensures the method becomes filterable; documentation then provides description, references, and implementation details.

## 5. Good practices and Examples pages

[Good practices](https://estopinj.github.io/dam/practices) and [Examples](https://estopinj.github.io/dam/examples) pages follow the same process as [method documentation pages](#3-revise-an-existing-documentation-page):

1. Scroll to the bottom of the page and click **Edit this page on GitHub**.
2. Click the pencil icon to edit the `.md` file.
3. Propose changes on a new `doc/<short-topic>` branch, then open a pull request against `main`.

New pages are added the same way: create a `.md` file under `contents/practices/` or `contents/examples/` on a `doc/<short-topic>` branch and open a pull request against `main`.

## Questions?

Open a blank issue or contact the maintainers. Thanks for improving NaviDAM.