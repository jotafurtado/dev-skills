#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { parseDocument } from "yaml";

const MAX_SKILL_NAME_LENGTH = 64;
const MAX_DESCRIPTION_LENGTH = 1024;
const MAX_COMPATIBILITY_LENGTH = 500;

// Agent Skills specification fields. `disable-model-invocation` is a client
// extension (Cursor), not a core spec field; it is allowed so published
// skills remain valid on hosts that honor it.
const SPEC_PROPERTIES = new Set([
  "name",
  "description",
  "license",
  "compatibility",
  "metadata",
  "allowed-tools",
]);
const CLIENT_EXTENSIONS = new Set(["disable-model-invocation"]);
const ALLOWED_PROPERTIES = new Set([...SPEC_PROPERTIES, ...CLIENT_EXTENSIONS]);

export function fail(message) {
  console.error(message);
  return message;
}

export function parseFrontmatter(frontmatter) {
  const document = parseDocument(frontmatter);
  if (document.errors.length) {
    throw new Error(document.errors.map((error) => error.message).join("; "));
  }
  const fields = document.toJS({ mapAsMap: true });
  if (!(fields instanceof Map)) {
    throw new Error("Frontmatter must be a YAML mapping");
  }
  return fields;
}

export function validate(fields, directoryName) {
  const unexpected = [...fields.keys()].filter((key) => !ALLOWED_PROPERTIES.has(key));
  if (unexpected.length) {
    return `Unexpected key(s) in SKILL.md frontmatter: ${unexpected.sort().join(", ")}. Allowed properties are: ${[...ALLOWED_PROPERTIES].sort().join(", ")}`;
  }

  for (const required of ["name", "description"]) {
    if (!fields.has(required)) {
      return `Missing '${required}' in frontmatter`;
    }
  }

  for (const key of ["name", "description", "license", "compatibility", "allowed-tools"]) {
    if (fields.has(key) && typeof fields.get(key) !== "string") {
      return `'${key}' must be a string`;
    }
  }
  if (fields.has("metadata")) {
    const metadata = fields.get("metadata");
    if (!(metadata instanceof Map)) {
      return "'metadata' must be a map of string keys to string values";
    }
    for (const [key, value] of metadata) {
      if (typeof key !== "string" || typeof value !== "string") {
        return "'metadata' must be a map of string keys to string values";
      }
    }
  }
  if (fields.has("disable-model-invocation") && typeof fields.get("disable-model-invocation") !== "boolean") {
    return "'disable-model-invocation' must be a boolean client extension";
  }

  const name = fields.get("name").trim();
  if (!name) {
    return "Name cannot be empty";
  }
  if (!/^[a-z0-9-]+$/.test(name)) {
    return `Name '${name}' should be hyphen-case (lowercase letters, digits, and hyphens only)`;
  }
  if (name.startsWith("-") || name.endsWith("-") || name.includes("--")) {
    return `Name '${name}' cannot start/end with hyphen or contain consecutive hyphens`;
  }
  if (name.length > MAX_SKILL_NAME_LENGTH) {
    return `Name is too long (${name.length} characters). Maximum is ${MAX_SKILL_NAME_LENGTH} characters.`;
  }
  if (directoryName && name !== directoryName) {
    return `Name '${name}' must match the parent directory name '${directoryName}'`;
  }

  const description = fields.get("description").trim();
  if (!description) {
    return "Description cannot be empty";
  }
  if (description.length > MAX_DESCRIPTION_LENGTH) {
    return `Description is too long (${description.length} characters). Maximum is ${MAX_DESCRIPTION_LENGTH} characters.`;
  }

  if (fields.has("compatibility")) {
    const compatibility = fields.get("compatibility").trim();
    if (!compatibility) {
      return "Compatibility cannot be empty when provided";
    }
    if (compatibility.length > MAX_COMPATIBILITY_LENGTH) {
      return `Compatibility is too long (${compatibility.length} characters). Maximum is ${MAX_COMPATIBILITY_LENGTH} characters.`;
    }
  }

  return null;
}

export async function validateSkillDirectory(skillDirectory) {
  const resolved = resolve(skillDirectory);
  const directoryName = basename(resolved);
  let content;
  try {
    content = await readFile(resolve(resolved, "SKILL.md"), "utf8");
  } catch (error) {
    return error.code === "ENOENT" ? "SKILL.md not found" : error.message;
  }

  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) {
    return content.startsWith("---") ? "Invalid frontmatter format" : "No YAML frontmatter found";
  }

  try {
    return validate(parseFrontmatter(match[1]), directoryName);
  } catch (error) {
    return `Invalid YAML in frontmatter: ${error.message}`;
  }
}

async function main() {
  const [skillDirectory] = process.argv.slice(2);
  if (!skillDirectory || process.argv.length !== 3) {
    console.error("Usage: node validate_skill.mjs <skill_directory>");
    console.error(
      "Validates Agent Skills frontmatter (name, description, license, compatibility, metadata, allowed-tools). Client extension disable-model-invocation is allowed.",
    );
    process.exitCode = 1;
    return;
  }

  const error = await validateSkillDirectory(skillDirectory);
  if (error) {
    console.error(error);
    process.exitCode = 1;
    return;
  }

  console.log("Skill is valid!");
}

const invokedDirectly = import.meta.url === `file://${process.argv[1]}`;
if (invokedDirectly) {
  await main();
}
