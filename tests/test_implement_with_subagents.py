import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "implement-with-subagents"


class ImplementWithSubagentsPayloadTests(unittest.TestCase):
    """Runtime payload must not depend on maintainer-only repo paths."""

    def test_skill_does_not_link_source_repo_adrs(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        self.assertNotIn("docs/adr/", skill)
        self.assertIn("installer does not copy them", skill)

    def test_worker_contract_ships_a_prompt_template(self):
        contract = (SKILL_ROOT / "references" / "worker-contract.md").read_text()
        self.assertIn("## Prompt template", contract)
        self.assertIn("{absolute path to implement/SKILL.md}", contract)
        self.assertIn('"outcome": "success" | "failure"', contract)
        self.assertIn("Do not git commit", contract)

    def test_dirty_tree_procedure_is_ordered_and_complete(self):
        adapters = (SKILL_ROOT / "references" / "host-adapters.md").read_text()
        self.assertIn("### Procedure", adapters)
        self.assertIn("Completeness check", adapters)
        self.assertIn("Do **not** `git checkout` the ticket branch", adapters)
        self.assertIn("Untracked files (`??`)", adapters)
        self.assertIn("Never declare success on `Already up to date`", adapters)


if __name__ == "__main__":
    unittest.main()
