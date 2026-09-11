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
| Brand-new method from scratch (assess + document) | [Both issues, in order](#3-add-a-brand-new-method-from-scratch) |
| Revision of an existing [documentation page](https://estopinj.github.io/dam/methods) | [Pull request](#4-revise-an-existing-documentation-page) |
| Find a method that needs help | [Pending list](#5-what-methods-need-help) |
| Revise or add a [Good practices page](https://estopinj.github.io/dam/practices) | [Pull request](#6-good-practices-pages) |
| Revise or add an [Examples page](https://estopinj.github.io/dam/examples) | [Pull request](#7-examples-pages) |

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

## 3. Add a brand-new method from scratch

Fully positioning a new method requires two steps, in order:

1. **Assess it** with the **Method assessment** issue template.
2. **Document it** with the **Method documentation** issue template.

Assessment first ensures the method becomes filterable; documentation then provides description, references, and implementation details.

## 4. Revise an existing documentation page

Revisions of existing [documentation pages](https://estopinj.github.io/dam/methods) are made via pull requests, not issues.

From the website:

1. Scroll to the bottom and click **Edit this page on GitHub**.
2. Click the pencil icon to edit the `.md` file:

   <img src="https://estopinj.github.io/dam/assets/images/github-pencil-edit.svg" alt="GitHub pencil icon to edit a file" width="32" style="vertical-align:middle; border:1px solid #d0d7de; border-radius:6px; padding:4px; background:#f6f8fa;" />
3. Propose changes on the shared `doc` branch (or a new `doc/<short-topic>` branch for larger work, e.g. `doc/synthetic-controls-refs`), then open a pull request against `main` (or `dev` if open) with a clear title (e.g. `docs: clarify assumptions on Synthetic controls`).

Alternatively, edit the page source directly under `contents/methods/`, commit on the `doc` branch, and open a pull request.

For assessment corrections, use the **Method assessment** issue template instead (see section 1).

## 5. What methods need help?

See the pending list of methods waiting to be assessed or documented (auto-generated from the assessment table; file to be added at `contents/methods/pending.md`).

If unsure where to start, pick a method from that list and follow sections 1–2.

## 6. Good practices pages

[Good practices pages](https://estopinj.github.io/dam/practices) follow the same process as [method documentation pages](#4-revise-an-existing-documentation-page):

1. Scroll to the bottom of the page and click **Edit this page on GitHub**.
2. Click the pencil icon to edit the `.md` file.
3. Propose changes on the shared `doc` branch (or a new `doc/<short-topic>` branch for larger work), then open a pull request against `main` (or `dev` if open).

New pages are added the same way: create a `.md` file under `contents/practices/` on the `doc` branch and open a pull request.

## 7. Examples pages

[Examples pages](https://estopinj.github.io/dam/examples) follow the same process as [Good practices pages](#6-good-practices-pages):

1. Scroll to the bottom of the page and click **Edit this page on GitHub**.
2. Click the pencil icon to edit the `.md` file.
3. Propose changes on the shared `doc` branch (or a new `doc/<short-topic>` branch for larger work), then open a pull request against `main` (or `dev` if open).

New pages are added the same way: create a `.md` file under `contents/examples/` on the `doc` branch and open a pull request.

## Questions?

Open a blank issue or contact the maintainers. Thanks for improving NaviDAM.