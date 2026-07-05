---
name: filament-v5-official-first
description: "Constrói interfaces Filament v5 usando SEMPRE componentes oficiais antes de qualquer markup/CSS custom. Ativa ao criar ou editar qualquer coisa Filament: resources, infolists, forms, tables, actions, schemas, panels, widgets, relation managers, custom pages, filtros, colunas, entries, fields, modais, wizards ou testes de painel. Também dispara quando o usuário menciona 'Filament', 'painel admin', 'admin panel', 'infolist', 'view page', 'form schema', 'table column', 'exibir payload', 'mostrar JSON', 'badge de status', ou pede para renderizar/exibir/formatar dados dentro de uma página Filament."
license: MIT
compatible_agents:
  - Claude Code
  - Cursor
  - Windsurf
  - Copilot
tags:
  - laravel
  - php
  - filament
  - admin-panel
  - backend
metadata:
  author: community
  version: "1.0.0"
  domain: backend
  filament_version: "5.x"
  laravel_version: ">=12.x"
  php_version: ">=8.5"
  triggers: Filament, infolist, form schema, table column, action, panel, widget, resource, relation manager, custom page, badge, CodeEntry, KeyValueEntry
  role: specialist
  scope: implementation
  output-format: code
---

# Filament v5 — Componente Oficial Primeiro

O erro que esta skill previne não é falta de conhecimento — é excesso de confiança. Você sabe renderizar um JSON com `<pre>` estilizado, então escreve o `<pre>`. Mas o Filament v5 já tem `CodeEntry` com syntax highlighting, botão de copiar e dark mode, pronto. O componente oficial nunca entrou na sua lista de opções porque você nem parou para considerar que ele existisse. Esta skill existe para forçar essa parada.

## O gate obrigatório (execute ANTES de escrever markup)

Antes de escrever `<div>`, `<span>`, `<pre>`, `@foreach`, classes Tailwind ou qualquer view Blade custom dentro de um contexto Filament, **pare e execute estes 3 passos**:

1. **Classifique o dado** em uma primitiva de apresentação: código/JSON, key-value, cor, imagem, badge/status, lista, repetição, ícone/booleano, data/hora, dinheiro, texto formatado.
2. **Toda primitiva dessa lista TEM componente oficial.** Encontre-o no inventário abaixo e use-o. Não existe "caso simples demais para componente" — o componente É o caso simples.
3. **Se não estiver no inventário**, execute o protocolo de fetch (última seção) ANTES de concluir que não existe. "Não lembro desse componente" não é evidência de que ele não existe.

**CSS/Blade custom é permitido somente para ajuste fino de layout** (espaçamento, alinhamento, largura) — **nunca** para renderizar dados. Se você se pegar escrevendo um `<pre>` estilizado, um `<span>` colorido ou um loop Blade dentro de um resource, esse é o sinal de que pulou o gate. Volte ao passo 1.

Confiança não é verificação: o erro acontece exatamente no momento em que você "sabe" renderizar algo à mão. Quanto mais óbvia a solução custom parecer, mais provável que exista componente oficial para ela.

## Anti-padrões: não faça X, faça Y

**❌ JSON/código com `<pre>` + CSS custom → ✅ `CodeEntry`**

```php
// ❌ NUNCA
ViewEntry::make('payload')->view('filament.custom-json-pre') // <pre> com CSS

// ✅ SEMPRE — highlighting via Phiki, dark mode, tudo pronto
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('payload')
    ->grammar(Grammar::Json)
    ->copyable()
```

**❌ Status colorido com `<span>` + Tailwind → ✅ `badge()` + enum `HasColor`**

```php
// ❌ NUNCA
// <span class="rounded bg-green-100 px-2 text-green-800">{{ $status }}</span>

// ✅ SEMPRE — em infolist (TextEntry) ou table (TextColumn), a API é a mesma
TextEntry::make('status')->badge() // cor/label/ícone vêm do enum

// O enum carrega a semântica:
use Filament\Support\Contracts\{HasColor, HasIcon, HasLabel};

enum OrderStatus: string implements HasLabel, HasColor, HasIcon
{
    case Pending = 'pending';
    case Shipped = 'shipped';

    public function getLabel(): string { /* ... */ }
    public function getColor(): string { /* 'warning', 'success'... */ }
    public function getIcon(): \Filament\Support\Icons\Heroicon { /* ... */ }
}
```

