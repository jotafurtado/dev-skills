# Visual fallback when the dedicated UI/UX skill is unavailable

`laravel-filament-v5-ui-ux` ships ready-to-adapt compositions for Filament 5 surfaces — `references/table.md` for record tables, `references/form-layout.md` for page structure, `references/form-fields.md` for everyday fields, `references/form-inputs.md` for collection and content-heavy controls. Prefer those over composing a surface from scratch. Use this file only when that skill is unavailable.

Choose the documented official component that matches the data and interaction already requested. Preserve the existing panel theme and retain accessible labels, keyboard operation, visible focus, responsive readability, and non-colour state cues. Do not recreate official components with Blade or CSS when an official primitive fits.

For a custom surface, name the official component options checked and the concrete unsupported gap. Keep the custom code to the smallest surface. Disclose that the composition library was unavailable.

Use `references/screenshots.md` only to locate a relevant official example when direct inspection is possible. It is not a curated selection guide.
