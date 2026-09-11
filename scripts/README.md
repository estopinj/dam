# Maintenance scripts

These scripts support local maintenance of the Jekyll site and its assessment data.
Run them from the repository root with Python 3:

```bash
python3 scripts/add_categories.py
python3 scripts/clean_method_assessments.py
python3 scripts/generate_method_pages.py
```

`generate_method_pages.py` creates missing method pages from the TSV assessment data. Review its output before committing generated pages.

## Assessment TSV updates are automatic

Replacing `_data/DetectionAttribution methods - Method Assessment.tsv` (e.g. with a
fresh export) needs no manual step:

- **Local (`jekyll serve` / `jekyll build`):** the `_plugins/clean_method_assessments.rb`
  hook regenerates the gitignored `_data/method_assessments_clean.tsv` (skipping the
  3 metadata rows) on every build, including `--watch` rebuilds. Just rebuild/refresh.
- **Remote (PR or push to `main`):** `ci.yml` and `pages.yml` both run
  `scripts/clean_method_assessments.py` before `jekyll build`, so the deployed site
  always renders the committed TSV. A malformed upload (wrong header, missing
  `Method` column) fails the build instead of silently rendering empty tables.

`python3 scripts/clean_method_assessments.py` remains available for manual use
(e.g. to inspect the cleaned file), but it is no longer required before building.
