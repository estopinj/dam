import json
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "scripts"))

import assessment_consensus as ac  # noqa: E402


def vote(confidence, **answers):
    return {"assessor": "A", "confidence": confidence, "answers": {k: v.split("|") for k, v in answers.items()}}


def status_of(votes):
    return ac.method_status(votes)


def test_single_vote_is_single_status_with_confidence():
    result = status_of([vote(4, IID="Required")])
    assert result["status"] == "single"
    assert result["confidence"] == 4


def test_two_identical_assessments_are_consensus():
    votes = [vote(4, IID="Required", Objective="Detection"), vote(2, IID="Required", Objective="Detection")]
    result = status_of(votes)
    assert result["status"] == "consensus"
    assert result["agreement_share"] == 1


def test_two_opposite_ordinal_answers_are_debated():
    votes = [vote(3, IID="Required"), vote(3, IID="Relaxes assumption")]
    result = status_of(votes)
    assert result["status"] == "debated"
    assert result["criteria"][0]["debated"] is True


def test_adjacent_ordinal_answers_get_partial_credit():
    # Adjacent levels have similarity 0.5, so best-supported agreement is (1 + 0.5) / 2 = 0.75.
    votes = [vote(3, IID="Required"), vote(3, IID="Recommended")]
    assert status_of(votes)["status"] == "consensus"


def test_two_thirds_of_assessors_agreeing_is_consensus():
    votes = [vote(3, IID="Required"), vote(3, IID="Required"), vote(3, IID="Relaxes assumption")]
    crit = status_of(votes)["criteria"][0]
    assert crit["agreement"] == pytest.approx(2 / 3, abs=1e-3)
    assert crit["debated"] is False


def test_confidence_weights_the_agreement():
    # 1 confident vote vs 1 unsure vote on opposite answers: 5/(5+1) = 0.83 -> agreement
    votes = [vote(5, Language="R"), vote(1, Language="Python")]
    assert status_of(votes)["status"] == "consensus"
    assert ac.consensus_value(votes, "Language") == ["R"]


def test_multiple_choice_uses_jaccard():
    assert ac.similarity("Language", ["R", "Python"], ["R"]) == 0.5
    assert ac.similarity("Language", ["R"], ["Python"]) == 0.0


def test_non_level_ordinal_answers_only_match_themselves():
    assert ac.similarity("IID", ["Inapplicable"], ["Required"]) == 0.0
    assert ac.similarity("IID", ["Inapplicable"], ["Inapplicable"]) == 1.0


def test_share_of_criteria_decides_method_status():
    agree = dict(Objective="Detection", Language="R", Usage="a")
    votes = [vote(3, IID="Required", **agree), vote(3, IID="Relaxes assumption", **agree)]
    result = status_of(votes)
    assert (result["agreeing"], result["evaluated"]) == (3, 4)
    assert result["status"] == "consensus"  # 3/4 >= 2/3


def test_published_value_prefers_current_value_on_tie():
    votes = [vote(3, Language="R"), vote(3, Language="Python")]
    assert ac.compute_published(votes, {"Language": "Python"})["Language"] == "Python"
    assert ac.compute_published(votes, {"Language": "R"})["Language"] == "R"


def test_published_confidence_is_rounded_mean():
    votes = [vote(5, IID="Required"), vote(2, IID="Required")]
    assert ac.compute_published(votes)[ac.CONFIDENCE_COLUMN] == "4"


def test_status_file_hides_issue_numbers(tmp_path):
    votes_dir = tmp_path / "votes"
    votes_dir.mkdir()
    data = {"method": "M", "votes": [dict(vote(3, IID="Required"), issue=12), dict(vote(3, IID="Required"), issue=13)]}
    (votes_dir / "m.json").write_text(json.dumps(data), encoding="utf-8")
    out = tmp_path / "status.json"
    ac.build_status_file(votes_dir, out)
    text = out.read_text(encoding="utf-8")
    assert json.loads(text)["M"]["status"] == "consensus"
    assert "issue" not in text


def test_ordinal_levels_match_issue_template():
    src = (ROOT_DIR / ".github/ISSUE_TEMPLATE/method-assessment.yml").read_text(encoding="utf-8")
    for block in yaml.safe_load(src)["body"]:
        field_id = block.get("id")
        if not field_id or not re.search(r"# Ordinal criteria\n\s+id: " + field_id + "\n", src) or field_id == "confidence":
            continue
        label = block["attributes"]["label"]
        entry = next((v for k, v in ac.CRITERIA.items() if v[0] == label or k == label), None)
        assert entry is not None, f"{label} missing from CRITERIA"
        assert entry[1] == "ordinal"
        assert entry[2] == [o for o in block["attributes"]["options"] if o != "Inapplicable"]
