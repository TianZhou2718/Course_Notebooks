#!/usr/bin/env python3
"""Generate Markdown notebook cards from structured data."""

from __future__ import annotations

import sys
import os
from pathlib import Path
import tomllib

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
ATTACHMENTS_DIR = REPO_ROOT / "src" / "attachments"
GITHUB_LOGO = "github-logo.png"

THEME_STYLES: dict[str, tuple[str, str]] = {
    "📘": ("#3457d5", "#f5f7ff"),
    "📗": ("#218f63", "#f3fbf5"),
    "📕": ("#b6303a", "#fff6f6"),
}
DEFAULT_STYLE = ("#3c4655", "#f7f8fa")

HERO_STYLES: dict[str, tuple[str, str, str]] = {
    "💻": ("linear-gradient(120deg, #eef1ff, #ffffff)", "#d7ddff", "rgba(76, 99, 185, 0.15)"),
    "📘": ("linear-gradient(120deg, #eef1ff, #ffffff)", "#d7ddff", "rgba(76, 99, 185, 0.15)"),
    "📗": ("linear-gradient(120deg, #f3fbf6, #ffffff)", "#cee3d8", "rgba(33, 143, 99, 0.18)"),
    "📕": ("linear-gradient(120deg, #fff0f2, #ffffff)", "#f5ccd2", "rgba(182, 48, 58, 0.18)"),
}
DEFAULT_HERO_STYLE = ("linear-gradient(120deg, #eef1ff, #ffffff)", "#d7ddff", "rgba(76, 99, 185, 0.15)")


def load_data() -> list[dict]:
    if not DATA_DIR.exists():
        raise Exception("Data directory not found.")

    pages: list[dict] = []
    for toml_path in sorted(DATA_DIR.rglob("*.toml")):
        with toml_path.open("rb") as fh:
            raw = tomllib.load(fh)
        file_pages = raw.get("pages")
        if not file_pages:
            continue
        pages.extend(file_pages)

    if not pages:
        raise Exception("No pages defined in notebook card data.")

    pages.sort(key=lambda page: page.get("file", ""))
    return pages


def normalize_text(value: str) -> str:
    """Collapse whitespace so TOML multiline strings render cleanly."""
    return " ".join(value.strip().split())


def render_heading(card: dict) -> str:
    icon = card.get("icon") or card.get("theme") or "📘"
    title = card["title"]
    text = f"{icon} &nbsp {title}"
    href = card.get("title_url") or card.get("notebook_link")
    if href:
        return f'<a href="{href}" style="color: inherit; text-decoration: none;"> {text}</a>'
    return text


