import os
import csv
import re
import textwrap
import json
import shutil
import subprocess
from pathlib import Path
from tsv_clean import clean_tsv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# === CONFIGURATION ===
INPUT_FILE = PROJECT_ROOT / "_data/DetectionAttribution methods - Method Assessment.tsv"
OUTPUT_FILE = PROJECT_ROOT / "_data/method_assessments_clean.tsv"
DICTS_FILE = PROJECT_ROOT / "_data/cat_dicts.json"
OUTPUT_ROOT = PROJECT_ROOT / "contents/methods"
LAYOUT = "method"


def norm(text):
    return " ".join(text.split())


def split_list(raw):
    return [norm(x) for x in raw.split(",") if norm(x)]


def slugify(text):
    text = text.strip().lower()
    text = text.replace("/", "-").replace("&", "and")
    text = re.sub(r"[^\w\- ]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


# Read from file (slug dictionaries are extended on the fly with new categories)
with open(DICTS_FILE, "r") as f:
    data = json.load(f)

CATEGORY_FOLDER_MAP = {norm(k): v for k, v in data["CATEGORY_FOLDER_MAP"].items()}
SUBCAT_FOLDER_MAP = {norm(k): v for k, v in data["SUBCAT_FOLDER_MAP"].items()}
SUBCAT_PARENT = {norm(k): norm(v) for k, v in data["SUBCAT_PARENT"].items()}

clean_tsv(INPUT_FILE, OUTPUT_FILE)

# === Read and skip first 3 lines ===
with open(INPUT_FILE, newline='', encoding='utf-8') as f:
    lines = f.readlines()[3:]

rows = list(csv.DictReader(lines, delimiter="\t"))

# === Register categories / sub-categories that are new in the TSV ===
dicts_changed = False
for row in rows:
    cats = split_list(row.get("Category", ""))
    subs = split_list(row.get("Sub-category", ""))
    for c in cats:
        if c not in CATEGORY_FOLDER_MAP:
            CATEGORY_FOLDER_MAP[c] = slugify(c)
            dicts_changed = True
    for sc in subs:
        if sc not in SUBCAT_FOLDER_MAP:
            SUBCAT_FOLDER_MAP[sc] = slugify(sc)
            dicts_changed = True
        if sc not in SUBCAT_PARENT and cats:
            SUBCAT_PARENT[sc] = cats[0]
            dicts_changed = True
if dicts_changed:
    data["CATEGORY_FOLDER_MAP"] = CATEGORY_FOLDER_MAP
    data["SUBCAT_FOLDER_MAP"] = SUBCAT_FOLDER_MAP
    data["SUBCAT_PARENT"] = SUBCAT_PARENT
    with open(DICTS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {DICTS_FILE} with new categories/sub-categories")


# === Existing pages, indexed by front-matter title ===
def read_front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return text, m


def front_matter_title(path):
    try:
        _, m = read_front_matter(path)
    except (OSError, UnicodeDecodeError):
        return None
    if not m:
        return None
    t = re.search(r"^title:\s*(.*?)\s*$", m.group(1), re.M)
    return norm(t.group(1).strip("\"'")) if t else None


EXISTING = {}
for md in OUTPUT_ROOT.rglob("*.md"):
    title = front_matter_title(md)
    if title:
        EXISTING.setdefault(title, []).append(md)


def find_existing(method, filepath, is_index):
    if filepath.exists():
        return filepath
    for cand in EXISTING.get(method, []):
        if (cand.name == "index.md") == is_index and cand.exists():
            return cand
    return None


def move_page(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(src)],
        cwd=PROJECT_ROOT, capture_output=True,
    ).returncode == 0
    if tracked:
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=PROJECT_ROOT, check=True)
    else:
        shutil.move(str(src), str(dst))
    # Remove now-empty folders left behind
    d = src.parent
    while d != OUTPUT_ROOT and d.exists() and not any(d.iterdir()):
        d.rmdir()
        d = d.parent
    print(f"Moved: {src} -> {dst}")


NOTE_START = "<!-- category-note:start -->"
NOTE_END = "<!-- category-note:end -->"
NOTE_RE = re.compile(
    r"(?:" + re.escape(NOTE_START) + r".*?" + re.escape(NOTE_END) +
    r"|\{% if page\.category_note != '' %\}.*?\{% endif %\})\n*",
    re.S,
)


def join_links(links):
    if len(links) <= 1:
        return "".join(links)
    if len(links) == 2:
        return f"{links[0]} and {links[1]}"
    return ", ".join(links[:-1]) + f", and {links[-1]}"


