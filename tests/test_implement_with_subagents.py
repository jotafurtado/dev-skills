import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "maintenance"))

from implement_orchestration import (  # noqa: E402
    GitStatusEntry,
    ReviewResult,
    ReviewVerdict,
    Ticket,
    WorkerResult,
    blocker_is_complete,
    can_mark_ticket_done,
    classify_status_entries,
    commit_sha_is_new,
    compute_frontier,
    dirty_tree_integrate,
    post_worker_phase,
    run_wave,
    should_integrate,
)



class FakeTracker:
    def __init__(self, tickets: dict[str, Ticket]):
        self.tickets = tickets
        self.restored: list[tuple[str, str]] = []
        self.done: list[tuple[str, str]] = []

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self.tickets[ticket_id]

    def list_tickets(self) -> list[Ticket]:
        return list(self.tickets.values())

    def claim(self, ticket_id: str) -> bool:
        ticket = self.tickets[ticket_id]
        if "ready-for-agent" not in ticket.labels:
            return False
        ticket.labels.discard("ready-for-agent")
        ticket.comments.append("claimed by implement-with-subagents")
        return True

    def restore_ready_for_agent(self, ticket_id: str, reason: str) -> None:
        ticket = self.tickets[ticket_id]
        ticket.labels.add("ready-for-agent")
        ticket.comments.append(reason)
        self.restored.append((ticket_id, reason))

    def mark_done(self, ticket_id: str, commit_sha: str) -> None:
        ticket = self.tickets[ticket_id]
        ticket.acceptance = [True] * max(len(ticket.acceptance), 1)
        ticket.comments.append(f"done {commit_sha}")
        self.done.append((ticket_id, commit_sha))


class FakeHost:
    def __init__(
        self,
        *,
        workers: dict[str, WorkerResult] | None = None,
        worktree_files: dict[str, str] | None = None,
        head: str = "abc111",
        git_log: list[str] | None = None,
        review: ReviewResult | None = None,
        commit_sha: str | None = None,
        merge_message: str = "Already up to date",
        merge_ok: bool = True,
        tests_pass: bool = True,
    ):
        self.workers = workers or {}
        self.worktree_files = worktree_files or {}
        self.orchestrator_files: dict[str, str] = {}
        self.head = head
        self.git_log = git_log if git_log is not None else [head]
        self.review = review or ReviewResult(verdict=ReviewVerdict.PASS)
        self.commit_sha = commit_sha
        self.merge_message = merge_message
        self.merge_ok = merge_ok
        self.tests_pass = tests_pass
        self.spawn_log: list[str] = []
        self.integrated: list[str] = []
        self.commits: list[str] = []

    def spawn_worker(self, ticket: Ticket) -> WorkerResult:
        self.spawn_log.append(ticket.id)
        return self.workers[ticket.id]

    def orchestrator_head(self) -> str:
        return self.head

    def git_log_shas(self) -> list[str]:
        return list(self.git_log)

    def path_exists(self, relative_path: str) -> bool:
        return relative_path in self.orchestrator_files

    def path_content(self, relative_path: str) -> str | None:
        return self.worktree_files.get(relative_path)

    def copy_from_worktree(self, ticket_id: str, relative_path: str, content: str) -> None:
        self.orchestrator_files[relative_path] = content
        self.integrated.append(ticket_id)

    def delete_orchestrator_path(self, relative_path: str) -> None:
        self.orchestrator_files.pop(relative_path, None)

    def run_tests(self, ticket_id: str) -> bool:
        return self.tests_pass

    def run_review(self, ticket_id: str, fixed_point: str) -> ReviewResult:
        return self.review

    def commit(self, ticket_id: str, message: str) -> str | None:
        if self.commit_sha is None:
            return None
        self.commits.append(self.commit_sha)
        self.git_log = [self.commit_sha, *self.git_log]
        self.head = self.commit_sha
        return self.commit_sha

    def attempt_branch_merge(self, ticket_id: str) -> tuple[bool, str]:
        return self.merge_ok, self.merge_message


def success_worker(**overrides) -> WorkerResult:
    base = WorkerResult(
        outcome="success",
        start_head="abc111",
        worktree_head="abc111",
        status_entries=[GitStatusEntry(code="M", path="src/feature.py")],
    )
    for key, value in overrides.items():
        setattr(base, key, value)
    return base


def run_wave_abort_on_failure(frontier, host, tracker):
    """Planted counterexample: stop spawning after the first failed worker."""
    spawned: list[str] = []
    results = {}
    for ticket in frontier:
        if not tracker.claim(ticket.id):
            continue
        result = host.spawn_worker(ticket)
        spawned.append(ticket.id)
        results[ticket.id] = result
        if result.outcome == "failure":
            break
    return spawned, results



