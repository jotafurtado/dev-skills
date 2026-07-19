# Security boundaries in Filament 5

Read this file before changing uploads, inline-editable columns, raw HTML, relationship actions, bulk actions, imports/exports, tenancy, authorization, or sensitive fields. Filament supplies UI and integration hooks; the application still owns authorization, query scope, data isolation, and server-side invariants.

## On this page

- Resource, custom-action, and inline-edit authorization
- Relationship selection and file-path boundaries
- HTML, Markdown, URL, import, and export safety
- Tenancy, sensitive Livewire state, and minimum tests

## Start with the boundary

Identify all of these before coding:

- actor and policy ability;
- panel and current tenant;
- records and files the actor may read or mutate;
- whether the operation runs inside a panel request, Livewire request, queue, console command, or external route;
- untrusted text, HTML, URLs, filenames, and exported spreadsheet cells;
- positive and negative tests that prove the boundary.

Do not treat an invisible button, disabled field, filtered dropdown, hidden navigation item, or displayed table query as authorization by itself.

## Resource policies and custom behavior

Resource pages and built-in Resource actions observe registered Laravel model policies. Keep `viewAny()`, `view()`, `create()`, `update()`, `delete()` and their bulk/soft-delete counterparts aligned with the intended UI.

Custom pages, Livewire components, queries, and action callbacks need explicit authorization and scoping when they fall outside built-in CRUD checks. Use an action's documented `authorize()` API plus Laravel policies or gates instead of duplicating role checks in visibility closures. Keep business invariants in the server-side domain/application layer so a manipulated Livewire request cannot bypass them.

In production, implement Filament's panel-access contract and make `canAccessPanel()` distinguish panels when audiences differ. If the threat model requires MFA, configure it for each relevant panel and remember that Filament panel MFA does not protect separate API or non-Filament authentication flows.

