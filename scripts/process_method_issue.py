"""Create or update a method documentation page from a 'Method documentation'
GitHub issue (.github/ISSUE_TEMPLATE/new-method-documentation.yml).

Input: the parsed issue form answers as JSON (field id -> string, or list of
strings for checkboxes/multi-selects), provided via the ISSUE_JSON env var.
This JSON is normally produced by the stefanbuck/github-issue-parser action
in the accompanying GitHub Actions workflow, but can also be supplied by
hand for local testing:

    ISSUE_JSON="$(cat issue.json)" ISSUE_NUMBER=123 ISSUE_AUTHOR=octocat \
        python3 scripts/process_method_issue.py

Behavior:
- If no existing method page matches the submitted method name, a new page is
  created. If the issue's Category (and optionally Sub-category) fields are
  filled in, it's placed in the matching contents/methods/<category>[/<sub>]/
  folder, using the same mapping as scripts/generate_method_pages.py. Otherwise
  it falls back to contents/methods/_pending/<slug>.md for manual sorting.
- If a matching page already exists (matched by front matter title), each
  submitted field is merged into its corresponding section: it replaces the
  section's default placeholder text on first contribution, or is appended
  after any existing content on subsequent contributions.
"""
import json
import os
import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
METHODS_ROOT = PROJECT_ROOT / "contents/methods"
PENDING_DIR = METHODS_ROOT / "_pending"
CAT_DICTS_FILE = PROJECT_ROOT / "_data/cat_dicts.json"
LAYOUT = "method"

with open(CAT_DICTS_FILE, encoding="utf-8") as f:
    _cat_dicts = json.load(f)
CATEGORY_FOLDER_MAP = _cat_dicts["CATEGORY_FOLDER_MAP"]
SUBCAT_FOLDER_MAP = _cat_dicts["SUBCAT_FOLDER_MAP"]

# Maps issue field id -> (section heading text, default placeholder text)
# Headings/placeholders mirror _layouts/method_template.md.
SECTIONS = [
    ("description", "## Description & principle",
     "A clear, technical yet accessible explanation of the method, its core principle(s)."),
    ("variant", "### Major variants",
     "If the method has variants that seem important, either already widespread or promising and well documented."),
    ("online_resources", "### Further online resources",
     'References to useful online resources to get started, e.g. [explanation blogs](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html){:target="_blank"}'),
    ("method_references", "### Method",
     "- One or a few key academic references that introduce or formalize the method."),
    ("rs_data", "#### With RS data in Ecology / Biodiversity", "- A"),
    ("rs_data_field", "#### Without RS data (Ecology domain)", "- B"),
    ("python_pkg", "#### Python", ""),
    ("r_pkg", "#### R", ""),
    ("code_list", "### Code Cells", "Template code cells or GitHub Gist links."),
]

FRONT_MATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+\S")


def slugify(text):
    text = text.strip().lower()
    text = text.replace("/", "-").replace("&", "and")
    text = re.sub(r"[^\w\- ]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def load_issue_fields():
    raw = os.environ.get("ISSUE_JSON")
    if not raw:
        print("ISSUE_JSON env var is empty or missing", file=sys.stderr)
        sys.exit(1)
    data = json.loads(raw)
    fields = {}
    for key, value in data.items():
        if key in ("category", "sub_category"):
            # Keep as a list: values are used to pick a folder, not inserted as text.
            if isinstance(value, str):
                value = [v.strip() for v in value.split("\n") if v.strip()]
            fields[key] = [str(v).strip() for v in value or []]
            continue
        if isinstance(value, list):
            value = "\n".join(str(v) for v in value)
        fields[key] = (value or "").strip()
    return fields


def determine_destination(fields):
    """Return (destination_dir, parent_name) for a new method page, based on
    the issue's Category/Sub-category fields, mirroring generate_method_pages.py."""
    categories = fields.get("category") or []
    if not categories:
        return PENDING_DIR, "Uncategorized"

    category = categories[0]
    category_dir = METHODS_ROOT / CATEGORY_FOLDER_MAP.get(category, "uncategorized")

    sub_categories = fields.get("sub_category") or []
    if not sub_categories:
        return category_dir, category

    sub_category = sub_categories[0]
    sub_dir = category_dir / SUBCAT_FOLDER_MAP.get(sub_category, slugify(sub_category))
    return sub_dir, sub_category


def iter_method_files():
    if not METHODS_ROOT.exists():
        return
    for path in METHODS_ROOT.rglob("*.md"):
        yield path


def find_existing_file(method_name):
    target = method_name.strip().strip('"').casefold()
    for path in iter_method_files():
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            continue
        try:
            front_matter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            continue
        title = str(front_matter.get("title", "")).strip().strip('"')
        if title.casefold() == target:
            return path
    return None


def find_section_bounds(lines, heading_text):
    """Return (heading_idx, end_idx) for the first line matching heading_text,
    where end_idx is the index of the next heading line (or len(lines))."""
    heading_idx = None
    for i, line in enumerate(lines):
        if HEADING_RE.match(line) and line.lstrip("#").strip() == heading_text.lstrip("#").strip():
            heading_idx = i
            break
    if heading_idx is None:
        return None, None
    end_idx = len(lines)
    for i in range(heading_idx + 1, len(lines)):
        if HEADING_RE.match(lines[i]):
            end_idx = i
            break
    return heading_idx, end_idx


def merge_section(text, heading, placeholder, new_value):
    if not new_value:
        return text
    lines = text.split("\n")
    heading_idx, end_idx = find_section_bounds(lines, heading)
    if heading_idx is None:
        print(f"Warning: heading '{heading}' not found, skipping field", file=sys.stderr)
        return text

    section_lines = lines[heading_idx + 1:end_idx]
    section_text = "\n".join(section_lines)

    if placeholder and placeholder in section_text:
        section_text = section_text.replace(placeholder, new_value, 1)
    elif not placeholder and section_text.strip() == "":
        section_text = "\n" + new_value + "\n"
    else:
        section_text = section_text.rstrip("\n") + "\n\n" + new_value + "\n"

    new_lines = lines[:heading_idx + 1] + section_text.split("\n") + lines[end_idx:]
    return "\n".join(new_lines)


def warn_if_category_mismatch(path, fields):
    """The existing file's category/sub-category always takes precedence: this
    only logs a warning when the issue's submitted category diverges from it."""
    categories = fields.get("category") or []
    if not categories:
        return
    expected_dir, _ = determine_destination(fields)
    if path.parent != expected_dir:
        print(
            f"Warning: issue category suggests '{expected_dir.relative_to(METHODS_ROOT)}' "
            f"but existing page lives in '{path.parent.relative_to(METHODS_ROOT)}'. "
            "Keeping the existing classification.",
            file=sys.stderr,
        )


def update_existing_file(path, fields):
    warn_if_category_mismatch(path, fields)
    text = path.read_text(encoding="utf-8")
    for field_id, heading, placeholder in SECTIONS:
        text = merge_section(text, heading, placeholder, fields.get(field_id, ""))
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.relative_to(PROJECT_ROOT)}")


