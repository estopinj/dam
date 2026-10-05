import json
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT_DIR / "scripts" / "validation"
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

from navidam_batch_validate import enrich_dataframe, format_summary_json, summarize_dataframe


class StubSuggestionEngine:
    def suggest_methods(self, row):
        return row["Suggestions"]


def test_multi_method_alignment_scoring_and_summary():
    df = pd.DataFrame(
        [
            {
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
                "Method_Reported_By_Authors": "two-way fixed effects estimator; Convergent Cross Mapping",
                "Suggestions": ["Panel designs, TWFE"],
            },
            {
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
                "Method_Reported_By_Authors": "Process tracing; Multiple-case study",
                "Suggestions": ["PC"],
            },
            {
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
                "Method_Reported_By_Authors": "Convergent Cross Mapping",
                "Suggestions": ["CCM"],
            },
            {
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
                "Method_Reported_By_Authors": float("nan"),
                "Suggestions": ["PC"],
            },
        ]
    )

    enriched = enrich_dataframe(df, StubSuggestionEngine())

    assert enriched.loc[0, "Reported_Method_Concept"] == "Panel designs, TWFE; CCM"
    assert bool(enriched.loc[0, "Within_navidam"])
    assert not bool(enriched.loc[1, "Within_navidam"])
    assert bool(enriched.loc[2, "Within_navidam"])
    assert enriched.loc[3, "Reported_Method_Concept"] == ""
    assert enriched.loc[3, "Within_navidam"] == ""
    assert not bool(enriched.loc[3, "Recall_Evaluable"])

    summary = summarize_dataframe(enriched, "test.csv")
    assert summary["evaluable_articles"] == 3
    assert summary["correctly_recovered_articles"] == 2
    assert summary["correctly_recovered_methods"] == [["Panel designs, TWFE", "CCM"], ["CCM"]]
    assert summary["not_recovered_methods"] == [["process tracing", "multiple case study"]]
    assert json.loads(format_summary_json([summary])) == [summary]