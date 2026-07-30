#!/usr/bin/env python3
"""Run the behavioral eval prompts in a disposable paired agent installation.

The script records raw model output; a maintainer must review every assertion before
marking a release as passed. It deliberately does not let a model self-certify a pass.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path


SKILLS = ("laravel-filament-5-ui-ux", "laravel-filament-v5")
AGENT_COMMANDS = {
    "codex": ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only"],
    "claude-code": ["claude", "--print", "--permission-mode", "dontAsk", "--tools", ""],
}


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def prompt_for_eval(prompt: str) -> str:
    return (
        "Use the installed Filament skills. This is a read-only behavioral evaluation. "
        "Do not modify files. Give a concise visual decision trace, cite local reviewed "
        "catalog evidence, cover responsive and accessibility treatment, and route exact "
        "installed-version APIs, security, implementation, and tests to laravel-filament-v5.\n\n"
        + prompt
    )


def write_report(path: Path, agent: str, source: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "agent": agent,
                "recorded_at": datetime.now(UTC).isoformat(),
                "source": str(source),
                "review_required": True,
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
            completed = run(AGENT_COMMANDS[args.agent] + [prompt_for_eval(item["prompt"])], workspace)
            records.append(
                {
                    "id": item["id"],
                    "status": "recorded" if completed.returncode == 0 else "failed",
                    "assertions": item["assertions"],
                    "transcript": completed.stdout,
                    "stderr": completed.stderr,
                }
            )
            write_report(args.output, args.agent, source, records)

    write_report(args.output, args.agent, source, records)
    return 0 if all(record["status"] == "recorded" for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
