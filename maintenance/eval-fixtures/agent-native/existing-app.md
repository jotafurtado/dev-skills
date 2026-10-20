# Existing app: website example mismatch

Synthetic project evidence. The version numbers describe this fictional project
and do not certify a real release's exports.

| Evidence | Value |
| --- | --- |
| App manifest Core constraint | `^0.198.0` |
| Lockfile Core resolution | `0.198.0` |
| Lockfile Toolkit resolution | `0.198.1` |
| Existing domain controls | Imported through `@/components/ui/*` |
| Local skills inventory | `agent-native-docs`, `agent-native-toolkit` |
| Target change | Add a project-specific filter in the existing settings layout |

A developer copied a current website example using an export called
`ProjectSettingsFilter`. This export name is intentionally invented for the
fixture. The local build says that it is not exported by the selected public
entry point. The full installed exports, source, and type declarations have not
been supplied.

The developer proposes installing the newest Core and Toolkit, or deep-importing
a similarly named file from Toolkit's private source and copying the settings
runtime into the app. No framework upgrade has been requested. The existing
settings page and local control adapters otherwise work.

The task is to choose the investigation and minimal repair path. No build,
documentation search, or dependency modification has been executed by the
responding agent.
