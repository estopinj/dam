import pandas as pd
import requests
import json
import os
import argparse
import csv
import re
import tempfile
import sys
import shlex
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader
from openai import OpenAI, APIConnectionError, APIStatusError, APITimeoutError

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
CSV_DIR = SCRIPT_DIR / "csvs"
DEFAULT_RESULTS_CSV = SCRIPT_DIR / "NaviDAM_Triage_Results.csv"
DEFAULT_PDF_DIR = SCRIPT_DIR / "downloaded_pdfs"
LOGS_DIR = SCRIPT_DIR / "logs"
METHOD_ASSESSMENTS_PATH = ROOT_DIR / "_data" / "method_assessments_clean.tsv"
NON_EMPIRICAL_TITLE_PATTERNS = [
    r"\breview\b",
    r"\bperspective\b",
    r"\bintroduction\b",
    r"\bcommentary\b",
    r"\beditorial\b",
    r"\bopinion\b",
    r"\bprimer\b",
    r"\bframework\b",
]
NON_EMPIRICAL_ABSTRACT_PATTERNS = [
    r"\bwe review\b",
    r"\bthis review\b",
    r"\bwe propose\b",
    r"\bwe argue\b",
    r"\bwe discuss\b",
    r"\bwe outline\b",
    r"\bwe describe advances\b",
    r"\bwill require\b",
    r"\bcould help\b",
    r"\bour aim is to provide\b",
    r"\bdiscussion of frontiers\b",
]
EMPIRICAL_ABSTRACT_PATTERNS = [
    r"\bwe analy[sz]e\b",
    r"\bwe applied\b",
    r"\bapplying\b",
    r"\bwe estimate\b",
    r"\bwe quantified?\b",
    r"\bwe found\b",
    r"\busing [^.\n]{0,120}\bdata\b",
    r"\btime series\b",
    r"\bdataset\b",
    r"\bobservational data\b",
    r"\bacross \d+\b",
    r"\b\d+-year\b",
    r"\bwe combine [^.\n]{0,120}\bdata\b",
    r"\bwe fit\b",
    r"\bwe simulate\b",
]
STRONG_EMPIRICAL_ABSTRACT_PATTERNS = [
    r"\bwe analy[sz]e\b",
    r"\bwe applied\b",
    r"\bapplying [^.\n]{0,120}\btime series\b",
    r"\bwe estimate\b",
    r"\bwe quantified?\b",
    r"\bwe found\b",
    r"\bwe fit\b",
    r"\bwe simulate\b",
    r"\busing a \d+-year time series\b",
    r"\bacross \d+ (locations|sites|countries|plots|rivers)\b",
    r"\b95% ci\b",
]

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
    "Observed_Method_Name": "Method_Reported_By_Authors",
    "Method": "Method_Reported_By_Authors",
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
    "Assessment_Model",
    "Original_Title",
    "DOI",
    "Source Linkout",
    "Screening_Decision",
    "Screening_Reason",
    "NaviDAM_Status",
    "Assessment_Error",
    "Assessment_Validation_Issues",
    "Method_Reported_By_Authors",
    "Method_Evidence",
    *FILTER_CRITERIA,
]


class LLMConfigurationError(Exception):
    pass


class LLMInferenceError(Exception):
    pass


class TeeStream:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
        return len(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def sanitize_filename_part(value, fallback="value"):
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "").strip())
    cleaned = cleaned.strip("-._")
    return cleaned or fallback


def build_run_log_path(argv, assessment_model_label):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_part = sanitize_filename_part(assessment_model_label, fallback="model")
    args_part = sanitize_filename_part("__".join(argv) if argv else "default-run", fallback="default-run")
    filename = f"validation_v2__{timestamp}__{model_part}__{args_part}.log"
    return LOGS_DIR / filename


def print_log_block(title, lines):
    print(f"\n[{title}]")
    for line in lines:
        print(line)


