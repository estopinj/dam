import pandas as pd
import requests
import json
import os
import argparse
import csv
import re
import tempfile
from pathlib import Path
from pypdf import PdfReader
from openai import OpenAI

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
CSV_DIR = SCRIPT_DIR / "csvs"
DEFAULT_RESULTS_CSV = SCRIPT_DIR / "NaviDAM_Triage_Results.csv"
DEFAULT_PDF_DIR = SCRIPT_DIR / "downloaded_pdfs"
METHOD_ASSESSMENTS_PATH = ROOT_DIR / "_data" / "method_assessments_clean.tsv"

FILTER_CRITERIA = [
    "Objective",
    "Estimand",
    "Type",
    "Minimal TS length",
    "Handles few samples",
    "Handles huge datasets (n)",
    "Handles missing data",
    "RS-data proven",
    "Fonctional form",
    "No unobserved confounders",
    "No interference",
    "Well-defined treatments",
    "Common support (positivity)",
    "Causal Markov Condition",
    "Faithfulness",
    "IID",
    "Model specific",
    "Requires explicit processes",
    "Exposure type",
    "Number of variables",
    "Propaguates uncertainty",
    "Handles lag effects",
    "Parametric nature",
    "Language",
    "Usage",
]

MULTI_VALUE_CRITERIA = {
    "Estimand",
    "Type",
    "Fonctional form",
    "Model specific",
    "Requires explicit processes",
    "Exposure type",
    "Number of variables",
    "Parametric nature",
    "Language",
    "Usage",
}

LEGACY_FIELD_MAP = {
    "Observed_Method_Name": "Method",
    "Outcome_Objective": "Objective",
    "Outcome_Estimand": "Estimand",
    "Data_Compatibility_Type": "Type",
    "Data_Compatibility_Required_TS_length": "Minimal TS length",
    "Data_Compatibility_Handles_few_samples": "Handles few samples",
    "Data_Compatibility_Handles_huge_datasets": "Handles huge datasets (n)",
    "Data_Compatibility_Handles_missing_data": "Handles missing data",
    "Data_Compatibility_RS_data_proven": "RS-data proven",
    "Assumptions_Functional_form": "Fonctional form",
    "Assumptions_No_unobserved_confounders": "No unobserved confounders",
    "Assumptions_No_interference": "No interference",
    "Assumptions_Well_defined_treatments": "Well-defined treatments",
    "Assumptions_Common_support_positivity": "Common support (positivity)",
    "Assumptions_Causal_Markov_Condition": "Causal Markov Condition",
    "Assumptions_Faithfulness": "Faithfulness",
    "Assumptions_IID": "IID",
    "Assumptions_Model_specific_assumption": "Model specific",
    "Assumptions_Requires_explicit_processes": "Requires explicit processes",
    "Model_Properties_Exposure_type": "Exposure type",
    "Model_Properties_Number_of_variables": "Number of variables",
    "Model_Properties_Propagates_uncertainty": "Propaguates uncertainty",
    "Model_Properties_Handles_lag_effects": "Handles lag effects",
    "Model_Properties_Parametric_nature": "Parametric nature",
    "Implementation_Language": "Language",
    "Implementation_Usage": "Usage",
}

OPTION_ALIASES = {
    "Minimal TS length": {
        "Handles <= 10": "Handles ≤ 10",
        "<= 10": "Handles ≤ 10",
        ">= 10": "≥ 10",
        ">= 100": "≥ 100",
    },
    "Exposure type": {
        "Continuous or Time-varying": "Continuous / Time-varying",
        "Continuous or Time varying": "Continuous / Time-varying",
        "Time-varying": "Continuous / Time-varying",
    },
    "No unobserved confounders": {
        "Assumption-free": "Relaxes assumption",
    },
    "No interference": {
        "Assumption-free": "Relaxes assumption",
    },
    "Well-defined treatments": {
        "Assumption-free": "Relaxes assumption",
    },
    "Common support (positivity)": {
        "Assumption-free": "Relaxes assumption",
    },
    "Causal Markov Condition": {
        "Assumption-free": "Relaxes assumption",
    },
    "Faithfulness": {
        "Assumption-free": "Relaxes assumption",
    },
    "IID": {
        "Assumption-free": "Relaxes assumption",
    },
}

