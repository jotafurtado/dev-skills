<?php

namespace App\Filament\Resources\Operations\Tables;

use Filament\Actions\BulkAction;
use Filament\Tables\Columns\IconColumn;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Table;

class OperationsTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('id')->label('ID'),
                TextColumn::make('reference')->label('Reference'),
                TextColumn::make('site_name')->label('Site'),
                TextColumn::make('asset_tag')->label('Asset'),
                TextColumn::make('status')->badge(),
                IconColumn::make('exception')->boolean()->label('Exception'),
                TextColumn::make('opened_at')->dateTime(),
                TextColumn::make('owner.name')->label('Owner'),
                TextColumn::make('region'),
                TextColumn::make('priority'),
            ])
            ->filters([
                SelectFilter::make('status'),
                SelectFilter::make('region'),
                SelectFilter::make('priority'),
            ])
            ->toolbarActions([
                BulkAction::make('assign'),
                BulkAction::make('export'),
            ]);
    }
}
