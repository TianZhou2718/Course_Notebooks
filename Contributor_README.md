
## Updating notebook cards

Notebook “cards” are generated from structured data so you only have to edit the course metadata once. Add or update entries in `data/notebook_cards.toml` and then regenerate the Markdown pages by running:

```bash
python3 scripts/generate_notebook_cards.py
```

The script overwrites the affected files in `src/content/`, so make edits to the data file instead of the Markdown files directly.

- Optional fields: `contributor` (and `contributor_url`) add a credit line for whoever maintains the notebook.