def render_new_file(method_name, fields, parent):
    author = fields.get("author") or "Unknown"
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    issue_url = os.environ.get("ISSUE_URL", "")
    date = (os.environ.get("ISSUE_DATE") or "")[:10]

    def value_or_placeholder(field_id, heading, placeholder):
        return fields.get(field_id) or placeholder

    pending_note = (
        "<!-- This method is pending categorization: move it to the right\n"
        "     contents/methods/<category>/ folder and set `parent` accordingly. -->\n"
        if parent == "Uncategorized" else ""
    )
    front_matter = (
        "---\n"
        f"layout: {LAYOUT}\n"
        f'title: "{method_name}"\n'
        f'parent: "{parent}"\n'
        f"date: {date}\n"
        f"author: {author}\n"
        "---\n"
        "<!-- Auto-generated from a Method documentation issue"
        + (f" (#{issue_number}: {issue_url})" if issue_number else "")
        + " -->\n"
        + pending_note
    )

    body = f"""
## Table of Contents
{{: .no_toc .text-delta }}

1. TOC
{{:toc}}


## Description & principle
{value_or_placeholder(*SECTIONS[0])}


### Major variants
{{: .no_toc }}
{{: .d-inline-block }}
optional
{{: .label}}

{value_or_placeholder(*SECTIONS[1])}

### Further online resources
{{: .no_toc }}

{value_or_placeholder(*SECTIONS[2])}


## Reference articles
### Method
{{: .no_toc }}
{value_or_placeholder(*SECTIONS[3])}

### Research applications
{{: .no_toc }}
#### With RS data in Ecology / Biodiversity
{{: .no_toc }}
{value_or_placeholder(*SECTIONS[4])}

#### Without RS data (Ecology domain)
{{: .no_toc }}
{{: .d-inline-block }}
optional
{{: .label}}

{value_or_placeholder(*SECTIONS[5])}

## Implementation

#### Python
{{: .no_toc }}

{fields.get("python_pkg", "")}

#### R
{{: .no_toc }}

{fields.get("r_pkg", "")}

### Code Cells
{{: .no_toc }}
{{: .d-inline-block }}
optional
{{: .label}}

{value_or_placeholder(*SECTIONS[8])}


<!-- For referencement in toc before automatic table -->
## Assessment table
"""
    return front_matter + body


def create_new_file(method_name, fields):
    dest_dir, parent = determine_destination(fields)
    dest_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(method_name)
    filepath = dest_dir / f"{slug}.md"
    if filepath.exists():
        print(f"{filepath} already exists, updating it instead of creating", file=sys.stderr)
        update_existing_file(filepath, fields)
        return "updated", filepath
    filepath.write_text(render_new_file(method_name, fields, parent), encoding="utf-8")
    print(f"Created {filepath.relative_to(PROJECT_ROOT)}")
    return ("created-pending" if parent == "Uncategorized" else "created"), filepath


def write_github_output(status, filepath):
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"status={status}\n")
        f.write(f"filepath={filepath.relative_to(PROJECT_ROOT)}\n")


def main():
    fields = load_issue_fields()
    method_name = fields.get("method_name", "").strip()
    if not method_name:
        print("No method_name field found in issue, aborting", file=sys.stderr)
        sys.exit(1)

    existing = find_existing_file(method_name)
    if existing:
        update_existing_file(existing, fields)
        status, filepath = "updated", existing
    else:
        status, filepath = create_new_file(method_name, fields)

    write_github_output(status, filepath)


if __name__ == "__main__":
    main()
