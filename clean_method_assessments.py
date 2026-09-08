from tsv_clean import clean_tsv

# === CONFIGURATION ===
INPUT_FILE  = "_data/DetectionAttribution methods - Method Assessment.tsv"
OUTPUT_FILE = "_data/method_assessments_clean.tsv"

clean_tsv(INPUT_FILE, OUTPUT_FILE)

print(f"Cleaned data written to {OUTPUT_FILE}")