import { criteria, criteriaOptionLabelMap, compositeOptions, ordinalCriteriaOrder, hideCompositeConstituents, multipleAllowedCriteria } from './criteria.js';
console.log("Filter.js loaded!");

const siteBaseurl = JSON.parse(document.getElementById('site-baseurl').textContent);
const objectiveCriteriaMap = JSON.parse(document.getElementById('objective-criteria-map').textContent);
const choicesInstances = {};


function updateCriteriaStatus() {
  let anyCount = 0;
  let unsureCount = 0;
  let assessedCount = 0;

  // Determine which criteria are currently used
  const objectiveSelect = document.getElementById("filter-Objective");
  let usedCriteriaKeys;
  if (objectiveSelect && objectiveSelect.value && objectiveCriteriaMap[objectiveSelect.value]) {
    usedCriteriaKeys = objectiveCriteriaMap[objectiveSelect.value].concat(["Objective"]);
  } else {
    // If no objective selected, use all criteria
    usedCriteriaKeys = criteria.map(c => c.key);
  }

  criteria.forEach(criterion => {
    if (!usedCriteriaKeys.includes(criterion.key)) return; // skip unused criteria
    const select = document.getElementById("filter-" + criterion.key);
    if (!select) return;
    if (select.value === "") {
      anyCount++;
    } else if (select.value === "__unsure__") {
      unsureCount++;
    } else {
      assessedCount++;
    }
  });

  const statusDiv = document.getElementById("criteria-status");
  if (statusDiv) {
    statusDiv.classList.remove("green", "intermediary");
    statusDiv.innerHTML =
      `<span style="margin-right:1em;">Any: <strong>${anyCount}</strong></span>` +
      `<span style="margin-right:1em;">Unsure: <strong>${unsureCount}</strong></span>` +
      `<span>Assessed: <strong>${assessedCount}</strong></span>`;
    if (anyCount === 0 && unsureCount === 0) {
      statusDiv.classList.add("green");
    } else if (anyCount === 0 && unsureCount > 0) {
      statusDiv.classList.add("intermediary");
    }
  }
}


function getUsedCriteriaKeys() {
  const objectiveSelect = document.getElementById("filter-Objective");
  if (objectiveSelect && objectiveSelect.value && objectiveCriteriaMap[objectiveSelect.value]) {
    return objectiveCriteriaMap[objectiveSelect.value].concat(["Objective"]);
  } else {
    return criteria.map(c => c.key);
  }
}



