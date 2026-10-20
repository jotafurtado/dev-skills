# Agent-Native

Development guidance for apps built with the BuilderIO Agent-Native framework.
The skill covers fundamentals and UI: shared actions, SQL data, authorization,
agent-visible application context, synchronization, and component selection.

## Install

```bash
npx skills add jotafurtado/dev-skills --skill agent-native
```

## How it works

The agent starts with the app's resolved Core/Toolkit versions and existing
instructions. It loads only the relevant English references, then verifies APIs
against installed documentation and public exports before implementing them.

The UI catalog maps product needs to component families and official docs. It
does not freeze every prop or API signature. Local framework skills remain the
version-specific guide when available. Advanced integrations, operations, and
deployment are linked rather than duplicated.

Use it to add a shared action and UI, select a chat surface, reuse Toolkit
components, or investigate missing agent context and stale screens. Generic
agents and React Native are outside its activation scope.

## Requirements

- A coding agent that supports Agent Skills and can read project files.
- Installed package documentation/source, or access to official online docs.
- For implementation, the target app's own framework/runtime requirements.

No runtime dependencies or executable scripts are bundled with the skill.

## Verification

From the repository root:

```bash
node maintenance/validate_skill.mjs skills/agent-native
python3 maintenance/eval_skills.py validate-datasets
python3 maintenance/eval_skills.py run --judge description --skill agent-native --out maintenance/evals-out/agent-native-description
```

The dataset includes 20 activation queries and four output scenarios with
synthetic project evidence under `maintenance/eval-fixtures/agent-native/`.
Fixtures are evaluation-only, not framework templates or runnable apps.

Description/mock judges are deterministic maintenance checks, not evidence of
model quality. Tool-enabled candidate/baseline runs should receive identical
fixture evidence; only the candidate receives this skill. The repository's live
harness can also compare isolated answers when credentials are configured, but
it does not execute a real app or prove integration behavior. Keep outputs under
`maintenance/evals-out/`, outside the distributed skill.

The repository's [verification record](../../maintenance/agent-native/verification.md)
documents the exercised checks, paired reviews, and known evaluation limitations.

## Sources and maintenance

See [documentation lookup and provenance](references/documentation.md) for
source precedence, official links, and the checked source revision. Core and
Toolkit evolve independently; confirm the target installation rather than
treating the catalog's review date as a compatibility guarantee.

MIT.
