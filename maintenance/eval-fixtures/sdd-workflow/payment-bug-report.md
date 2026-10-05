# Payment timeout bug

## Reproduction

1. Start checkout and authorize a valid card.
2. Leave the spinner on the confirmation step until the gateway times out.
3. Refresh the order page.

## Observed

The queue worker logs `PaymentGatewayTimeout`. The confirmation UI never leaves
the spinner and never shows a failure state. The order stays `processing`.

## Impact

Buyers retry the card and can be charged twice. Support cannot tell a timeout
from a successful authorization.

Environment: production, Laravel 11, Redis queue, Stripe gateway v2024-11-20.
