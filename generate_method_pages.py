import os
import csv
import re
import textwrap

# === CONFIGURATION ===
INPUT_FILE = "_data/method_assessments.tsv"
OUTPUT_ROOT = "contents/methods"
LAYOUT = "method"

# === Category → folder mapping ===
CATEGORY_FOLDER_MAP = {
    "Adjusted methods (Backdoor C.)": "adjusted",
    "Alternative paradigms": "alternative",
    "Causal ML": "causal_ML",
    "Independent detection": "detection", 
    "Causal discovery": "discovery",
    "Ecology-guided Modelling": "ecology-guided",
    "Experiments": "experiments",
    "Quasi-experiments": "quasi-exps",
    "Counterfactual & future simulations": "simulations",
    "Versatile tools": "tools"
}

# === Category → folder mapping ===
CATEGORY_TITLE_MAP = {
    "Adjusted methods (Backdoor C.)": "Adjusted methods",
    "Alternative paradigms": "Alternative paradigms",
    "Causal ML": "Causal ML",
    "Independent detection": "Independent detection", 
    "Causal discovery": "Causal discovery",
    "Ecology-guided Modelling": "Ecology-guided Modelling",
    "Experiments": "Experiments",
    "Quasi-experiments": "Quasi-experiments",
    "Counterfactual & future simulations": "Counterfactual & future simulations",
    "Versatile tools": "Versatile tools"
}


with open("_data/method_assessments.tsv", newline='', encoding='utf-8') as infile, \
     open("_data/method_assessments_clean.tsv", "w", newline='', encoding='utf-8') as outfile:
    
    lines = infile.readlines()[3:]  # skip metadata
    writer = outfile.writelines(lines)



def slugify(text):
    text = text.strip().lower()
    text = text.replace("/", "-").replace("&", "and")
    text = re.sub(r"[^\w\- ]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text

# === Read and skip first 3 lines ===
with open(INPUT_FILE, newline='', encoding='utf-8') as f:
    lines = f.readlines()[3:]

reader = csv.DictReader(lines, delimiter="\t")

for row in reader:
    method = row.get("Method list", "").strip()
    category_raw = row.get("Category", "").strip()
    assessor = row.get("Assessor", "").strip()

    if not method or not category_raw:
        continue

    # Use first category only
    main_category = category_raw.split(",")[0].strip()
    folder_name = CATEGORY_FOLDER_MAP.get(main_category, "uncategorized")

    # Parent
    parent_name = CATEGORY_TITLE_MAP.get(main_category, "uncategorized")

    # Slugified file name
    slug = slugify(method)
    category_folder = os.path.join(OUTPUT_ROOT, folder_name)
    os.makedirs(category_folder, exist_ok=True)

    filepath = os.path.join(category_folder, f"{slug}.md")

    # if os.path.exists(filepath):
    #     print(f"Skipping existing: {filepath}")
    #     continue

    front_matter = f"""---
layout: {LAYOUT}
title: "{method.strip()}"
parent: "{parent_name}"
nav_order: 1
date: 2025-07-17
author: Mrs. Young
---
<!-- This file was auto-generated from {INPUT_FILE} -->
"""
    
    categories_raw = [cat.strip() for cat in category_raw.split(",")]
    main_category = categories_raw[0]
    other_categories = categories_raw[1:]

    # Build hyperlinked list of other categories
    other_links = []
    for oc in other_categories:
        label = oc
        slug = CATEGORY_FOLDER_MAP.get(oc, slugify(oc))
        url = f"/{slug}/"
        other_links.append(f"[{label}]({url})")

    # Grammar-aware formatting of the list
    if len(other_links) == 1:
        category_note = f"This method also belongs to {other_links[0]}."
    elif len(other_links) == 2:
        category_note = f"This method also belongs to {other_links[0]} and {other_links[1]}."
    elif len(other_links) > 2:
        category_note = (
            "This method also belongs to " +
            ", ".join(other_links[:-1]) +
            f", and {other_links[-1]}."
        )
    else:
        category_note = ""


    body = textwrap.dedent(f"""\
        {{% if page.category_note != '' %}}
        {{: .note }}
        {category_note}
        {{% endif %}}
        
        
        ## Table of Contents
        {{: .no_toc .text-delta }}

        1. TOC
        {{:toc}}


        ## Description & principle 
        A clear, technical yet accessible explanation of the method, its core principle(s).


        ### Major variants
        {{: .no_toc }}
        {{: .d-inline-block }}
        optional
        {{: .label}}

        If the method has variants that seem important, either already widespread or promising and well documented. 

        ### Further online resources
        {{: .no_toc }}

        References to useful online resources to get started, e.g. [explanation blogs](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html){{:target="_blank"}}


        ## Reference articles
        ### Method
        {{: .no_toc }}
        - One or a few key academic references that introduce or formalize the method. 

        ### Research applications
        {{: .no_toc }}
        #### With RS data in Ecology / Biodiversity
        {{: .no_toc }}
        - A

        #### Without RS data (Ecology domain)
        {{: .no_toc }}
        {{: .d-inline-block }}
        optional
        {{: .label}}

        - B

        ## Packages 

        #### Python
        {{: .no_toc }}

        #### R
        {{: .no_toc }}

        ### Code Cells
        {{: .no_toc }}
        {{: .d-inline-block }}
        optional
        {{: .label}}


        <!-- For referencement in toc before automatic table -->
        ## Assessment table
    """)
    

    with open(filepath, "w", encoding="utf-8") as out:
        # out.write(front_matter)
        out.write(front_matter.strip() + "\n\n" + body.strip() + "\n")

    print(f"Created: {filepath}")