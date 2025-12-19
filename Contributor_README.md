## Notebook Contributor Notes

Notebook “cards” are generated from structured data. To add or update notebook, modify metadata files (in `/toml`) in `data/` directory. Then regenerate (and overwrite) the md files by running:

```bash
python3 scripts/generate_notebook_cards.py
```

- Notebook metadata:
    - `icon`: visual icon on notebook card, default is "📘"
    - `title`
    - `notebook_link`: relative path to notebook pdf
    - `last_updated`
    - `descriptions`: list of description paragrahs
- Optional metadata
    - `contributor`: credit line for contributor
    - `contributor_url`: url to contributor's github

## Local Development on mdBook

Reference: [mdBook Documentation](https://rust-lang.github.io/mdBook/)

To locally deploy (and serve mdBook), use
```bash
mdbook serve - o
```