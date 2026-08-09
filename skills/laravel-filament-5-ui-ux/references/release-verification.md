# Release verification evidence

This file records the release comparison and the repeatable checks for version 1.1.0. It does not replace a model's final implementation review; it makes routing, discovery, and evidence expectations testable before publishing.

## Candidate compared with the baseline

The baseline is `laravel-filament-v5` alone. It owns installed-version APIs, implementation, security, and tests. The candidate is `laravel-filament-5-ui-ux`, installed alone for visual work or paired with the baseline for implementation work.

| Prompt surface | Baseline-only boundary | Candidate evidence requirement | Pass condition |
|---|---|---|---|
| Settings form | Can implement after API verification, but does not own visual selection when the visual skill is installed. | Read the compact index or query the reviewed local catalog, compare layout candidates, state responsive treatment. | A visible decision trace names the selected official pattern and evidence. |
| Operational table | Retains table APIs and tests. | Compare reviewed table patterns, filters, actions, density, and actionable empty-state candidates. | The choice is evidence-grounded rather than generic card-first advice. |
| Record detail | Retains entry APIs and tests. | Establish identity/status hierarchy before secondary history, then inspect the routed evidence. | Primary facts remain visible and the trace states responsive handling. |
| Dashboard or panel shell | Retains implementation and configuration APIs. | Use the dashboard or panel-shell reference and preserve the panel theme. | The trace identifies reviewed candidates and avoids invented shell styling. |
| Actions and feedback | Retains action APIs, confirmation, security, and tests. | Compare action grouping, confirmation, overlay, notification, or empty-state candidates. | The selected feedback pattern explains the workflow risk and recovery path. |

The repository checks this contract structurally in `tests/test_laravel_filament_5_ui_ux.py`: visual trigger evals route to the candidate, while implementation/API responsibility remains with the baseline. Human or model forward runs must use the prompts in `evals/evals.json` and score each assertion with a transcript citation in `evals/forward-runs/claude-code.json`.

## Single-agent forward-run evidence

Version 1.1.0 records scored forward-run evidence from one clean paired agent installation: Claude Code. The retained artifact is `evals/forward-runs/claude-code.json`. Each result stores assertions as `{assertion, verdict, evidence}` objects. `review_required` stays true until every assertion is scored `pass` or `fail` with a non-empty transcript citation. A recorded `fail` is valid evidence when the citation shows the gap.

The 1.1.0 scored record reuses the prior clean Claude Code transcripts (15/`recorded`) and migrates them into the per-assertion verdict schema rather than re-invoking the agent. Maintainer review filled every `verdict` and `evidence` citation; `review_required` is therefore `false`. Recorded fails remain on the image-evidence / coverage-gap assertions called out during review.

**Release decision:** re-running the 15 scenarios against skill 1.1.0 (Convergence T033 / FR-017 literal re-execution) was waived because of agent token cost. The migrated and scored `claude-code.json` is the accepted forward-run evidence for this release. A future maintenance release may replace it with a fresh run when cost is acceptable.

Agent command profiles for Codex and Cursor remain in `scripts/run_forward_evals.py` for invocation parity checks in the unit suite. Those profiles are not release evidence for 1.1.0; multi-agent raw dumps are no longer retained.

## Coverage matrix expectations

The comparison table above remains the scoring rubric. When reviewing `claude-code.json`, confirm that each coverage area below either passes with a citation or fails with an explicit citation of the gap:

| Coverage area | What to check in the transcript |
|---|---|
| Forms and schema layouts | Evidence: local reviewed catalog candidates for responsive columns, sections, ordinary wrappers, and fused fields. Authority: `laravel-filament-v5` owns APIs, validation, implementation, and tests. |
| Tables | Evidence: local reviewed catalog table, filter, bulk-action, and empty-state patterns. Authority: `laravel-filament-v5` owns table/action APIs, authorization, implementation, and tests. |
| Responsive records | Evidence: local reviewed Split and Stack mobile variants, including mobile-first table selection of `responsive-identity-centred-table`. Authority: `laravel-filament-v5` owns table-layout APIs, policies, implementation, and tests. |
| Record details | Evidence: local reviewed `record-detail-infolist` variants. Authority: `laravel-filament-v5` owns infolist/View APIs, document authorization, implementation, and tests. |
| Dashboards | Evidence: local reviewed Stats Overview, chart, table-widget, and dashboard-filter patterns. Authority: `laravel-filament-v5` owns widget/filter APIs, scope security, implementation, and tests. |
| Navigation and authentication | Evidence: local reviewed top-navigation, sidebar-navigation, and authentication-surface patterns. Authority: `laravel-filament-v5` owns panel/auth APIs, authorization boundaries, implementation, and tests. |
| Actions and feedback | Evidence: local reviewed action-group, confirmation, overlay, callout, notification, and empty-state patterns. Authority: `laravel-filament-v5` owns action/modal APIs, policy enforcement, implementation, and tests. |
| Offline and no-vision fallback | Evidence: local reviewed catalog interpretation; screenshot inspection disclosed when unavailable. Authority: `laravel-filament-v5` owns installed API verification, authorization, implementation, and tests. |
| Justified custom UI | Evidence: local reviewed native patterns first; custom Blade, CSS, or Livewire only with documented candidates and a concrete unsupported gap. Authority: `laravel-filament-v5` owns upload APIs/security, implementation, and tests. |

## Clean-install smoke test

Run the following from the repository root:

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/release_install_smoke.py
```

It creates disposable workspaces and uses `npx skills add --copy --yes` to test separate and paired installs for Codex, Claude Code, and Cursor. Every run verifies discovery, `skills-lock.json`, and the universal `SKILL.md` and `README.md` entry points; it also checks that the installed UI/UX release still identifies the Jota Furtado Dev Skills grouping. The Codex run verifies that `agents/openai.yaml` survived installation. The script removes its own temporary workspaces after the run.

## Release checklist

1. Run the deterministic unit suite and catalog validator (including compact-index drift).
2. Parse both eval JSON files and run whitespace checks.
3. Run the clean-install smoke test above.
4. Run the forward prompts in `evals/evals.json` with Claude Code via `scripts/run_forward_evals.py --agent claude-code --output .../claude-code.json`, then score every assertion against the transcript.
5. Review the authority boundary: candidate owns visual selection; baseline owns APIs, implementation, security, and tests.

When a model runtime is unavailable, record that limitation rather than claiming a forward-run result. The catalog remains usable offline after installation.