RESULT_COLUMNS = [
    "Publication ID",
    "Original_Title",
    "DOI",
    "Source Linkout",
    "NaviDAM_Status",
    "Assessment_Validation_Issues",
    "Method",
    *FILTER_CRITERIA,
]


def get_openai_client():
    """Build the API client only when needed so local test runs can start cleanly."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def split_criterion_values(raw_value):
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        parts = raw_value
    else:
        parts = [raw_value]

    values = []
    for part in parts:
        if part is None:
            continue
        text = str(part).strip()
        if not text:
            continue
        values.extend(piece.strip() for piece in re.split(r"\s*[;,]\s*", text) if piece.strip())
    return values


def load_filter_vocabulary():
    if not METHOD_ASSESSMENTS_PATH.exists():
        raise FileNotFoundError(f"Missing NaviDAM method assessment file: {METHOD_ASSESSMENTS_PATH}")

    vocabulary = {criterion: [] for criterion in FILTER_CRITERIA}
    seen = {criterion: set() for criterion in FILTER_CRITERIA}

    with METHOD_ASSESSMENTS_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing_columns = [criterion for criterion in FILTER_CRITERIA if criterion not in reader.fieldnames]
        if missing_columns:
            raise ValueError(f"Missing expected NaviDAM criteria columns: {missing_columns}")

        for row in reader:
            for criterion in FILTER_CRITERIA:
                for option in split_criterion_values(row.get(criterion, "")):
                    if option not in seen[criterion]:
                        seen[criterion].add(option)
                        vocabulary[criterion].append(option)

    for criterion in FILTER_CRITERIA:
        for fallback in ("Don't know", "Inapplicable"):
            if fallback not in seen[criterion]:
                vocabulary[criterion].append(fallback)

    return vocabulary


FILTER_VOCABULARY = load_filter_vocabulary()


def build_assessment_schema():
    schema = {
        "Method": (
            "The exact method name used by the study, matching the paper wording as closely as possible. "
            "Return a single string, not a list."
        )
    }
    for criterion in FILTER_CRITERIA:
        selection_rule = "Select one or more exact options" if criterion in MULTI_VALUE_CRITERIA else "Select exactly one exact option"
        allowed_options = " / ".join(FILTER_VOCABULARY[criterion])
        schema[criterion] = f"{selection_rule} from the NaviDAM vocabulary: {allowed_options}"
    return schema


NAVIDAM_ASSESSMENT_SCHEMA = build_assessment_schema()


def normalize_option_value(criterion, option):
    normalized = str(option).strip()
    normalized = normalized.replace(">=", "≥").replace("<=", "≤")
    normalized = OPTION_ALIASES.get(criterion, {}).get(normalized, normalized)
    return normalized


def normalize_assessment_results(raw_results):
    normalized = {column: "" for column in ["Method", *FILTER_CRITERIA]}
    issues = []

    if not isinstance(raw_results, dict):
        issues.append("Model output was not a JSON object.")
        return normalized, issues

    for raw_key, raw_value in raw_results.items():
        normalized_key = LEGACY_FIELD_MAP.get(raw_key, raw_key)
        if normalized_key not in normalized:
            issues.append(f"Unexpected field '{raw_key}' ignored.")
            continue

        if normalized_key == "Method":
            normalized[normalized_key] = str(raw_value).strip() if raw_value is not None else ""
            continue

        allowed_values = set(FILTER_VOCABULARY[normalized_key])
        parsed_values = []
        for option in split_criterion_values(raw_value):
            value = normalize_option_value(normalized_key, option)
            if value in allowed_values:
                if value not in parsed_values:
                    parsed_values.append(value)
            else:
                issues.append(f"{normalized_key}: unsupported option '{option}' dropped.")

        if not parsed_values:
            normalized[normalized_key] = "Don't know"
            continue

        if normalized_key in MULTI_VALUE_CRITERIA:
            normalized[normalized_key] = ", ".join(parsed_values)
        else:
            normalized[normalized_key] = parsed_values[0]
            if len(parsed_values) > 1:
                issues.append(f"{normalized_key}: multiple values returned; kept '{parsed_values[0]}'.")

    if not normalized["Method"]:
        issues.append("Method: missing extracted method name.")

    for criterion in FILTER_CRITERIA:
        if not normalized[criterion]:
            normalized[criterion] = "Don't know"

    return normalized, issues


def blank_result_record(row):
    record = {column: "" for column in RESULT_COLUMNS}
    record.update(
        {
            "Publication ID": str(row.get("Publication ID", "")).strip(),
            "Original_Title": row.get("Title", ""),
            "DOI": row.get("DOI", ""),
            "Source Linkout": row.get("Source Linkout", ""),
            "NaviDAM_Status": "ONLINE_PDF_FAILED",
            "Assessment_Validation_Issues": "",
        }
    )
    return record


def parse_chat_completion_json(response):
    content = response.choices[0].message.content
    if isinstance(content, list):
        content = "".join(part.text for part in content if hasattr(part, "text"))
    return json.loads(content)

def extract_text_from_pdf_file(filepath):
    """Helper to extract text from a physical file path safely."""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages[:15]: 
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text if text.strip() else None
    except Exception:
        return None


def response_looks_like_pdf(response):
    content_type = response.headers.get("Content-Type", "").lower()
    if "pdf" in content_type:
        return True
    return response.content.lstrip().startswith(b"%PDF")

def download_and_extract_pdf_url(pdf_url, pub_id):
    """Downloads web open-access links."""
    temp_path = None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(pdf_url, headers=headers, timeout=20)
        if response.status_code != 200:
            return None
        if not response_looks_like_pdf(response):
            return None
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{pub_id}.pdf") as handle:
            handle.write(response.content)
            temp_path = Path(handle.name)
            
        text = extract_text_from_pdf_file(temp_path)
        temp_path.unlink(missing_ok=True)
        return text
    except Exception:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        return None

def analyze_paper_with_navidam(full_text, is_full_text=True):
    """Submits full extracted text to the JSON structural LLM engine."""
    client = get_openai_client()
    if client is None:
        return None

    context_status = "FULL-TEXT RESEARCH PAPER PDF" if is_full_text else "METADATA RECOVERY RECORD"
    
    prompt = f"""
    You are an expert methodology validator system checking empirical research articles for the NaviDAM Suggestion framework.
    You are parsing a {context_status}.
    
    Analyze this extracted text layer:
    ---
    {full_text[:45000]}
    ---
    
    Task: Identify the exact 'Method' used by the researchers and populate the NaviDAM criteria fields.
    Return only fields from the required schema, using the exact field names and exact option spellings provided there.
    If the paper is ambiguous for a criterion, return "Don't know".
    
    Required Schema Configuration:
    {json.dumps(NAVIDAM_ASSESSMENT_SCHEMA, indent=2)}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a specialized academic meta-parser. Output strictly in deterministic valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        return parse_chat_completion_json(response)
    except Exception:
        return None


