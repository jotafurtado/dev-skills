# Shared domain enums in Filament 5

Use a backed enum when the same finite state or option set appears across forms, tables, infolists, filters, actions, or navigation. Keep a local closure for truly one-off presentation; do not duplicate a shared label/color/icon mapping across surfaces.

Resolve the installed Filament version first. The contracts below match Filament 5.1.1 and should be checked against installed source when a later patch changes them.

## Complete status enum

```php
namespace App\Enums;

use BackedEnum;
use Filament\Support\Contracts\HasColor;
use Filament\Support\Contracts\HasIcon;
use Filament\Support\Contracts\HasLabel;
use Filament\Support\Icons\Heroicon;
use Illuminate\Contracts\Support\Htmlable;

enum OrderStatus: string implements HasLabel, HasColor, HasIcon
{
    case Pending = 'pending';
    case Shipped = 'shipped';

    public function getLabel(): string | Htmlable | null
    {
        return match ($this) {
            self::Pending => 'Pending',
            self::Shipped => 'Shipped',
        };
    }

    public function getColor(): string | array | null
    {
        return match ($this) {
            self::Pending => 'warning',
            self::Shipped => 'success',
        };
    }

    public function getIcon(): string | BackedEnum | Htmlable | null
    {
        return match ($this) {
            self::Pending => Heroicon::Clock,
            self::Shipped => Heroicon::Truck,
        };
    }
}
```

Use narrower covariant return types such as `string` when every case guarantees one, but keep the full contract when `null`, custom color arrays, or `Htmlable` values are possible.

## Cast once, reuse across surfaces

Cast the model attribute to the enum so display components receive enum instances:

```php
protected function casts(): array
{
    return [
        'status' => OrderStatus::class,
    ];
}
```

Then reuse the same enum without repeating maps:

```php
use App\Enums\OrderStatus;
use Filament\Forms\Components\Select;
use Filament\Infolists\Components\TextEntry;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;

Select::make('status')
    ->options(OrderStatus::class);

TextColumn::make('status')
    ->badge();

TextEntry::make('status')
    ->badge();

SelectFilter::make('status')
    ->options(OrderStatus::class);
```

`HasLabel` supplies option and display labels. With an enum-cast state, `HasColor` and `HasIcon` supply badge semantics to supported components. Keep labels understandable without color alone.

Official reference: [Enum tricks](https://filamentphp.com/docs/5.x/advanced/enums.md)
