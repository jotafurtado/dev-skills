# Documentation lookup and provenance

## Lookup order

1. Inspect the app's instructions, local framework skills, dependency resolution,
   and installed public exports/types. Prefer its version-matched documentation
   to current website examples when implementing an existing app.
2. If the installed app exposes the documented `framework-search` action, use
   it for bounded discovery across docs and source. Use `docs-search` or
   `source-search` for the full selected page/file. Check the app's scripts and
   action definitions before assuming an invocation command.
3. If those readers are unavailable, inspect installed package files directly.
   Current locations are listed below; resolve their existence in the target app.
4. For missing material or a new app, use the official English Markdown pages
   and official repository. Match source to the resolved package version where
   possible. Current `main` and website docs are not proof of older compatibility.

| Material | Documented location |
| --- | --- |
| Core docs index and pages | `node_modules/@agent-native/core/docs/AGENTS.md`, `docs/content/` within that package |
| Core implementation and public declarations | `node_modules/@agent-native/core/dist/`, package `exports` |
| Toolkit readable source | `node_modules/@agent-native/toolkit/src/`, package `exports` |
| Optional first-party template corpus | `node_modules/@agent-native/core-corpus/corpus/templates/` |

The corpus is optional and carries template source, not Core runtime source.
If its examples are needed, first determine whether the existing app already
includes it. Any addition must match Core's exact resolved version and stay
within the task's dependency-change authorization. Missing corpus files do not
justify a broad framework upgrade.

## Bounded English discovery

[llms.txt](https://www.agent-native.com/llms.txt) is a discovery index. It includes
localized pages and duplicate HTML/Markdown entries. Search/filter it for the
needed topic, select canonical `/docs/` English pages, and prefer their `.md`
variant. Load selected pages rather than the whole index or every translation.
If a Markdown mirror fails, try its canonical English HTML page or official
version-matched source.

Record the installed version and the page or source definition behind an API.
Check package exports as well as the implementation: finding a symbol in private
source does not make it a supported import. For a moved export or API mismatch,
consult installed migration guidance before editing dependencies.

If no matching evidence is accessible, report the missing API/version and the
sources tried. Continue independent work; leave dependent implementation blocked
instead of presenting current website examples as verified for the installation.

## Topic routes

| Task | Official starting pages |
| --- | --- |
| Start or select a template | [Getting Started](https://www.agent-native.com/docs/getting-started.md), [Templates](https://www.agent-native.com/docs/cloneable-saas.md) |
| Actions and permissions | [Actions](https://www.agent-native.com/docs/actions-overview.md), [Access](https://www.agent-native.com/docs/actions-access-control.md) |
| UI component choice | [Component API](https://www.agent-native.com/docs/components.md), [Toolkit](https://www.agent-native.com/docs/agent-native-toolkit.md) |
| Framework customization | Installed `customizing-agent-native` skill; [official source](https://github.com/BuilderIO/agent-native/blob/3d6a9d3851761be8b65f76238a123cb2195ac6a1/.agents/skills/customizing-agent-native/SKILL.md) as a discovery fallback |
| Version drift | [Versioning and Stability](https://www.agent-native.com/docs/versioning-and-stability.md), installed migration manifest |
| Framework skill coverage | [Skills Guide](https://www.agent-native.com/docs/skills-guide.md), template's actual `.agents/skills/` directory |
| External agents and integrations | [External Agents](https://www.agent-native.com/docs/external-agents.md), [MCP](https://www.agent-native.com/docs/mcp-protocol.md), [A2A](https://www.agent-native.com/docs/a2a-protocol.md) |
| Operations and deployment | [Observability](https://www.agent-native.com/docs/toolkit-observability.md), [Workspace Deployment](https://www.agent-native.com/docs/workspace-deployment.md), hosting guide for the selected target |

Integrations, operations, deployment, and migrations are documentation routes in
this skill, not bundled implementation playbooks.

## Authoring provenance

This skill's original English summaries were checked against official English
docs and the BuilderIO repository on 2026-10-17. Source inspection used commit
[`3d6a9d3851761be8b65f76238a123cb2195ac6a1`](https://github.com/BuilderIO/agent-native/tree/3d6a9d3851761be8b65f76238a123cb2195ac6a1).
This is a provenance marker, not a supported-version pin.

The official README identifies the framework as MIT; the inspected Core and
Toolkit package manifests declare MIT. The repository root package separately
declares ISC. This skill uses independently written guidance and links rather
than vendored framework code or a translated documentation dump.

Primary source pointers:

- [Official repository](https://github.com/BuilderIO/agent-native)
- [Framework documentation lookup skill](https://github.com/BuilderIO/agent-native/blob/3d6a9d3851761be8b65f76238a123cb2195ac6a1/.agents/skills/agent-native-docs/SKILL.md)
- [Toolkit ownership skill](https://github.com/BuilderIO/agent-native/blob/3d6a9d3851761be8b65f76238a123cb2195ac6a1/.agents/skills/agent-native-toolkit/SKILL.md)

When maintaining this skill, refresh the affected catalog entries and source
links, not every page indiscriminately. Keep dates and package ownership honest;
re-run relevant evaluations after changing workflow or activation behavior.