def resolve_input_csv(csv_name=None):
    """Resolve a CSV from an explicit path or from the local csvs directory."""
    if csv_name:
        explicit_path = Path(csv_name)
        if explicit_path.exists():
            return explicit_path.resolve()

        bundled_path = CSV_DIR / csv_name
        if bundled_path.exists():
            return bundled_path.resolve()

    available_csvs = sorted(CSV_DIR.glob("*.csv"))
    if available_csvs:
        return available_csvs[0].resolve()

    return None


def print_failed_pdf_manifest(results_df, pdf_dir):
    """Print a download checklist for rows still blocked on local PDFs."""
    failed_rows = results_df[results_df["NaviDAM_Status"] == "ONLINE_PDF_FAILED"]
    if failed_rows.empty:
        print("\n[Download List] No PDFs remain in ONLINE_PDF_FAILED status.")
        return

    print(f"\n[Download List] {len(failed_rows)} PDF(s) still need manual download into '{pdf_dir}':")
    for _, row in failed_rows.iterrows():
        pub_id = str(row.get("Publication ID", "")).strip()
        doi = row.get("DOI", "")
        title = row.get("Original_Title", "")
        link = row.get("Source Linkout", "")
        print(f" - {pub_id}.pdf | DOI: {doi} | Title: {title} | Link: {link}")

