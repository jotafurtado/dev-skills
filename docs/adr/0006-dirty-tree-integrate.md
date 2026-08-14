# Dirty-tree integrate when workers must not commit

Status: Accepted

## Context

Field use of `implement-with-subagents` (presenter Pipeline, tickets 01–06) showed that host-adapter text telling the orchestrator to “merge the ticket branch” is false under the worker contract: workers must not commit, so the ticket branch stays at the same SHA as the orchestrator branch and `git merge` is a no-op. The real diff lives in the worktree working tree. Trusting the worker’s `filesTouched` list without `git status` almost shipped a ticket without its acceptance tests.

## Decision

Define **dirty-tree integrate** as the default integrate verb for all hosts: after `outcome: success`, copy every path from `git status --short` in the worktree (tracked + untracked, minus local junk) onto the orchestrator branch, then test, review, and commit there. Treat `filesTouched` as an index only. Prefer host apply/merge only when it actually transfers that dirty tree; never declare success on “Already up to date.”

Also record related field rules in the same skill revision: Cursor isolate fallback to manual `git worktree add`, degraded in-process `/code-review`, resume handshake with SHA-from-git-only, and next-wave only after `git log` shows the commit.

## Consequences

- Isolation still protects the orchestrator branch; parallelism is unchanged.
- Copy-based integrate can miss ignored build artifacts by design; status is the checklist.
- OMP/Cursor adapters document fallbacks instead of assuming native runners always start.
