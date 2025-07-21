import os
import csv
import re
import textwrap
import json

# === CONFIGURATION ===
INPUT_FILE = "_data/method_assessments.tsv"
DICTS_FILE = "_data/cat_dicts.json"
OUTPUT_ROOT = "contents/methods"
LAYOUT = "method"


# Read from file
with open(DICTS_FILE, "r") as f:
    data = json.load(f)

# Access individual dictionaries
CATEGORY_FOLDER_MAP = data["CATEGORY_FOLDER_MAP"]
SUBCAT_FOLDER_MAP = data["SUBCAT_FOLDER_MAP"]
SUBCAT_PARENT = data["SUBCAT_PARENT"]


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
    subcategory_raw = row.get("Sub-category", "").strip()
    assessor = row.get("Assessor", "").strip()

    if not method or not category_raw:
        continue

    # Use first category only
    CAT = category_raw.split(",")[0].strip()
    CAT_folder_name = CATEGORY_FOLDER_MAP.get(CAT, "uncategorized")
    CAT_folder = os.path.join(OUTPUT_ROOT, CAT_folder_name)
    os.makedirs(CAT_folder, exist_ok=True)

    #print("Category raw before if:", category_raw)
    #print("Sub-category raw before if:", subcategory_raw)
    if not subcategory_raw:
        # print("No sub-category found, using main category as parent: CAT =", CAT)
        # If no sub-category, use main category as parent
        # Parent
        PARENT = CAT
        # Slugified file name
        slug = slugify(method)
        filepath = os.path.join(CAT_folder, f"{slug}.md")

    # There is a sub-category
    else:
        # If sub-category exists, use it for parent and folder name
        SUBCAT = subcategory_raw.split(",")[0].strip()
        SUBCAT_folder_name = SUBCAT_FOLDER_MAP.get(SUBCAT, "uncategorized")
        # Creates sub-category folder if it does not already exist
        SUBCAT_folder = os.path.join(CAT_folder, SUBCAT_folder_name)
        os.makedirs(SUBCAT_folder, exist_ok=True)

        # Index file for sub-category
        if method == SUBCAT:
            # Parent
            PARENT = CAT
            filepath = os.path.join(SUBCAT_folder, "index.md")
        # Member of sub-category
        else:
            # Parent
            PARENT = SUBCAT
            filepath = os.path.join(SUBCAT_folder, f"{slugify(method)}.md")


    # if os.path.exists(filepath):
    #     print(f"Skipping existing: {filepath}")
    #     continue


    front_matter = f"""---
layout: {LAYOUT}
title: "{method}"
parent: "{PARENT}"
date: 2025-07-17
author: Mrs. Young
---
<!-- This file was auto-generated from {INPUT_FILE} -->
"""
    
    # Building category note when there are multiple categories
    categories_raw = [cat.strip() for cat in category_raw.split(",")]
    other_categories = categories_raw[1:]

    # Build hyperlinked list of other categories
    other_links = []
    for oc in other_categories:
        label = oc
        slug = CATEGORY_FOLDER_MAP.get(oc, slugify(oc))
        url = f"{{ site.url }}/{slug}/"
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

    if method == SUBCAT:
        body = textwrap.dedent(f"""\
        {{% if page.category_note != '' %}}
        {{: .note }}
        {category_note}
        {{% endif %}}

        ## Assessment table
    """)
    

    with open(filepath, "w", encoding="utf-8") as out:
        # out.write(front_matter)
        out.write(front_matter.strip() + "\n\n" + body.strip() + "\n")

    print(f"Created: {filepath}")


    # Check if index.md does not already exists
    index_path = os.path.join(SUBCAT_folder, "index.md")
    if not os.path.exists(index_path):
        # Create index.md for sub-category

        body = textwrap.dedent(f"""
# {SUBCAT}
""")
        
        with open(index_path, "w", encoding="utf-8") as index_file:
            index_file.write(f"""---
title: "{SUBCAT}"
parent: "{CAT}"
---
""" + "\n\n" + body.strip() + "\n")