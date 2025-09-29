# SDN-LAB-TEMPLATE

Source-of-truth for rendering consistent `README.md` + `INSTRUCTIONS.md` across all SDN labs.

## How it works
- Each lab repo contains a tiny `lab.yml` with metadata.
- This repo provides Jinja2 templates and a renderer to generate Markdown files.
- A GitHub Action can open PRs across many lab repos to keep them in sync.

## Quick start
1. In each lab repo, create or extract `lab.yml` (see `scripts/extract_lab_meta.py`).
2. Test rendering locally:
   ```bash
   python scripts/render.py sample/lab.yml /path/to/your/lab-repo
