# Maintenance scripts

These scripts support local maintenance of the Jekyll site and its assessment data.
Run them from the repository root with Python 3:

```bash
python3 scripts/add_categories.py
python3 scripts/clean_method_assessments.py
python3 scripts/generate_method_pages.py
```

`generate_method_pages.py` creates missing method pages from the TSV assessment data. Review its output before committing generated pages.
