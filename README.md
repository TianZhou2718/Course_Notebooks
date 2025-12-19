# Course Notebooks

![Static Badge](https://img.shields.io/badge/Github-black?style=for-the-badge&logo=github&link=https%3A%2F%2Fgithub.com%2FTianZhou2718%2FCourse_Notebooks)
![GitHub License](https://img.shields.io/github/license/TianZhou2718/Course_Notebooks?style=for-the-badge)


---

Here's the [link](https://tianzhou2718.github.io/Course_Notebooks/) to the website.

This website serves as a centralized hub for a collection of notebooks used in various courses offered by Johns Hopkins University. Free feel to explore a diverse range of materials designed to enhance your understanding of mathematics and computer science.

## Updating notebook cards

Notebook “cards” are generated from structured data so you only have to edit the course metadata once. Add or update entries in `data/notebook_cards.toml` and then regenerate the Markdown pages by running:

```bash
python3 scripts/generate_notebook_cards.py
```

The script overwrites the affected files in `src/content/`, so make edits to the data file instead of the Markdown files directly.

- Optional fields: `contributor` (and `contributor_url`) add a credit line for whoever maintains the notebook.
