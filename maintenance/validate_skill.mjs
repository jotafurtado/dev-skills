#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const MAX_SKILL_NAME_LENGTH = 64;
const ALLOWED_PROPERTIES = new Set([
  "name",
  "description",
  "license",
  "allowed-tools",
  "metadata",
  "disable-model-invocation",
]);

function fail(message) {
  console.error(message);
  process.exitCode = 1;
}

function parseScalar(value) {
  const trimmed = value.trim();

  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }

  return trimmed;
}

function parseFrontmatter(frontmatter) {
  const fields = new Map();

  for (const line of frontmatter.split("\n")) {
    if (!line.trim() || line.startsWith("#")) {
      continue;
    }

    if (/^\s/.test(line)) {
      continue;
    }

    const match = line.match(/^([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?$/);
    if (!match) {
      throw new Error(`Invalid top-level frontmatter line: ${line}`);
    }

    const [, key, value = ""] = match;
    fields.set(key, parseScalar(value));
  }

  return fields;
}

function validate(fields) {
  const unexpected = [...fields.keys()].filter((key) => !ALLOWED_PROPERTIES.has(key));
  if (unexpected.length) {
    return `Unexpected key(s) in SKILL.md frontmatter: ${unexpected.sort().join(", ")}. Allowed properties are: ${[...ALLOWED_PROPERTIES].sort().join(", ")}`;
  }

  for (const required of ["name", "description"]) {
    if (!fields.has(required)) {
      return `Missing '${required}' in frontmatter`;
    }
  }

  const name = fields.get("name").trim();
  if (name && !/^[a-z0-9-]+$/.test(name)) {
    return `Name '${name}' should be hyphen-case (lowercase letters, digits, and hyphens only)`;
  }
  if (name.startsWith("-") || name.endsWith("-") || name.includes("--")) {
    return `Name '${name}' cannot start/end with hyphen or contain consecutive hyphens`;
  }
  if (name.length > MAX_SKILL_NAME_LENGTH) {
    return `Name is too long (${name.length} characters). Maximum is ${MAX_SKILL_NAME_LENGTH} characters.`;
  }

  const description = fields.get("description").trim();
  if (description.includes("<") || description.includes(">")) {
    return "Description cannot contain angle brackets (< or >)";
  }
  if (description.length > 1024) {
    return `Description is too long (${description.length} characters). Maximum is 1024 characters.`;
  }

  return null;
}

async function main() {
  const [skillDirectory] = process.argv.slice(2);
  if (!skillDirectory || process.argv.length !== 3) {
    fail("Usage: node validate_skill.mjs <skill_directory>");
    return;
  }

  let content;
  try {
    content = await readFile(resolve(skillDirectory, "SKILL.md"), "utf8");
  } catch (error) {
    fail(error.code === "ENOENT" ? "SKILL.md not found" : error.message);
    return;
  }

  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    fail(content.startsWith("---") ? "Invalid frontmatter format" : "No YAML frontmatter found");
    return;
  }

  try {
    const error = validate(parseFrontmatter(match[1]));
    if (error) {
      fail(error);
      return;
    }
  } catch (error) {
    fail(`Invalid YAML in frontmatter: ${error.message}`);
    return;
  }

  console.log("Skill is valid!");
}

await main();
