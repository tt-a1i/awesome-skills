#!/usr/bin/env python3
"""Portable structural checks for standalone HTML design artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.has_viewport = False
        self.has_main = False
        self.title_depth = 0
        self.title_text: list[str] = []
        self.ids: list[str] = []
        self.images: list[tuple[str, str | None]] = []
        self.external_dependencies: list[str] = []
        self.button_stack: list[dict[str, object]] = []
        self.inaccessible_buttons = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = (values.get("lang") or "").strip()
        elif tag == "meta" and (values.get("name") or "").lower() == "viewport":
            self.has_viewport = bool((values.get("content") or "").strip())
        elif tag == "main":
            self.has_main = True
        elif tag == "title":
            self.title_depth += 1
        elif tag == "img":
            self.images.append((values.get("src") or "", values.get("alt")))
        elif tag == "button":
            self.button_stack.append(
                {
                    "named": bool(values.get("aria-label") or values.get("title")),
                    "text": [],
                }
            )

        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)

        dependency = ""
        if tag == "script":
            dependency = values.get("src") or ""
        elif tag == "link" and (values.get("rel") or "").lower() == "stylesheet":
            dependency = values.get("href") or ""
        if urlparse(dependency).scheme in {"http", "https"}:
            self.external_dependencies.append(dependency)

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)
        if self.button_stack:
            text = self.button_stack[-1]["text"]
            assert isinstance(text, list)
            text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        elif tag == "button" and self.button_stack:
            button = self.button_stack.pop()
            text = button["text"]
            assert isinstance(text, list)
            if not button["named"] and not "".join(text).strip():
                self.inaccessible_buttons += 1


def local_asset_path(artifact_path: Path, source: str) -> Path | None:
    parsed = urlparse(source)
    if not source or parsed.scheme in {"http", "https", "data"} or source.startswith("#"):
        return None
    if parsed.scheme == "file":
        return Path(unquote(parsed.path))
    return (artifact_path.parent / unquote(parsed.path)).resolve()


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("artifact", type=Path, help="HTML artifact to check")
    args = argument_parser.parse_args()
    artifact_path = args.artifact.expanduser().resolve()

    if not artifact_path.is_file():
        print(f"ERROR: artifact not found: {artifact_path}", file=sys.stderr)
        return 1

    html = artifact_path.read_text(encoding="utf-8")
    parser = ArtifactParser()
    parser.feed(html)
    errors: list[str] = []
    warnings: list[str] = []

    if not re.search(r"<!doctype\s+html", html, flags=re.IGNORECASE):
        errors.append("missing HTML5 doctype")
    if not parser.html_lang:
        errors.append("missing <html lang=\"…\">")
    if not parser.has_viewport:
        errors.append("missing viewport meta tag")
    if not "".join(parser.title_text).strip():
        errors.append("missing non-empty <title>")
    if not parser.has_main:
        errors.append("missing semantic <main> landmark")

    duplicate_ids = sorted(
        element_id for element_id, count in Counter(parser.ids).items() if count > 1
    )
    if duplicate_ids:
        errors.append(f"duplicate element ids: {', '.join(duplicate_ids)}")

    for source, alt in parser.images:
        if alt is None:
            errors.append(f"image missing alt attribute: {source or '<empty src>'}")
        asset_path = local_asset_path(artifact_path, source)
        if asset_path is not None and not asset_path.is_file():
            errors.append(f"missing image asset: {asset_path}")

    if parser.inaccessible_buttons:
        errors.append(f"{parser.inaccessible_buttons} button(s) have no text or accessible label")
    if parser.external_dependencies:
        warnings.append(
            f"{len(parser.external_dependencies)} remote script/stylesheet dependency path(s); verify offline behavior"
        )
    if ("<button" in html.lower() or "<a " in html.lower()) and not re.search(
        r":focus-visible|:focus\b", html, flags=re.IGNORECASE
    ):
        warnings.append("no explicit focus style found for interactive elements")

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    local_images = sum(
        local_asset_path(artifact_path, source) is not None for source, _ in parser.images
    )
    print(
        f"PASS: semantic shell present; {len(parser.images)} images "
        f"({local_images} local); {len(parser.ids)} unique ids; {len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
