import contextlib
import io
import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import scripts.validation.validation_v2 as validation


def test_align_option_to_closest_vocabulary_value():
    assert (
        validation.align_option_to_vocabulary(
            "Objective",
            "Causal relationship",
            validation.FILTER_VOCABULARY["Objective"],
        )
        == "Causal relationship(s)"
    )
    assert (
        validation.align_option_to_vocabulary(
            "Estimand",
            "Average treatment effect (ATE)",
            validation.FILTER_VOCABULARY["Estimand"],
        )
        == "ATE"
    )
    assert (
        validation.align_option_to_vocabulary(
            "Handles few samples",
            "Yes ≤10",
            validation.FILTER_VOCABULARY["Handles few samples"],
        )
        == "Yes ≤ 10"
    )
    assert (
        validation.align_option_to_vocabulary(
            "Minimal TS length",
            ">= 10",
            validation.FILTER_VOCABULARY["Minimal TS length"],
        )
        == "≥ 10"
    )
    assert (
        validation.align_option_to_vocabulary(
            "Objective",
            "Causal effect",
            validation.FILTER_VOCABULARY["Objective"],
        )
        == "Causal effect"
    )

    normalized, issues = validation.normalize_assessment_results(
        {
            "Method_Reported_By_Authors": "Change detection method",
            "Method_Evidence": "The method was applied to detect change.",
            "Objective": "Causal relationship",
            "Estimand": "Average treatment effect (ATE)",
        }
    )
    assert normalized["Objective"] == "Causal relationship(s)"
    assert normalized["Estimand"] == "ATE"
    assert not issues


def test_normalize_method_extraction_keeps_multiple_methods_and_evidence():
    method_names, method_evidence = validation.normalize_method_extraction(
        {
            "Methods": [
                {
                    "Method_Reported_By_Authors": "Difference-in-differences",
                    "Method_Evidence": "We used a difference-in-differences design.",
                },
                {
                    "Method_Reported_By_Authors": "difference-in-differences",
                    "Method_Evidence": "Treatment effects were estimated using DiD.",
                },
                {
                    "Method_Reported_By_Authors": "BACI",
                    "Method_Evidence": "We applied a before-after control-impact analysis.",
                },
            ]
        }
    )

    assert method_names == "Difference-in-differences; BACI"
    assert "We used a difference-in-differences design." in method_evidence
    assert "Treatment effects were estimated using DiD." in method_evidence
    assert "before-after control-impact analysis" in method_evidence


def test_criteria_prompt_emphasizes_objective_and_estimand(monkeypatch):
    captured_messages = []

    def capture_completion(messages, model, base_url):
        captured_messages.extend(messages)
        return {}

    monkeypatch.setattr(validation, "create_chat_completion", capture_completion)

    validation.extract_criteria_from_paper(
        "Article text",
        {},
        "Difference-in-differences",
        "We used a difference-in-differences design.",
        "FULL-TEXT RESEARCH PAPER PDF",
        {"model": "test-model", "base_url": "http://localhost:11434/v1"},
    )

    prompt = captured_messages[-1]["content"]
    assert "Give special attention to Objective and Estimand" in prompt
    assert "Objective is the analytical task" in prompt
    assert "Estimand is the target quantity or contrast" in prompt


def test_method_prompts_only_extract_detection_and_attribution_methods(monkeypatch):
    captured_messages = []

    def capture_completion(messages, model, base_url):
        captured_messages.extend(messages)
        return {"Methods": []}

    monkeypatch.setattr(validation, "create_chat_completion", capture_completion)
    settings = {"model": "test-model", "base_url": "http://localhost:11434/v1"}

    validation.extract_method_from_paper("Article text", {}, "FULL TEXT", settings)
    validation.refine_method_from_paper("Article text", {}, "old method", "old evidence", "FULL TEXT", settings)

    prompts = [message["content"] for message in captured_messages if message["role"] == "user"]
    scope_instruction = "Include only methods directly used for change detection or attribution of changes to drivers"
    assert len(prompts) == 2
    assert all(scope_instruction in prompt for prompt in prompts)


def test_online_triage_reassesses_active_model_and_keeps_other_models(tmp_path, monkeypatch):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "results.csv"
    input_path.write_text(
        "Dimensions export metadata\n"
        "Publication ID,DOI,Title,Abstract,Source Linkout\n"
        "pub.test,10.1/test,Test study,We estimate effects using observational data.,https://example.invalid/test.pdf\n",
        encoding="utf-8",
    )

    current_model = validation.get_assessment_model_label()
    pd.DataFrame(
        [
            {
                "Publication ID": "pub.test",
                "Assessment_Model": current_model,
                "Method_Reported_By_Authors": "old method",
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
            },
            {
                "Publication ID": "pub.test",
                "Assessment_Model": "ollama::other-model",
                "Method_Reported_By_Authors": "other-model method",
                "NaviDAM_Status": "ASSESSMENT_COMPLETED",
            },
        ]
    ).to_csv(output_path, index=False)

    monkeypatch.setattr(validation, "load_unsuited_pub_ids", lambda: set())
    monkeypatch.setattr(validation, "download_and_extract_pdf_url", lambda *args, **kwargs: "full paper text")
    monkeypatch.setattr(
        validation,
        "analyze_paper_with_navidam",
        lambda *args, **kwargs: {
            "Method_Reported_By_Authors": "new method",
            "Method_Evidence": "direct evidence",
        },
    )
    monkeypatch.setattr(validation, "update_download_manifest", lambda *args, **kwargs: ("dummy", 0, 2))

    with contextlib.redirect_stdout(io.StringIO()):
        validation.run_online_triage_pass(
            input_path,
            max_rows=1,
            output_csv_path=output_path,
            auto_pdf_download=False,
        )

    results = pd.read_csv(output_path)
    assert len(results) == 2
    active_result = results[results["Assessment_Model"] == current_model].iloc[0]
    other_result = results[results["Assessment_Model"] == "ollama::other-model"].iloc[0]
    assert active_result["Method_Reported_By_Authors"] == "new method"
    assert other_result["Method_Reported_By_Authors"] == "other-model method"