def render_card(card: dict, attachments_rel: str) -> str:
    icon = card.get("icon", "📘")
    accent, background = THEME_STYLES.get(icon, DEFAULT_STYLE)
    heading = render_heading(card)
    descriptions = card.get("descriptions") or []
    last_updated = card.get("last_updated", "")
    notebook_link = card.get("notebook_link")
    link_text = card.get("notebook_link_text", "View Notebook")
    contributor = card.get("contributor")
    contributor_url = card.get("contributor_url")

    if not notebook_link:
        raise ValueError(f"Card '{card.get('title')}' is missing 'notebook_link'.")

    lines = [
        '<div class="notebook-card" '
        f'style="margin: 0.85cm 0; padding: 1.25em 1.4em; border-radius: 18px; '
        f'border: 1px solid {accent}33; background: {background}; '
        'box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);">',
        '  <div style="display: flex; justify-content: space-between; flex-wrap: wrap; '
        'align-items: center; gap: 0.75rem;">',
        f'    <h3 style="margin: 0; font-size: 1.7rem; font-weight: 600;"> {heading}</h3>',
        "  </div>",
    ]
    lines.append(
        '  <div style="margin-top: 0.7em;">\n'
        '    <span style="display: inline-block; padding: 0.2em 0.7em; border-radius: 999px; '
        'background: #e1e4eb; color: #4b5563; font-size: 0.8rem; font-weight: 600; '
        'letter-spacing: 0.03em; text-transform: uppercase;">Description</span>\n'
        "  </div>"
    )
    lines.append('  <div style="margin-top: 0.5em;">')
    for desc in descriptions:
        pretty_desc = normalize_text(desc)
        lines.append(
            '    <p style="margin: 0 0 0.45em 0; font-size: 1.2rem; color: #3b3f45; line-height: 1.5;">'
            f"{pretty_desc}</p>"
        )
    lines.append("  </div>")

    if contributor:
        logo_path = f"{attachments_rel}/{GITHUB_LOGO}"
        if contributor_url:
            github_logo = (
                f'<a href="{contributor_url}" style="margin-left: 0.6em; display: inline-flex; '
                'align-items: center;">'
                f'<img src="{logo_path}" '
                'alt="GitHub" style="width: 18px; height: 18px; vertical-align: middle;" /></a>'
            )
        else:
            github_logo = ""

        lines.append(
            '  <div style="margin-top: 0.45em;">\n'
            '    <span style="display: inline-block; padding: 0.2em 0.7em; border-radius: 999px; '
            'background: #e1e4eb; color: #4b5563; font-size: 0.8rem; font-weight: 600; '
            'letter-spacing: 0.03em; text-transform: uppercase;">Contributor</span>\n'
            "  </div>"
        )
        lines.append(
            '  <div style="margin-top: 0.35em; padding-left: 0.3em; font-size: 1.2rem; color: #5f6368; '
            'display: flex; align-items: center; gap: 0.4em;">'
            f"{contributor}{github_logo}</div>"
        )

    lines.append(
        '  <div style="margin-top: 0.95em; display: flex; align-items: center; '
        'justify-content: space-between; flex-wrap: wrap; gap: 0.6rem;">'
    )
    lines.append(
        f'    <a href="{notebook_link}" '
        f'style="font-weight: 600; color: {accent}; text-decoration: none;">{link_text} →</a>'
    )
    right_section = ['    <div style="display: flex; align-items: center; gap: 0.55em;">']
    if last_updated:
        right_section.append(
            f'      <span style="font-size: 1.2rem; color: #60656f;">Last Updated: {last_updated}</span>'
        )
    right_section.append(f'      <span style="font-size: 1.3rem;">{icon}</span>')
    right_section.append("    </div>")
    lines.extend(right_section)
    lines.append("  </div>")
    lines.append("</div>")

    return "\n".join(lines)


def render_page(page: dict) -> str:
    heading = page.get("heading")
    subtitle = page.get("subtitle", "")
    hero_icon = page.get("hero_icon", "📘")
    if not heading:
        raise ValueError(f"Page entry for {page.get('file')} is missing a heading.")

    cards = page.get("cards") or []
    if not cards:
        raise ValueError(f"Page '{heading}' must define at least one card.")

    background, border, shadow = HERO_STYLES.get(hero_icon, DEFAULT_HERO_STYLE)

    hero_block = [
        f'<div style="margin-top: 0.5rem; padding: 1.4rem 1.6rem; border-radius: 26px; background: {background}; '
        f'border: 1px solid {border}; box-shadow: 0 18px 35px {shadow}; text-align: center;">',
        f'  <div style="font-size: 2.8rem;">{hero_icon}</div>',
        f'  <div style="font-size: 2.3rem; font-weight: 700; color: #1f2a4f; margin-top: 0.35rem;">{heading}</div>',
    ]
    if subtitle:
        hero_block.append(
            f'  <div style="font-size: 1rem; color: #5d6481; margin-top: 0.35rem;">{subtitle}</div>'
        )
    hero_block.append("</div>")

    content_lines = hero_block + [""]
    target_path = REPO_ROOT / page["file"]
    attachments_rel = os.path.relpath(ATTACHMENTS_DIR, target_path.parent)
    rendered_cards = [render_card(card, attachments_rel) for card in cards]
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
