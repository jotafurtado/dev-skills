# Testing Nova Changes

Nova 5 does not document a general-purpose public testing DSL for resources,
fields, dashboards, or actions. Do not invent helpers such as `Nova::actingAs`,
`assertNovaField`, or undocumented endpoint contracts.

Base tests on:

- [Laravel Testing](https://laravel.com/docs/testing) using the page matching
  the installed Laravel major.
- [Laravel HTTP Tests](https://laravel.com/docs/http-tests) when exercising
  application-owned routes or responses.
- [Laravel Authorization](https://laravel.com/docs/authorization) for policies.
- [Laravel Filesystem](https://laravel.com/docs/filesystem) for storage fakes.
- The relevant [Nova v5 documentation index](https://nova.laravel.com/docs/llms.txt)
  for the feature's documented contract.

## Match the existing suite

Before adding tests, inspect `phpunit.xml`, `tests/`, Composer scripts, and
installed development dependencies. Continue with Pest or PHPUnit according to
the project; do not introduce a second framework just for Nova.

Run the project's existing command when defined. Otherwise, official Laravel
supports:

```shell
php artisan test
./vendor/bin/pest
./vendor/bin/phpunit
```

Use a targeted path or `--filter` first. Expand to the relevant suite and then
the full suite when change risk, runtime, and project practice justify it.

## Proportional strategy

### Low-risk presentation/configuration

Examples: label text, field visibility callback, metric width, menu placement.

- Run syntax, formatter, and static analysis used by the project.
- Add a focused unit test only when the callback or transformation contains
  meaningful logic.
- Perform a Nova UI smoke check if visual placement or generated frontend output
  is the behavior under change.

### Resource persistence and validation

- Prefer feature tests because Laravel boots the application and database.
- Assert model state and validation rules through application-owned, stable
  boundaries.
- Cover create/update differences, database constraints, casts, and hooks.
- Avoid hard-coding undocumented Nova internal JSON payloads or routes solely to
  obtain endpoint coverage.

### Authorization

- Test policy methods directly for representative allowed and denied users.
- Cover the `viewNova` gate when access rules change.
- Include Nova-specific `Nova::whenServing` or resource policy behavior only
  through officially documented/public behavior available in the installed
  version.
- Distinguish row visibility (`indexQuery`) from record authorization (`view`).
- Include attach/detach/add/action paths when those policy methods change.

### Actions, filters, lenses, and metrics

- Extract domain work or query construction into application services/query
  objects when it needs detailed unit tests.
- Assert database effects, dispatched jobs/events/notifications, and result
  transformations through Laravel's official fakes where appropriate.
- For queued actions, test the domain job/service separately and verify queue
  configuration; do not claim browser completion before a worker runs.
- Exercise complex lens/filter/metric SQL against the project's test database,
  including empty data and tenant/authorization scopes.
- Add a Nova UI smoke test only if registration, serialization, or interaction
  is the primary risk.

### File fields

- Use Laravel's documented `Storage::fake()` where the driver-independent path
  is under test.
- Assert validation failures, stored paths/metadata, replacement, pruning, and
  deletion.
- Add a real-driver integration check for signed URLs, ACLs, temporary URLs, or
  provider-specific behavior when necessary.

### Custom fields, cards, filters, and tools

- Start with the generated component's existing frontend test/build setup.
- Run the package's documented `npm` build command after frontend changes.
- Test application-owned API routes with Laravel HTTP tests and explicit route
  authorization.
- Use browser/end-to-end coverage for interaction that cannot be established by
  PHP tests or component tests.

## Verification report

Report:

1. Exact commands run and whether they passed.
2. Tests added or updated and the behavior they cover.
3. Checks not run, with a reason (for example, no licensed Nova dependencies in
   the environment or no configured browser runner).
4. Any remaining manual Nova UI or external storage verification.

Never report a Nova feature as verified solely because a PHP file parses.
