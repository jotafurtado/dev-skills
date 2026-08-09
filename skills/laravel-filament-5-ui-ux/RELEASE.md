# Release 1.1.0

`laravel-filament-5-ui-ux` is a Filament 5.x only visual-pattern skill. It selects and composes reviewed official patterns for forms, record details, tables, dashboards, panel shells, actions, feedback, and empty states. It does not provide Filament 3.x or 4.x guidance.

## What changed in 1.1.0

- Primary selection path is the compact derived index `references/visual-catalog-index.md`, resolved from the skill install directory rather than the project working directory.
- Catalog query remains available as an optional alternative when a local Python runtime can execute `scripts/query_visual_catalog.py`.
- Query dimensions no longer include `available_width`. Surface is the only restrictive filter; other dimensions add ranking weight.
- Invalid vocabulary fails closed with named dimensions and close-match suggestions.
- Forward-run evidence records per-assertion `verdict` and `evidence` citations; `review_required` is derived from any remaining `unscored` assertion.

## Authority boundary

This skill owns visual option discovery, screenshot comparison, pattern selection, responsive presentation, and the visual decision trace. Install `laravel-filament-v5` alongside it when the task also needs installed-version APIs, implementation, security, or tests; that skill owns those concerns.

Install the visual skill alone when a task is design or review only:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-5-ui-ux
```

Install both skills for implementation work:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-5-ui-ux --skill laravel-filament-v5
```

## Runtime fallbacks and maintenance

The reviewed catalog works offline after installation. When image inspection or network access is unavailable, use the local reviewed interpretation and disclose that limitation in the visual decision trace. Custom Blade, Livewire, CSS, or theme work is an escape hatch only after naming the official candidates checked and the concrete gap they cannot cover.

Synchronize the catalog, regenerate the compact index, review new or changed evidence outside the repository, classify it, and run the release evidence in [`references/release-verification.md`](./references/release-verification.md) before a maintenance release. The repository stores URLs and original analysis, not official screenshot binaries.

## Release gates

Run catalog validation, deterministic tests, eval JSON parsing, whitespace checks, the clean-install smoke test (`scripts/release_install_smoke.py`), and a final authority-boundary review. Record raw clean-agent forward-evaluation transcripts with `scripts/run_forward_evals.py`; score every assertion with a `pass`/`fail` verdict and transcript citation before treating the release as reviewed. The verification reference compares the candidate with the main Filament baseline and defines single-agent forward-run evidence. Keep the skill presented under the Jota Furtado Dev Skills repository origin.
