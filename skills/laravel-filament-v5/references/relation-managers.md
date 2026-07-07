# Managing relationships in resources

Filament ships four official tools for related records. Picking the wrong one is the most common relationship mistake — classify first. ([managing-relationships doc](https://filamentphp.com/docs/5.x/resources/managing-relationships.md))

## Choosing the right tool

| Tool | Relationship types | Use when |
|---|---|---|
| **Relation manager** — interactive table under the Edit/View page | `HasMany`, `HasManyThrough`, `BelongsToMany`, `MorphMany`, `MorphToMany` | Related records have their own lifecycle: list, create, edit, attach/detach, delete without leaving the page |
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

- **Read-only mode**: on the View page, mutating actions are hidden automatically. Override `public function isReadOnly(): bool { return false; }` to allow edits there, or disable globally with `$panel->readOnlyRelationManagersOnResourceViewPagesByDefault(false)`.
- **Pivot attributes** (`BelongsToMany` / `MorphToMany`): add pivot columns to the table and pivot fields to the form like normal fields — but they MUST be listed in `->withPivot()` on **both** sides of the relationship.
- **Attach/detach vs create**: `AttachAction` links existing records (with `->preloadRecordSelect()`, `->recordSelectSearchColumns([...])`, `->multiple()`); `CreateAction` makes new ones. `AssociateAction`/`DissociateAction` are the `HasMany` equivalents.
- **Unconventional inverse names**: `$table->inverseRelationship('section')` when the inverse doesn't follow Laravel naming.
- The whole relation manager is a standard table — every feature in `references/tables.md` applies.