# Mode 1: Initial Online Web Assessment Check
def run_online_triage_pass(csv_path, max_rows=3, output_csv_path=DEFAULT_RESULTS_CSV, pdf_dir=DEFAULT_PDF_DIR):
    df = pd.read_csv(csv_path, skiprows=1)
    df = df.head(max_rows) # Dev bounded parameters
    
    evaluated_records = []
    print(f"Starting Triage: Running online assessment checks for top {len(df)} entries...")
    
    for idx, row in df.iterrows():
        pub_id = str(row.get('Publication ID')).strip()
        pdf_url = row.get('Source Linkout', None)
        record = blank_result_record(row)
            
        full_text = None
        if pd.notna(pdf_url):
            full_text = download_and_extract_pdf_url(pdf_url, pub_id)
            
        if full_text:
            print(f" -> Paper {pub_id}: Link active. Running complete AI matrix evaluation.")
            assessment_results = analyze_paper_with_navidam(full_text, is_full_text=True)
            if assessment_results is None:
                if get_openai_client() is None:
                    print(f" -> Warning for {pub_id}: OPENAI_API_KEY is not configured. PDF extracted but analysis was skipped.")
                    record["NaviDAM_Status"] = "OPENAI_API_KEY_MISSING"
                else:
                    print(f" -> Warning for {pub_id}: extraction call failed or returned invalid JSON.")
                    record["NaviDAM_Status"] = "ASSESSMENT_SYSTEM_ERROR"
            else:
                normalized_results, issues = normalize_assessment_results(assessment_results)
                record.update(normalized_results)
                record["Assessment_Validation_Issues"] = " | ".join(issues)
                record["NaviDAM_Status"] = "ASSESSMENT_COMPLETED_WITH_WARNINGS" if issues else "ASSESSMENT_COMPLETED"
        else:
            print(f" -> Warning for {pub_id}: PDF URL broken or unreachable. Tagged and skipped.")
            
        evaluated_records.append(record)
        
    results_df = pd.DataFrame(evaluated_records, columns=RESULT_COLUMNS)
    results_df.to_csv(output_csv_path, index=False)
    print(f"\n Triage execution complete. Records cataloged in '{output_csv_path}'")
    print_failed_pdf_manifest(results_df, pdf_dir)
    return results_df

