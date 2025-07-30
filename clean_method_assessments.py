import os
import csv
import re
import textwrap
import json

# === CONFIGURATION ===
INPUT_FILE  = "_data/Attribution methods - Method Assessment.tsv"
OUTPUT_FILE = "_data/method_assessments_clean.tsv"


with open(INPUT_FILE, newline='', encoding='utf-8') as infile, \
     open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as outfile:
    
    lines = infile.readlines()[3:]  # skip metadata
    writer = outfile.writelines(lines)

print(f"Cleaned data written to {OUTPUT_FILE}")