<?php

// app/Filament/Resources/Orders/Tables/OrdersTable.php

namespace App\Filament\Resources\Orders\Tables;

use Filament\Actions\Action;
use Filament\Actions\ExportAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Columns\ToggleColumn;
use Filament\Tables\Table;

class OrdersTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('number'),
                ToggleColumn::make('status'),
            ])
            ->headerActions([
                ExportAction::make(),
            ])
            ->recordActions([
                Action::make('approve')
                    ->visible(fn (): bool => auth()->user()?->is_manager === true),
            ]);
    }
}