document.addEventListener('DOMContentLoaded', function() {

  // Only run if method-data and criteria-filters exist
  if (!document.getElementById('method-data') || !document.getElementById('criteria-filters')) {
    console.log("Required elements not found, script not running.");
    return;
  }
  console.log("Script started");

  // 1. Load method data
  const methodData = JSON.parse(document.getElementById('method-data').textContent);

  // 2. Define the criteria you want dropdowns for (column names from your TSV)
  //  Replaced by an import
  

  // 3. Get unique options for each criterion
  const optionsByCriterion = {};
  criteria.forEach(criterion => {
    const opts = new Set();
    methodData.forEach(m => {
      if (m[criterion.key]) {
        m[criterion.key].split(",").forEach(val => {
          const trimmed = val.trim();
          if (trimmed !== "Don't know" && trimmed !== "Inapplicable") {
            opts.add(trimmed);
          }
        });
      }
    });

    // Add composite options if defined
    if (compositeOptions[criterion.key]) {
      Object.keys(compositeOptions[criterion.key]).forEach(opt => opts.add(opt));
    }

    let optsArr = Array.from(opts);

    // Remove "Any" and "Unsure" for custom sorting
    const anyIdx = optsArr.indexOf("");
    const unsureIdx = optsArr.indexOf("__unsure__");
    let anyOpt = null, unsureOpt = null;
    if (anyIdx !== -1) anyOpt = optsArr.splice(anyIdx, 1)[0];
    if (unsureIdx !== -1) unsureOpt = optsArr.splice(optsArr.indexOf("__unsure__"), 1)[0];

    // Remove individual options that are included in a composite ONLY if flagged in hideCompositeConstituents
    if (compositeOptions[criterion.key] && hideCompositeConstituents[criterion.key]) {
      const compositeIncluded = new Set();
      Object.entries(compositeOptions[criterion.key]).forEach(([compOpt, arr]) => {
        if (hideCompositeConstituents[criterion.key][compOpt]) {
          arr.forEach(opt => compositeIncluded.add(opt));
        }
      });
      optsArr = optsArr.filter(opt => !compositeIncluded.has(opt));
    }

    // Custom sort for ordinal criteria
    if (ordinalCriteriaOrder[criterion.key]) {
      const order = ordinalCriteriaOrder[criterion.key];
      optsArr.sort((a, b) => order.indexOf(a) - order.indexOf(b));
    } else {
      optsArr.sort(); // default alphabetical for non-ordinal
    }

    // Re-add "Any" at the start and "Unsure" at the end
    if (anyOpt !== null) optsArr.unshift(anyOpt);
    if (unsureOpt !== null) optsArr.push(unsureOpt);

    optionsByCriterion[criterion.key] = optsArr;
  });


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

  // Move "Assumptions" to the end of categoryOrder
  const idx = categoryOrder.indexOf("Assumptions");
  if (idx !== -1) {
    categoryOrder.splice(idx, 1); // Remove "Assumptions"
    categoryOrder.push("Assumptions"); // Add it at the end
  }

  categoryOrder.forEach(category => {
    criteria.filter(c => c.category === category).forEach(criterion => {
      // Insert category heading and collapsible container if this is a new category
      if (criterion.category !== lastCategory && criterion.category !== "__standalone__") {
        const catHeading = document.createElement("div");
        catHeading.style.marginTop = "1.5em";
        catHeading.style.marginLeft = "0em";
        catHeading.style.fontSize = "1.3em";
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
        catHelp.style.fontSize = "0.75em";
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

      const label = document.createElement("label");
      label.style.display = "inline-block";
      label.style.whiteSpace = "nowrap";
      if (criterion.key === "Objective") {
        label.classList.add("objective-highlight");
      }
      label.appendChild(document.createTextNode(criterion.label + ": "));

      // Create a container for (?) and select, and indent it
      const rightContainer = document.createElement("span");
      rightContainer.className = "criteria-select-container";

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
      helpLink.style.position = "absolute";
      helpLink.style.left = "220px"; // Adjust this value to align all (?) marks vertically
      helpLink.style.marginLeft = "0"; // Remove any previous margin-left
      helpLink.style.marginRight = "6px";
      helpLink.style.fontSize = "0.75em";
      // helpLink.style.color = "#a89cc8";
      helpLink.innerHTML = "(?)";

      label.style.position = "relative";
      label.style.minWidth = "220px";

      const select = document.createElement("select");
      select.id = "filter-" + criterion.key;


      // Allow multiple selection if in multipleAllowedCriteria
      if (multipleAllowedCriteria.includes(criterion.key)) {
        select.multiple = true;
        select.size = Math.min(optionsByCriterion[criterion.key].length, 6); // or any preferred size
        select.value = ""; // Select "Any" by default
      }


      if (criterion.key === "Objective") {
        select.classList.add("objective-highlight");
      }
      let optionsHtml = `<option value="" style="font-style:italic;">Any</option>` +
      optionsByCriterion[criterion.key].map(opt => {
        const displayLabel = criteriaOptionLabelMap[criterion.key] && criteriaOptionLabelMap[criterion.key][opt]
          ? criteriaOptionLabelMap[criterion.key][opt]
          : opt;
        return `<option value="${opt}">${displayLabel}</option>`;
      }).join("");
      if (criterion.key !== "Objective") {
        optionsHtml += `<option value="__unsure__" style="font-style:italic;">Unsure</option>`;
      }
      select.innerHTML = optionsHtml;

      // When a selection is made, expand the next category
      select.addEventListener("change", function() {
      // Find all VISIBLE criteria in this category
      const currentCategory = criterion.category;
      // Only consider divs that are visible and in this category
      if (!categoryContainers[currentCategory]) return;
      const visibleCriteriaInCategory = Array.from(categoryContainers[currentCategory].children)
        .filter(child => child.style.display !== "none");
      // Check if this is the last visible criterion in the category
      if (
        visibleCriteriaInCategory.length > 0 &&
    visibleCriteriaInCategory[visibleCriteriaInCategory.length - 1] === rowDiv
      ) {
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
          }
        }
      }
    });

      label.appendChild(helpLink);
      rightContainer.appendChild(select);

      // Choices.js initialization for multi-select
      if (multipleAllowedCriteria.includes(criterion.key)) {
        const choicesInstance = new Choices(select, {
          removeItemButton: true,
          shouldSort: false,
          position: 'bottom',
          placeholder: true,
          placeholderValue: 'Select options',
          searchEnabled: false
        });
        choicesInstances[criterion.key] = choicesInstance;
        // Ensure "Any" is visually selected on load
        choicesInstance.setChoiceByValue('');

        let prevSelectedValues = Array.from(select.selectedOptions).map(opt => opt.value);
        select.addEventListener('change', function(e) {
          const anyOption = select.querySelector('option[value=""]');
          const selectedValues = Array.from(select.selectedOptions).map(opt => opt.value);

          // Only remove "Any" if it was previously selected and now another option is selected
          if (
            anyOption &&
            prevSelectedValues.includes("") && // "Any" was previously selected
            selectedValues.includes("") &&
            selectedValues.length > 1
          ) {
            setTimeout(() => {
              anyOption.selected = false;
              choicesInstances[criterion.key].removeActiveItemsByValue('');
              // Reselect all other selected values to ensure Choices.js UI is correct
              selectedValues.filter(v => v !== "").forEach(val => {
                choicesInstances[criterion.key].setChoiceByValue(val);
              });
            }, 0);
          }

          // If nothing is selected, select "Any" by default
          if (selectedValues.length === 0 && anyOption) {
            setTimeout(() => {
              anyOption.selected = true;
              choicesInstances[criterion.key].setChoiceByValue('');
            }, 0);
          }

          // Update prevSelectedValues for next change
          prevSelectedValues = selectedValues;
        });
    }

      // Create a container for tags (right-aligned)
    const tagContainer = document.createElement("span");
    tagContainer.className = "criteria-tag-container";

    // Ordinal tag
    if (ordinalCriteriaOrder[criterion.key]) {
      const ordinalTag = document.createElement("span");
      ordinalTag.className = "ordinal-tag";
      ordinalTag.title = "Options are ordered: selecting a value includes all higher options.";
      ordinalTag.textContent = "Ordinal";
      tagContainer.appendChild(ordinalTag);
    }

    // Multiple allowed tag
    if (multipleAllowedCriteria.includes(criterion.key)) {
      const multiTag = document.createElement("span");
      multiTag.className = "multiple-tag";
      multiTag.title = "You can select multiple options (click to select, click again to deselect).";
      multiTag.textContent = "Multiple";
      tagContainer.appendChild(multiTag);
    }

    const rowDiv = document.createElement("div");
    rowDiv.className = "criteria-row";
    rowDiv.appendChild(label);
    rowDiv.appendChild(rightContainer);
    rowDiv.appendChild(tagContainer);
    rowDiv.dataset.criterionKey = criterion.key;

      if (criterion.category === "__standalone__") {
        filtersDiv.appendChild(rowDiv);
      } else {
        categoryContainers[criterion.category].appendChild(rowDiv);
      }
    });
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

  // Show only criteria relevant to the selected objective
  const relevant = objectiveCriteriaMap[selectedObjective] || [];
  document.querySelectorAll('[data-criterion-key]').forEach(div => {
    if (relevant.includes(div.dataset.criterionKey) || div.dataset.criterionKey === "Objective") {
      div.style.display = "";
    } else {
      div.style.display = "none";
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

  // Finally, re-filter methods based on new visibility
  filterMethods();
  updateCriteriaStatus();

  });



  // 5. Filter and display methods
  function filterMethods() {
    let filtered = methodData;
    const usedCriteriaKeys = getUsedCriteriaKeys();
    criteria.forEach(criterion => {
      if (!usedCriteriaKeys.includes(criterion.key)) return; // skip unused criteria
      const val = document.getElementById("filter-" + criterion.key).value;
      if (val && val !== "__unsure__") {
        // 1. Composite option logic
        if (
          compositeOptions[criterion.key] &&
          compositeOptions[criterion.key][val]
        ) {
          const included = compositeOptions[criterion.key][val];
          filtered = filtered.filter(m => {
            if (!m[criterion.key]) return false;
            const methodVals = m[criterion.key].split(",").map(x => x.trim());
            // Accept if any of the method's values is in the composite set
            return (
              methodVals.some(opt => included.includes(opt)) ||
              methodVals.includes("Don't know") ||
              methodVals.includes("Inapplicable")
            );
          });
          return; // skip to next criterion
        }

        // 2. Ordinal logic
        if (
          ordinalCriteriaOrder[criterion.key] &&
          ordinalCriteriaOrder[criterion.key].includes(val)
        ) {
          const order = ordinalCriteriaOrder[criterion.key];
          const selectedIdx = order.indexOf(val);
          filtered = filtered.filter(m => {
            if (!m[criterion.key]) return false;
            const methodVals = m[criterion.key].split(",").map(x => x.trim());
            // Accept if any of the method's values is at or above the selected level
            return (
              methodVals.some(opt => order.indexOf(opt) >= selectedIdx) ||
              methodVals.includes("Don't know") ||
              methodVals.includes("Inapplicable")
            );
          });
          return; // skip to next criterion
        }

        // 3. Default logic (non-composite, non-ordinal)
        filtered = filtered.filter(m => {
          if (!m[criterion.key]) return false;
          const methodVals = m[criterion.key].split(",").map(x => x.trim());
          return (
            methodVals.includes(val) ||
            methodVals.includes("Don't know") ||
            methodVals.includes("Inapplicable")
          );
        });
      }
      // If val is "" (Any) or "__unsure__", do not filter (i.e., skip filtering for this criterion)
    });
    displayMethods(filtered);
  }


  
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

      // Filter out methods with missing "Method"
      const validMethods = methods.filter(m => m["Method"]);
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
          // 1. Display methods with no subcategory first
          if (grouped[cat]["__no_subcat__"]) {
              html += "<ul>";
              grouped[cat]["__no_subcat__"].forEach(m => {
                  const methodName = m["Method"];
                  const methodSlug = slugify(methodName);
                  const categoryFolder = CATEGORY_FOLDER_MAP[cat] || slugify(cat);
                  
                  // No subcategory for these methods
                  const url = `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;

                  html += `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${methodName}</a></li>`;
              });
              html += "</ul>";
          }
          
          // 2. Then display all subcategories
          Object.keys(grouped[cat]).forEach(subcat => {
              if (subcat === "__no_subcat__") return;
              html += `<h4 style="margin-left:1em">${subcat}</h4>`;
              html += "<ul>";
              grouped[cat][subcat].forEach(m => {
                  const methodName = m["Method"];
                  const methodSlug = slugify(methodName);
                  const categoryFolder = CATEGORY_FOLDER_MAP[cat] || slugify(cat);
                  const subcatFolder = SUBCAT_FOLDER_MAP[subcat] || slugify(subcat);

                  let url;
                  if (methodName === subcat) {
                      // Link to the subcategory folder (index.md)
                      url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/`;
                  } else if (subcat !== "__no_subcat__") {
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
  document.getElementById("filter-" + criterion.key).addEventListener("change", function() {
      filterMethods();
      updateCriteriaStatus();
    });
  });

  // 8. Initial display
  displayMethods(methodData);
  console.log("Initial methods displayed");
  updateCriteriaStatus();
  // });

  // Add this at the end, after your other event listeners:
    const resetBtn = document.getElementById("reset-filters-btn");
    if (resetBtn) {
      resetBtn.addEventListener("click", function(e) {
        e.preventDefault();
        criteria.forEach(criterion => {
          const select = document.getElementById("filter-" + criterion.key);
          if (!select) return;
          if (multipleAllowedCriteria.includes(criterion.key) && choicesInstances[criterion.key]) {
            choicesInstances[criterion.key].removeActiveItems();
            choicesInstances[criterion.key].setChoiceByValue('');
          } else {
            select.value = "";
          }
        });
        filterMethods();
        updateCriteriaStatus();

        // Collapse all criteria categories
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

      });
    }

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