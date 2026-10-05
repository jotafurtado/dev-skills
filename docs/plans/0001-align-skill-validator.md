# 0001 — Align skill validator

Status: Implemented  
Depends on: none  
Unblocks: 0002, 0003, 0004, 0006  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Make `maintenance/validate_skill.mjs` agree with the current Agent Skills
specification, then move operational requirements onto the standard
`compatibility` field.

## Why this phase is first

The current validator accepts invalid skills and rejects valid portable
metadata. Later phases that add evals or change frontmatter cannot trust
`Skill is valid!` until this is fixed.

## Work

1. Replace the frontmatter schema in `maintenance/validate_skill.mjs` with the
   specification:
   - required: non-empty `name` and `description`;
   - `name` is 1–64 chars, `a-z0-9-` only, no leading/trailing/consecutive
     hyphens, and equal to the parent directory name;
   - `description` is 1–1024 chars;
   - optional `license`, `allowed-tools`, `metadata`;
   - optional top-level `compatibility` of 1–500 chars when present;
   - `metadata` remains a string-to-string map.
2. Keep `disable-model-invocation` as an explicit client extension, documented
   in the validator help or a short comment, not as an unmarked core field.
3. Add deterministic fixtures under `tests/` (or `maintenance/fixtures/`) for:
   - valid minimal skill;
   - valid skill with top-level `compatibility`;
   - `name` that does not match the directory;
   - empty `name` or `description`;
   - over-limit `description` and `compatibility`;
   - unknown top-level keys.
4. After the validator accepts the standard field, move runtime requirements
   from `metadata.compatibility` to top-level `compatibility` on the skills
   that declare them, especially `implement-with-subagents`.
5. Run the validator against all six published skills and keep them passing.

## Completion

- Validator fixtures for valid and invalid cases exist and are exercised by
  repository tests.
- A skill whose `name` differs from its directory fails.
- Empty required fields fail.
- Top-level `compatibility` within 500 characters passes.
- All six current skills pass the corrected validator.
- Skills with execution requirements use the standard `compatibility` field.

## Out of scope

Eval runners, description rewrites, and orchestration scenario tests.
