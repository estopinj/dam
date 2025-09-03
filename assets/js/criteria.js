export const criteria = [
  // Objective (standalone, no category heading)
  { key: "Objective", label: "Objective", category: "__standalone__" },
  // Outcome
  { key: "Estimand", label: "Estimand", category: "Outcome" },
  { key: "Validity", label: "Target validity", category: "Outcome" },
  // Data compatibility
  { key: "Type", label: "Type", category: "Data compatibility" },
  { key: "Required TS length", label: "Required TS length", category: "Data compatibility" },
  { key: "Handles few samples", label: "Handles few samples", category: "Data compatibility" },
  { key: "Handles huge datasets (n)", label: "Handles huge datasets (n)", category: "Data compatibility" },
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
  { key: "IDD", label: "IDD", category: "Assumptions" },
  { key: "Model specific", label: "Model specific", category: "Assumptions" },
  // Model properties
  { key: "Requires explicit processes", label: "Requires explicit processes", category: "Model properties" },
  { key: "Exposure type", label: "Exposure type", category: "Model properties" },
  { key: "Number of variables", label: "Number of variables", category: "Model properties" },
  { key: "Propaguates uncertainty", label: "Propagates uncertainty", category: "Model properties" },
  { key: "Handles lag effects", label: "Handles lag effects", category: "Model properties" },
  { key: "Parametric nature", label: "Parametric nature", category: "Model properties" },
  // Packages
  { key: "Language", label: "Language", category: "Packages" },
  { key: "Usage", label: "Usage", category: "Packages" }
];





// Always include all possible options (other than "Any" and "Unsure") 
// for an ordinal criterion in its ordinalCriteriaOrder array,
// in the correct order from lowest to highest.
export const ordinalCriteriaOrder = {
  // "Required TS length": ["Handles ≤ 10", "≥ 10", "≥ 100"]
  // Add more ordinal criteria as needed
};





export const compositeOptions = {
  "Estimand": {
    "Any treatment effect": ["ATE", "ATT", "LATE", "CATE"],
    // Add more composite options as needed
  },
  // Add more criteria with composite options as needed
};




export const criteriaOptionLabelMap = {
  "Objective": {
    // "option_value": "Option Label",
  },
  // "Estimand": {
    // "ATE": "Average Treatment Effect",
  // },
  "Validity": {
    // "option_value": "Option Label",
  },
  "Type": {
    // "option_value": "Option Label",
  },
  "Required TS length": {
    // "option_value": "Option Label",
  },
  "Handles few samples": {
    // "option_value": "Option Label",
  },
  "Handles huge datasets (n)": {
    // "option_value": "Option Label",
  },
  "Handles missing data": {
    // "option_value": "Option Label",
  },
  "RS-data proven": {
    // "option_value": "Option Label",
  },
  "Fonctional form": {
    // "option_value": "Option Label",
  },
  "No unobserved confounders": {
    // "option_value": "Option Label",
  },
  "No interference": {
    // "option_value": "Option Label",
  },
  "Well-defined treatments": {
    // "option_value": "Option Label",
  },
  "Common support (positivity)": {
    // "option_value": "Option Label",
  },
  "Causal Markov Condition": {
    // "option_value": "Option Label",
  },
  "Faithfulness": {
    // "option_value": "Option Label",
  },
  "IDD": {
    // "option_value": "Option Label",
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
    // "option_value": "Option Label",
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