Official references: [Resource authorization](https://filamentphp.com/docs/5.x/resources/overview.md#authorization) · [Security](https://filamentphp.com/docs/5.x/advanced/security.md)

## Inline-editable table columns

`ToggleColumn`, `CheckboxColumn`, `SelectColumn`, and `TextInputColumn` save directly and do **not** automatically check the model's `update` policy. Disable editing with the same authorization rule that protects the full edit flow:

```php
use Filament\Tables\Columns\ToggleColumn;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Gate;

ToggleColumn::make('is_active')
    ->disabled(fn (Model $record): bool => Gate::denies('update', $record));
```

Use a full Edit page or authorized modal action when the mutation needs validation, confirmation, related writes, or a richer audit trail. Test both an allowed and denied user.

Official reference: [Inline editable columns](https://filamentphp.com/docs/5.x/advanced/security.md#inline-editable-columns)

## Relationship actions and selection queries

`AttachAction`, `AssociateAction`, detach/dissociate variants, and their bulk forms need deliberate authorization. Relation-manager read-only state is a UI mode, not a complete policy strategy.

- Scope attach/associate resolution with `recordSelectOptionsQuery()` so an injected record key outside the allowed set is rejected.
- Treat a `tableSelect()` table's filters or `modifyQueryUsing()` as presentation only; enforce the same restriction in the record-select options query.
- For bulk actions, use the documented policy method or `authorizeIndividualRecords()` when per-record authorization is required, accepting the extra query cost.
- Scope pivot mutations and verify both relationship sides when tenant or ownership boundaries matter.

```php
use Filament\Actions\AttachAction;
use Illuminate\Database\Eloquent\Builder;

AttachAction::make()
    ->recordSelectOptionsQuery(
        fn (Builder $query): Builder => $query->whereBelongsTo(auth()->user()),
    );
```

Official reference: [Managing relationships](https://filamentphp.com/docs/5.x/resources/managing-relationships.md)

## File uploads

`FileUpload` accepts a client-submitted path on the configured disk. If a disk contains files for multiple users, tenants, or records, isolate paths by disk/directory or enable path authorization:

```php
use Filament\Forms\Components\FileUpload;

FileUpload::make('attachment')
    ->preventFilePathTampering();
```

Also apply these rules:

- Choose disk, directory, and visibility from the actual access model. Visibility defaults to private unless the disk is literally named `public`.
- Add `visibility('public')` only for files intended for unauthenticated public delivery.
- Validate file type and size according to the domain; do not trust the original client filename or MIME claim alone.
- Configure `APP_URL` and storage CORS correctly when previews use another origin.
- Delete replaced or removed files through model/application lifecycle logic. Filament cannot know whether another record still references the file.
- Test that one user or tenant cannot reuse another record's stored path.

Official reference: [File upload](https://filamentphp.com/docs/5.x/forms/file-upload.md)

## HTML, Markdown, and URLs

Prefer `TextEntry->markdown()` or Filament's sanitized `html()` rendering over raw Blade output. Filament's sanitizer intentionally permits some inline style features; applications rendering untrusted rich text may need a stricter sanitizer configuration. Do not wrap user content in `HtmlString` merely to bypass escaping.

Validate user-controlled links against the schemes and destinations the domain permits. For an HTML URL, `Illuminate\Support\Str::sanitizeUrl()` provides Filament's default relative/HTTP/HTTPS scheme check; add host allowlists, SSRF protection, or extra schemes only when the use case requires them. Do not concatenate untrusted strings into raw HTML, action URLs, attributes, or JavaScript.

Do not pass user-controlled names or values to `extra*Attributes()` without strict validation; those APIs intentionally support raw Alpine/Livewire attributes.

Official reference: [Security](https://filamentphp.com/docs/5.x/advanced/security.md)

## Imports and exports

Treat imports and exports as queued data-access features, not merely buttons:

- `ImportAction` does not perform per-record policy checks. Authorize create/update in importer lifecycle hooks when trigger-level access is not sufficient, and tenant-scope relationship resolution and `resolveRecord()`.
- Mark sensitive `ImportColumn` values with `sensitive()` so failed-row logging does not persist them in plain text.
- `ExportAction` does not perform per-record policy checks. Scope the export with `modifyQueryUsing()` or a reliable model scope so the generated file cannot include records the actor may not view.
- Filament writes untrusted formula-leading values such as `=`, `+`, `-`, and `@` without neutralizing them. Apply the application's spreadsheet policy with `formatStateUsing()` for exports and sanitize/warn for import failure CSVs.
- Verify authorization for import failure files and generated export downloads, including any custom policy that replaces Filament's default owner-only behavior.
- Set maximum rows, chunk size, queue, storage disk, retention, and retry behavior according to operational limits; test a representative queued run.

Official references: [Import action](https://filamentphp.com/docs/5.x/actions/import.md) · [Export action](https://filamentphp.com/docs/5.x/actions/export.md)

## Tenancy

Treat tenancy as a data-isolation boundary, not navigation decoration.

- Implement `canAccessTenant()` so guessing another tenant identifier cannot grant access.
- Confirm which Resources are automatically tenant-scoped and manually scope custom pages, actions, widgets, queries, jobs, and models without a tenant-aware Resource.
- Avoid unqualified `withoutGlobalScopes()` on tenant-aware queries; it can remove Filament's tenancy scope.
- Use `scopedUnique()` / `scopedExists()` where validation must honor tenant model scopes.
- Register tenant-sensitive middleware as tenant middleware, persistent across Livewire requests when required.
- Remember that work outside a tenant-aware panel request may not have a current tenant or automatic scope.

Official reference: [Multi-tenancy](https://filamentphp.com/docs/5.x/users/tenancy.md)

## Sensitive form state

Livewire state is client-visible and client-modifiable. `hidden()`, `disabled()`, `readOnly()`, and a hidden form component express UI behavior, not trust. Derive owner IDs, tenant IDs, privileged flags, prices, and similar sensitive values on the server and enforce them again during persistence. Keep unused sensitive model attributes out of hydrated state; use the model's `$hidden` property or the Resource page's documented form-data mutation hook when appropriate.

## Minimum security tests

For each applicable boundary, test:

1. an authorized user can perform the intended operation;
2. an unauthorized user cannot see or execute it;
3. a crafted record key, file path, or relationship key outside the allowed scope is rejected;
4. a tenant cannot read or mutate another tenant's data;
5. bulk operations skip or reject unauthorized records as designed;
6. custom HTML, URLs, and exported values remain safe for the intended consumer.

Use `references/testing.md` for Filament test helpers and preserve the project's existing security-test conventions.
