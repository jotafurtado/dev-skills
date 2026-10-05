<?php

namespace App\Filament\Resources\Teams\RelationManagers;

use Filament\Actions\AttachAction;
use Filament\Forms\Components\FileUpload;
use Filament\Schemas\Schema;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Columns\ToggleColumn;
use Filament\Tables\Table;

class UsersRelationManager
{
    public function form(Schema $schema): Schema
    {
        return $schema->components([
            FileUpload::make('identity_document')
                ->disk('local')
                ->directory('identity-documents'),
        ]);
    }

    public function table(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('email'),
                ToggleColumn::make('is_active'),
            ])
            ->headerActions([
                AttachAction::make(),
            ]);
    }
}
