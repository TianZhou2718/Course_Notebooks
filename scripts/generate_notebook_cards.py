#!/usr/bin/env python3
"""Generate Markdown notebook cards from structured data."""

from __future__ import annotations

import sys
from pathlib import Path
import tomllib

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "notebook_cards.toml"


def load_data() -> list[dict]:
    if not DATA_FILE.exists():
        sys.exit(f"Data file not found: {DATA_FILE}")

    with DATA_FILE.open("rb") as fh:
        raw = tomllib.load(fh)

    pages = raw.get("pages")
    if not pages:
        sys.exit("No pages defined in notebook card data.")

    return pages


def normalize_text(value: str) -> str:
    """Collapse whitespace so TOML multiline strings render cleanly."""
    return " ".join(value.strip().split())


def render_heading(card: dict) -> str:
    icon = card.get("icon", "📘")
    title = card["title"]
    
    text = f"{icon} &nbsp {title}"
    
    href = card.get("notebook_link")
    if href:
        return f'<a href="{href}"> {text}</a>'
    return text


def render_card(card: dict) -> str:
    icon = card.get("icon", "📘")
    heading = render_heading(card)
    descriptions = card.get("descriptions") or []
    last_updated = card.get("last_updated", "")

    lines = [
        f'<blockquote class="callout callout_default" theme="{icon}">',
        f"  <h3 style=\"margin-top: 0.75cm;\"> {heading}</h3>",
        "  <ul style=\"margin: 10px 0; padding-bottom: 0.25cm;\">",
    ]

    for index, desc in enumerate(descriptions):
        pretty_desc = normalize_text(desc)
        suffix = " <p>" if index == len(descriptions) - 1 else ""
        lines.append(f"    <li>Course Description: {pretty_desc}</li>{suffix}")

    if last_updated:
        lines.append(f"    <li>Last Updated: {last_updated}</li>")

    notebook_link = card.get("notebook_link")
    if not notebook_link:
        raise ValueError(f"Card '{card.get('title')}' is missing 'notebook_link'.")
    else: 
        lines.append(f"    <li><a href=\"{notebook_link}\">Link to Notebook</a></li>")
    
    lines.append("  </ul>")
    lines.append("</blockquote>")

    return "\n".join(lines)


def render_page(page: dict) -> str:
    heading = page.get("heading")
    if not heading:
        raise ValueError(f"Page entry for {page.get('file')} is missing a heading.")

    cards = page.get("cards") or []
    if not cards:
        raise ValueError(f"Page '{heading}' must define at least one card.")

    content_lines = [f"# {heading}", ""]
    rendered_cards = [render_card(card) for card in cards]
    content_lines.append("\n\n".join(rendered_cards))
    content_lines.append("")
    return "\n".join(content_lines)


def write_page(page: dict) -> None:
    target = REPO_ROOT / page["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_page(page), encoding="utf-8")
    rel = target.relative_to(REPO_ROOT)
    print(f"Wrote {rel}")


def main() -> None:
    pages = load_data()
    for page in pages:
        write_page(page)


if __name__ == "__main__":
    main()
