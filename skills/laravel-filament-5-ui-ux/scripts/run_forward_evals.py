#!/usr/bin/env python3
"""Run the behavioral eval prompts in a disposable paired agent installation.

The script records raw model output; a maintainer must review every assertion before
marking a release as passed. It deliberately does not let a model self-certify a pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path


SKILLS = ("laravel-filament-5-ui-ux", "laravel-filament-v5")
AGENT_TIMEOUT_SECONDS = 180
AGENT_COMMANDS = {
    "codex": ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only"],
    "claude-code": ["claude", "--print", "--permission-mode", "plan"],
    "cursor": ["cursor", "agent", "--print", "--output-format", "json", "--mode", "ask", "--trust"],
}


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=AGENT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            command,
            124,
            stdout=exc.stdout or "",
            stderr=f"Agent timed out after {AGENT_TIMEOUT_SECONDS} seconds.",
        )


def prompt_for_eval(prompt: str) -> str:
    return (
        "Use the installed Filament skills. This is a read-only behavioral evaluation. "
        "Do not modify files. Give a concise visual decision trace, cite local reviewed "
        "catalog evidence, cover responsive and accessibility treatment, and route exact "
        "installed-version APIs, security, implementation, and tests to laravel-filament-v5.\n\n"
        + prompt
    )


def workspace_snapshot(workspace: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in workspace.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        snapshot[str(path.relative_to(workspace))] = digest
    return snapshot


def scoreable_assertions(assertions: list[str]) -> list[dict[str, str]]:
    """Wrap eval assertion strings as unscored review records."""
    return [
        {"assertion": assertion, "verdict": "unscored", "evidence": ""}
        for assertion in assertions
    ]


def review_required(records: list[dict[str, object]]) -> bool:
    """Derive whether any assertion still needs a human verdict."""
    for record in records:
        for assertion in record.get("assertions", []):
            if isinstance(assertion, dict) and assertion.get("verdict") == "unscored":
                return True
            if isinstance(assertion, str):
                return True
    return False


def write_report(path: Path, agent: str, source: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "agent": agent,
                "recorded_at": datetime.now(UTC).isoformat(),
                "source": str(source),
                "review_required": review_required(records),
                "results": records,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=tuple(AGENT_COMMANDS), required=True)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ids", nargs="*", type=int, help="Evaluate only these eval IDs")
    args = parser.parse_args()

    if shutil.which("npx") is None or shutil.which(AGENT_COMMANDS[args.agent][0]) is None:
        parser.error(f"npx and {AGENT_COMMANDS[args.agent][0]} are required")

    source = args.source.resolve()
    eval_path = source / "skills" / SKILLS[0] / "evals" / "evals.json"
    evals = json.loads(eval_path.read_text())["evals"]
    if args.ids:
        evals = [item for item in evals if item["id"] in args.ids]
    if not evals:
        parser.error("no matching evals")

    records: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="filament-ui-ux-forward-") as temporary:
        workspace = Path(temporary)
        install = ["npx", "skills", "add", str(source), "--agent", args.agent, "--copy", "--yes"]
        for skill in SKILLS:
            install.extend(("--skill", skill))
        installed = run(install, workspace)
        if installed.returncode:
            raise RuntimeError(installed.stderr or installed.stdout)

        for item in evals:
            before_snapshot = workspace_snapshot(workspace)
            completed = run(AGENT_COMMANDS[args.agent] + [prompt_for_eval(item["prompt"])], workspace)
            has_transcript = bool(completed.stdout.strip())
            workspace_changed = before_snapshot != workspace_snapshot(workspace)
            records.append(
                {
                    "id": item["id"],
                    "status": "recorded" if completed.returncode == 0 and has_transcript and not workspace_changed else "failed",
                    "assertions": scoreable_assertions(item["assertions"]),
                    "transcript": completed.stdout,
                    "stderr": completed.stderr or ("Workspace changed during evaluation." if workspace_changed else ("No transcript was produced." if not has_transcript else "")),
                    "workspace_changed": workspace_changed,
                }
            )
            write_report(args.output, args.agent, source, records)

    write_report(args.output, args.agent, source, records)
    return 0 if all(record["status"] == "recorded" for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
