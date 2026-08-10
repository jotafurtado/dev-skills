#!/usr/bin/env python3
"""Install the release candidate into clean agent workspaces and verify discovery."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


SKILLS = ("laravel-filament-v5-ui-ux", "laravel-filament-v5")
DEFAULT_AGENTS = ("codex", "claude-code", "cursor")


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"Command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed.stdout


def installed_skill_paths(workspace: Path, skill: str) -> list[str]:
    return sorted(str(path.relative_to(workspace)) for path in workspace.rglob(f"{skill}/SKILL.md"))


def verify_installed_presentation(workspace: Path, paths: list[str], skill: str) -> None:
    for relative_skill_path in paths:
        skill_root = workspace / Path(relative_skill_path).parent
        for entry_point in ("SKILL.md", "README.md"):
            if not (skill_root / entry_point).is_file():
                raise RuntimeError(f"{skill} is missing its universal {entry_point} entry point")

        skill_contents = (skill_root / "SKILL.md").read_text()
        if f"name: {skill}" not in skill_contents:
            raise RuntimeError(f"{skill} has an unexpected universal SKILL.md entry point")

        if skill == SKILLS[0]:
            release = skill_root / "RELEASE.md"
            if not release.is_file() or "Jota Furtado Dev Skills" not in release.read_text():
                raise RuntimeError("UI/UX release presentation lost its Jota Furtado Dev Skills grouping")


def verify_install(workspace: Path, source: Path, agent: str, skills: tuple[str, ...]) -> dict[str, object]:
    command = ["npx", "skills", "add", str(source), "--agent", agent, "--copy", "--yes"]
    for skill in skills:
        command.extend(("--skill", skill))
    run(command, workspace)

    discovered = {skill: installed_skill_paths(workspace, skill) for skill in skills}
    missing = [skill for skill, paths in discovered.items() if not paths]
    if missing:
        raise RuntimeError(f"{agent} did not discover: {', '.join(missing)}")
    for skill, paths in discovered.items():
        verify_installed_presentation(workspace, paths, skill)

    lockfile = workspace / "skills-lock.json"
    if not lockfile.is_file():
        raise RuntimeError(f"{agent} did not create skills-lock.json")
    lock = json.loads(lockfile.read_text())
    serialized_lock = json.dumps(lock)
    for skill in skills:
        if skill not in serialized_lock:
            raise RuntimeError(f"{agent} lockfile does not mention {skill}")

    if agent == "codex":
        metadata = [workspace / Path(path).parent / "agents" / "openai.yaml" for path in discovered[SKILLS[0]]]
        if not any(path.is_file() for path in metadata):
            raise RuntimeError("Codex install did not retain agents/openai.yaml metadata")

    return {
        "agent": agent,
        "skills": list(skills),
        "discovered": discovered,
        "presentation": "universal entry points and Jota Furtado Dev Skills grouping verified",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--agents", nargs="+", choices=DEFAULT_AGENTS, default=DEFAULT_AGENTS)
    args = parser.parse_args()

    source = args.source.resolve()
    if not (source / "skills" / SKILLS[0] / "SKILL.md").is_file():
        parser.error(f"{source} is not a dev-skills source checkout")
    if shutil.which("npx") is None:
        parser.error("npx is required for installation smoke tests")

    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="filament-ui-ux-release-") as temporary:
        root = Path(temporary)
        for agent in args.agents:
            for label, skills in (("separate", (SKILLS[0],)), ("paired", SKILLS)):
                workspace = root / f"{agent}-{label}"
                workspace.mkdir()
                result = verify_install(workspace, source, agent, skills)
                result["mode"] = label
                results.append(result)

    print(json.dumps({"status": "passed", "results": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
