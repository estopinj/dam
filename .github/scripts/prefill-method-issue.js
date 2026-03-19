"use strict";

const fs = require("fs");
const path = require("path");

const NO_RESPONSE = "_No response_";
const TARGET_METHOD_LABEL = "Target method name";

const ISSUE_LABELS = {
  author: "Page’s Author & Date",
  description: "Description & principle",
  variant: "Major variants",
  online_resources: "Further online resources",
  method_references: "Method",
  rs_data: "With RS data in Ecology / Biodiversity",
  rs_data_field: "Without RS data (Ecology domain)",
  python_pkg: "Python",
  r_pkg: "R",
  code_list: "Code Cells",
};

function normalizeText(value) {
  return (value || "")
    .replace(/\r\n/g, "\n")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
    .toLowerCase();
}

function normalizeTitle(value) {
  return (value || "")
    .replace(/^\[|\]$/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function slugify(value) {
  return normalizeTitle(value)
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function isMeaningful(value) {
  const normalized = normalizeText(value);
  if (!normalized || normalized === normalizeText(NO_RESPONSE)) {
    return false;
  }

  const placeholders = [
    "method description",
    "this method is used to",
    "a clear, technical yet accessible explanation of the method, its core principle(s).",
    "if the method has variants that seem important, either already widespread or promising and well documented.",
    "references to useful online resources to get started",
    "one or a few key academic references that introduce or formalize the method.",
    "link toward the package documentation or repository.",
    "code examples to run the method",
  ];

  return !placeholders.some((p) => normalized.includes(p));
}

function cleanExtractedBlock(value) {
  if (!value) {
    return "";
  }

  const lines = value
    .replace(/\r\n/g, "\n")
    .split("\n")
    .filter((line) => !/^\{:\s*\..*\}\s*$/.test(line.trim()))
    .filter((line) => !/^optional\s*$/i.test(line.trim()));

  const cleaned = lines.join("\n").trim();
  return isMeaningful(cleaned) ? cleaned : "";
}

function extractFrontmatter(text) {
  const match = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
  const frontmatter = {};
  if (!match) {
    return frontmatter;
  }

  const body = match[1];
  for (const line of body.split("\n")) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) {
      continue;
    }
    frontmatter[m[1].trim().toLowerCase()] = m[2].trim().replace(/^"|"$/g, "");
  }

  return frontmatter;
}

function extractBetween(text, startRegex, endRegexList) {
  const startMatch = startRegex.exec(text);
  if (!startMatch) {
    return "";
  }

  const start = startMatch.index + startMatch[0].length;
  let end = text.length;

  for (const endRegex of endRegexList) {
    endRegex.lastIndex = 0;
    const subText = text.slice(start);
    const endMatch = endRegex.exec(subText);
    if (endMatch) {
      end = Math.min(end, start + endMatch.index);
    }
  }

  return cleanExtractedBlock(text.slice(start, end));
}

function extractMethodFields(markdown) {
  const frontmatter = extractFrontmatter(markdown);

  return {
    author: isMeaningful(frontmatter.author || "") ? frontmatter.author : "",
    description: extractBetween(markdown, /^##\s+Description\s*&\s*principle\s*\n/m, [/^###\s+Major\s+variants\s*\n/m]),
    variant: extractBetween(markdown, /^###\s+Major\s+variants\s*\n/m, [/^###\s+Further\s+online\s+resources\s*\n/m]),
    online_resources: extractBetween(markdown, /^###\s+Further\s+online\s+resources\s*\n/m, [/^##\s+Reference\s+articles\s*\n/m]),
    references: "",
    method_references: extractBetween(markdown, /^###\s+Method\s*\n/m, [/^###\s+Research\s+applications\s*\n/m]),
    rs_data: extractBetween(markdown, /^####\s+With\s+RS\s+data\s+in\s+Ecology\s*\/\s*Biodiversity\s*\n/m, [/^####\s+Without\s+RS\s+data\s+\(Ecology\s+domain\)\s*\n/m]),
    rs_data_field: extractBetween(markdown, /^####\s+Without\s+RS\s+data\s+\(Ecology\s+domain\)\s*\n/m, [/^##\s+Packages\s*\n/m]),
    python_pkg: extractBetween(markdown, /^####\s+Python\s*\n/m, [/^####\s+R\s*\n/m]),
    r_pkg: extractBetween(markdown, /^####\s+R\s*\n/m, [/^###\s+Code\s+Cells\s*\n/m]),
    code_list: extractBetween(markdown, /^###\s+Code\s+Cells\s*\n/m, [/^##\s+Assessment\s+table\s*\n/m]),
  };
}

function getMarkdownFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...getMarkdownFiles(fullPath));
      continue;
    }

    if (entry.isFile() && entry.name.endsWith(".md") && entry.name !== "index.md") {
      files.push(fullPath);
    }
  }

  return files;
}

function findMatchingMethodFile(methodsRoot, issueTitle) {
  const files = getMarkdownFiles(methodsRoot);
  const normalizedTitle = normalizeTitle(issueTitle);
  const slug = slugify(issueTitle);

  const scored = [];
  for (const filePath of files) {
    const content = fs.readFileSync(filePath, "utf8");
    const frontmatter = extractFrontmatter(content);
    const fileName = path.basename(filePath, ".md");

    let score = 0;
    if (normalizeText(frontmatter.title || "") === normalizeText(normalizedTitle)) {
      score = Math.max(score, 100);
    }
    if (slugify(frontmatter.title || "") === slug) {
      score = Math.max(score, 90);
    }
    if (fileName.toLowerCase() === slug || fileName.toLowerCase() === normalizedTitle.toLowerCase()) {
      score = Math.max(score, 80);
    }

    if (score > 0) {
      scored.push({ filePath, content, score });
    }
  }

  scored.sort((a, b) => b.score - a.score || a.filePath.localeCompare(b.filePath));
  return scored.length ? scored[0] : null;
}

function readIssueSection(body, label) {
  const regex = new RegExp(
    `(^###\\s+${escapeRegExp(label)}\\s*\\n)([\\s\\S]*?)(?=\\n#+\\s+|$)`,
    "m"
  );
  const match = body.match(regex);
  if (!match) {
    return "";
  }
  return match[2].trim();
}

function extractTargetMethodName(issueBody) {
  const fromBody = readIssueSection(issueBody, TARGET_METHOD_LABEL);
  if (isMeaningful(fromBody)) {
    return fromBody.trim();
  }

  return "";
}

function replaceIssueSection(body, label, nextValue) {
  const regex = new RegExp(
    `(^###\\s+${escapeRegExp(label)}\\s*\\n)([\\s\\S]*?)(?=\\n#+\\s+|$)`,
    "m"
  );

  if (!regex.test(body)) {
    return body;
  }

  return body.replace(regex, (_full, header) => `${header}${nextValue || NO_RESPONSE}\n`);
}

function mergeField(existingValue, submittedValue) {
  const existing = isMeaningful(existingValue) ? existingValue.trim() : "";
  const submitted = isMeaningful(submittedValue) ? submittedValue.trim() : "";

  if (existing && submitted) {
    if (normalizeText(existing) === normalizeText(submitted)) {
      return existing;
    }
    return `${existing}\n\n${submitted}`;
  }

  if (existing) {
    return existing;
  }
  if (submitted) {
    return submitted;
  }
  return "";
}

function buildPrefilledBody({ issueTitle, issueBody, methodsRoot }) {
  if (!issueBody.includes(`### ${ISSUE_LABELS.description}`)) {
    return {
      changed: false,
      updatedBody: issueBody,
      reason: "not_issue_form",
      usedExistingFields: [],
      targetMethodName: "",
    };
  }

  const targetMethodName = extractTargetMethodName(issueBody);
  if (!targetMethodName) {
    return {
      changed: false,
      updatedBody: issueBody,
      reason: "missing_target_method",
      usedExistingFields: [],
      targetMethodName: "",
    };
  }

  const match = findMatchingMethodFile(methodsRoot, targetMethodName);
  if (!match) {
    return {
      changed: false,
      updatedBody: issueBody,
      reason: "no_match",
      usedExistingFields: [],
      targetMethodName,
    };
  }

  const existingFields = extractMethodFields(match.content);
  let updatedBody = issueBody;
  let changed = false;
  const usedExistingFields = [];
  const suggestedFields = [];

  for (const [fieldKey, label] of Object.entries(ISSUE_LABELS)) {
    const before = readIssueSection(updatedBody, label);
    const submitted = before;
    const existing = isMeaningful(existingFields[fieldKey]) ? existingFields[fieldKey].trim() : "";
    const merged = mergeField(existing, submitted);

    const candidateBody = replaceIssueSection(updatedBody, label, merged);
    const after = readIssueSection(candidateBody, label);

    if (normalizeText(before) !== normalizeText(after)) {
      changed = true;
      updatedBody = candidateBody;
    }

    if (existing && merged && normalizeText(merged).includes(normalizeText(existing))) {
      usedExistingFields.push(label);
    }
    if (isMeaningful(submitted) && merged && normalizeText(merged).includes(normalizeText(submitted.trim()))) {
      suggestedFields.push(label);
    }
  }

  return {
    changed,
    updatedBody,
    matchedFile: path.relative(process.cwd(), match.filePath).replace(/\\/g, "/"),
    reason: "matched",
    usedExistingFields: [...new Set(usedExistingFields)],
    suggestedFields: [...new Set(suggestedFields)],
    targetMethodName,
  };
}

module.exports = {
  buildPrefilledBody,
};
