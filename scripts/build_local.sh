#!/usr/bin/env bash
# Local build mirroring .github/workflows/pages.yml.
# Usage: scripts/build_local.sh [serve] [--baseurl /dam]
set -euo pipefail

cd "$(dirname "$0")/.."

MODE="build"
BASEURL=""
while [ $# -gt 0 ]; do
  case "$1" in
    serve) MODE="serve" ;;
    --baseurl) BASEURL="$2"; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
  shift
done

python3 scripts/generate_method_pages.py

rm -rf _site .jekyll-cache
export JEKYLL_ENV=production
bundle exec jekyll "$MODE" --baseurl "$BASEURL"
