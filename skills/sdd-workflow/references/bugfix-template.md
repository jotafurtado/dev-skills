# Bugfix Analysis Template

Use for `bugfix.md`. The artifact describes the defect and the behavior contract
for its correction before a technical design is selected.

## Structure

```markdown
# Bugfix: [Spec title]

## 1. Summary

[User/system impact and why the issue matters.]

## 2. Reproduction

- **Environment/version:** [Relevant versions and configuration.]
- **Preconditions:** [Required state.]
- **Steps:**
  1. [Step.]
  2. [Step.]
- **Observed result:** [Concrete result, error, log, or state.]
- **Reproduction reliability:** [Always/intermittent/unknown, with evidence.]

## 3. Behavior contract

### Current defective behavior

- **BUG-CURRENT-001:** **WHEN** [trigger], **THEN THE SYSTEM**
  [incorrect observable behavior].

### Expected behavior

- **BUG-AC-001:** **WHEN** [trigger], **THE SYSTEM SHALL** [correct result].

### Behavior that must remain unchanged

- **REG-001:** **WHEN** [unaffected condition], **THE SYSTEM SHALL CONTINUE TO**
  [existing observable behavior].

## 4. Evidence and root cause

- **Evidence:** [Logs, failing tests, traces, code paths, or reproduction.]
- **Root-cause status:** [confirmed | suspected | unknown]
- **Root cause:** [Explanation or hypotheses clearly labeled.]
- **Affected boundary:** [Components, users, data, integrations.]

## 5. Constraints and risks

- **Constraint:** [Compatibility, security, data, rollout, or operational limit.]
- **Risk:** [Regression or migration risk.]

## 6. Regression strategy

- [Test or observation that reproduces the defect before the fix.]
- [Tests for BUG-AC IDs.]
- [Tests for REG IDs and adjacent behavior.]

## 7. Open questions

- **Q-001:** [Question and blocking/non-blocking status.]
```

## Authoring rules

- Do not claim a root cause without runtime, test, log, trace, or code-path
  evidence. Use `suspected` or `unknown` while investigation continues.
- During design, inspect the affected code paths and update the root-cause status
  when evidence confirms or disproves the hypothesis.
- Keep `BUG-CURRENT-*`, `BUG-AC-*`, and `REG-*` IDs stable.
- Expected and unchanged behavior must be observable and testable.
- Capture the smallest affected boundary; do not turn the bugfix into an
  unrelated refactor.
- Resolve blocking questions and approve `bugfix.md` before generating the fix
  design.