def print_run_header(csv_path, output_csv_path, pdf_dir, log_path, argv):
    settings = get_llm_settings()
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 72)
    print("NaviDAM Validation Run")
    print("=" * 72)
    print(f"Using input CSV: {csv_path}")
    print(f"Assessment model: {get_assessment_model_label()}")
    print(f"Date and time: {started_at}")
    print_log_block(
        "Run Configuration",
        [
            f"Provider: {settings['provider']}",
            f"Model: {settings['model']}",
            f"Base URL: {settings['base_url'] or 'default OpenAI endpoint'}",
            f"Output CSV: {output_csv_path}",
            f"PDF directory: {pdf_dir}",
            f"Log file: {log_path}",
            f"Command: python {Path(__file__).name} {shlex.join(argv)}" if argv else f"Command: python {Path(__file__).name}",
        ],
    )


def install_run_logger(argv):
    log_path = build_run_log_path(argv, get_assessment_model_label())
    log_handle = log_path.open("w", encoding="utf-8", buffering=1)
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = TeeStream(original_stdout, log_handle)
    sys.stderr = TeeStream(original_stderr, log_handle)
    return log_path, log_handle, original_stdout, original_stderr


def restore_run_logger(log_handle, original_stdout, original_stderr):
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    log_handle.close()


