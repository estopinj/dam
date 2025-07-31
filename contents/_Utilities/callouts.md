---
title: Callouts
parent: Utilities
nav_order: 7
categories:
- _Utilities
---

# Callouts
{: .d-inline-block }

New (v0.4.0)
{: .label .label-green }



Common kinds of callouts include `highlight`, `important`, `new`, `note`, and `warning`.

{: .warning }
These callout names are *not* pre-defined by the theme: you need to define your own names.


## An untitled callout
{: .no_toc .text-delta }

```markdown
{: .highlight }
A paragraph
```

{: .highlight }
A paragraph


## A single paragraph callout
{: .no_toc .text-delta }

```markdown
{: .note }
A paragraph
```

{: .note }
A paragraph

```markdown
{: .note-title }
> My note title
>
> A paragraph with a custom title callout
```

{: .note-title }
> My note title
>
> A paragraph with a custom title callout

## A multi-paragraph callout
{: .no_toc .text-delta }

```markdown
{: .important }
> A paragraph
>
> Another paragraph
>
> The last paragraph
```

{: .important }
> A paragraph
>
> Another paragraph
>
> The last paragraph

```markdown
{: .important-title }
> My important title
>
> A paragraph
>
> Another paragraph
>
> The last paragraph
```

{: .important-title }
> My important title
>
> A paragraph
>
> Another paragraph
>
> The last paragraph

## An indented callout
{: .no_toc .text-delta }

```markdown
> {: .highlight }
  A paragraph
```

> {: .highlight }
  A paragraph

## Indented multi-paragraph callouts
{: .no_toc .text-delta }

```markdown
> {: .new }
> > A paragraph
> >
> > Another paragraph
> >
> > The last paragraph
```

> {: .new }
> > A paragraph
> >
> > Another paragraph
> >
> > The last paragraph


## Nested callouts
{: .no_toc .text-delta }

```markdown
{: .important }
> {: .warning }
> A paragraph
```

{: .important }
> {: .warning }
> A paragraph

## Opaque background
{: .no_toc .text-delta }

```markdown
{: .important }
> {: .opaque }
> <div markdown="block">
> {: .warning }
> A paragraph
> </div>
```

{: .important }
> {: .opaque }
> <div markdown="block">
> {: .warning }
> A paragraph
> </div>
