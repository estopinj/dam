console.log("Filter.js loaded!");

const siteBaseurl = JSON.parse(document.getElementById('site-baseurl').textContent);
const objectiveCriteriaMap = JSON.parse(document.getElementById('objective-criteria-map').textContent);


document.addEventListener('DOMContentLoaded', function() {

  // Only run if method-data and criteria-filters exist
  if (!document.getElementById('method-data') || !document.getElementById('criteria-filters')) {
    console.log("Required elements not found, script not running.");
    return;
  }
  // document.addEventListener("turbolinks:load", function() {
  // document.addEventListener("DOMContentLoaded", function() {
  console.log("Script started");

  // 1. Load method data
  const methodData = JSON.parse(document.getElementById('method-data').textContent);
  console.log("Loaded methodData:", methodData);

  // 2. Define the criteria you want dropdowns for (column names from your TSV)
const criteria = [
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
  

  // 3. Get unique options for each criterion
  const optionsByCriterion = {};
  criteria.forEach(criterion => {
    const opts = new Set();
    methodData.forEach(m => {
      if (m[criterion.key]) {
        m[criterion.key].split(",").forEach(val => opts.add(val.trim()));
      }
    });
    optionsByCriterion[criterion.key] = Array.from(opts).sort();
  });
  console.log("Options by criterion:", optionsByCriterion);

  const criteriaMapping = JSON.parse(document.getElementById('criteria-mapping').textContent);

  // Mapping of category names to permalinks
  const categoryLinks = {
    "Outcome": `${siteBaseurl}/outcome`,
    "Data compatibility": `${siteBaseurl}/data`,
    "Assumptions": `${siteBaseurl}/assumptions`,
    "Model properties": `${siteBaseurl}/properties`,
    "Packages": `${siteBaseurl}/packages`
  };

  // 4. Render dropdowns
  const filtersDiv = document.getElementById("criteria-filters");
  console.log("filtersDiv:", filtersDiv);
  

  let lastCategory = null;
  let categoryContainers = {}; // Store containers for each category

  // Build category order array in the order they appear in criteria
  const categoryOrder = [];
  criteria.forEach(c => {
      if (!categoryOrder.includes(c.category)) categoryOrder.push(c.category);
  });

  criteria.forEach(criterion => {
    // Insert category heading and collapsible container if this is a new category
    if (criterion.category !== lastCategory && criterion.category !== "__standalone__") {
      const catHeading = document.createElement("div");
      catHeading.style.marginTop = "1em";
      catHeading.style.marginLeft = "0.5em";
      catHeading.style.fontSize = "1.1em";
      catHeading.style.cursor = "pointer";
      catHeading.style.display = "flex";
      catHeading.style.alignItems = "center";

      // Category name (as span, not link)
      const catName = document.createElement("span");
      catName.textContent = criterion.category;
      catName.style.fontWeight = "bold";

      // Add expand/collapse indicator
      const arrow = document.createElement("span");
      arrow.textContent = " ▶";
      arrow.style.marginLeft = "0.5em";
      arrow.style.marginRight = "0.5em";

      // Create the help link (?)
      const catHelp = document.createElement("a");
      catHelp.href = categoryLinks[criterion.category] || "#";
      catHelp.target = "_blank";
      catHelp.rel = "noopener noreferrer";
      catHelp.title = `More info about ${criterion.category}`;
      catHelp.style.marginLeft = "0.5em";
      catHelp.style.fontSize = "0.85em";
      catHelp.innerHTML = "(?)";

      // Collapsible container for this category's criteria
      const catContainer = document.createElement("div");
      catContainer.style.display = "none";
      catContainer.dataset.category = criterion.category;
      categoryContainers[criterion.category] = catContainer;

      // Toggle on heading click (but not when clicking the help link)
      catHeading.addEventListener("click", function(e) {
        if (e.target === catHelp) return; // Don't toggle if help clicked
        const isOpen = catContainer.style.display === "block";
        catContainer.style.display = isOpen ? "none" : "block";
        arrow.textContent = isOpen ? " ▶" : " ▼";
      });

      catHeading.appendChild(catName);
      catHeading.appendChild(arrow);
      catHeading.appendChild(catHelp);
      filtersDiv.appendChild(catHeading);
      filtersDiv.appendChild(catContainer);
      lastCategory = criterion.category;
    }

    // Render the criterion as before, but append to catContainer
    const wrapper = document.createElement("div");
    wrapper.style.marginBottom = "0.5em";
    wrapper.dataset.criterionKey = criterion.key;

    const label = document.createElement("label");
    label.style.display = "inline-block";
    label.style.whiteSpace = "nowrap";
    if (criterion.key === "Objective") {
      wrapper.classList.add("objective-frame");
      label.classList.add("objective-highlight");
      wrapper.style.marginTop = "1.5em";
      wrapper.style.marginBottom = "1.5em";
      wrapper.style.background = "#f5f7ff"; // subtle highlight background
      wrapper.style.borderRadius = "6px";
      wrapper.style.boxShadow = "0 2px 8px rgba(42,58,140,0.06)";
      wrapper.style.padding = "1em 0.5em";
    }
    label.appendChild(document.createTextNode(criterion.label + ": "));

    // Create a container for (?) and select, and indent it
    const rightContainer = document.createElement("span");
    rightContainer.style.marginLeft = "7em";

    const criterionSlug = slugify(criterion.key);
    const helpLink = document.createElement("a");
    const criteriaMapping = JSON.parse(document.getElementById('criteria-mapping').textContent);

    // When creating the help link for a criterion:
    const helpHref = criteriaMapping[criterion.key]
      ? siteBaseurl + criteriaMapping[criterion.key]
      : `${siteBaseurl}/contents/criteria/${criterionSlug}`;
    helpLink.href = helpHref;
    helpLink.target = "_blank";
    helpLink.rel = "noopener noreferrer";
    helpLink.title = `More info about ${criterion.label}`;
    helpLink.style.marginRight = "6px";
    helpLink.style.fontSize = "0.85em";
    helpLink.innerHTML = "(?)";

    const select = document.createElement("select");
    select.id = "filter-" + criterion.key;
    if (criterion.key === "Objective") {
      select.classList.add("objective-highlight");
    }
    select.innerHTML = `<option value="">(Any)</option>` +
      optionsByCriterion[criterion.key].map(opt => `<option value="${opt}">${opt}</option>`).join("");

    // When a selection is made, expand the next category
    select.addEventListener("change", function() {
      // Find all criteria in this category
      const currentCategory = criterion.category;
      const criteriaInCategory = criteria.filter(c => c.category === currentCategory);
      // Check if this is the last criterion in the category
      if (criteriaInCategory[criteriaInCategory.length - 1].key === criterion.key) {
        // Find the next category in order
        const idx = categoryOrder.indexOf(currentCategory);
        if (idx !== -1 && idx < categoryOrder.length - 1) {
          const nextCat = categoryOrder[idx + 1];
          const nextContainer = categoryContainers[nextCat];
          // Find the heading for the next category
          const nextHeading = Array.from(filtersDiv.children).find(
            el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === nextCat
          );
          if (nextContainer && nextHeading) {
            nextContainer.style.display = "block";
            // Update arrow
            const arrow = nextHeading.querySelector("span:nth-child(2)");
            if (arrow) arrow.textContent = " ▼";
            // Optionally, scroll into view:
            nextHeading.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        }
      }
    });

    rightContainer.appendChild(helpLink);
    rightContainer.appendChild(select);

    wrapper.appendChild(label);
    wrapper.appendChild(rightContainer);
    // categoryContainers[criterion.category].appendChild(wrapper);
    if (criterion.category === "__standalone__") {
      filtersDiv.appendChild(wrapper);
    } else {
      categoryContainers[criterion.category].appendChild(wrapper);
    }
  });


  // After the rendering loop, add this Objective change handler:
  const objectiveSelect = document.getElementById("filter-Objective");
  objectiveSelect.addEventListener("change", function() {
  const selectedObjective = objectiveSelect.value;
  if (!selectedObjective) {
    // Find the currently open category (if any)
    let openCat = null;
    categoryOrder.forEach(cat => {
      if (cat === "__standalone__") return;
      const container = categoryContainers[cat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
      );
      if (container && heading && heading.style.display !== "none" && container.style.display === "block") {
        openCat = cat;
      }
    });

    // Show all criteria and all category headings, collapse all containers
    document.querySelectorAll('[data-criterion-key]').forEach(div => {
      div.style.display = "";
    });
    categoryOrder.forEach(cat => {
      if (cat === "__standalone__") return;
      const container = categoryContainers[cat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
      );
      if (container) container.style.display = "none";
      if (heading) heading.style.display = "";
      // Set arrow to collapsed
      if (heading) {
        const arrow = heading.querySelector("span:nth-child(2)");
        if (arrow) arrow.textContent = " ▶";
      }
    });

    // Restore previously open category, if any
    if (openCat) {
      const container = categoryContainers[openCat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === openCat
      );
      if (container && heading) {
        container.style.display = "block";
        const arrow = heading.querySelector("span:nth-child(2)");
        if (arrow) arrow.textContent = " ▼";
      }
    }
    return;
  }
  const relevant = objectiveCriteriaMap[selectedObjective] || [];
  document.querySelectorAll('[data-criterion-key]').forEach(div => {
    if (relevant.includes(div.dataset.criterionKey) || div.dataset.criterionKey === "Objective") {
      div.style.display = "";
    } else {
      div.style.display = "none";
      // Optionally clear the value:
      const sel = div.querySelector("select");
      if (sel) sel.value = "";
    }
  });
  
  // After updating criterion visibility:
  categoryOrder.forEach(cat => {
    if (cat === "__standalone__") return;
    const container = categoryContainers[cat];
    const heading = Array.from(filtersDiv.children).find(
      el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
    );
    // Check if any visible criterion in this category
    const hasVisible = Array.from(container.children).some(child => child.style.display !== "none");
    if (!hasVisible) {
      container.style.display = "none";
      if (heading) heading.style.display = "none";
    } else {
      if (heading) heading.style.display = "";
    }
  });
  // Find and expand the first non-empty category
  for (const cat of categoryOrder) {
    if (cat === "__standalone__") continue;
    const container = categoryContainers[cat];
    const heading = Array.from(filtersDiv.children).find(
      el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
    );
    if (container && heading && heading.style.display !== "none") {
      container.style.display = "block";
      // Update arrow
      const arrow = heading.querySelector("span:nth-child(2)");
      if (arrow) arrow.textContent = " ▼";
      break;
    }
  }
  });



  // 5. Filter and display methods
  function filterMethods() {
    let filtered = methodData;
    criteria.forEach(criterion => {
      const val = document.getElementById("filter-" + criterion.key).value;
      if (val) {
        filtered = filtered.filter(m =>
          m[criterion.key] && m[criterion.key].split(",").map(x => x.trim()).includes(val)
        );
      }
    });
    displayMethods(filtered);
  }

  // 6. Display filtered methods
// function displayMethods(methods) {
//     const div = document.getElementById("filtered-methods");
//     if (!div) {
//         console.log("filtered-methods div not found!");
//         return;
//     }

//     // Load category/subcat mappings
//     const catDicts = JSON.parse(document.getElementById('cat-dicts').textContent);
//     const CATEGORY_FOLDER_MAP = catDicts.CATEGORY_FOLDER_MAP;
//     const SUBCAT_FOLDER_MAP = catDicts.SUBCAT_FOLDER_MAP;


//     // Filter out methods with missing "Method list"
//     const validMethods = methods.filter(m => m["Method list"]);
//     if (validMethods.length === 0) {
//         div.innerHTML = "<p>No methods match your criteria.</p>";
//         return;
//     }
//     if (validMethods.length === methodData.length) {
//         div.innerHTML = `Any <a href="${siteBaseurl}/methods" target="_blank" rel="noopener noreferrer">method</a>!`;
//         return;
//     }
//     div.innerHTML = "<ul>" + validMethods.map(m => {
//     // Get first category and sub-category
//     const category = m["Category"] ? m["Category"].split(",")[0].trim() : "";
//     const subcat = m["Sub-category"] ? m["Sub-category"].split(",")[0].trim() : "";
//     const methodName = m["Method list"];
//     const methodSlug = slugify(methodName);
//     const categoryFolder = CATEGORY_FOLDER_MAP[category] || slugify(category);
//     const subcatFolder = SUBCAT_FOLDER_MAP[subcat] || slugify(subcat);

//     let url;
//     if (methodName in SUBCAT_FOLDER_MAP) {
//         // Subcategory index page
//         url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/`;
//     } else if (subcat) {
//         // Method in subcategory
//         url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/${methodSlug}/`;
//     } else {
//         // Method in category only
//         url = `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;
//     }

//     return `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${methodName}</a></li>`;
//   }).join("") + "</ul>";
// }
function displayMethods(methods) {
    const div = document.getElementById("filtered-methods");
    if (!div) {
        console.log("filtered-methods div not found!");
        return;
    }

    // Load category/subcat mappings
    const catDicts = JSON.parse(document.getElementById('cat-dicts').textContent);
    const CATEGORY_FOLDER_MAP = catDicts.CATEGORY_FOLDER_MAP;
    const SUBCAT_FOLDER_MAP = catDicts.SUBCAT_FOLDER_MAP;
    const SUBCAT_PARENT = catDicts.SUBCAT_PARENT;

    // Filter out methods with missing "Method list"
    const validMethods = methods.filter(m => m["Method list"]);
    if (validMethods.length === 0) {
        div.innerHTML = "<p>No methods match your criteria.</p>";
        return;
    }
    if (validMethods.length === methodData.length) {
        div.innerHTML = `Any <a href="${siteBaseurl}/methods" target="_blank" rel="noopener noreferrer">method</a>!`;
        return;
    }

    // Group methods by category and subcategory
    const grouped = {};
    validMethods.forEach(m => {
        // Get label for category and subcategory
        let category = m["Category"] ? m["Category"].split(",")[0].trim() : "";
        let subcat = m["Sub-category"] ? m["Sub-category"].split(",")[0].trim() : "";

        // Map folder to label
        let categoryLabel = Object.keys(CATEGORY_FOLDER_MAP).find(
            k => CATEGORY_FOLDER_MAP[k] === slugify(category)
        ) || category;

        let subcatLabel = Object.keys(SUBCAT_FOLDER_MAP).find(
            k => SUBCAT_FOLDER_MAP[k] === slugify(subcat)
        ) || subcat;

        // If subcat exists, get its parent category label
        if (subcatLabel && SUBCAT_PARENT[subcatLabel]) {
            categoryLabel = SUBCAT_PARENT[subcatLabel];
        }

        if (!grouped[categoryLabel]) grouped[categoryLabel] = {};
        if (subcatLabel) {
            if (!grouped[categoryLabel][subcatLabel]) grouped[categoryLabel][subcatLabel] = [];
            grouped[categoryLabel][subcatLabel].push(m);
        } else {
            if (!grouped[categoryLabel]["__no_subcat__"]) grouped[categoryLabel]["__no_subcat__"] = [];
            grouped[categoryLabel]["__no_subcat__"].push(m);
        }
    });

    // Build HTML
    let html = "<div class='method-categories'>";
    Object.keys(grouped).forEach(cat => {
        html += `<div class="method-category-block"><h3>${cat}</h3>`;
        Object.keys(grouped[cat]).forEach(subcat => {
            if (subcat !== "__no_subcat__") {
                html += `<h4 style="margin-left:1em">${subcat}</h4>`;
            }
            html += "<ul>";
            grouped[cat][subcat].forEach(m => {
                const methodName = m["Method list"];
                const methodSlug = slugify(methodName);
                const categoryFolder = CATEGORY_FOLDER_MAP[cat] || slugify(cat);
                const subcatFolder = SUBCAT_FOLDER_MAP[subcat] || slugify(subcat);

                let url;
                if (subcat !== "__no_subcat__") {
                    url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/${methodSlug}/`;
                } else {
                    url = `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;
                }

                html += `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${methodName}</a></li>`;
              });
          html += "</ul>";
      });
      html += "</div>";
  });
  html += "</div>";
  div.innerHTML = html;
}

  // 7. Attach event listeners
  criteria.forEach(criterion => {
    document.getElementById("filter-" + criterion.key).addEventListener("change", filterMethods);
  });

  // 8. Initial display
  displayMethods(methodData);
  console.log("Initial methods displayed");
// });
});

// Helper for slugifying (if needed)
function slugify(text) {
  if (!text) return '';
  return text
    .toString()
    .trim()
    .toLowerCase()
    .replace(/\//g, "-")         // replace "/" with "-"
    .replace(/&/g, "and")        // replace "&" with "and"
    .replace(/[^\w\- ]/g, "")    // remove all non-word, non-hyphen, non-space chars
    .replace(/\s+/g, "-");       // replace spaces with "-"
}