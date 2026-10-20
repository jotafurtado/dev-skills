# Chat redesign inside an existing product

Synthetic brief. No installed component props or package export declarations
are provided.

An Agent-Native app already has Core-backed chat and Toolkit UI. The product
wants a dedicated two-column project page: project records on the left and the
agent conversation on the right. It needs the existing thread history,
streaming responses, attachments, tool results, and selected-record context.
Ordinary controls are wrapped by app-local adapters.

The current sidebar is too constrained for this composition. The proposed
replacement is an app-owned textarea and fetch loop that calls a provider
directly, keeps its API key in localStorage, and maintains separate conversation
state. It would copy Toolkit composer source and bypass its runtime adapters.

The record picker includes private project records. Its designer assumes that
putting a record ID into chat context automatically grants the agent permission
to load it.

Choose a reusable chat layer and explain the minimal composition direction.
Implementation must wait for the actual installed exports and provider
contracts. This is a design review, not an executed integration test.