def get_llm_settings():
    """Read provider settings for any OpenAI-compatible chat completion endpoint."""
    api_key = os.environ.get("NAVIDAM_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("NAVIDAM_LLM_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4o"
    base_url = os.environ.get("NAVIDAM_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    provider = os.environ.get("NAVIDAM_LLM_PROVIDER") or ("openai-compatible" if base_url else "openai")
    return {
        "api_key": api_key,
        "model": model,
        "base_url": base_url,
        "provider": provider,
    }


def get_assessment_model_label():
    settings = get_llm_settings()
    return f"{settings['provider']}::{settings['model']}"


def llm_endpoint_allows_missing_key(base_url):
    if not base_url:
        return False
    normalized = str(base_url).strip().lower()
    return normalized.startswith("http://localhost") or normalized.startswith("http://127.0.0.1")


def llm_endpoint_supports_response_format(base_url):
    if not base_url:
        return True
    normalized = str(base_url).strip().lower()
    if normalized.startswith("http://localhost") or normalized.startswith("http://127.0.0.1"):
        return False
    return True


def get_llm_client():
    """Build the API client only when needed so local test runs can start cleanly."""
    settings = get_llm_settings()
    api_key = settings["api_key"]
    if not api_key:
        if llm_endpoint_allows_missing_key(settings["base_url"]):
            api_key = "ollama"
        else:
            raise LLMConfigurationError(
                "No LLM API key configured. Set NAVIDAM_LLM_API_KEY or OPENAI_API_KEY."
            )

    client_kwargs = {"api_key": api_key}
    if settings["base_url"]:
        client_kwargs["base_url"] = settings["base_url"]
    return OpenAI(**client_kwargs)

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

METHOD_EXTRACTION_SCHEMA = {
    "Method_Reported_By_Authors": (
        "The exact method name used by the authors, matching the paper wording as closely as possible. "
        "Return the most specific named algorithm, estimator, statistical design, or causal model explicitly implemented in the study. "
        "Do not return a broad family such as 'causal discovery approach', 'quasi-experimental design', or 'Bayesian network structure learning' when a more specific named method appears in the paper."
    ),
    "Method_Evidence": (
        "A short quote or very close paraphrase from the paper that directly names the applied method."
    ),
}

METHOD_BROAD_PATTERNS = [
    r"\bcausal discovery approach\b",
    r"\bcausal discovery method\b",
    r"\bconstraint-based causal discovery\b",
    r"\bbayesian network structure learning\b",
    r"\bbayesian network learning\b",
    r"\bquasi-experimental design\b",
    r"\bquasi-experiment\b",
    r"\bmachine learning method\b",
    r"\bregression model\b",
    r"\bstatistical model\b",
    r"\bnonparametric causal discovery\b",
    r"\bobservational design\b",
]


def build_assessment_schema():
    schema = dict(METHOD_EXTRACTION_SCHEMA)
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
    normalized = {column: "" for column in ["Method_Reported_By_Authors", "Method_Evidence", *FILTER_CRITERIA]}
    issues = []

    if not isinstance(raw_results, dict):
        issues.append("Model output was not a JSON object.")
        return normalized, issues

    for raw_key, raw_value in raw_results.items():
        normalized_key = LEGACY_FIELD_MAP.get(raw_key, raw_key)
        if normalized_key not in normalized:
            issues.append(f"Unexpected field '{raw_key}' ignored.")
            continue

        if normalized_key in {"Method_Reported_By_Authors", "Method_Evidence"}:
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

    if not normalized["Method_Reported_By_Authors"]:
        issues.append("Method_Reported_By_Authors: missing extracted method name.")

    for criterion in FILTER_CRITERIA:
        if not normalized[criterion]:
            normalized[criterion] = "Don't know"

    return normalized, issues


def classify_study_screening(row):
    title = str(row.get("Title", "") or "")
    abstract = str(row.get("Abstract", "") or "")
    source_title = str(row.get("Source title", "") or "")
    publication_type = str(row.get("Publication Type", "") or "")

    title_lower = title.casefold()
    abstract_lower = abstract.casefold()
    source_lower = source_title.casefold()
    publication_type_lower = publication_type.casefold()

    if any(re.search(pattern, title_lower) for pattern in NON_EMPIRICAL_TITLE_PATTERNS):
        return "NON_EMPIRICAL_SKIP", "Title suggests a review, perspective, introduction, or conceptual framework paper."

    if any(keyword in publication_type_lower for keyword in ["review", "editorial", "perspective"]):
        return "NON_EMPIRICAL_SKIP", f"Publication Type indicates a non-empirical paper: {publication_type}."

    empirical_hits = [pattern for pattern in EMPIRICAL_ABSTRACT_PATTERNS if re.search(pattern, abstract_lower)]
    strong_empirical_hits = [pattern for pattern in STRONG_EMPIRICAL_ABSTRACT_PATTERNS if re.search(pattern, abstract_lower)]
    conceptual_hits = [pattern for pattern in NON_EMPIRICAL_ABSTRACT_PATTERNS if re.search(pattern, abstract_lower)]

    if conceptual_hits and not strong_empirical_hits:
        return "NON_EMPIRICAL_SKIP", "Abstract describes a conceptual, perspective, or framework contribution without an empirical application."

    if "trends in" in source_lower and conceptual_hits and not strong_empirical_hits:
        return "NON_EMPIRICAL_SKIP", f"Journal and abstract indicate a perspective-style article from {source_title}."

    if strong_empirical_hits:
        return "EMPIRICAL_APPLICATION", "Metadata suggests an applied empirical study with data and reported analyses."

    if empirical_hits and not conceptual_hits:
        return "UNCERTAIN_PROCEED", "Metadata contains some empirical signals, but not enough to confirm an applied study with confidence."

    return "UNCERTAIN_PROCEED", "Metadata does not strongly confirm or exclude an empirical application, so assessment proceeds."


def blank_result_record(row):
    record = {column: "" for column in RESULT_COLUMNS}
    record.update(
        {
            "Publication ID": str(row.get("Publication ID", "")).strip(),
            "Assessment_Model": get_assessment_model_label(),
            "Original_Title": row.get("Title", ""),
            "DOI": row.get("DOI", ""),
            "Source Linkout": row.get("Source Linkout", ""),
            "Screening_Decision": "",
            "Screening_Reason": "",
            "NaviDAM_Status": "ONLINE_PDF_FAILED",
            "Assessment_Error": "",
            "Assessment_Validation_Issues": "",
            "Method_Evidence": "",
        }
    )
    return record


def load_existing_results(output_csv_path):
    if not Path(output_csv_path).exists():
        return pd.DataFrame(columns=RESULT_COLUMNS)

    existing_df = pd.read_csv(output_csv_path)
    for column in RESULT_COLUMNS:
        if column not in existing_df.columns:
            existing_df[column] = ""
    return existing_df[RESULT_COLUMNS]


def result_row_key(publication_id, assessment_model):
    return (str(publication_id).strip(), str(assessment_model).strip())


def existing_result_keys(results_df):
    if results_df.empty:
        return set()
    return {
        result_row_key(row.get("Publication ID", ""), row.get("Assessment_Model", ""))
        for _, row in results_df.iterrows()
    }


def combine_results(existing_df, new_rows):
    new_df = pd.DataFrame(new_rows, columns=RESULT_COLUMNS)
    if existing_df.empty:
        return new_df
    if new_df.empty:
        return existing_df[RESULT_COLUMNS]
    return pd.concat([existing_df[RESULT_COLUMNS], new_df[RESULT_COLUMNS]], ignore_index=True)


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

def extract_json_object_from_text(text):
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]

    return None


def coerce_json_text(content):
    text = str(content or "").strip()
    if not text:
        raise json.JSONDecodeError("Empty response content", text, 0)

    if text.startswith("```"):
        fenced_match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL | re.IGNORECASE)
        if fenced_match:
            text = fenced_match.group(1).strip()

    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        extracted = extract_json_object_from_text(text)
        if extracted is not None:
            json.loads(extracted)
            return extracted
        raise


