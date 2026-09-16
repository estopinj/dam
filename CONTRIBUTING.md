<!-- Logos (absolute URLs so they render both on GitHub and on the Jekyll site) -->
<div class="logo-row">
  <img src="https://estopinj.github.io/dam/assets/images/logos/Obsgession_text_logo.png" alt="Obsgession" style="width:250px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/logo-FRB-Cesab-anglais_cropped.png" alt="FRB Cesab" style="width:175px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/Logo_cnrs.png" alt="CNRS" style="width:60px; margin:0 18px; vertical-align:middle;">
  <img src="https://estopinj.github.io/dam/assets/images/logos/logo-leca.png" alt="LECA" style="width:150px; margin:0 18px; vertical-align:middle;">
</div>
--------------------------------

# Contributing to NaviDAM 👋

Welcome, and thanks for your interest in NaviDAM! ✨

NaviDAM is a collaborative effort. Method suggestions depend directly on the quality and number of method assessments: the more complete and accurate the assessments, the more useful the guidance.

All contributions are welcome, and your ideas matter more than perfect formatting. 🙏 No coding skills are required for most contributions — fixing a typo, adding a reference, or sharing domain expertise is already valuable.

Please follow the [Code of Conduct](https://github.com/estopinj/dam/blob/main/CODE_OF_CONDUCT.md) in all interactions. Be kind, use inclusive language, and assume good intent, especially when discussing methods or assessments where opinions may differ. 🤝

## At a glance 💡

| Goal | How |
|------|-----|
| New assessment or revision of an existing assessment | 📝 [Method assessment issue](#1-assess-a-method-new-or-revision) |
| New documentation page or completion of an existing one | 📝 [Method documentation issue](#2-document-a-method-new-or-completion) |
| Revision of an existing [documentation page](https://estopinj.github.io/dam/methods) | 🔍 [Pull request](#3-revise-an-existing-documentation-page) |
| Brand-new method from scratch (assess + document) | ✨ [Both issues, in order](#4-add-a-brand-new-method-from-scratch) |
| Revise or add a [Good practices](https://estopinj.github.io/dam/practices) or [Examples](https://estopinj.github.io/dam/examples) page | 🔍 [Pull request](#5-good-practices-and-examples-pages) |
| Question, site bug, or infrastructure suggestion | 💬 [Blank issue](https://github.com/estopinj/dam/issues/new/choose) |

> Go to **Issues > New issue** and choose the matching template: <https://github.com/estopinj/dam/issues/new/choose>.
> Before opening a new issue, please search [existing issues](https://github.com/estopinj/dam/issues) to avoid duplicates and consider joining an ongoing discussion.

## 1. Assess a method (new or revision) 📝

Use the **Method assessment** issue template for both cases. Assessments position [methods](https://estopinj.github.io/dam/methods) against the [criteria](https://estopinj.github.io/dam/criteria).

- **New assessment:** choose `Is the method already assessed in NaviDAM? > No`, give the method name, and fill in the criteria.
- **Revision:** choose `Is the method already assessed in NaviDAM? > Yes`, give the exact existing method name, and fill in the full form with suggested values. Only differing criteria are proposed as changes for maintainer review.

💡 **Tips for a good assessment:**
- Base family-level assessments on the most common or original variant, and add options matching major, widespread variants.
- Use the [criteria pages](https://estopinj.github.io/dam/criteria) to check definitions before answering.
- Add rationale or comments at the end of the form to justify choices — this greatly helps review.

What happens next: a pull request is opened automatically. New rows are added directly; revisions are listed as old → new suggestions to accept or reject. A maintainer reviews and may ask for clarification in the issue thread.

## 2. Document a method (new or completion) 📝

Use the **Method documentation** issue template for both cases. Documentation fills the [methods](https://estopinj.github.io/dam/methods) pages (description, references, implementation).

- **New page:** choose `Is the method already documented in NaviDAM? > No`. A page is created from the submission.
- **Completion:** choose `Yes`, give the exact page title, and fill in only the sections to add. Placeholders are replaced on first contribution; later contributions are appended.

💡 **Tips for good documentation:**
- Follow the standard page structure: *Description & principle*, *Major variants*, *Reference articles* (method + research applications), *Implementation* (Python / R), and the *Assessment table*.
- Prefer one clear, well-commented implementation example per language over an exhaustive list of variants.
- Cite key references (method paper + ecological applications where possible) and link useful tutorials or blogs.
- Keep language clear and accessible: readers range from beginners to experts.

### What methods need help? 🌱

Good first contributions include completing thin pages, adding references, or documenting a method you know well. If unsure where to start, browse the [methods panel](https://estopinj.github.io/dam/methods) for pages with placeholders and follow sections 1–2 above.

## 3. Revise an existing documentation page 🔍

Revisions of existing [documentation pages](https://estopinj.github.io/dam/methods) are made via pull requests, not issues. Even small fixes (typos, broken links, clearer wording) are welcome — there is no minimum size for a useful contribution. ✨

From the website:

1. Scroll to the bottom and click **Edit this page on GitHub**.
2. Click the pencil icon ✏️ to edit the `.md` file.
3. Propose changes on a new `doc/<short-topic>` branch (e.g. `doc/synthetic-controls-refs`), then open a pull request against `main` with a clear title (e.g. `docs: clarify assumptions on Synthetic controls`).

💡 **Pull request best practices:**
- Keep changes focused: one topic per pull request is much easier to review.
- Write a clear title and describe what you changed and why.
- If the work is still in progress, open a draft pull request to get early feedback.
- Be responsive to reviewer comments — discussion is part of the process.

For assessment corrections, use the **Method assessment** issue template instead (see section 1).

## 4. Add a brand-new method from scratch ✨

Fully positioning a new method requires two steps, in order:

1. **Assess it** with the **Method assessment** issue template.
2. **Document it** with the **Method documentation** issue template.

Assessment first ensures the method becomes filterable; documentation then provides description, references, and implementation details.

## 5. Good practices and Examples pages 🔍

Revisions of [Good practices](https://estopinj.github.io/dam/practices) and [Examples](https://estopinj.github.io/dam/examples) pages follow the same process as [method documentation pages](#3-revise-an-existing-documentation-page):

1. Scroll to the bottom of the page and click **Edit this page on GitHub**.
2. Click the pencil icon ✏️ to edit the `.md` file.
3. Propose changes on a new `doc/<short-topic>` branch, then open a pull request against `main`.

New pages are added the same way: create a `.md` file under `contents/practices/` or `contents/examples/` on a `doc/<short-topic>` branch and open a pull request against `main`.

💡 For new pages, look at an existing page in the same panel as a template (front-matter + section structure), keep filenames in lower-case with hyphens, and link to related [criteria](https://estopinj.github.io/dam/criteria) or [methods](https://estopinj.github.io/dam/methods) where relevant.

## Recognition 🙌

Contributors are credited as page authors on the pages they create or substantially complete, and every issue and pull request is part of the public record. If you contributed and are not credited, please let us know in the relevant thread.

## Licensing 📄

By contributing, you agree that your contributions will be shared under the repository's licenses: code under GPLv3+, documentation and scientific text under CC BY 4.0. See [`LICENSE`](https://github.com/estopinj/dam/blob/main/LICENSE) for details.

## Questions? 💬

- Open a [blank issue](https://github.com/estopinj/dam/issues/new/choose) for questions, bug reports, or suggestions about the site itself.
- For direct contact, see the [About page](https://estopinj.github.io/dam/about).

Thanks for improving NaviDAM! 🎉