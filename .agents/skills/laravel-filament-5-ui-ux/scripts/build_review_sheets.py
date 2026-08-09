#!/usr/bin/env python3
"""Build temporary, family-grouped screenshot review sheets for maintainers."""

from __future__ import annotations

import argparse
import html
import json
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


SKILL_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = SKILL_ROOT / "references" / "screenshot-inventory.json"


def download_image(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "dev-skills-catalog-review/1.0"})
    with urlopen(request, timeout=30.0) as response:
        return response.read()


def _image_filename(name: str) -> str:
    return name.replace("/", "-") + ".jpg"


def build_review_sheet(
    screenshots: list[dict[str, Any]],
    output: Path,
    *,
    download: Callable[[str], bytes] = download_image,
) -> Path:
    """Download only into `output` and write a portable, labelled HTML sheet."""
    images = output / "images"
    images.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[tuple[dict[str, Any], str]]] = defaultdict(list)
    for screenshot in sorted(screenshots, key=lambda item: (item.get("family", ""), item["name"])):
        filename = _image_filename(screenshot["name"])
        (images / filename).write_bytes(download(screenshot["light_image"]))
        grouped[screenshot.get("family") or "unclassified"].append((screenshot, filename))

    sections: list[str] = []
    for family, entries in sorted(grouped.items()):
        cards = "".join(
            "<figure><img src=\"images/{file}\" alt=\"{alt}\"><figcaption>"
            "<strong>{name}</strong><br>{status}</figcaption></figure>".format(
                file=html.escape(filename),
                alt=html.escape(item.get("alt", "")),
                name=html.escape(item["name"]),
                status=html.escape(item.get("status", "unreviewed")),
            )
            for item, filename in entries
        )
        sections.append(f"<section><h2>{html.escape(family)}</h2><div class=\"grid\">{cards}</div></section>")

    sheet = output / "index.html"
    sheet.write_text(
        "<!doctype html><meta charset=\"utf-8\"><title>Filament 5 catalog review</title>"
        "<style>body{font:16px system-ui;margin:2rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}figure{margin:0;border:1px solid #ccc;padding:1rem}img{width:100%;height:auto}figcaption{margin-top:.5rem}</style>"
        "<h1>Filament 5 catalog review</h1>" + "".join(sections) + "\n"
    )
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a temporary Filament 5 screenshot review sheet.")
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--output", type=Path, required=True, help="Temporary directory outside the repository")
    args = parser.parse_args()
    if SKILL_ROOT in args.output.resolve().parents:
        raise SystemExit("Review output must be outside the skill directory; do not store screenshot binaries in the repository.")
    screenshots = json.loads(args.inventory.read_text())["screenshots"]
    print(build_review_sheet(screenshots, args.output))


if __name__ == "__main__":
    main()
