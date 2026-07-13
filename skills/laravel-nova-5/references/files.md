# File Fields

Use this reference for `File`, `Image`, `Avatar`, and Vapor file fields. Read:

- [Nova File Fields](https://nova.laravel.com/docs/v5/resources/file-fields.md)
- The official Laravel filesystem page matching the installed framework major.

## Basic storage

```php
use Laravel\Nova\Fields\File;
use Laravel\Nova\Fields\Image;

// Fragment: returned from a resource's fields() method.
Image::make('Profile Photo')
    ->disk('public')
    ->maxWidth(100)
    ->prunable(),

File::make('Attachment')
    ->disk('s3')
    ->storeOriginalName('attachment_name')
    ->storeSize('attachment_size'),
```

The disk must exist in `config/filesystems.php`. Nova stores a relative path in
the field's model attribute by default. Run `php artisan storage:link` only when
using Laravel's local `public` disk and the conventional public symlink is
needed.

`prunable()` removes the underlying file when the model is deleted **through
Nova**. Deletions elsewhere in the application still need their own file
lifecycle logic.

## Validation and accepted types

`acceptedTypes()` only adds the browser input's `accept` attribute. Always pair
it with server-side Laravel validation rules suitable for the file:

```php
use Laravel\Nova\Fields\File;

// Fragment: returned from a resource's fields() method.
File::make('Contract')
    ->acceptedTypes('application/pdf')
    ->rules('required', 'file', 'mimes:pdf', 'max:10240'),
```

Choose size and MIME rules from application requirements. Do not trust original
filenames or client-provided content types as a security boundary.

## Custom storage

Use `path()` or `storeAs()` for a custom path/name. Use `store()` only when the
whole storage process must be controlled:

```php
use Illuminate\Http\Request;
use Laravel\Nova\Fields\File;

// Fragment: returned from a resource's fields() method.
File::make('Attachment')
    ->store(fn (Request $request, $model) => [
        'attachment' => $request->attachment->store('/', 's3'),
        'attachment_name' => $request->attachment->getClientOriginalName(),
        'attachment_size' => $request->attachment->getSize(),
    ]),
```

For reusable behavior, prefer the official invokable storage contract and copy
its full `__invoke` signature from the current v5 docs or installed package.
Nova also supports returning a post-persistence callback from `store()`; use
that documented form when the model must exist before related work runs.

## Deletion

Custom deletion callbacks should remove the object and return model attributes
that must become `null`:

```php
use Illuminate\Support\Facades\Storage;
use Laravel\Nova\Fields\File;
use Laravel\Nova\Http\Requests\NovaRequest;

// Fragment: returned from a resource's fields() method.
File::make('Attachment')
    ->disk('s3')
    ->delete(function (NovaRequest $request, $model, $disk, $path) {
        if (! $path) {
            return;
        }

        Storage::disk($disk)->delete($path);

        return [
            'attachment' => null,
            'attachment_name' => null,
            'attachment_size' => null,
        ];
    }),
```

Confirm whether missing objects, shared objects, soft deletes, and failed
storage operations need special handling before replacing Nova's default.

## Downloads and previews

- `disableDownload()` hides Nova's default download link.
- `download()` customizes the response and may return
  `Storage::disk($disk)->download(...)`.
- `preview()` and `thumbnail()` customize image URLs.
- Temporary URLs can be appropriate for large/private cloud files when the
  configured driver supports them.

Do not confuse a file field's `download()` callback with an action response.
Action downloads use `ActionResponse::download($name, $url)` in that documented
argument order.

## Verification

Test the configured testing disk with `Storage::fake()` where compatible with
the application's flow. Assert validation failures, stored model metadata,
object existence, replacement/deletion behavior, and authorization. Use a real
driver integration check when signed URLs, ACLs, or provider-specific behavior
is material.