def parse_chat_completion_json(response):
    content = response.choices[0].message.content
    if isinstance(content, list):
        content = "".join(part.text for part in content if hasattr(part, "text"))
    json_text = coerce_json_text(content)
    return json.loads(json_text)


def create_chat_completion(messages, model, base_url):
    client = get_llm_client()
    request_kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
    }
    if llm_endpoint_supports_response_format(base_url):
        request_kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**request_kwargs)
    return parse_chat_completion_json(response)


def method_label_is_broad(method_name):
    text = str(method_name or "").strip().casefold()
    if not text:
        return True
    return any(re.search(pattern, text) for pattern in METHOD_BROAD_PATTERNS)


def extract_method_from_paper(full_text, row_metadata, context_status, settings):
    metadata_block = json.dumps(row_metadata or {}, indent=2, ensure_ascii=True)
    prompt = f"""
    You are extracting only the primary method actually implemented and used by the authors in an empirical research paper.
    You are parsing a {context_status}.

    Paper metadata:
    {metadata_block}

    Extracted text:
    ---
    {full_text[:45000]}
    ---

    Task:
    1. Return 'Method_Reported_By_Authors' as the most specific named method explicitly used by the authors.
    2. Return 'Method_Evidence' as a direct quote or very close paraphrase that supports that method choice.

    Rules:
    - Prefer the exact named algorithm, estimator, or design implemented by the authors.
    - Do not answer with a broad family if a narrower named method is available.
    - If the paper says PC algorithm, return PC algorithm.
    - If the paper says difference-in-differences, return difference-in-differences.
    - If the method is genuinely unclear, return "Don't know".

    Required JSON schema:
    {json.dumps(METHOD_EXTRACTION_SCHEMA, indent=2)}
    """
    messages = [
        {"role": "system", "content": "Return strictly valid JSON. No prose outside JSON."},
        {"role": "user", "content": prompt},
    ]
    return create_chat_completion(messages, settings["model"], settings["base_url"])


def refine_method_from_paper(full_text, row_metadata, previous_method, previous_evidence, context_status, settings):
    metadata_block = json.dumps(row_metadata or {}, indent=2, ensure_ascii=True)
    prompt = f"""
    You are correcting a method extraction that is too broad.
    You are parsing a {context_status}.

    Paper metadata:
    {metadata_block}

    Extracted text:
    ---
    {full_text[:45000]}
    ---

    Previous answer:
    - Method_Reported_By_Authors: {previous_method}
    - Method_Evidence: {previous_evidence}

    The previous method label is too broad. Replace it with the most specific named algorithm, estimator, statistical design, or causal model explicitly implemented by the authors.
    If no narrower named method appears in the text, return the same method label.

    Required JSON schema:
    {json.dumps(METHOD_EXTRACTION_SCHEMA, indent=2)}
    """
    messages = [
        {"role": "system", "content": "Return strictly valid JSON. No prose outside JSON."},
        {"role": "user", "content": prompt},
    ]
    return create_chat_completion(messages, settings["model"], settings["base_url"])


def extract_criteria_from_paper(full_text, row_metadata, method_name, method_evidence, context_status, settings):
    metadata_block = json.dumps(row_metadata or {}, indent=2, ensure_ascii=True)
    criteria_schema = {criterion: NAVIDAM_ASSESSMENT_SCHEMA[criterion] for criterion in FILTER_CRITERIA}
    prompt = f"""
    You are extracting NaviDAM criteria from an empirical research paper.
    You are parsing a {context_status}.

    Paper metadata:
    {metadata_block}

    The author-reported method has already been extracted and must be treated as fixed context:
    - Method_Reported_By_Authors: {method_name}
    - Method_Evidence: {method_evidence}

    Extracted text:
    ---
    {full_text[:45000]}
    ---

    Task:
    Populate only the NaviDAM criteria fields below. Do not return Method_Reported_By_Authors or Method_Evidence here.
    Use the exact option spellings from the schema. If a criterion is ambiguous, return "Don't know".

    Required JSON schema:
    {json.dumps(criteria_schema, indent=2)}
    """
    messages = [
        {"role": "system", "content": "Return strictly valid JSON. No prose outside JSON."},
        {"role": "user", "content": prompt},
    ]
    return create_chat_completion(messages, settings["model"], settings["base_url"])


