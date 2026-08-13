# Allow disable-model-invocation in skill frontmatter

Status: Accepted

## Context

User-invoked skills in the Matt Pocock / Claude Skills model set `disable-model-invocation: true` so the description does not stay in agent context load. Our `maintenance/validate_skill.mjs` rejected that key, so deliberate flows such as `implement-with-subagents` could not be marked user-invoked without failing release validation.

## Decision

Add `disable-model-invocation` to the validator allowlist. Skills that are explicit user flows may set it to `true`. When set, keep `description` as a short human-facing summary (still required by the Agents Skills shape and this validator), not a model-routing trigger list.

## Consequences

- `implement-with-subagents` uses the flag.
- Other pack skills stay model-invoked unless they opt in.
- Hosts that ignore the flag still see the description; hosts that honor it drop that always-on context load.
