import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# === Category → folder mapping ===
CATEGORY_FOLDER_MAP = {
    "Adjusted methods (Backdoor C.)": "adjusted",
    "Alternative paradigms": "alternative",
    "Causal ML": "causal_ML",
    "Independent detection": "detection", 
    "Causal discovery": "discovery",
    "Ecology-guided Modelling": "ecology-guided",
    "Experiments": "experiments",
    "Quasi-experiments": "quasi-exps",
    "Counterfactual & future simulations": "simulations",
    "Versatile tools": "tools"
}

# === SubCategory → folder mapping ===
SUBCAT_FOLDER_MAP = {
"Linear regressions & extensions": "linear_regressions",
"Predictive models +  interpretability metrics": "predictive_models",
"Alternative effect identification methods": "alternative_effects",
"Meta-learners": "meta_learners",
"Constraint-based methods": "constraint_based",
"Score-based methods": "score_based",
"Continuous optimization": "continuous_optimization",
"Asymmetry-based": "asymmetry_based",
"Prediction-based approaches": "prediction_based",
"Intermediate confounding": "intermediate_confounding",
"Visualisation helpers": "visualisation_helpers",
"Robustness & significance tests": "robustness_significance",
"Causal interpretability": "causal_interpretability",
"Uncertainty tools": "uncertainty_tools",
"Trend detection": "trend_detection",
"RS breakpoint detection": "RS_breakpoint_detection",
"Frequently monitored indices": "frequently_monitored",
"Preliminary data correction": "preliminary_data_correction",
}

# === SubCategory → parent folder mapping ===
SUBCAT_PARENT = {
"Linear regressions & extensions": "Ecology-guided Modelling",
"Predictive models +  interpretability metrics": "Ecology-guided Modelling",
"Alternative effect identification methods": "Adjusted methods (Backdoor C.)",
"Meta-learners": "Causal ML",
"Constraint-based methods": "Causal discovery",
"Score-based methods": "Causal discovery",
"Continuous optimization": "Causal discovery",
"Asymmetry-based": "Causal discovery",
"Prediction-based approaches": "Alternative paradigms",
"Intermediate confounding": "Alternative paradigms",
"Visualisation helpers": "Versatile tools",
"Robustness & significance tests": "Versatile tools",
"Causal interpretability": "Versatile tools",
"Uncertainty tools": "Versatile tools",
"Trend detection": "Independent detection",
"RS breakpoint detection": "Independent detection",
"Frequently monitored indices": "Independent detection",
"Preliminary data correction": "Independent detection",
}

# Combine them into one dictionary or list
data = {
    "CATEGORY_FOLDER_MAP": CATEGORY_FOLDER_MAP,
    "SUBCAT_FOLDER_MAP": SUBCAT_FOLDER_MAP,
    "SUBCAT_PARENT": SUBCAT_PARENT
}


# Write to file
with open(PROJECT_ROOT / "_data" / "cat_dicts.json", "w") as f:
    json.dump(data, f, indent=4)