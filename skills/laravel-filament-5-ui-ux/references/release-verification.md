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

## Full clean Codex behavioral matrix

On 2026-07-28, Codex CLI 0.145.0 ran a read-only, clean paired installation of both skills. It read only the installed skill files and local reviewed catalog; no project APIs, network access, or screenshots were available. Every row passed: it compared official candidates, selected a pattern, named responsive and accessibility treatment, cited local evidence (or disclosed the unavailable visual inspection), and delegated exact APIs, security, implementation, and tests to `laravel-filament-v5`.

**Baseline-only contrast:** `laravel-filament-v5` supplies version-sensitive APIs, security, implementation, tests, and fallback visual guardrails, but not this skill's reviewed visual-catalog query, pattern-family comparison, screenshot inventory, or required visual decision trace. Across every probe below, the candidate therefore demonstrated improved official-pattern discovery and observable evidence use while the baseline retained its implementation authority.

| Coverage area | Result | Recorded evidence and authority |
|---|---|---|
| Forms and schema layouts | PASS | Evidence: local reviewed catalog candidates for responsive columns, sections, ordinary wrappers, and fused fields. Selected short related fields sharing width, long description spanning it, and a labelled location group only where its fields remain related. Authority: `laravel-filament-v5` owns APIs, validation, implementation, and tests. |
| Tables | PASS | Evidence: local reviewed catalog table, filter, bulk-action, and empty-state patterns. Selected compare-and-scan ordering, purposeful filters, grouped or bulk operations, and a filtered no-results reset. Authority: `laravel-filament-v5` owns table/action APIs, authorization, implementation, and tests. |
| Responsive records | PASS | Evidence: local reviewed Split and Stack mobile variants. Selected an identity-centred transformation retaining identity, state, selection, and primary action on narrow screens. Authority: `laravel-filament-v5` owns table-layout APIs, policies, implementation, and tests. |
| Record details | PASS | Evidence: local reviewed `record-detail-infolist` variants. Selected identity and labelled status before primary facts, with documents and audit information secondary. Authority: `laravel-filament-v5` owns infolist/View APIs, document authorization, implementation, and tests. |
| Dashboards | PASS | Evidence: local reviewed Stats Overview, chart, table-widget, and dashboard-filter patterns. Selected risk stats, then a labelled trend and intervention queue, with visible shared scope and the established panel theme. Authority: `laravel-filament-v5` owns widget/filter APIs, scope security, implementation, and tests. |
| Navigation and authentication | PASS | Evidence: local reviewed top-navigation, sidebar-navigation, and authentication-surface patterns. Selected top navigation for support, grouped sidebar navigation for the back-office, actionable badges only, and keyboard-operable mobile authentication paths. Authority: `laravel-filament-v5` owns panel/auth APIs, authorization boundaries, implementation, and tests. |
| Actions and feedback | PASS | Evidence: local reviewed action-group, confirmation, overlay, callout, notification, and empty-state patterns. Selected direct approval, focused correction overlay, archive confirmation, full-page compliance flow, and durable guidance distinct from transient feedback. Authority: `laravel-filament-v5` owns action/modal APIs, policy enforcement, implementation, and tests. |
| Offline and no-vision fallback | PASS | Evidence: local reviewed `record-detail-infolist` interpretation; screenshot inspection was explicitly unavailable. Selected identity/status, then primary facts, then secondary documents/audit. Authority: `laravel-filament-v5` owns installed API verification, authorization, implementation, and tests. |
| Justified custom UI | PASS | Evidence: local reviewed Builder or Repeater and upload patterns. Selected native collection and upload patterns; custom Blade, CSS, or Livewire require documented candidates and a concrete unsupported gap. Authority: `laravel-filament-v5` owns upload APIs/security, implementation, and tests. |

The matrix therefore exercises the visual coverage in `evals/evals.json` as grouped behavior probes. The earlier Claude Code record independently confirms the paired-skill authority split on the vendor View path.

## 2026-08-03 clean forward matrix

The full 15-prompt matrix was rerun from clean paired installations with Codex CLI 0.145.0, Claude Code 2.1.220, and Cursor CLI 3.14.7. Each agent produced 15 non-empty, reviewable transcripts (`recorded: 15`, `failed: 0`); the raw outputs are retained in `evals/forward-runs/{codex,claude-code,cursor}.json`. Codex ran with a read-only sandbox, Claude Code ran in plan mode, and Cursor ran with `--mode ask --trust` inside a disposable workspace because its plan-mode output stopped at progress updates rather than returning the behavioral trace. Ask mode is Cursor's read-only Q&A mode; the prompt also prohibits file changes, the runner snapshots the workspace before and after every prompt and marks any mutation as failed, and the disposable workspace is removed after each run.

The maintainer reviewed the recorded traces for catalog discovery, an explicit composition choice, responsive and accessibility treatment, and routing of version-sensitive APIs, security, implementation, and tests to `laravel-filament-v5`. Cursor's ask mode was selected specifically because it emits the complete decision trace needed for this review; the runner also applies a 180-second per-agent timeout and records timeout failures instead of hanging indefinitely.

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
4. Run the forward prompts in `evals/evals.json` with available clean Codex, Claude Code, and Cursor environments, scoring them against the comparison table.
5. Review the authority boundary: candidate owns visual selection; baseline owns APIs, implementation, security, and tests.

When a model runtime is unavailable, record that limitation rather than claiming a forward-run result. The catalog remains usable offline after installation.