def build_note(cats, subcats, main_cat):
    """Markdown note listing the other categories / sub-categories of the method."""
    parts = []
    other_cats = cats[1:]
    if other_cats:
        links = [
            f"[{c}]({{{{ site.baseurl }}}}/{CATEGORY_FOLDER_MAP[c]})" for c in other_cats
        ]
        parts.append(f"This method also belongs to {join_links(links)}.")
    other_subs = subcats[1:]
    if other_subs:
        links = []
        for sc in other_subs:
            parent = SUBCAT_PARENT.get(sc)
            parent_folder = CATEGORY_FOLDER_MAP.get(parent, CATEGORY_FOLDER_MAP[main_cat])
            links.append(
                f"[{sc}]({{{{ site.baseurl }}}}/{parent_folder}/{SUBCAT_FOLDER_MAP[sc]})"
            )
        label = "sub-category" if len(links) == 1 else "sub-categories"
        parts.append(f"It also belongs to the {label} {join_links(links)}.")
    if not parts:
        return ""
    return f"{NOTE_START}\n\n{{: .note }}\n{' '.join(parts)}\n\n{NOTE_END}"


def sync_page(path, parent, note):
    """Update the parent and the category note of an existing page, keeping the rest."""
    text, m = read_front_matter(path)
    if not m:
        return
    fm = m.group(1)
    if re.search(r"^parent:", fm, re.M):
        new_fm = re.sub(r"^parent:.*$", lambda _: f'parent: "{parent}"', fm, flags=re.M)
    else:
        new_fm = fm + f'\nparent: "{parent}"'
    body = NOTE_RE.sub("", text[m.end():].lstrip("\n"), count=1)
    comment = re.match(r"(<!--.*?-->\n)", body)
    if note:
        if comment:
            body = comment.group(1) + "\n" + note + "\n\n" + body[comment.end():].lstrip("\n")
        else:
            body = note + "\n\n" + body.lstrip("\n")
    new_text = f"---\n{new_fm}\n---\n{body}" if not body.startswith("\n") else f"---\n{new_fm}\n---{body}"
    new_text = new_text.rstrip("\n") + "\n"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated categories: {path}")


for row in rows:
    method = row.get("Method", "").strip()
    cats = split_list(row.get("Category", ""))
    subcats = split_list(row.get("Sub-category", ""))

    if not method or not cats:
        continue

    CAT = cats[0]
    CAT_folder = OUTPUT_ROOT / CATEGORY_FOLDER_MAP[CAT]
    SUBCAT = subcats[0] if subcats else None
    SUBCAT_folder = None
    is_index = bool(SUBCAT) and norm(method) == SUBCAT

    if not SUBCAT:
        PARENT = CAT
        filepath = CAT_folder / f"{slugify(method)}.md"
    else:
        SUBCAT_folder = CAT_folder / SUBCAT_FOLDER_MAP[SUBCAT]
        if is_index:
            PARENT = CAT
            filepath = SUBCAT_folder / "index.md"
        else:
            PARENT = SUBCAT
            filepath = SUBCAT_folder / f"{slugify(method)}.md"

    category_note = build_note(cats, subcats, CAT)

    ### Existing page: move to the right folder and sync categories ###
    existing = find_existing(norm(method), filepath, is_index)
    if existing is not None:
        if existing != filepath:
            if filepath.exists():
                print(f"WARNING: cannot move {existing}, {filepath} already exists")
                continue
            move_page(existing, filepath)
        sync_page(filepath, PARENT, category_note)
        continue
    ####################################

    front_matter = f"""---
layout: {LAYOUT}
title: "{method}"
parent: "{PARENT}"
date: 2025-07-17
author: Mrs. Young
---
<!-- This file was auto-generated from {INPUT_FILE.name} -->
"""
    note_block = category_note + "\n\n" if category_note else ""

    if is_index:
        body = f"{note_block}## Assessment table\n"
    else:
        body = note_block + textwrap.dedent("""\
        ## Table of Contents
        {: .no_toc .text-delta }

        1. TOC
        {:toc}


        ## Description & principle 
        A clear, technical yet accessible explanation of the method, its core principle(s).


        ### Major variants
        {: .no_toc }
        {: .d-inline-block }
        optional
        {: .label}

        If the method has variants that seem important, either already widespread or promising and well documented. 

        ### Further online resources
        {: .no_toc }

        References to useful online resources to get started, e.g. [explanation blogs](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html){:target="_blank"}


        ## Reference articles
        ### Method
        {: .no_toc }
        - One or a few key academic references that introduce or formalize the method. 

        ### Research applications
        {: .no_toc }
        #### With RS data in Ecology / Biodiversity
        {: .no_toc }
        - A

        #### Without RS data (Ecology domain)
        {: .no_toc }
        {: .d-inline-block }
        optional
        {: .label}

        - B

        ## Implementation 

        #### Python
        {: .no_toc }

        #### R
        {: .no_toc }

        ### Code Cells
        {: .no_toc }
        {: .d-inline-block }
        optional
        {: .label}


        <!-- For referencement in toc before automatic table -->
        ## Assessment table
        """)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(front_matter.strip() + "\n\n" + body.strip() + "\n", encoding="utf-8")
    print(f"Created: {filepath}")

    # Make sure the sub-category has an index page
    if SUBCAT:
        index_path = SUBCAT_folder / "index.md"
        if not index_path.exists() and find_existing(SUBCAT, index_path, True) is None:
            index_path.write_text(
                f'---\ntitle: "{SUBCAT}"\nparent: "{CAT}"\n---\n\n# {SUBCAT}\n',
                encoding="utf-8",
            )
