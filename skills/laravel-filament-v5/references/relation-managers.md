# Managing relationships in resources

Filament ships several official tools for related records. Classify the relationship and interaction before choosing one. ([managing-relationships doc](https://filamentphp.com/docs/5.x/resources/managing-relationships.md))

Snippets are focused fragments; keep the generated relation-manager/Resource class context and add model, action, `Schema`, and `Table` imports as needed.

## Choosing the right tool

| Tool | Relationship types | Use when |
|---|---|---|
| **Relation manager** — interactive table under the Edit/View page | `HasMany`, `HasManyThrough`, `BelongsToMany`, `MorphMany`, `MorphToMany` | Related records have their own lifecycle: list, create, edit, attach/detach, delete without leaving the page |
| **`ManageRelatedRecords` page** | Same table/form-based management use cases as a relation manager | Related management should have a dedicated Resource page, especially with record sub-navigation |
| **`Select` / `CheckboxList` with `->relationship()`** | `BelongsTo`, `MorphTo`, `BelongsToMany` | User picks from existing records; `->createOptionForm()` allows inline creation in a modal |
| **`Repeater` with `->relationship()`** | `HasMany`, `MorphMany` | CRUD related records *inside* the owner's form — only when the related model has FEW fields, otherwise the form gets very long |
| **Layout component with `->relationship()`** (`Fieldset`, `Section`, `Grid`) | `BelongsTo`, `HasOne`, `MorphOne` | The "relation" is really a 1:1 detail record; wrapped fields load/save on it automatically |

## Creating a relation manager

```bash
php artisan make:filament-relation-manager CategoryResource posts title
# owner resource · relationship name · title attribute
# add --soft-deletes to include restore/force-delete/trashed filter
```

The generated class defines `form(Schema $schema): Schema` and `table(Table $table): Table` — same APIs as a resource (see `references/forms.md` / `references/tables.md`). Register it in the resource:

```php
public static function getRelations(): array
{
    return [
        'posts' => RelationManagers\PostsRelationManager::class, // key = ?relation=posts in the URL
    ];
}
```

## Behavior notes

- **Read-only mode**: on the View page, mutating actions are hidden automatically. Override `public function isReadOnly(): bool { return false; }` to allow edits there, or disable globally with `$panel->readOnlyRelationManagersOnResourceViewPagesByDefault(false)`. This is UI behavior, not a replacement for policies.
- **Pivot attributes** (`BelongsToMany` / `MorphToMany`): add pivot columns to the table and pivot fields to the form like normal fields — but they MUST be listed in `->withPivot()` on **both** sides of the relationship.
- **Attach/detach vs create**: `AttachAction` links existing records (with `->preloadRecordSelect()`, `->recordSelectSearchColumns([...])`, `->multiple()`); `CreateAction` makes new ones. `AssociateAction`/`DissociateAction` are the `HasMany` equivalents. Scope eligible records with `recordSelectOptionsQuery()` and authorize the mutation; a `tableSelect()` filter alone is not a security boundary.
- **Unconventional inverse names**: `$table->inverseRelationship('section')` when the inverse doesn't follow Laravel naming.
- The whole relation manager is a standard table — every feature in `references/tables.md` applies.
- Read `references/security.md` for relationship and tenancy boundaries. After changing a manager, follow `references/testing.md`: assert the host Edit/View page renders it, then load it directly with `ownerRecord` and `pageClass`, including denied and cross-tenant cases when applicable.
