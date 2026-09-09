from pathlib import Path

from tsv_clean import clean_tsv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# === CONFIGURATION ===
INPUT_FILE  = PROJECT_ROOT / "_data/DetectionAttribution methods - Method Assessment.tsv"
OUTPUT_FILE = PROJECT_ROOT / "_data/method_assessments_clean.tsv"

clean_tsv(INPUT_FILE, OUTPUT_FILE)

print(f"Cleaned data written to {OUTPUT_FILE}")