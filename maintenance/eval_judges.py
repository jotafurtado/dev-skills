"""Pluggable judges for the skill evaluation harness."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

INFRASTRUCTURE_KINDS = frozenset(
    {"rate_limit", "timeout", "missing_credentials", "provider", "protocol"}
)

_STOP = frozenset(
    """
    a an the and or of to for in on at by with from as is are was be this that
    those these it its when use uses using do not don't than into over per via
    only also our your their them they we you before after without
    """.split()
)

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class InfrastructureError(Exception):
    """Host, provider, or protocol failure; excluded from skill pass-rate."""

    def __init__(
        self,
        kind: str,
        message: str = "",
        *,
        raw: str | None = None,
        preserve_output: bool = False,
        finish_reason: str | None = None,
        total_tokens: int | None = None,
    ) -> None:
        if kind not in INFRASTRUCTURE_KINDS:
            raise ValueError(f"unknown infrastructure kind: {kind}")
        super().__init__(message or kind)
        self.kind = kind
        self.raw = raw
        self.preserve_output = preserve_output
        self.finish_reason = finish_reason
        self.total_tokens = total_tokens


class Judge(ABC):
    usage_tokens: int | None = None

    @abstractmethod
    def select_skills(self, query: str, available_skills: list[str]) -> list[str]:
        raise NotImplementedError

    def complete(
        self,
        prompt: str,
        skill_name: str | None,
        files: list[str],
    ) -> dict[str, Any]:
        return {
            "text": f"response for {skill_name or 'baseline'}",
            "model": None,
            "total_tokens": None,
        }

    @abstractmethod
    def grade_output(
        self,
        prompt: str,
        assertions: list[str],
        skill_name: str | None,
        files: list[str],
        output_text: str,
    ) -> dict[str, Any]:
        raise NotImplementedError


def tokenize(text: str) -> list[str]:
    normalized = text.replace("/", " ").replace("_", " ")
    pieces: list[str] = []
    for token in _WORD.findall(normalized.lower()):
        pieces.append(token)
        pieces.extend(part for part in re.split(r"[-/]", token) if part)
        if token.endswith("s") and len(token) > 4:
            pieces.append(token[:-1])
    for part in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", normalized):
        pieces.append(part.lower())
    tokens: list[str] = []
    for piece in pieces:
        if piece in _STOP:
            continue
        if len(piece) == 1 and not piece.isdigit():
            continue
        tokens.append(piece)
    return tokens


def overlap_score(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.0
    left_set, right_set = set(left), set(right)
    return len(left_set & right_set) / len(left_set)


def parse_skill_markdown(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.S)
    if not match:
        return "", content
    frontmatter, body = match.group(1), match.group(2)
    description = ""
    desc_match = re.search(r"^description:\s*(.*)$", frontmatter, re.M)
    if desc_match:
        description = desc_match.group(1).strip()
        if len(description) >= 2 and description[0] in {'"', "'"} and description[-1] == description[0]:
            description = description[1:-1]
    return description, body


def _split_sentences(text: str) -> list[str]:
    return [part.strip() for part in _SENTENCE_SPLIT.split(text.strip()) if part.strip()]


def _negative_chunks(sentence: str) -> list[str]:
    body = re.sub(r"^do not trigger\s*(?:for\s*)?", "", sentence, flags=re.I)
    body = re.sub(r"^do not\s+", "", body, flags=re.I)
    body = re.sub(r"\s+is not a trigger\.?$", "", body, flags=re.I)
    chunks = re.split(r";\s*|\s*,\s+or for\s+|\s*,\s+for\s+", body)
    return [chunk.strip(" .") for chunk in chunks if chunk.strip(" .")]


def description_clauses(description: str) -> tuple[list[str], list[str]]:
    positives: list[str] = []
    negatives: list[str] = []
    for sentence in _split_sentences(description):
        lowered = sentence.lower()
        if (
            lowered.startswith("do not")
            or "do not trigger" in lowered
            or "is not a trigger" in lowered
            or lowered.startswith("don't")
        ):
            negatives.extend(_negative_chunks(sentence))
        else:
            positives.append(sentence)
    return positives, negatives


def _unless_satisfied(clause: str, query: str) -> bool:
    match = re.search(r"\bunless\b(.+)$", clause, flags=re.I)
    if not match:
        return False
    unless_text = re.split(r",\s+(?:for|or)\b", match.group(1), maxsplit=1)[0]
    unless_tokens = tokenize(unless_text)
    query_tokens = set(tokenize(query))
    if overlap_score(tokenize(query), unless_tokens) >= 0.34:
        return True
    unless_nums = {token for token in unless_tokens if token.isdigit()}
    query_nums = {token for token in query_tokens if token.isdigit()}
    return bool(unless_nums) and unless_nums <= query_nums and overlap_score(tokenize(query), unless_tokens) >= 0.12


def negative_applies(clause: str, query: str) -> bool:
    if _unless_satisfied(clause, query):
        return False
    without = re.search(r"\bwithout\b(.+)$", clause, flags=re.I)
    if without and overlap_score(tokenize(query), tokenize(without.group(1))) >= 0.28:
        return False
    core = re.split(r"\bunless\b", clause, maxsplit=1, flags=re.I)[0]
    if without and overlap_score(tokenize(query), tokenize(without.group(1))) < 0.28:
        head_tokens = tokenize(re.split(r"\bwithout\b", core, maxsplit=1, flags=re.I)[0])
        if set(tokenize(query)) & set(head_tokens):
            return True
    query_tokens = tokenize(query)
    clause_tokens = tokenize(core)
    if overlap_score(query_tokens, clause_tokens) >= 0.42:
        return True
    distinctive = [token for token in set(clause_tokens) if token not in {"earlier", "stacks", "mentions", "alone", "work"}]
    if len(set(query_tokens) & set(distinctive)) >= 3:
        return True
    for product, version in re.findall(r"([a-z]{3,})\s+(\d+)", core.lower()):
        if f"{product} {version}" in query.lower():
            return True
    lowered = query.lower()
    phrases = [
        phrase.strip()
        for phrase in re.findall(r"[a-z0-9][a-z0-9\- ]{5,}", core.lower())
        if len(phrase.strip()) >= 10
    ]
    return any(phrase in lowered for phrase in phrases)


def positive_score(query: str, positives: list[str]) -> float:
    if not positives:
        return 0.0
    query_tokens = tokenize(query)
    combined = tokenize(" ".join(positives))
    per_clause = [overlap_score(query_tokens, tokenize(item)) for item in positives]
    return max(overlap_score(query_tokens, combined), max(per_clause) if per_clause else 0.0)


class MockJudge(Judge):
    """Deterministic stand-in for tests. Results are simulated, not agent evidence."""

    KEYWORD_MAP: dict[str, str] = {
        "filament": "laravel-filament-v5",
        "orderresource": "laravel-filament-v5",
        "fileupload": "laravel-filament-v5",
        "importaction": "laravel-filament-v5",
        "exportaction": "laravel-filament-v5",
        "statsoverviewwidget": "laravel-filament-v5",
        "infolist": "laravel-filament-v5",
        "textentry": "laravel-filament-v5",
        "composition": "laravel-filament-v5-ui-ux",
        "responsive": "laravel-filament-v5-ui-ux",
        "layout": "laravel-filament-v5-ui-ux",
        "polish": "laravel-filament-v5-ui-ux",
        "nova": "laravel-nova-5",
        "commit": "prepare-commit",
        "changelog": "prepare-commit",
        "sdd": "sdd-workflow",
        "spec-driven": "sdd-workflow",
        "subagent": "implement-with-subagents",
        "workpool": "implement-with-subagents",
    }

    NEGATIVE_HINTS: dict[str, tuple[str, ...]] = {
        "laravel-filament-v5": ("polish", "tailwind", "react dashboard", "generic laravel admin"),
        "laravel-filament-v5-ui-ux": ("migrate these filament\\tables\\actions", "bulk approve action"),
        "laravel-nova-5": ("nova 4", "between two confirmed nova 4"),
    }

    RATE_LIMIT_MARKER = "__eval_rate_limit__"

    def select_skills(self, query: str, available_skills: list[str]) -> list[str]:
        self.usage_tokens = None
        if self.RATE_LIMIT_MARKER in query:
            raise InfrastructureError("rate_limit", "simulated rate limit")

        lowered = query.lower()
        selected: list[str] = []
        for keyword, skill in self.KEYWORD_MAP.items():
            if skill not in available_skills:
                continue
            if keyword in lowered and skill not in selected:
                hints = self.NEGATIVE_HINTS.get(skill, ())
                if any(hint in lowered for hint in hints):
                    continue
                selected.append(skill)
        return selected

    def complete(
        self,
        prompt: str,
        skill_name: str | None,
        files: list[str],
    ) -> dict[str, Any]:
        self.usage_tokens = None
        if self.RATE_LIMIT_MARKER in prompt:
            raise InfrastructureError("rate_limit", "simulated rate limit")
        label = skill_name or "baseline"
        return {
            "text": f"mock response for {label} ({'with_skill' if skill_name else 'no_skill'})",
            "model": "mock",
            "total_tokens": None,
            "evidence_mode": "simulated",
        }

    def grade_output(
        self,
        prompt: str,
        assertions: list[str],
        skill_name: str | None,
        files: list[str],
        output_text: str,
    ) -> dict[str, Any]:
        self.usage_tokens = None
        if self.RATE_LIMIT_MARKER in prompt:
            raise InfrastructureError("rate_limit", "simulated rate limit")

        assertion_results = []
        for assertion in assertions:
            passed = skill_name is not None and "without" not in assertion.lower()
            if skill_name is None:
                passed = False
            if "review-only" in assertion.lower() and "review only" in prompt.lower():
                passed = skill_name is not None
            assertion_results.append(
                {
                    "text": assertion,
                    "passed": passed,
                    "evidence": "simulated: deterministic stand-in; not a quote from agent output",
                }
            )

        passed_count = sum(1 for item in assertion_results if item["passed"])
        total = len(assertion_results)
        return {
            "assertion_results": assertion_results,
            "summary": {
                "passed": passed_count,
                "failed": total - passed_count,
                "total": total,
                "pass_rate": (passed_count / total) if total else 0.0,
            },
            "counts_as_skill_grade": True,
            "evidence_mode": "simulated",
        }


class DescriptionJudge(Judge):
    """Offline activator that scores queries against SKILL.md description clauses."""

    TRIGGER_THRESHOLD = 0.16

    def __init__(self, skills_dir: Path) -> None:
        self.skills_dir = skills_dir
        self.catalog: dict[str, dict[str, Any]] = {}
        if not skills_dir.is_dir():
            return
        for path in sorted(skills_dir.iterdir()):
            skill_md = path / "SKILL.md"
            if not path.is_dir() or not skill_md.is_file():
                continue
            description, body = parse_skill_markdown(skill_md)
            positives, negatives = description_clauses(description)
            self.catalog[path.name] = {
                "description": description,
                "body": body,
                "positives": positives,
                "negatives": negatives,
            }

    def select_skills(self, query: str, available_skills: list[str]) -> list[str]:
        self.usage_tokens = None
        scored: list[tuple[float, str]] = []
        query_tokens = set(tokenize(query))
        generic = {"from", "based", "with", "laravel", "workflow", "using"}
        for name in available_skills:
            record = self.catalog.get(name)
            if not record:
                continue
            if any(negative_applies(clause, query) for clause in record["negatives"]):
                continue
            score = positive_score(query, record["positives"])
            distinct = [
                token
                for token in tokenize(name.replace("-", " "))
                if len(token) >= 3 and token not in generic
            ]
            anchors = set(distinct)
            for sentence in record["positives"]:
                for word in re.findall(r"\b[A-Z][A-Za-z0-9-]{2,}\b", sentence):
                    anchors.add(word.lower())
            for token in tokenize(record["description"]):
                if "-" in token:
                    anchors.add(token)
            if not (query_tokens & anchors) and name not in query.replace("/", " "):
                continue
            if query_tokens & set(distinct):
                score = max(score, 0.22)
            if score >= self.TRIGGER_THRESHOLD:
                scored.append((score, name))
        scored.sort(reverse=True)
        return [name for _, name in scored]

    def complete(
        self,
        prompt: str,
        skill_name: str | None,
        files: list[str],
    ) -> dict[str, Any]:
        self.usage_tokens = None
        return {
            "text": (
                "Offline description activator. This is not an agent transcript "
                "and it does not apply the skill to the prompt."
            ),
            "model": "description",
            "total_tokens": None,
            "evidence_mode": "offline",
        }

    def grade_output(
        self,
        prompt: str,
        assertions: list[str],
        skill_name: str | None,
        files: list[str],
        output_text: str,
    ) -> dict[str, Any]:
        self.usage_tokens = None
        return {
            "assertion_results": [
                {
                    "text": assertion,
                    "passed": None,
                    "evidence": "offline: description activator does not grade agent output",
                }
                for assertion in assertions
            ],
            "summary": {
                "passed": 0,
                "failed": 0,
                "total": len(assertions),
                "pass_rate": None,
            },
            "counts_as_skill_grade": False,
            "evidence_mode": "offline",
        }


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
DEFAULT_OPENROUTER_MODEL = "google/gemini-3.5-flash-lite"
SELECT_MAX_TOKENS = 2048
GRADE_MAX_TOKENS = 4096
ANSWER_MAX_TOKENS = 8192


def _credential_from_env(environ: dict[str, str]) -> tuple[str, str | None]:
    for key in ("EVAL_SKILLS_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY"):
        value = (environ.get(key) or "").strip()
        if value:
            return value, key
    return "", None


def parse_model_json(text: str) -> Any:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\}|\[.*\])", stripped, flags=re.S)
        if match:
            return json.loads(match.group(1))
        raise


BASE_SYSTEM_INSTRUCTION = (
    "Answer the user using only this conversation. "
    "Project fixtures in the user message are the complete file context. "
    "Do not claim you ran tools, edited files, or opened anything that was not included."
)

_REFERENCE_PATH = re.compile(r"(?<![\w/`])((?:references|CONTEXT)(?:\.md|/[\w./-]+))")


def http_infrastructure_kind(code: int) -> str:
    if code in {401, 403}:
        return "missing_credentials"
    if code == 429:
        return "rate_limit"
    if code in {408, 504}:
        return "timeout"
    return "provider"


def extract_completion(body: dict[str, Any]) -> tuple[str, int | None]:
    try:
        choice = body["choices"][0]
        message = choice["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise InfrastructureError(
            "provider",
            f"completion payload missing choices: {exc}",
            raw=json.dumps(body)[:4000],
        ) from exc
    if not isinstance(message, dict):
        raise InfrastructureError("provider", "completion message is not an object", raw=json.dumps(body)[:4000])
    finish = choice.get("finish_reason")
    content = message.get("content")
    text = content if isinstance(content, str) else ""
    reasoning = message.get("reasoning")
    reasoning_text = reasoning if isinstance(reasoning, str) else ""
    usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
    tokens = usage.get("total_tokens") if isinstance(usage, dict) else None
    total_tokens = tokens if type(tokens) is int else None
    if finish == "length":
        raise InfrastructureError(
            "protocol",
            "truncated completion",
            raw=text or reasoning_text,
            preserve_output=bool(text),
            finish_reason="length",
            total_tokens=total_tokens,
        )
    if not text.strip():
        raise InfrastructureError(
            "protocol",
            "empty completion",
            raw=reasoning_text or text,
            preserve_output=False,
        )
    return text, total_tokens




def interpret_grade(raw: str, assertions: list[str], output_text: str) -> dict[str, Any]:
    if not assertions:
        raise InfrastructureError("protocol", "missing assertions", raw=raw)
    try:
        parsed = parse_model_json(raw)
    except json.JSONDecodeError as exc:
        raise InfrastructureError("protocol", f"malformed grade JSON: {exc}", raw=raw) from exc
    results = parsed.get("results") if isinstance(parsed, dict) else None
    if not isinstance(results, list):
        raise InfrastructureError("protocol", "grade JSON missing results array", raw=raw)
    source_lines = output_text.splitlines(keepends=True)
    by_id: dict[int, dict[str, Any]] = {}
    for item in results:
        if not isinstance(item, dict):
            raise InfrastructureError("protocol", "grade result is not an object", raw=raw)
        if type(item.get("passed")) is not bool:
            raise InfrastructureError("protocol", "grade passed must be a JSON boolean", raw=raw)
        assertion_id = item.get("assertion_id")
        if type(assertion_id) is not int or not 1 <= assertion_id <= len(assertions):
            raise InfrastructureError("protocol", "grade assertion id is out of range", raw=raw)
        if assertion_id in by_id:
            raise InfrastructureError("protocol", "duplicate grade result", raw=raw)
        start = item.get("evidence_start_line")
        end = item.get("evidence_end_line")
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(source_lines):
            raise InfrastructureError("protocol", "grade evidence line range is invalid", raw=raw)
        evidence = "".join(source_lines[start - 1:end])
        if not evidence.strip():
            raise InfrastructureError("protocol", "grade evidence contains only blank lines", raw=raw)
        by_id[assertion_id] = {
            "text": assertions[assertion_id - 1],
            "passed": item["passed"],
            "evidence": evidence,
            "evidence_start_line": start,
            "evidence_end_line": end,
        }
    if len(by_id) != len(assertions):
        raise InfrastructureError("protocol", "grade results do not match assertions", raw=raw)
    assertion_results = [by_id[index] for index in range(1, len(assertions) + 1)]
    passed_count = sum(1 for item in assertion_results if item["passed"])
    total = len(assertion_results)
    return {
        "assertion_results": assertion_results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": passed_count / total,
        },
        "counts_as_skill_grade": True,
        "evidence_mode": "model",
    }


def _is_skill_reference(path: str) -> bool:
    return bool(Path(path).suffix) and (path == "CONTEXT.md" or path.startswith("references/"))


def _paths_in(text: str) -> list[str]:
    found: list[str] = []
    for match in _REFERENCE_PATH.finditer(text):
        path = match.group(1).rstrip(".,)")
        if path not in found:
            found.append(path)
    return found


def _content_tokens(text: str) -> list[str]:
    return [token for token in tokenize(text) if len(token) >= 4]


def _tokens_align(left: str, right: str) -> bool:
    if left == right:
        return True
    return len(left) >= 5 and len(right) >= 5 and (left.startswith(right) or right.startswith(left))


def route_matches(blurb: str, prompt: str) -> bool:
    prompt_tokens = _content_tokens(prompt)
    fragments = [part.strip() for part in re.split(r"[,;]|—|–", blurb) if part.strip()]
    if not fragments:
        fragments = [blurb]
    for fragment in fragments:
        tokens = _content_tokens(fragment)
        if not tokens:
            continue
        shared = [token for token in tokens if any(_tokens_align(token, other) for other in prompt_tokens)]
        if not shared:
            continue
        if any(len(token) >= 8 for token in shared):
            return True
        ratio = len(shared) / len(tokens)
        if len(tokens) <= 3 and ratio >= 0.5:
            return True
        if len(tokens) > 3 and (ratio >= 0.34 or any(len(token) >= 5 for token in shared)):
            return True
    return False


def routing_entries(skill_md: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    lines = skill_md.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        bullet = re.match(r"^[-*] \[[^\]]+\]\(([^)]+)\)\s*:?\s*(.*)$", line)
        if bullet:
            path = bullet.group(1).strip()
            title_match = re.match(r"^[-*] \[([^\]]+)\]", line)
            title = title_match.group(1) if title_match else ""
            blurb_lines = [bullet.group(2)]
            nxt = index + 1
            while nxt < len(lines) and re.match(r"^\s+\S", lines[nxt]):
                blurb_lines.append(lines[nxt].strip())
                nxt += 1
            if _is_skill_reference(path):
                entries.append((f"{title} {' '.join(blurb_lines)}".strip(), path))
            index = nxt
            continue
        if line.startswith("|") and not re.match(r"^\|\s*-+", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and not cells[0].lower().startswith("task") and not cells[0].lower().startswith("building"):
                blob = " ".join(cells)
                paths = _paths_in(blob)
                blurb = " ".join(cell for cell in cells if not _paths_in(cell)) or blob
                for path in paths:
                    if _is_skill_reference(path):
                        entries.append((blurb, path))
        index += 1
    for match in re.finditer(r"`((?:references/[^`]+)|CONTEXT\.md)`", skill_md):
        start = skill_md.rfind("\n", 0, match.start()) + 1
        end = skill_md.find("\n", match.end())
        sentence = skill_md[start: end if end != -1 else len(skill_md)]
        path = match.group(1)
        if _is_skill_reference(path):
            entries.append((sentence, path))
    return entries


def relevant_reference_paths(skill_dir: Path, skill_md: str, prompt: str) -> list[str]:
    selected: list[str] = []
    seen: set[str] = set()
    if re.search(r"\(CONTEXT\.md\)|`CONTEXT\.md`", skill_md) and (skill_dir / "CONTEXT.md").is_file():
        selected.append("CONTEXT.md")
        seen.add("CONTEXT.md")
    for blurb, path in routing_entries(skill_md):
        if path in seen or not route_matches(blurb, prompt):
            continue
        if not (skill_dir / path).is_file():
            raise InfrastructureError("protocol", f"skill cites missing reference: {path}")
        selected.append(path)
        seen.add(path)
    return selected


def skill_instruction_bundle(skills_dir: Path, skill_name: str, prompt: str) -> str:
    skill_dir = skills_dir / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.is_file():
        raise InfrastructureError("protocol", f"missing SKILL.md for {skill_name}")
    skill_md = skill_md_path.read_text(encoding="utf-8")
    parts = [skill_md.rstrip()]
    for relative in relevant_reference_paths(skill_dir, skill_md, prompt):
        text = (skill_dir / relative).read_text(encoding="utf-8").rstrip()
        parts.append(f"---\n# {relative}\n\n{text}")
    return "\n\n".join(parts)


def read_fixture(root: Path, relative: str) -> str:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise InfrastructureError("protocol", f"fixture missing or escapes repository: {relative}")
    return path.read_text(encoding="utf-8")


def completion_user_content(prompt: str, root: Path, files: list[str]) -> str:
    if not files:
        return prompt
    blocks = [
        f"----- {relative} -----\n{read_fixture(root, relative).rstrip()}\n----- end {relative} -----"
        for relative in files
    ]
    return (
        prompt
        + "\n\nProject fixtures (complete file contents; this is the entire project context):\n\n"
        + "\n\n".join(blocks)
    )


def completion_messages(skill_bundle: str | None, user_content: str) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": BASE_SYSTEM_INSTRUCTION}]
    if skill_bundle is not None:
        messages.append(
            {
                "role": "system",
                "content": "Follow this skill for the answer.\n\n" + skill_bundle,
            }
        )
    messages.append({"role": "user", "content": user_content})
    return messages


class LiveJudge(Judge):
    """OpenAI-compatible chat judge. Skips when credentials are missing."""

    def __init__(
        self,
        skills_dir: Path,
        env: dict[str, str] | None = None,
        root: Path | None = None,
    ) -> None:
        environ = env if env is not None else os.environ
        self.skills_dir = skills_dir
        self.root = skills_dir.parent if root is None else root
        self.api_key, source = _credential_from_env(environ)
        explicit_base = (environ.get("EVAL_SKILLS_BASE_URL") or "").rstrip("/")
        if explicit_base:
            self.base_url = explicit_base
        elif source == "OPENROUTER_API_KEY":
            self.base_url = OPENROUTER_BASE_URL
        else:
            self.base_url = "https://api.openai.com/v1"
        default_model = (
            DEFAULT_OPENROUTER_MODEL
            if "openrouter.ai" in self.base_url
            else DEFAULT_OPENAI_MODEL
        )
        self.model = environ.get("EVAL_SKILLS_MODEL") or default_model
        self._descriptions = DescriptionJudge(skills_dir)

    def _require(self) -> None:
        if not self.api_key:
            raise InfrastructureError(
                "missing_credentials",
                "EVAL_SKILLS_API_KEY, OPENAI_API_KEY, or OPENROUTER_API_KEY is not set",
            )

    def _chat(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = ANSWER_MAX_TOKENS,
    ) -> tuple[str, int | None]:
        self._require()
        payload_obj: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "max_tokens": max_tokens,
        }
        if "openrouter.ai" in self.base_url:
            payload_obj["reasoning"] = {"effort": "low"}
        payload = json.dumps(payload_obj).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if "openrouter.ai" in self.base_url:
            headers["HTTP-Referer"] = "https://github.com/jotafurtado/dev-skills"
            headers["X-Title"] = "dev-skills eval harness"
        last_error: Exception | None = None
        for attempt in range(4):
            request = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=payload,
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    raw_body = response.read().decode("utf-8")
                try:
                    body = json.loads(raw_body)
                except json.JSONDecodeError as exc:
                    raise InfrastructureError(
                        "provider",
                        f"completion response is not JSON: {exc}",
                        raw=raw_body[:4000],
                    ) from exc
                break
            except InfrastructureError:
                raise
            except urllib.error.HTTPError as error:
                last_error = error
                if error.code == 429 and attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                detail = error.read().decode("utf-8", errors="replace")
                raise InfrastructureError(
                    http_infrastructure_kind(error.code),
                    f"HTTP {error.code}: {detail or error}",
                    raw=detail,
                ) from error
            except urllib.error.URLError as error:
                last_error = error
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                raise InfrastructureError("timeout", str(error)) from error
        else:
            raise InfrastructureError("timeout", str(last_error))

        usage = body.get("usage") if isinstance(body, dict) else None
        tokens = usage.get("total_tokens") if isinstance(usage, dict) else None
        self.usage_tokens = tokens if type(tokens) is int else None
        text, tokens = extract_completion(body)
        return text, tokens

    def build_completion_request(
        self,
        prompt: str,
        skill_name: str | None,
        files: list[str],
    ) -> list[dict[str, str]]:
        bundle = skill_instruction_bundle(self.skills_dir, skill_name, prompt) if skill_name else None
        user = completion_user_content(prompt, self.root, files)
        return completion_messages(bundle, user)

    def select_skills(self, query: str, available_skills: list[str]) -> list[str]:
        self.usage_tokens = None
        catalog = []
        for name in available_skills:
            record = self._descriptions.catalog.get(name)
            if record:
                catalog.append(f"- {name}: {record['description']}")
        messages = [
            {
                "role": "system",
                "content": (
                    "Select which agent skills should load for the user query. "
                    "Reply with a JSON array of skill names, nothing else. "
                    "Honor each description's use-when and do-not clauses."
                ),
            },
            {
                "role": "user",
                "content": "Skills:\n" + "\n".join(catalog) + "\n\nQuery:\n" + query,
            },
        ]
        text, tokens = self._chat(messages, max_tokens=SELECT_MAX_TOKENS)
        self.usage_tokens = tokens
        try:
            parsed = parse_model_json(text)
        except json.JSONDecodeError as exc:
            raise InfrastructureError(
                "protocol",
                f"malformed skill selection JSON: {exc}",
                raw=text,
            ) from exc
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise InfrastructureError(
                "protocol",
                "skill selection JSON must be an array of strings",
                raw=text,
            )
        return [name for name in parsed if name in available_skills]

    def complete(
        self,
        prompt: str,
        skill_name: str | None,
        files: list[str],
    ) -> dict[str, Any]:
        self.usage_tokens = None
        messages = self.build_completion_request(prompt, skill_name, files)
        text, tokens = self._chat(messages, max_tokens=ANSWER_MAX_TOKENS)
        self.usage_tokens = tokens
        return {
            "text": text,
            "model": self.model,
            "total_tokens": tokens,
            "evidence_mode": "model",
        }

    def grade_output(
        self,
        prompt: str,
        assertions: list[str],
        skill_name: str | None,
        files: list[str],
        output_text: str,
    ) -> dict[str, Any]:
        self.usage_tokens = None
        if not assertions:
            raise InfrastructureError("protocol", "missing assertions")
        listed = "\n".join(f"{index}: {item}" for index, item in enumerate(assertions, start=1))
        numbered_output = "\n".join(f"{index}: {line}" for index, line in enumerate(output_text.splitlines(), start=1))
        text, tokens = self._chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Grade the agent output against each assertion. "
                        'Return JSON: {"results": [{"assertion_id": int, "passed": bool, '
                        '"evidence_start_line": int, "evidence_end_line": int}]}. '
                        "Use the assertion IDs and inclusive 1-based output line numbers. "
                        "Include exactly one result per assertion; passed must be a JSON boolean. "
                        "Select the actual output lines supporting the verdict; do not recopy "
                        "assertion text or quotes. For an absent requirement, mark false and "
                        "select the closest relevant output lines rather than inventing evidence. "
                        "Evaluate only observable response content. This is an isolated prompt "
                        "with no tools: claims of running checks, editing files, or producing a "
                        "real commit are not execution evidence. "
                    ),
                },
                {
                    "role": "user",
                    "content": f"Prompt:\n{completion_user_content(prompt, self.root, files)}\n\nNumbered output:\n{numbered_output}\n\nAssertions:\n{listed}",
                },
            ],
            max_tokens=GRADE_MAX_TOKENS,
        )
        self.usage_tokens = tokens
        graded = interpret_grade(text, assertions, output_text)
        graded["raw_reply"] = text
        return graded


def load_judge(name: str, skills_dir: Path, env: dict[str, str] | None = None) -> Judge:
    if name == "mock":
        return MockJudge()
    if name == "description":
        return DescriptionJudge(skills_dir)
    if name == "live":
        return LiveJudge(skills_dir, env=env)
    raise ValueError(f"unknown judge: {name}")
