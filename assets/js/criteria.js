export const criteria = [
  // Objective (standalone, no category heading)
  { key: "Objective", label: "Objective", category: "__standalone__" },

  // Outcome
  { key: "Estimand", label: "Estimand", category: "Outcome" },
  { key: "Validity", label: "Validity", category: "Outcome" },

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