# Mode 2: Offline Local Catch-Up Sweep Processing
def run_local_folder_catchup(triage_csv_path, input_folder_path=DEFAULT_PDF_DIR):
    """Sifts out rows with the failure flag and scans your local storage folder for an offline catch-up run."""
    if not os.path.exists(triage_csv_path):
        print(f"Error: Target tracking file '{triage_csv_path}' missing.")
        return
        
    df = pd.read_csv(triage_csv_path)
    failed_rows = df[df['NaviDAM_Status'] == "ONLINE_PDF_FAILED"]
    
    if failed_rows.empty:
        print("Success: Zero rows found with an active 'ONLINE_PDF_FAILED' flag. Data is clean.")
        return
        
    print(f"Found {len(failed_rows)} flagged rows. Scanning folder: '{input_folder_path}' for manual uploads...")
    
    for idx, row in df.iterrows():
        if row['NaviDAM_Status'] != "ONLINE_PDF_FAILED":
            continue
            
        pub_id = row['Publication ID']
        local_pdf_path = os.path.join(input_folder_path, f"{pub_id}.pdf")
        
        if os.path.exists(local_pdf_path):
            print(f" -> Found matching offline resource file for row: {pub_id}. Extracting local text layer...")
            local_text = extract_text_from_pdf_file(local_pdf_path)
            
            if local_text:
                assessment_results = analyze_paper_with_navidam(local_text, is_full_text=True)
                if assessment_results is None:
                    if get_openai_client() is None:
                        df.at[idx, 'NaviDAM_Status'] = "OPENAI_API_KEY_MISSING"
                        print(f"    -> Warning: OPENAI_API_KEY is not configured. Local PDF was read but analysis was skipped.")
                    else:
                        df.at[idx, 'NaviDAM_Status'] = "ASSESSMENT_SYSTEM_ERROR"
                        print(f"    -> Warning: extraction call failed or returned invalid JSON.")
                else:
                    normalized_results, issues = normalize_assessment_results(assessment_results)
                    for field, value in normalized_results.items():
                        df.at[idx, field] = value
                    df.at[idx, 'Assessment_Validation_Issues'] = " | ".join(issues)
                    df.at[idx, 'NaviDAM_Status'] = "ASSESSMENT_COMPLETED_WITH_WARNINGS" if issues else "ASSESSMENT_COMPLETED"
                    print(f"    -> Success: Local fallback criteria mapped for {pub_id}.")
            else:
                print(f"    -> Warning: Local file '{local_pdf_path}' exists but contains no extractable text strings.")
        else:
            print(f" -> Notice: Local file '{pub_id}.pdf' not found in folder yet. Keeping error flag.")
    df.to_csv(triage_csv_path, index=False)
    print(f"\n Master log metrics updated and overwritten back to '{triage_csv_path}'.")
    print_failed_pdf_manifest(df, input_folder_path)


def main():
    parser = argparse.ArgumentParser(description="Run NaviDAM validation triage on a CSV export.")
    parser.add_argument(
        "csv_filename",
        nargs="?",
        default="Joint.csv",
        help="CSV filename or path. Falls back to the first CSV in scripts/validation/csvs.",
    )
    parser.add_argument(
        "--input-csv",
        dest="input_csv",
        help="Explicit input CSV filename or path. Overrides the positional csv_filename when provided.",
    )
    parser.add_argument(
        "--output-csv",
        default=str(DEFAULT_RESULTS_CSV),
        help="Path for the triage results CSV.",
    )
    parser.add_argument(
        "--pdf-dir",
        default=str(DEFAULT_PDF_DIR),
        help="Folder used for manual PDF downloads and offline catch-up files.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=3,
        help="Limit the online triage pass to the first N rows.",
    )
    parser.add_argument(
        "--catchup",
        action="store_true",
        help="Run the offline local-folder catch-up pass instead of the online pass.",
    )
    parser.add_argument(
        "--triage-csv",
        default=None,
        help="Tracking CSV for the catch-up pass. Defaults to --output-csv.",
    )
    args = parser.parse_args()

    output_csv_path = Path(args.output_csv).expanduser().resolve()
    pdf_dir = Path(args.pdf_dir).expanduser().resolve()
    pdf_dir.mkdir(parents=True, exist_ok=True)

    if args.catchup:
        triage_csv_path = Path(args.triage_csv).expanduser().resolve() if args.triage_csv else output_csv_path
        run_local_folder_catchup(triage_csv_path, pdf_dir)
        return

    requested_csv = args.input_csv or args.csv_filename
    csv_path = resolve_input_csv(requested_csv)
    if csv_path is None:
        print(
            f"Initialization Error: Could not find '{requested_csv}' and no CSV files were found in '{CSV_DIR}'."
        )
        return

    print(f"Using input CSV: {csv_path}")
    run_online_triage_pass(
        csv_path,
        max_rows=args.max_rows,
        output_csv_path=output_csv_path,
        pdf_dir=pdf_dir,
    )

    print(f"\n[Workspace Setup] Created folder: '{pdf_dir}'")
    print("If any row logged a failure flag, download its full PDF, name it as 'pub.ID.pdf' and place it there.")
    print(f"Then run the local catch-up pass with: python {Path(__file__).name} --catchup --triage-csv {output_csv_path} --pdf-dir {pdf_dir}")


if __name__ == "__main__":
    main()