class FrontierWaveTests(unittest.TestCase):
    def test_only_unblocked_ready_for_agent_tickets_enter_wave(self):
        blocker_claimed = Ticket(
            id="01",
            slug="base",
            labels=set(),
            status="claimed",
            acceptance=[False],
        )
        blocked = Ticket(
            id="02",
            slug="needs-base",
            labels={"ready-for-agent"},
            blockers=["01"],
        )
        ready = Ticket(
            id="03",
            slug="free",
            labels={"ready-for-agent"},
            blockers=[],
        )
        tracker = FakeTracker({"01": blocker_claimed, "02": blocked, "03": ready})

        self.assertFalse(blocker_is_complete(blocker_claimed))
        self.assertEqual([ticket.id for ticket in compute_frontier(tracker)], ["03"])

        resolved_blocker = Ticket(
            id="01",
            slug="base",
            labels=set(),
            status="resolved",
            acceptance=[True],
        )
        tracker_resolved = FakeTracker(
            {
                "01": resolved_blocker,
                "02": Ticket(
                    id="02",
                    slug="needs-base",
                    labels={"ready-for-agent"},
                    blockers=["01"],
                ),
            }
        )
        self.assertEqual([ticket.id for ticket in compute_frontier(tracker_resolved)], ["02"])


class WaveIsolationTests(unittest.TestCase):
    def test_one_worker_failure_does_not_abort_successful_siblings(self):
        tickets = {
            "10": Ticket(id="10", slug="a", labels={"ready-for-agent"}),
            "11": Ticket(id="11", slug="b", labels={"ready-for-agent"}),
        }
        workers = {
            "10": WorkerResult(outcome="failure"),
            "11": success_worker(status_entries=[GitStatusEntry(code="M", path="b.py")]),
        }

        buggy_tracker = FakeTracker(deepcopy(tickets))
        buggy_host = FakeHost(workers=workers)
        buggy_spawned, buggy_results = run_wave_abort_on_failure(list(tickets.values()), buggy_host, buggy_tracker)
        self.assertEqual(buggy_spawned, ["10"])
        self.assertNotIn("11", buggy_results)

        ok_tracker = FakeTracker(deepcopy(tickets))
        ok_host = FakeHost(workers=workers)
        wave = run_wave(list(tickets.values()), ok_host, ok_tracker)
        self.assertEqual(wave.spawned, ["10", "11"])
        self.assertEqual(ok_host.spawn_log, ["10", "11"])
        self.assertEqual(wave.results["10"].outcome, "failure")
        self.assertEqual(wave.results["11"].outcome, "success")


class IntegrateSelectionTests(unittest.TestCase):
    def test_unsuccessful_workers_are_not_integrated(self):
        ticket = Ticket(id="20", slug="feat", labels={"ready-for-agent"})
        tracker = FakeTracker({"20": ticket})
        host = FakeHost(
            workers={"20": WorkerResult(outcome="failure")},
            worktree_files={"src/x.py": "change"},
        )

        result = post_worker_phase(ticket, host.workers["20"], host, tracker)
        self.assertFalse(result.integrated)
        self.assertEqual(host.integrated, [])

        tracker_ok = FakeTracker({"20": Ticket(id="20", slug="feat", labels={"ready-for-agent"})})
        host_ok = FakeHost(
            worktree_files={"src/x.py": "change"},
            commit_sha="def999",
        )
        worker = success_worker(status_entries=[GitStatusEntry(code="M", path="src/x.py")])
        ok = post_worker_phase(tracker_ok.get_ticket("20"), worker, host_ok, tracker_ok)
        self.assertTrue(ok.integrated)
        self.assertEqual(host_ok.integrated, ["20"])


