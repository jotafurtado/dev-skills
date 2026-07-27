#!/usr/bin/env python3
"""Synchronize official Filament 5 screenshot metadata without replacing review work."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import time
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_URL = "https://filamentphp.com/docs/5.x"
DEFAULT_OUTPUT = SKILL_ROOT / "references" / "screenshot-inventory.json"
SCREENSHOT_PATTERN = re.compile(
    r"<AutoScreenshot\b(?P<attributes>[^>]*)/?>", re.IGNORECASE | re.DOTALL
)
ATTRIBUTE_PATTERN = re.compile(r"(?P<key>name|alt)=[\"'](?P<value>[^\"']+)[\"']")
DOC_LINK_PATTERN = re.compile(r"href=[\"'](?P<href>/docs/5\.x/[^\"'#?]+)[\"']")
SOURCE_IDENTITY_FIELDS = ("name", "alt", "documentation", "light_image", "dark_image")


def fetch_text(url: str, *, retries: int = 3, timeout: float = 20.0) -> str:
    """Fetch a documentation page with bounded retries and explicit failures."""
    request = Request(url, headers={"User-Agent": "dev-skills-catalog-sync/1.0"})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except (OSError, URLError) as error:
            last_error = error
            if attempt + 1 < retries:
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"Could not fetch {url}: {last_error}") from last_error


def discover_markdown_pages(index_url: str, *, fetch: Callable[[str], str] = fetch_text) -> list[str]:
    """Find versioned documentation pages from the official documentation index."""
    document = fetch(index_url)
    pages = {
        "https://filamentphp.com"
        + (href if href.endswith(".md") else f"{href}.md")
        for match in DOC_LINK_PATTERN.finditer(document)
        for href in [match.group("href")]
    }
    if not pages:
        raise ValueError(f"No Filament 5 documentation pages found at {index_url}")
    return sorted(pages)


def _parse_screenshots(page_url: str, document: str) -> list[dict[str, str]]:
    screenshots: list[dict[str, str]] = []
    for tag in SCREENSHOT_PATTERN.finditer(document):
        attributes = dict(ATTRIBUTE_PATTERN.findall(tag.group("attributes")))
        name = attributes.get("name")
        if not name:
            continue
        screenshots.append(
            {
                "name": name,
                "alt": attributes.get("alt", ""),
                "documentation": page_url,
                "light_image": f"https://filamentphp.com/docs/images/5.x/light/{name}.jpg",
                "dark_image": f"https://filamentphp.com/docs/images/5.x/dark/{name}.jpg",
            }
        )
    return screenshots


def build_inventory(
    page_urls: Iterable[str],
    *,
    fetch: Callable[[str], str] = fetch_text,
    existing: dict[str, Any] | None = None,
    workers: int = 8,
) -> dict[str, Any]:
    """Build stable inventory data, retaining review fields for unchanged evidence."""
    pages = sorted(set(page_urls))
    existing_by_name = {
        item["name"]: item for item in (existing or {}).get("screenshots", [])
    }
    failures: list[str] = []

    def parse_page(url: str) -> list[dict[str, str]]:
        return _parse_screenshots(url, fetch(url))

    discovered: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {executor.submit(parse_page, url): url for url in pages}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                discovered.extend(future.result())
            except Exception as error:  # Keep all failures visible to maintainers.
                failures.append(f"{url}: {error}")

    if failures:
        raise RuntimeError("Catalog synchronization failed:\n" + "\n".join(sorted(failures)))

    screenshots: list[dict[str, Any]] = []
    for item in sorted(discovered, key=lambda value: (value["name"], value["documentation"])):
        prior = existing_by_name.get(item["name"])
        unchanged = prior and all(prior.get(key) == item[key] for key in SOURCE_IDENTITY_FIELDS)
        review = {
            key: prior[key]
            for key in ("status", "family", "variant", "decision_relevance", "notes")
            if unchanged and key in prior
        }
        screenshots.append({**item, **review} if review else {**item, "status": "unreviewed"})

    manifest = {
        page: sorted(item["name"] for item in discovered if item["documentation"] == page)
        for page in pages
    }
    return {
        "schema_version": 1,
        "crawl": {"manifest": manifest, "pages": pages, "status": "complete"},
        "screenshots": screenshots,
    }


def write_inventory(path: Path, inventory: dict[str, Any]) -> None:
    """Write canonical JSON with no volatile synchronization metadata."""
    path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize Filament 5 screenshot metadata.")
    parser.add_argument("--index-url", default=DEFAULT_INDEX_URL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    existing = json.loads(args.output.read_text()) if args.output.exists() else None
    pages = discover_markdown_pages(args.index_url)
    inventory = build_inventory(pages, existing=existing, workers=args.workers)
    write_inventory(args.output, inventory)
    print(f"Synchronized {len(inventory['screenshots'])} screenshots into {args.output}")


if __name__ == "__main__":
    main()
