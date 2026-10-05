import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "maintenance" / "validate_skill.mjs"
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
SKILLS = ROOT / "skills"


def run_validator(skill_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(VALIDATOR), str(skill_dir)],
        capture_output=True,
        text=True,
    )


class ValidateSkillTests(unittest.TestCase):
    def test_non_string_description_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "typed-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: typed-skill\ndescription: true\n---\n# Typed Skill\n"
            )
            result = run_validator(skill)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("description", result.stderr.lower())

    def test_yaml_types_and_duplicate_keys_are_rejected(self):
        invalid_fields = (
            "name: 123\ndescription: Example",
            "name: typed-skill\ndescription: [Example]",
            "name: typed-skill\ndescription: Example\nlicense: false",
            "name: typed-skill\ndescription: Example\ncompatibility: 123",
            "name: typed-skill\ndescription: Example\nallowed-tools: [Read]",
            "name: typed-skill\ndescription: Example\nmetadata: text",
            "name: typed-skill\ndescription: Example\nmetadata:\n  version: 1",
            "name: typed-skill\ndescription: Example\nmetadata:\n  1: value",
            'name: typed-skill\ndescription: Example\ndisable-model-invocation: "false"',
            "name: typed-skill\ndescription: First\ndescription: Second",
        )
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "typed-skill"
            skill.mkdir()
            for fields in invalid_fields:
                with self.subTest(fields=fields):
                    (skill / "SKILL.md").write_text(f"---\n{fields}\n---\n# Skill\n")
                    result = run_validator(skill)
                    self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_standard_yaml_scalars_and_metadata_are_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "typed-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                '---\r\nname: typed-skill\r\ndescription: >-\r\n'
                '  Handle <records> with "quotes".\r\n'
                '  Use when importing records.\r\n'
                'license: MIT # license comment\r\n'
                'metadata:\r\n  author: "O\'Reilly"\r\n  version: "1"\r\n'
                'allowed-tools: Read Bash(git:*)\r\n'
                'disable-model-invocation: false\r\n---\r\n# Skill\r\n',
                newline="",
            )
            result = run_validator(skill)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_valid_minimal_skill(self):
        result = run_validator(FIXTURES / "valid-minimal")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skill is valid!", result.stdout)

    def test_valid_top_level_compatibility(self):
        result = run_validator(FIXTURES / "valid-compatibility")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skill is valid!", result.stdout)

    def test_name_must_match_directory(self):
        result = run_validator(FIXTURES / "mismatched-directory")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must match the parent directory name", result.stderr)

    def test_empty_required_fields_fail(self):
        result = run_validator(FIXTURES / "empty-required-values")
        self.assertNotEqual(result.returncode, 0)

    def test_description_over_limit_fails(self):
        result = run_validator(FIXTURES / "overlimit-description")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Description is too long", result.stderr)

    def test_compatibility_over_limit_fails(self):
        result = run_validator(FIXTURES / "overlimit-compatibility")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Compatibility is too long", result.stderr)

    def test_unknown_top_level_key_fails(self):
        result = run_validator(FIXTURES / "unknown-key")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unexpected key", result.stderr)

    def test_published_skills_pass(self):
        published = sorted(path for path in SKILLS.iterdir() if path.is_dir())
        self.assertEqual(len(published), 6)
        for skill in published:
            with self.subTest(skill=skill.name):
                result = run_validator(skill)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Skill is valid!", result.stdout)



if __name__ == "__main__":
    unittest.main()
