#!/usr/bin/env python3
"""Locate a paired Filament skill by reading SKILL.md frontmatter.

The search order matches the directories the skills CLI writes for the agents
this repository smoke-tests (Cursor, Codex, Claude Code), plus the universal
``~/.agents/skills`` location. A directory that exists under the requested
name is not a hit unless its frontmatter ``name`` matches. There is no
fallback composition file when nothing matches.
"""

from __future__ import annotations

import re
from pathlib import Path


NAME_RE = re.compile(r"^name:\s*(\S+)\s*$", re.M)

# Project-relative skill directories. Cursor and Codex use the first;
# Claude Code uses the second.
PROJECT_SKILL_DIRS = (
    Path(".agents/skills"),
    Path(".claude/skills"),
)

# Home-relative skill directories, in the order a miss should keep searching.
HOME_SKILL_DIRS = (
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".cursor/skills"),
    Path(".codex/skills"),
)


def frontmatter_name(skill_md: Path) -> str | None:
    """Return the ``name`` field from a SKILL.md frontmatter block."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    match = NAME_RE.search(text[3:end])
    if match is None:
        return None
    return match.group(1).strip("'\"")


def discover_sibling_skill(
    name: str,
    *,
    skill_dir: Path | None = None,
    project: Path | None = None,
    home: Path | None = None,
) -> Path | None:
    """Return the first SKILL.md whose frontmatter name is ``name``.

    ``skill_dir`` is the directory of the skill already being followed. Its
    sibling is checked before project and home roots. ``None`` means no file
    matched; callers must not invent the other skill's facts.
    """
    candidates: list[Path] = []
    if skill_dir is not None:
        candidates.append(skill_dir.parent / name / "SKILL.md")
    if project is not None:
        for relative in PROJECT_SKILL_DIRS:
            candidates.append(project / relative / name / "SKILL.md")
    if home is not None:
        for relative in HOME_SKILL_DIRS:
            candidates.append(home / relative / name / "SKILL.md")

    seen: set[Path] = set()
    for path in candidates:
        try:
            key = path.resolve()
        except OSError:
            key = path
        if key in seen:
            continue
        seen.add(key)
        if path.is_file() and frontmatter_name(path) == name:
            return path
    return None
