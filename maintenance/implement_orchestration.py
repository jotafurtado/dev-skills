"""Testable orchestration helpers for implement-with-subagents."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Protocol


class ReviewVerdict(str, Enum):
    PASS = "pass"
    P0 = "p0"
    SPEC_FAIL = "spec-fail"


@dataclass(frozen=True)
class GitStatusEntry:
    code: str
    path: str


@dataclass
class WorkerResult:
    outcome: str
    files_touched: list[str] = field(default_factory=list)
    worktree_head: str = ""
    start_head: str = ""
    status_entries: list[GitStatusEntry] = field(default_factory=list)
    error: str | None = None


@dataclass
class Ticket:
    id: str
    slug: str
    labels: set[str] = field(default_factory=set)
    blockers: list[str] = field(default_factory=list)
    acceptance: list[bool] = field(default_factory=list)
    status: str = ""
    comments: list[str] = field(default_factory=list)
    requires_work: bool = True

    @property
    def ready_for_agent(self) -> bool:
        return "ready-for-agent" in self.labels


@dataclass
class ReviewResult:
    verdict: ReviewVerdict
    findings: list[str] = field(default_factory=list)


@dataclass
class IntegrateResult:
    ok: bool
    copied_paths: list[str] = field(default_factory=list)
    skipped_paths: list[str] = field(default_factory=list)
    deleted_paths: list[str] = field(default_factory=list)
    reason: str | None = None


@dataclass
class PostWorkerResult:
    integrated: bool
    committed: bool
    commit_sha: str | None = None
    ready_for_agent_restored: bool = False
    marked_done: bool = False
    reason: str | None = None


@dataclass
class WaveResult:
    spawned: list[str]
    results: dict[str, WorkerResult]
    aborted_early: bool = False


class Tracker(Protocol):
    def get_ticket(self, ticket_id: str) -> Ticket: ...
    def list_tickets(self) -> list[Ticket]: ...
    def claim(self, ticket_id: str) -> bool: ...
    def restore_ready_for_agent(self, ticket_id: str, reason: str) -> None: ...
    def mark_done(self, ticket_id: str, commit_sha: str) -> None: ...


class HostAdapter(Protocol):
    def spawn_worker(self, ticket: Ticket) -> WorkerResult: ...
    def orchestrator_head(self) -> str: ...
    def git_log_shas(self) -> list[str]: ...
    def path_exists(self, relative_path: str) -> bool: ...
    def path_content(self, relative_path: str) -> str | None: ...
    def copy_from_worktree(self, ticket_id: str, relative_path: str, content: str) -> None: ...
    def delete_orchestrator_path(self, relative_path: str) -> None: ...
    def run_tests(self, ticket_id: str) -> bool: ...
    def run_review(self, ticket_id: str, fixed_point: str) -> ReviewResult: ...
    def commit(self, ticket_id: str, message: str) -> str | None: ...
    def attempt_branch_merge(self, ticket_id: str) -> tuple[bool, str]: ...


def blocker_is_complete(blocker: Ticket) -> bool:
    if blocker.status.lower() == "resolved":
        return True
    if blocker.acceptance and all(blocker.acceptance):
        return True
    if blocker.ready_for_agent:
        return False
    if blocker.status.lower() == "claimed":
        return False
    return False


def compute_frontier(tracker: Tracker) -> list[Ticket]:
    frontier: list[Ticket] = []
    for ticket in tracker.list_tickets():
        if not ticket.ready_for_agent:
            continue
        if all(blocker_is_complete(tracker.get_ticket(blocker_id)) for blocker_id in ticket.blockers):
            frontier.append(ticket)
    return sorted(frontier, key=lambda item: item.id)


def should_integrate(worker: WorkerResult) -> bool:
    return worker.outcome == "success"


def is_junk_path(relative_path: str) -> bool:
    path = PurePosixPath(relative_path.replace("\\", "/"))
    if "node_modules" in path.parts:
        return True
    if path.name in {".DS_Store", "Thumbs.db", ".env"}:
        return True
    if path.name.startswith(".env.") and path.name != ".env.example":
        return True
    return False


def classify_status_entries(entries: list[GitStatusEntry]) -> tuple[list[str], list[str], list[str]]:
    copy_paths: list[str] = []
    skip_paths: list[str] = []
    delete_paths: list[str] = []
    for entry in entries:
        if is_junk_path(entry.path):
            skip_paths.append(entry.path)
            continue
        code = entry.code.strip()
        if code.startswith("D"):
            delete_paths.append(entry.path)
        elif code.startswith("R"):
            old_path, _, new_path = entry.path.partition(" -> ")
            delete_paths.append(old_path)
            copy_paths.append(new_path or entry.path)
        elif code.startswith("?"):
            copy_paths.append(entry.path)
        else:
            copy_paths.append(entry.path)
    return copy_paths, skip_paths, delete_paths


def dirty_tree_integrate(ticket: Ticket, worker: WorkerResult, host: HostAdapter, tracker: Tracker) -> IntegrateResult:
    if worker.outcome != "success":
        return IntegrateResult(ok=False, reason="worker not successful")
    if worker.worktree_head != worker.start_head:
        tracker.restore_ready_for_agent(ticket.id, "worker committed in worktree")
        return IntegrateResult(ok=False, reason="worker committed")

    copy_paths, skip_paths, delete_paths = classify_status_entries(worker.status_entries)
    actionable = copy_paths or delete_paths
    merge_ok, merge_message = host.attempt_branch_merge(ticket.id)
    if ticket.requires_work and not actionable:
        if merge_ok:
            tracker.restore_ready_for_agent(ticket.id, merge_message)
            return IntegrateResult(ok=False, reason=merge_message)
        tracker.restore_ready_for_agent(ticket.id, "empty worktree status")
        return IntegrateResult(ok=False, reason="empty dirty tree")

    for relative_path in delete_paths:
        host.delete_orchestrator_path(relative_path)
    for relative_path in copy_paths:
        content = host.path_content(relative_path)
        if content is None:
            tracker.restore_ready_for_agent(ticket.id, f"missing worktree path {relative_path}")
            return IntegrateResult(ok=False, reason=f"missing path {relative_path}")
        host.copy_from_worktree(ticket.id, relative_path, content)
    for relative_path in copy_paths:
        if not host.path_exists(relative_path):
            tracker.restore_ready_for_agent(ticket.id, f"completeness check failed for {relative_path}")
            return IntegrateResult(ok=False, reason=f"completeness check failed for {relative_path}")

    return IntegrateResult(ok=True, copied_paths=copy_paths, skipped_paths=skip_paths, deleted_paths=delete_paths)


def review_blocks_commit(review: ReviewResult) -> bool:
    return review.verdict in {ReviewVerdict.P0, ReviewVerdict.SPEC_FAIL}


def commit_sha_is_new(previous_head: str, git_log: list[str]) -> bool:
    return bool(git_log) and git_log[0] != previous_head


def can_mark_ticket_done(previous_head: str, git_log: list[str], commit_sha: str | None) -> bool:
    return bool(commit_sha) and bool(git_log) and commit_sha == git_log[0] and commit_sha_is_new(previous_head, git_log)


def post_worker_phase(ticket: Ticket, worker: WorkerResult, host: HostAdapter, tracker: Tracker) -> PostWorkerResult:
    if not should_integrate(worker):
        return PostWorkerResult(integrated=False, committed=False, reason="worker unsuccessful")

    fixed_point = host.orchestrator_head()
    integrate = dirty_tree_integrate(ticket, worker, host, tracker)
    if not integrate.ok:
        return PostWorkerResult(integrated=False, committed=False, ready_for_agent_restored=True, reason=integrate.reason)
    if not host.run_tests(ticket.id):
        tracker.restore_ready_for_agent(ticket.id, "tests failed after integrate")
        return PostWorkerResult(integrated=True, committed=False, ready_for_agent_restored=True, reason="tests failed")

    review = host.run_review(ticket.id, fixed_point)
    if review_blocks_commit(review):
        tracker.restore_ready_for_agent(ticket.id, f"review {review.verdict.value}")
        return PostWorkerResult(integrated=True, committed=False, ready_for_agent_restored=True, reason=f"review {review.verdict.value}")

    commit_sha = host.commit(ticket.id, f"feat({ticket.slug}): implement {ticket.id}")
    git_log = host.git_log_shas()
    if not can_mark_ticket_done(fixed_point, git_log, commit_sha):
        tracker.restore_ready_for_agent(ticket.id, "commit SHA not on git log")
        return PostWorkerResult(integrated=True, committed=False, ready_for_agent_restored=True, reason="missing commit SHA")

    tracker.mark_done(ticket.id, commit_sha)
    return PostWorkerResult(integrated=True, committed=True, commit_sha=commit_sha, marked_done=True)


def run_wave(frontier: list[Ticket], host: HostAdapter, tracker: Tracker) -> WaveResult:
    spawned: list[str] = []
    results: dict[str, WorkerResult] = {}
    for ticket in frontier:
        if not tracker.claim(ticket.id):
            continue
        results[ticket.id] = host.spawn_worker(ticket)
        spawned.append(ticket.id)
    return WaveResult(spawned=spawned, results=results, aborted_early=False)
