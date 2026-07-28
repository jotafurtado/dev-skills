# Release 1.0.0

`laravel-filament-5-ui-ux` is a Filament 5.x only visual-pattern skill. It selects and composes reviewed official patterns for forms, record details, tables, dashboards, panel shells, actions, feedback, and empty states. It does not provide Filament 3.x or 4.x guidance.

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

Synchronize the catalog, review new or changed evidence outside the repository, classify it, and run the verification commands in `README.md` before a maintenance release. The repository stores URLs and original analysis, not official screenshot binaries.

## Release gates

Run catalog validation, deterministic tests, skill-structure validation, eval JSON parsing, whitespace checks, installation smoke tests, and a final authority-boundary review. Keep the skill presented under the Jota Furtado Dev Skills repository origin.
