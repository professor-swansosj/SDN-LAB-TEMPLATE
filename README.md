# SDN-LAB-TEMPLATE

One-paragraph intro here (keep ≤ 120 chars per line to satisfy MD013).

## How it works

- Each lab repo contains a small `lab.yml`.
- The template renders `README.md` and `INSTRUCTIONS.md`.

## Quick start

1. In each lab repo, create/update `lab.yml`.
2. Run the renderer from the template repo:

```bash
python scripts/render.py /path/to/lab.yml /path/to/lab
```

Commit those README tweaks onto your branch:

```bash
git add README.md
git commit -m "docs: fix markdownlint spacing in README"
git push
```
