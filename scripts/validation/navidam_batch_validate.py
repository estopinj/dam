from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from navidam_suggester import NaviDAMSuggestionEngine, method_concept_label


SUGGESTED_METHODS_COLUMN = "NaviDAM_Suggested_Methods"
SUGGESTED_METHOD_COUNT_COLUMN = "NaviDAM_Suggested_Method_Count"
MATCHED_METHODS_COLUMN = "Matched_Suggested_Method_Concepts"
LEGACY_MATCHED_METHODS_COLUMN = "NaviDAM_Matched_Suggested_Methods"
REPORTED_METHOD_NORMALIZED_COLUMN = "Reported_Method_Concept"
WITHIN_NAVIDAM_COLUMN = "Within_navidam"
LEGACY_REPORTED_METHOD_NAVIDAM_COLUMN = "NaviDAM_Reported_Method_Concept"
LEGACY_REPORTED_METHOD_NORMALIZED_COLUMN = "NaviDAM_Reported_Method_Canonical"
EVALUABLE_COLUMN = "Recall_Evaluable"
LEGACY_EVALUABLE_COLUMN = "NaviDAM_Recall_Evaluable"

NON_EVALUABLE_STATUSES = {
    "",
    "ASSESSMENT_SYSTEM_ERROR",
    "LLM_CONFIGURATION_ERROR",
    "LOCAL_PDF_FAILED",
    "ONLINE_PDF_FAILED",
    "SCREENED_OUT_NON_EMPIRICAL",
}
def is_evaluable(row):
    status = str(row.get("NaviDAM_Status", "") or "").strip()
    reported_method = str(row.get("Method_Reported_By_Authors", "") or "").strip()
    return status not in NON_EVALUABLE_STATUSES and bool(reported_method)


def enrich_dataframe(df, engine, limit=None):
    enriched_df = df.copy()
    max_rows = len(enriched_df) if limit is None else min(limit, len(enriched_df))

    for idx in range(max_rows):
        row = enriched_df.iloc[idx]
        suggestions = engine.suggest_methods(row)
        reported_concept = method_concept_label(row.get("Method_Reported_By_Authors", ""))
        suggested_concepts = []
        for suggestion in suggestions:
            suggestion_concept = method_concept_label(suggestion)
            if suggestion_concept and suggestion_concept not in suggested_concepts:
                suggested_concepts.append(suggestion_concept)
        evaluable = is_evaluable(row)

        enriched_df.at[idx, SUGGESTED_METHODS_COLUMN] = "; ".join(suggestions) if suggestions else ""
        enriched_df.at[idx, SUGGESTED_METHOD_COUNT_COLUMN] = len(suggestions)
        enriched_df.at[idx, MATCHED_METHODS_COLUMN] = "; ".join(suggested_concepts) if suggested_concepts else ""
        enriched_df.at[idx, REPORTED_METHOD_NORMALIZED_COLUMN] = reported_concept
        enriched_df.at[idx, WITHIN_NAVIDAM_COLUMN] = bool(reported_concept and reported_concept in set(suggested_concepts)) if evaluable else ""
        enriched_df.at[idx, EVALUABLE_COLUMN] = evaluable

    return enriched_df


def summarize_dataframe(df, csv_label):
    evaluable_df = df[df[EVALUABLE_COLUMN] == True]
    total = int(len(evaluable_df))
    hits = int(evaluable_df[WITHIN_NAVIDAM_COLUMN].eq(True).sum()) if total else 0
    recall = hits / total if total else None
    return {
        "source": csv_label,
        "evaluable_articles": total,
        "recall": recall,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Batch-run NaviDAM suggestions and recall scoring on parsed result CSVs.")
    parser.add_argument("csv_paths", nargs="+", help="Parsed NaviDAM result CSV files to enrich.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional directory for enriched CSV outputs. Defaults to updating each input file in place.",
    )
    parser.add_argument(
        "--summary-json",
        default=None,
        help="Optional JSON file path for combined recall summary output.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for quick validation runs.",
    )
    return parser.parse_args()


def resolve_output_path(input_path, output_dir):
    if not output_dir:
        return input_path
    output_root = Path(output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    return output_root / input_path.name


def reorder_output_columns(df):
    preferred_validation_columns = [
        SUGGESTED_METHODS_COLUMN,
        MATCHED_METHODS_COLUMN,
        SUGGESTED_METHOD_COUNT_COLUMN,
        EVALUABLE_COLUMN,
        REPORTED_METHOD_NORMALIZED_COLUMN,
        WITHIN_NAVIDAM_COLUMN,
    ]

    base_columns = [column for column in df.columns if column not in preferred_validation_columns]
    ordered_validation_columns = [column for column in preferred_validation_columns if column in df.columns]
    return df[base_columns + ordered_validation_columns]


def main():
    args = parse_args()
    engine = NaviDAMSuggestionEngine()
    combined_summary = []
    combined_frames = []

    for csv_arg in args.csv_paths:
        csv_path = Path(csv_arg).expanduser().resolve()
        df = pd.read_csv(csv_path)
        for optional_column in [
            SUGGESTED_METHODS_COLUMN,
            MATCHED_METHODS_COLUMN,
            LEGACY_MATCHED_METHODS_COLUMN,
            REPORTED_METHOD_NORMALIZED_COLUMN,
            WITHIN_NAVIDAM_COLUMN,
            LEGACY_EVALUABLE_COLUMN,
            LEGACY_REPORTED_METHOD_NAVIDAM_COLUMN,
            LEGACY_REPORTED_METHOD_NORMALIZED_COLUMN,
            EVALUABLE_COLUMN,
        ]:
            if optional_column in df.columns:
                df[optional_column] = df[optional_column].fillna("")
        columns_to_drop = [
            column
            for column in [
                "NaviDAM_Validation_Task",
                LEGACY_MATCHED_METHODS_COLUMN,
                LEGACY_EVALUABLE_COLUMN,
                LEGACY_REPORTED_METHOD_NAVIDAM_COLUMN,
                LEGACY_REPORTED_METHOD_NORMALIZED_COLUMN,
                "NaviDAM_Recall_Hit",
            ]
            if column in df.columns
        ]
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)

        enriched_df = enrich_dataframe(df, engine, limit=args.limit)
        enriched_df = reorder_output_columns(enriched_df)
        output_path = resolve_output_path(csv_path, args.output_dir)
        enriched_df.to_csv(output_path, index=False)

        combined_frames.append(enriched_df)
        per_file_summary = summarize_dataframe(enriched_df, csv_path.name)
        combined_summary.append(per_file_summary)

        print(f"Updated {output_path}")
        recall = "n/a" if per_file_summary["recall"] is None else f"{per_file_summary['recall']:.3f}"
        print(f"  evaluable={per_file_summary['evaluable_articles']} recall={recall}")

    if combined_frames:
        merged_df = pd.concat(combined_frames, ignore_index=True)
        row = summarize_dataframe(merged_df, "combined")
        combined_summary.append(row)
        recall = "n/a" if row["recall"] is None else f"{row['recall']:.3f}"
        print(f"Combined: evaluable={row['evaluable_articles']} recall={recall}")

    if args.summary_json:
        summary_path = Path(args.summary_json).expanduser().resolve()
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with summary_path.open("w", encoding="utf-8") as handle:
            json.dump(combined_summary, handle, indent=2)
        print(f"Wrote summary to {summary_path}")


if __name__ == "__main__":
    main()