class DirtyTreeIntegrateTests(unittest.TestCase):
    def test_dirty_tree_integrate_copies_non_junk_and_refuses_noop_merge(self):
        ticket = Ticket(id="30", slug="copy", labels={"ready-for-agent"})
        tracker = FakeTracker({"30": ticket})
        worker = success_worker(
            status_entries=[
                GitStatusEntry(code="M", path="src/tracked.py"),
                GitStatusEntry(code="??", path="new/untracked.txt"),
                GitStatusEntry(code="??", path="node_modules/pkg/index.js"),
                GitStatusEntry(code="??", path=".DS_Store"),
                GitStatusEntry(code="??", path=".env"),
            ]
        )
        host = FakeHost(
            worktree_files={
                "src/tracked.py": "tracked",
                "new/untracked.txt": "fresh",
                "node_modules/pkg/index.js": "skip-me",
                ".DS_Store": "skip-me",
                ".env": "secret",
            }
        )

        result = dirty_tree_integrate(ticket, worker, host, tracker)
        self.assertTrue(result.ok)
        copy_paths, skip_paths, _ = classify_status_entries(worker.status_entries)
        self.assertEqual(set(copy_paths), {"src/tracked.py", "new/untracked.txt"})
        self.assertEqual(set(skip_paths), {"node_modules/pkg/index.js", ".DS_Store", ".env"})
        self.assertEqual(host.orchestrator_files["src/tracked.py"], "tracked")
        self.assertEqual(host.orchestrator_files["new/untracked.txt"], "fresh")
        self.assertNotIn("node_modules/pkg/index.js", host.orchestrator_files)
        self.assertNotIn(".env", host.orchestrator_files)

        noop_tracker = FakeTracker({"30": ticket})
        noop_host = FakeHost(worktree_files={}, merge_message="Already up to date")
        noop_worker = success_worker(status_entries=[])
        noop = dirty_tree_integrate(ticket, noop_worker, noop_host, noop_tracker)
        self.assertFalse(noop.ok)
        self.assertEqual(noop.reason, "Already up to date")
        self.assertEqual(noop_tracker.restored, [("30", "Already up to date")])

        empty_tracker = FakeTracker({"30": ticket})
        empty_host = FakeHost(worktree_files={}, merge_ok=False)
        empty = dirty_tree_integrate(ticket, noop_worker, empty_host, empty_tracker)
        self.assertFalse(empty.ok)
        self.assertEqual(empty.reason, "empty dirty tree")


class ReviewGateTests(unittest.TestCase):
    def test_review_p0_or_spec_fail_prevents_commit_and_restores_ready_for_agent(self):
        ticket = Ticket(id="40", slug="review", labels={"ready-for-agent"})
        worker = success_worker(status_entries=[GitStatusEntry(code="M", path="src/r.py")])

        for verdict in (ReviewVerdict.P0, ReviewVerdict.SPEC_FAIL):
            tracker = FakeTracker({"40": Ticket(id="40", slug="review", labels={"ready-for-agent"})})
            host = FakeHost(
                worktree_files={"src/r.py": "body"},
                review=ReviewResult(verdict=verdict, findings=["blocked"]),
                commit_sha="should-not-exist",
            )
            result = post_worker_phase(tracker.get_ticket("40"), worker, host, tracker)
            self.assertTrue(result.integrated)
            self.assertFalse(result.committed)
            self.assertTrue(result.ready_for_agent_restored)
            self.assertEqual(host.commits, [])
            self.assertIn("ready-for-agent", tracker.get_ticket("40").labels)

        tracker_ok = FakeTracker({"40": Ticket(id="40", slug="review", labels={"ready-for-agent"})})
        host_ok = FakeHost(worktree_files={"src/r.py": "body"}, commit_sha="sha444")
        ok = post_worker_phase(tracker_ok.get_ticket("40"), worker, host_ok, tracker_ok)
        self.assertTrue(ok.committed)
        self.assertEqual(host_ok.commits, ["sha444"])


class CompletionShaTests(unittest.TestCase):
    def test_ticket_completion_requires_new_commit_sha_on_git_log(self):
        self.assertFalse(can_mark_ticket_done("abc111", ["abc111"], "abc111"))
        self.assertFalse(can_mark_ticket_done("abc111", ["abc111"], None))
        self.assertTrue(commit_sha_is_new("abc111", ["def222", "abc111"]))

        ticket = Ticket(id="50", slug="done", labels={"ready-for-agent"})
        tracker = FakeTracker({"50": ticket})
        worker = success_worker(status_entries=[GitStatusEntry(code="M", path="src/d.py")])
        host_no_commit = FakeHost(worktree_files={"src/d.py": "x"}, commit_sha=None, head="abc111", git_log=["abc111"])
        blocked = post_worker_phase(ticket, worker, host_no_commit, tracker)
        self.assertFalse(blocked.committed)
        self.assertFalse(blocked.marked_done)
        self.assertEqual(tracker.done, [])

        tracker_ok = FakeTracker({"50": Ticket(id="50", slug="done", labels={"ready-for-agent"})})
        host_ok = FakeHost(worktree_files={"src/d.py": "x"}, commit_sha="new777", head="abc111", git_log=["abc111"])
        ok = post_worker_phase(tracker_ok.get_ticket("50"), worker, host_ok, tracker_ok)
        self.assertTrue(ok.marked_done)
        self.assertEqual(tracker_ok.done, [("50", "new777")])
        self.assertEqual(host_ok.git_log_shas()[0], "new777")


class ShouldIntegrateTests(unittest.TestCase):
    def test_should_integrate_only_success(self):
        self.assertTrue(should_integrate(WorkerResult(outcome="success")))
        self.assertFalse(should_integrate(WorkerResult(outcome="failure")))


if __name__ == "__main__":
    unittest.main()
