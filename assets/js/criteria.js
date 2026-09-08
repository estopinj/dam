export const criteria = [
  // Objective (standalone, no category heading)
  { key: "Objective", label: "Objective", category: "__standalone__" },
  // Outcome
  { key: "Estimand", label: "Estimand", category: "Outcome" },
  // Data compatibility
  { key: "Type", label: "Type", category: "Data compatibility" },
  { key: "Minimal TS length", label: "Minimal TS length", category: "Data compatibility" },
  { key: "Handles few samples", label: "Handles few samples", category: "Data compatibility" },
  { key: "Handles huge datasets (n)", label: "Scalable to big data", category: "Data compatibility" },
  { key: "Handles missing data", label: "Handles missing data", category: "Data compatibility" },
  { key: "RS-data proven", label: "RS-data proven", category: "Data compatibility" },
  // Assumptions
  { key: "Fonctional form", label: "Functional form", category: "Assumptions" },
  { key: "No unobserved confounders", label: "No unobserved confounders", category: "Assumptions" },
  { key: "No interference", label: "No interference", category: "Assumptions" },
  { key: "Well-defined treatments", label: "Well-defined treatments", category: "Assumptions" },
  { key: "Common support (positivity)", label: "Common support (positivity)", category: "Assumptions" },
  { key: "Causal Markov Condition", label: "Causal Markov Condition", category: "Assumptions" },
  { key: "Faithfulness", label: "Faithfulness", category: "Assumptions" },
  { key: "IID", label: "IID", category: "Assumptions" },
  { key: "Model specific", label: "Model specific", category: "Assumptions" },
  // Model properties
  { key: "Requires explicit processes", label: "Requires explicit processes", category: "Model properties" },
  { key: "Exposure type", label: "Exposure type", category: "Model properties" },
  { key: "Number of variables", label: "Number of variables", category: "Model properties" },
  { key: "Propaguates uncertainty", label: "Propagates uncertainty", category: "Model properties" },
  { key: "Handles lag effects", label: "Handles lag effects", category: "Model properties" },
  { key: "Parametric nature", label: "Parametric nature", category: "Model properties" },
  // Implementation
  { key: "Language", label: "Language", category: "Implementation" },
  { key: "Usage", label: "Usage", category: "Implementation" }
];





// Always include all possible options (other than "Any" and "Unsure") 
// for an ordinal criterion in its ordinalCriteriaOrder array,
// in the correct order from lowest to highest:
// Right options are included when a lowest level (left) is selected.
// From most to least permissive options
export const ordinalCriteriaOrder = {
  "Minimal TS length": ["≥ 100", "≥ 10", "Handles ≤ 10"],
  "Handles few samples": ["No", "10 to 100", "Yes ≤ 10", "Yes CT design"],
  "Handles huge datasets (n)": ["No", "Most dont", "Most do", "Yes", "Necessary"],
  "Handles missing data": ["No: requires prelim. correction", "Partially", "Yes"],
  "RS-data proven": ["No", "Few applications", "Yes"],
  "Propaguates uncertainty": ["Needs model-agnostic propagation", "Model-specific tools", "Inherent capacity"],
  "Handles lag effects": ["No", "Possible", "Yes"],
  "No unobserved confounders": ["Required", "Recommended", "Relaxes assumption"],
  "No interference": ["Required", "Recommended", "Relaxes assumption"],
  "Well-defined treatments": ["Required", "Recommended", "Relaxes assumption"],
  "Common support (positivity)": ["Required", "Recommended", "Relaxes assumption"],
  "Causal Markov Condition": ["Required", "Recommended", "Relaxes assumption"],
  "Faithfulness": ["Required", "Recommended", "Relaxes assumption"],
  "IID": ["Required", "Recommended", "Relaxes assumption"],
  // Add more ordinal criteria as needed
};




export const compositeOptions = {
  "Estimand": {
    "Any treatment effect": ["ATE", "ATT", "LATE", "CATE"],
    // Add more composite options as needed
  },
  "Handles huge datasets (n)": {
    "Necessary": ["Yes", "Most do"]
  }
};


export const hideCompositeConstituents = {
  "Handles huge datasets (n)": {
    "Necessary": true
  }
};



export const criteriaOptionLabelMap = {
  "Objective": {
    "Detection": "Change detection"
  },
  // "Estimand": {
    // "ATE": "Average Treatment Effect",
  // },
  "Type": {
    // "option_value": "Option Label",
  },
  "Minimal TS length": {
    "≥ 10": "At least ~10 time points",
    "≥ 100": "100 as order of magnitude",
  },
  "Handles few samples": {
    "Yes CT design": "Yes, Control/Treatment design",
    "No": "No need",
  },
  "Handles huge datasets (n)": {
    "Most dont": "Not prioritized",
    "No": "No need",
  },
  "Handles missing data": {
    "No: requires prelim. correction": "No, complete data only",
    "Partially": "Simple corrections feasible",
    "Yes": "Yes, built-in / prelim. correction",
  },
  "RS-data proven": {
    "No": "No need",
    "Few applications": "At least few RS applications exist",
    "Yes": "Yes, many RS applications exist"
  },
  "Fonctional form": {
    // "option_value": "Option Label",
  },
  "No unobserved confounders": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "No interference": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "Well-defined treatments": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "Common support (positivity)": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "Causal Markov Condition": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "Faithfulness": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "IID": {
    "Relaxes assumption": "Method relaxes assumption",
    "Required": "Assumption required",
  },
  "Model specific": {
    // "option_value": "Option Label",
  },
  "Requires explicit processes": {
    // "option_value": "Option Label",
  },
  "Exposure type": {
    // "option_value": "Option Label",
  },
  "Number of variables": {
    // "option_value": "Option Label",
  },
  "Propaguates uncertainty": {
    // "option_value": "Option Label",
  },
  "Handles lag effects": {
    "No": "No need",
  },
  "Parametric nature": {
    // "option_value": "Option Label",
  },
  "Language": {
    // "option_value": "Option Label",
  },
  "Usage": {
    // "option_value": "Option Label",
  }
};



export const multipleAllowedCriteria = [
  "Estimand",
  "Type",
  // "Handles few samples",
  "Fonctional form",
  "Model specific",
  "Requires explicit processes",
  "Exposure type",
  "Number of variables",
  "Parametric nature",
  "Language",
  "Usage"
  // Add more as needed
];