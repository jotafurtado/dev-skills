# Release verification evidence

This file records the release comparison and the repeatable checks for version 1.0.0. It does not replace a model's final implementation review; it makes routing, discovery, and evidence expectations testable before publishing.

## Candidate compared with the baseline

The baseline is `laravel-filament-v5` alone. It owns installed-version APIs, implementation, security, and tests. The candidate is `laravel-filament-5-ui-ux`, installed alone for visual work or paired with the baseline for implementation work.

| Prompt surface | Baseline-only boundary | Candidate evidence requirement | Pass condition |
|---|---|---|---|
| Settings form | Can implement after API verification, but does not own visual selection when the visual skill is installed. | Query the reviewed local catalog, compare layout candidates, state responsive treatment. | A visible decision trace names the selected official pattern and evidence. |
| Operational table | Retains table APIs and tests. | Compare reviewed table patterns, filters, actions, density, and actionable empty-state candidates. | The choice is evidence-grounded rather than generic card-first advice. |
| Record detail | Retains entry APIs and tests. | Establish identity/status hierarchy before secondary history, then inspect the routed evidence. | Primary facts remain visible and the trace states responsive handling. |
| Dashboard or panel shell | Retains implementation and configuration APIs. | Use the dashboard or panel-shell reference and preserve the panel theme. | The trace identifies reviewed candidates and avoids invented shell styling. |
| Actions and feedback | Retains action APIs, confirmation, security, and tests. | Compare action grouping, confirmation, overlay, notification, or empty-state candidates. | The selected feedback pattern explains the workflow risk and recovery path. |

The repository checks this contract structurally in `tests/test_laravel_filament_5_ui_ux.py`: visual trigger evals route to the candidate, while implementation/API responsibility remains with the baseline. Human or model forward runs must use the prompts in `evals/evals.json` and score the pass condition in this table; retain the output with the release record when a runtime is available.

## 2026-07-28 forward-run record

Clean paired installations were exercised before the release commit. Codex queried the installed local catalog for `record-detail`, `present-scannable-record-details`, `parallel`, and `wide`; it selected `record-detail-infolist` and returned the reviewed official screenshot/documentation evidence. The resulting trace preserves the required candidate split: visual hierarchy, evidence comparison, responsive presentation, and the visual decision trace stay with this skill; API signatures, implementation, security, and tests go to `laravel-filament-v5`.

Claude Code received the equivalent vendor View prompt from a clean paired installation. Its response put vendor identity and a labelled verification-state badge first, followed by a compact fact grid; it moved history and related detail below the primary scan path, kept a single focused correction action, and assigned Infolist/Schema APIs, action authorization, state guards, and tests to `laravel-filament-v5`. This meets the record-detail comparison pass condition. The Codex and Claude Code prompts were read-only and made no changes to the disposable workspaces.

## Clean-install smoke test

Run the following from the repository root:

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/release_install_smoke.py
```

It creates disposable workspaces and uses `npx skills add --copy --yes` to test separate and paired installs for Codex, Claude Code, and Cursor. Every run verifies discovery, `skills-lock.json`, and the universal `SKILL.md` and `README.md` entry points; it also checks that the installed UI/UX release still identifies the Jota Furtado Dev Skills grouping. The Codex run verifies that `agents/openai.yaml` survived installation. The script removes its own temporary workspaces after the run.

## Release checklist

1. Run the deterministic unit suite and catalog validator.
2. Parse both eval JSON files and run whitespace checks.
3. Run the clean-install smoke test above.
4. Run the forward prompts in `evals/evals.json` with available clean Codex and Claude Code environments, scoring them against the comparison table.
5. Review the authority boundary: candidate owns visual selection; baseline owns APIs, implementation, security, and tests.

When a model runtime is unavailable, record that limitation rather than claiming a forward-run result. The catalog remains usable offline after installation.