def analyze_paper_with_navidam(full_text, row_metadata=None, is_full_text=True):
    """Submits full extracted text to the JSON structural LLM engine."""
    settings = get_llm_settings()

    context_status = "FULL-TEXT RESEARCH PAPER PDF" if is_full_text else "METADATA RECOVERY RECORD"
    try:
        method_results = extract_method_from_paper(full_text, row_metadata, context_status, settings)
        method_name = str(method_results.get("Method_Reported_By_Authors", "")).strip()
        method_evidence = str(method_results.get("Method_Evidence", "")).strip()

        if method_label_is_broad(method_name):
            refined_method_results = refine_method_from_paper(
                full_text,
                row_metadata,
                method_name,
                method_evidence,
                context_status,
                settings,
            )
            refined_name = str(refined_method_results.get("Method_Reported_By_Authors", "")).strip()
            refined_evidence = str(refined_method_results.get("Method_Evidence", "")).strip()
            if refined_name:
                method_name = refined_name
            if refined_evidence:
                method_evidence = refined_evidence

        criteria_results = extract_criteria_from_paper(
            full_text,
            row_metadata,
            method_name,
            method_evidence,
            context_status,
            settings,
        )
        criteria_results["Method_Reported_By_Authors"] = method_name
        criteria_results["Method_Evidence"] = method_evidence
        return criteria_results
    except LLMConfigurationError:
        raise
    except json.JSONDecodeError as exc:
        raise LLMInferenceError(f"Provider returned non-JSON content: {exc}") from exc
    except APITimeoutError as exc:
        raise LLMInferenceError(f"LLM request timed out for provider '{settings['provider']}'.") from exc
    except APIConnectionError as exc:
        raise LLMInferenceError(f"Could not connect to provider '{settings['provider']}': {exc}") from exc
    except APIStatusError as exc:
        status_code = getattr(exc, "status_code", "unknown")
        if status_code == 401:
            raise LLMInferenceError(
                f"Authentication failed for provider '{settings['provider']}'. Check the API key."
            ) from exc
        if status_code == 402:
            raise LLMInferenceError(
                f"Provider '{settings['provider']}' reported payment required or exhausted credits."
            ) from exc
        if status_code == 403:
            raise LLMInferenceError(
                f"Provider '{settings['provider']}' rejected access to model '{settings['model']}'."
            ) from exc
        if status_code == 404:
            raise LLMInferenceError(
                f"Model '{settings['model']}' was not found on provider '{settings['provider']}'."
            ) from exc
        if status_code == 429:
            raise LLMInferenceError(
                f"Provider '{settings['provider']}' rate-limited the request or the quota is exhausted."
            ) from exc
        raise LLMInferenceError(
            f"Provider '{settings['provider']}' returned HTTP {status_code}: {exc}"
        ) from exc
    except Exception as exc:
        raise LLMInferenceError(f"Unexpected LLM error from provider '{settings['provider']}': {exc}") from exc


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
        print("\n[Download List]")
        print("No PDFs remain in ONLINE_PDF_FAILED status.")
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
    existing_df = load_existing_results(output_csv_path)
    seen_keys = existing_result_keys(existing_df)
    current_model = get_assessment_model_label()
    
    evaluated_records = []
    print_log_block(
        "Online Triage",
        [
            f"Assessment model: {current_model}",
            f"Rows requested: {max_rows}",
            f"Rows to process in this pass: {len(df)}",
        ],
    )
    
    for idx, row in df.iterrows():
        pub_id = str(row.get('Publication ID')).strip()
        row_key = result_row_key(pub_id, current_model)
        if row_key in seen_keys:
            print(f" - Paper {pub_id}: skipped because it was already processed with model '{current_model}'.")
            continue

        pdf_url = row.get('Source Linkout', None)
        record = blank_result_record(row)
        screening_decision, screening_reason = classify_study_screening(row)
        record["Screening_Decision"] = screening_decision
        record["Screening_Reason"] = screening_reason

        if screening_decision == "NON_EMPIRICAL_SKIP":
            record["NaviDAM_Status"] = "SCREENED_OUT_NON_EMPIRICAL"
            print(f" - Paper {pub_id}: skipped before PDF assessment. {screening_reason}")
            evaluated_records.append(record)
            continue
            
        full_text = None
        if pd.notna(pdf_url):
            full_text = download_and_extract_pdf_url(pdf_url, pub_id)
            
        if full_text:
            print(f" - Paper {pub_id}: link active. Running assessment.")
            try:
                row_metadata = {
                    "Publication ID": row.get("Publication ID", ""),
                    "Title": row.get("Title", ""),
                    "Abstract": row.get("Abstract", ""),
                    "Source title": row.get("Source title", ""),
                    "Publication Type": row.get("Publication Type", ""),
                }
                assessment_results = analyze_paper_with_navidam(full_text, row_metadata=row_metadata, is_full_text=True)
                normalized_results, issues = normalize_assessment_results(assessment_results)
                record.update(normalized_results)
                record["Assessment_Validation_Issues"] = " | ".join(issues)
                record["NaviDAM_Status"] = "ASSESSMENT_COMPLETED_WITH_WARNINGS" if issues else "ASSESSMENT_COMPLETED"
            except LLMConfigurationError as exc:
                record["NaviDAM_Status"] = "LLM_CONFIGURATION_ERROR"
                record["Assessment_Error"] = str(exc)
                print(f"   Warning: {exc}")
            except LLMInferenceError as exc:
                record["NaviDAM_Status"] = "ASSESSMENT_SYSTEM_ERROR"
                record["Assessment_Error"] = str(exc)
                print(f"   Warning: {exc}")
        else:
            print(f" - Paper {pub_id}: warning. PDF URL broken or unreachable. Tagged and skipped.")
            
        evaluated_records.append(record)
        seen_keys.add(row_key)
        
    results_df = combine_results(existing_df, evaluated_records)
    results_df.to_csv(output_csv_path, index=False)
    print_log_block(
        "Run Summary",
        [
            f"New rows written in this pass: {len(evaluated_records)}",
            f"Results CSV: {output_csv_path}",
        ],
    )
    print_failed_pdf_manifest(pd.DataFrame(evaluated_records, columns=RESULT_COLUMNS), pdf_dir)
    return results_df