**Outros da mesma família:**

| ❌ Não faça | ✅ Faça |
|---|---|
| `@foreach` em Blade para array associativo | `KeyValueEntry::make('meta')` |
| `@foreach` para lista de itens relacionados | `RepeatableEntry::make('items')->schema([...])` |
| `<div style="background: {{ $color }}">` | `ColorEntry::make('color')` |
| `<img>` com classes de avatar | `ImageEntry::make('avatar')->circular()` |
| SVG inline / string de ícone para booleano | `IconEntry::make('is_active')->boolean()` |
| Formatar data/dinheiro à mão no Blade | `TextEntry::make('...')->dateTime()` / `->money('BRL')` |
| JS custom de "copiar para clipboard" | `->copyable()` (disponível em vários entries) |
| Renderizar Markdown/HTML com lib externa | `TextEntry::make('body')->markdown()` / `->html()` |

## Inventário de componentes oficiais v5

Isto é memória, não documentação: assinatura mínima + link. Na dúvida sobre um método específico, abra o link — não invente.

### Infolists — exibição read-only (`Filament\Infolists\Components\*`)

Usados dentro de `public function infolist(Schema $schema): Schema` em View pages.

| Componente | Para quê | Assinatura mínima | Doc 5.x |
|---|---|---|---|
| `TextEntry` | Texto, data, dinheiro, badge, listas | `TextEntry::make('title')->badge()` · `->dateTime()` · `->money('BRL')` · `->markdown()` · `->listWithLineBreaks()` | [text-entry](https://filamentphp.com/docs/5.x/infolists/text-entry) |
| `CodeEntry` | Código, JSON, payloads, logs | `CodeEntry::make('payload')->grammar(Grammar::Json)->copyable()` | [code-entry](https://filamentphp.com/docs/5.x/infolists/code-entry) |
| `KeyValueEntry` | Array associativo / metadata | `KeyValueEntry::make('meta')` | [key-value-entry](https://filamentphp.com/docs/5.x/infolists/key-value-entry) |
| `ColorEntry` | Amostra de cor | `ColorEntry::make('color')` | [color-entry](https://filamentphp.com/docs/5.x/infolists/color-entry) |
| `ImageEntry` | Imagens, avatares | `ImageEntry::make('avatar')->circular()` · `->stacked()` | [image-entry](https://filamentphp.com/docs/5.x/infolists/image-entry) |
| `IconEntry` | Ícone, booleano visual | `IconEntry::make('is_active')->boolean()` | [icon-entry](https://filamentphp.com/docs/5.x/infolists/icon-entry) |
| `RepeatableEntry` | Coleções/relações repetidas | `RepeatableEntry::make('comments')->schema([...])` | [repeatable-entry](https://filamentphp.com/docs/5.x/infolists/repeatable-entry) |

### Forms — edição (`Filament\Forms\Components\*`)

Usados dentro de `public static function form(Schema $schema): Schema`.

| Componente | Para quê | Assinatura mínima | Doc 5.x |
|---|---|---|---|
| `TextInput` | Texto, e-mail, número, senha | `TextInput::make('email')->email()->required()` | [text-input](https://filamentphp.com/docs/5.x/forms/text-input) |
| `Textarea` | Texto longo simples | `Textarea::make('notes')->rows(4)` | [textarea](https://filamentphp.com/docs/5.x/forms/textarea) |
| `Select` | Opções, relacionamentos | `Select::make('author_id')->relationship('author', 'name')->searchable()->preload()` | [select](https://filamentphp.com/docs/5.x/forms/select) |
| `Checkbox` / `Toggle` | Booleano | `Toggle::make('is_active')` | [toggle](https://filamentphp.com/docs/5.x/forms/toggle) |
| `ToggleButtons` | Poucas opções visíveis (status!) | `ToggleButtons::make('status')->options(OrderStatus::class)->inline()` | [toggle-buttons](https://filamentphp.com/docs/5.x/forms/toggle-buttons) |
| `Radio` / `CheckboxList` | Opções em lista | `CheckboxList::make('tags')->options([...])` | [checkbox-list](https://filamentphp.com/docs/5.x/forms/checkbox-list) |
| `DateTimePicker` | Data/hora (há `DatePicker`, `TimePicker`) | `DateTimePicker::make('published_at')` | [date-time-picker](https://filamentphp.com/docs/5.x/forms/date-time-picker) |
| `FileUpload` | Arquivos, imagens | `FileUpload::make('attachment')->image()` — default é **privado**; `->visibility('public')` só se necessário | [file-upload](https://filamentphp.com/docs/5.x/forms/file-upload) |
| `RichEditor` / `MarkdownEditor` | Texto rico | `RichEditor::make('body')` | [rich-editor](https://filamentphp.com/docs/5.x/forms/rich-editor) |
| `Repeater` | Linhas repetidas / relações | `Repeater::make('items')->schema([...])` — não ocupa largura total por padrão | [repeater](https://filamentphp.com/docs/5.x/forms/repeater) |
| `Builder` | Blocos de conteúdo flexíveis | `Builder::make('content')->blocks([...])` | [builder](https://filamentphp.com/docs/5.x/forms/builder) |
| `TagsInput` | Lista de strings | `TagsInput::make('tags')` | [tags-input](https://filamentphp.com/docs/5.x/forms/tags-input) |
| `KeyValue` | Editar array associativo | `KeyValue::make('meta')` | [key-value](https://filamentphp.com/docs/5.x/forms/key-value) |
| `ColorPicker` | Escolher cor | `ColorPicker::make('color')` | [color-picker](https://filamentphp.com/docs/5.x/forms/color-picker) |
| `CodeEditor` | Editar código/JSON | `CodeEditor::make('config')` — verifique a assinatura exata na doc 5.x | [code-editor](https://filamentphp.com/docs/5.x/forms/code-editor) |
| `Hidden` | Valor oculto | `Hidden::make('user_id')` | [hidden](https://filamentphp.com/docs/5.x/forms/hidden) |

### Tables — colunas e filtros (`Filament\Tables\Columns\*`, `Filament\Tables\Filters\*`)

| Componente | Para quê | Assinatura mínima | Doc 5.x |
|---|---|---|---|
| `TextColumn` | Texto, data, dinheiro, **badge** | `TextColumn::make('status')->badge()->sortable()->searchable()` · `->money('BRL')` · `->dateTime()` | [columns/text](https://filamentphp.com/docs/5.x/tables/columns/text) |
| `IconColumn` | Ícone/booleano | `IconColumn::make('is_active')->boolean()` | [columns/icon](https://filamentphp.com/docs/5.x/tables/columns/icon) |
| `ImageColumn` | Imagens/avatares | `ImageColumn::make('avatar')->circular()` | [columns/image](https://filamentphp.com/docs/5.x/tables/columns/image) |
| `ColorColumn` | Amostra de cor | `ColorColumn::make('color')` | [columns/color](https://filamentphp.com/docs/5.x/tables/columns/color) |
| `SelectColumn` / `ToggleColumn` / `TextInputColumn` / `CheckboxColumn` | Edição inline na tabela | `ToggleColumn::make('is_featured')` | [columns/toggle](https://filamentphp.com/docs/5.x/tables/columns/toggle) |
| `SelectFilter` | Filtro por opções/enum/relação | `SelectFilter::make('status')->options(OrderStatus::class)` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |
| `TernaryFilter` | Filtro sim/não/todos | `TernaryFilter::make('is_active')` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |
| `TrashedFilter` | Soft deletes | `TrashedFilter::make()` | [filters](https://filamentphp.com/docs/5.x/tables/filters/overview) |

### Layout — schemas (`Filament\Schemas\Components\*`)

Valem para forms E infolists (mesmo sistema de Schema em v5).

| Componente | Assinatura mínima | Doc 5.x |
|---|---|---|
| `Section` | `Section::make('Details')->columns(2)->collapsible()->schema([...])` | [sections](https://filamentphp.com/docs/5.x/schemas/sections) |
| `Grid` | `Grid::make(3)->schema([...])` | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts) |
| `Tabs` | `Tabs::make()->tabs([Tabs\Tab::make('General')->schema([...])])` | [tabs](https://filamentphp.com/docs/5.x/schemas/tabs) |
| `Wizard` | `Wizard::make([Wizard\Step::make('Order')->schema([...])])` | [wizards](https://filamentphp.com/docs/5.x/schemas/wizards) |
| `Fieldset` / `Flex` / `Group` | agrupamento e distribuição — verifique a assinatura exata na doc 5.x | [layouts](https://filamentphp.com/docs/5.x/schemas/layouts) |
| `Text` / `Icon` / `Image` (primes) | conteúdo estático arbitrário dentro de um schema — use ANTES de pensar em Blade custom; verifique na doc 5.x | [primes](https://filamentphp.com/docs/5.x/schemas/primes) |

⚠️ `Grid`, `Section` e `Repeater` **não ocupam toda a largura por padrão** — use `->columnSpan(...)` ou `->columnSpanFull()`.

### Actions (`Filament\Actions\*` — SEMPRE este namespace)

| Componente | Assinatura mínima | Doc 5.x |
|---|---|---|
| `Action` | `Action::make('approve')->requiresConfirmation()->action(fn ($record) => ...)` | [overview](https://filamentphp.com/docs/5.x/actions/overview) |
| Action com modal/formulário | `Action::make('edit')->schema([TextInput::make('reason')])` — modais usam `->schema()`, **não** `->form()` | [modals](https://filamentphp.com/docs/5.x/actions/modals) |
| `CreateAction`, `EditAction`, `ViewAction`, `DeleteAction`, `ActionGroup`, `BulkAction`, `DeleteBulkAction`, `ImportAction`, `ExportAction` | `DeleteAction::make()` | [overview](https://filamentphp.com/docs/5.x/actions/overview) |

## Quebras de API v5 — nunca sugira a forma antiga

Seu conhecimento de Filament v3/v4 vai te trair. Em v5:

- **Schema unificado**: `public function infolist(Schema $schema): Schema` e `public static function form(Schema $schema): Schema`. Top-level é `$schema->components([...])`. ❌ `$infolist->schema([...])` é v3 — não existe mais.
- **Namespaces por domínio**:
  - Layout (Section, Grid, Tabs, Flex, Fieldset, Wizard): `Filament\Schemas\Components\*`
  - Utilities (Get, Set): `Filament\Schemas\Components\Utilities\*`
  - Form fields: `Filament\Forms\Components\*`
  - Infolist entries: `Filament\Infolists\Components\*`
  - Table columns: `Filament\Tables\Columns\*` · filters: `Filament\Tables\Filters\*`
  - Actions: `Filament\Actions\*` — ❌ `Filament\Tables\Actions\*` foi **removido** em v5.
- **Métodos de tabela renomeados**: `->recordActions([...])` (não `->actions()`), `->groupedBulkActions([...])` (não `->bulkActions()`), `->toolbarActions([...])`.
- **Modais de Action**: `->schema([...])`, ❌ não `->form([...])`.
- **Ícones**: enum `Filament\Support\Icons\Heroicon` (ex.: `Heroicon::PencilSquare`). ❌ Nunca strings como `'heroicon-o-pencil'`. Para navegação, use as variantes `Outlined*`.
- **Enums de domínio**: backed string enums implementando `HasLabel`, `HasColor`, `HasIcon` (`Filament\Support\Contracts`) — é assim que badge/select/filter ganham label, cor e ícone de graça.
- **Operação condicional**: compare com `Operation::Create` / `Operation::Edit` / `Operation::View` — ❌ não compare strings `'create'`/`'edit'`.
- **File uploads são privados por default**: só adicione `->visibility('public')` quando acesso público for realmente necessário.

## Protocolo de fetch — backup de frescor

O inventário acima funciona offline e cobre o dia a dia. Busque a doc quando: (a) o componente/método não está no inventário; (b) você hesitou sobre uma assinatura; (c) o usuário citou algo que você não reconhece.

1. **Índice canônico para LLMs**: `https://filamentphp.com/docs/llms.txt` — lista todas as páginas; localize a página 5.x relevante.
2. **Página direta**: `https://filamentphp.com/docs/5.x/{seção}/{página}` (ex.: `5.x/infolists/code-entry`).
3. **MCP `laravel-boost` (`search-docs`)**, se ativo: use `packages: ["filament/filament"]`. ⚠️ **A resposta mistura 3.x/4.x/5.x** — descarte tudo que não estiver marcado `filament/filament@5.x`. Um trecho 3.x parece plausível e compila errado.
4. Nunca resolva a hesitação "de memória" com assinatura v3/v4. Se não conseguir verificar, escreva o link da doc no comentário e diga explicitamente que a assinatura precisa ser confirmada — não invente.

## Contexto do projeto-alvo

`filament/filament` **v5.6.0** · PHP 8.5 · Laravel 12 · Livewire 4 · Tailwind v4. Todo código gerado deve ser válido nessa combinação.
