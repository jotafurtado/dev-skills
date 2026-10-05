{{-- app/Filament/Resources/Orders/Pages/ViewOrder.php still renders payload via Blade. --}}
<pre>{{ json_encode($record->payload, JSON_PRETTY_PRINT) }}</pre>