# Mode 2: Offline Local Catch-Up Sweep Processing
def run_local_folder_catchup(triage_csv_path, input_folder_path=DEFAULT_PDF_DIR):
    """Sifts out rows with the failure flag and scans your local storage folder for an offline catch-up run."""
    if not os.path.exists(triage_csv_path):
        print(f"Error: Target tracking file '{triage_csv_path}' missing.")
        return
        
    df = pd.read_csv(triage_csv_path)
    current_model = get_assessment_model_label()
    failed_rows = df[
        (df['NaviDAM_Status'] == "ONLINE_PDF_FAILED")
        & (df['Assessment_Model'].fillna("") == current_model)
    ]
    
    if failed_rows.empty:
        print_log_block(
            "Offline Catch-Up",
            [f"No rows found with an active 'ONLINE_PDF_FAILED' flag for model '{current_model}'."],
        )
        return
        
    print_log_block(
        "Offline Catch-Up",
        [
            f"Assessment model: {current_model}",
            f"Flagged rows for this model: {len(failed_rows)}",
            f"Scanning folder: {input_folder_path}",
        ],
    )
    
    for idx, row in df.iterrows():
        if row['NaviDAM_Status'] != "ONLINE_PDF_FAILED" or str(row.get('Assessment_Model', '')) != current_model:
            continue
            
        pub_id = row['Publication ID']
        local_pdf_path = os.path.join(input_folder_path, f"{pub_id}.pdf")
        
        if os.path.exists(local_pdf_path):
            print(f" - Paper {pub_id}: found matching offline PDF. Extracting local text.")
            local_text = extract_text_from_pdf_file(local_pdf_path)
            
            if local_text:
                try:
                    row_metadata = {
                        "Publication ID": row.get("Publication ID", ""),
                        "Title": row.get("Original_Title", row.get("Title", "")),
                        "DOI": row.get("DOI", ""),
                        "Source Linkout": row.get("Source Linkout", ""),
                    }
                    assessment_results = analyze_paper_with_navidam(local_text, row_metadata=row_metadata, is_full_text=True)
                    normalized_results, issues = normalize_assessment_results(assessment_results)
                    for field, value in normalized_results.items():
                        df.at[idx, field] = value
                    df.at[idx, 'Assessment_Validation_Issues'] = " | ".join(issues)
                    df.at[idx, 'NaviDAM_Status'] = "ASSESSMENT_COMPLETED_WITH_WARNINGS" if issues else "ASSESSMENT_COMPLETED"
                    print(f"   Success: Local fallback criteria mapped for {pub_id}.")
                except LLMConfigurationError as exc:
                    df.at[idx, 'NaviDAM_Status'] = "LLM_CONFIGURATION_ERROR"
                    df.at[idx, 'Assessment_Error'] = str(exc)
                    print(f"   Warning: {exc}")
                except LLMInferenceError as exc:
                    df.at[idx, 'NaviDAM_Status'] = "ASSESSMENT_SYSTEM_ERROR"
                    df.at[idx, 'Assessment_Error'] = str(exc)
                    print(f"   Warning: {exc}")
            else:
                print(f"   Warning: Local file '{local_pdf_path}' exists but contains no extractable text strings.")
        else:
            print(f" - Paper {pub_id}: notice. Local file '{pub_id}.pdf' not found yet. Keeping error flag.")
    df.to_csv(triage_csv_path, index=False)
    print_log_block("Run Summary", [f"Master log updated: {triage_csv_path}"])
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
    parser.add_argument(
        "--show-llm-config",
        action="store_true",
        help="Print the active provider/model/base-url configuration and exit.",
    )
    args = parser.parse_args()

    if args.show_llm_config:
        settings = get_llm_settings()
        if settings["api_key"]:
            masked_key = "configured"
        elif llm_endpoint_allows_missing_key(settings["base_url"]):
            masked_key = "not required for local endpoint"
        else:
            masked_key = "missing"
        print(f"Provider: {settings['provider']}")
        print(f"Model: {settings['model']}")
        print(f"Assessment Model Label: {get_assessment_model_label()}")
        print(f"Base URL: {settings['base_url'] or 'default OpenAI endpoint'}")
        print(f"API key: {masked_key}")
        return

    argv = sys.argv[1:]
    log_path, log_handle, original_stdout, original_stderr = install_run_logger(argv)

    try:
        output_csv_path = Path(args.output_csv).expanduser().resolve()
        pdf_dir = Path(args.pdf_dir).expanduser().resolve()
        pdf_dir.mkdir(parents=True, exist_ok=True)

        if args.catchup:
            triage_csv_path = Path(args.triage_csv).expanduser().resolve() if args.triage_csv else output_csv_path
            print_run_header(triage_csv_path, output_csv_path, pdf_dir, log_path, argv)
            run_local_folder_catchup(triage_csv_path, pdf_dir)
            return

        requested_csv = args.input_csv or args.csv_filename
        csv_path = resolve_input_csv(requested_csv)
        if csv_path is None:
            print(
                f"Initialization Error: Could not find '{requested_csv}' and no CSV files were found in '{CSV_DIR}'."
            )
            return

        print_run_header(csv_path, output_csv_path, pdf_dir, log_path, argv)
        run_online_triage_pass(
            csv_path,
            max_rows=args.max_rows,
            output_csv_path=output_csv_path,
            pdf_dir=pdf_dir,
        )

        print_log_block(
            "Workspace Setup",
            [
                f"Created folder: {pdf_dir}",
                "If any row logged a failure flag, download its full PDF, name it as 'pub.ID.pdf' and place it there.",
                f"Then run the local catch-up pass with: python {Path(__file__).name} --catchup --triage-csv {output_csv_path} --pdf-dir {pdf_dir}",
            ],
        )
    finally:
        restore_run_logger(log_handle, original_stdout, original_stderr)


if __name__ == "__main__":
    main()