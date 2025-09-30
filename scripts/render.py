import sys, yaml, pathlib
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import os, fnmatch

root = pathlib.Path(__file__).resolve().parents[1]
templates_dir = root / "templates"
env = Environment(
    loader=FileSystemLoader(str(templates_dir)),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)

def build_tree(root=".", ignore_patterns=None, max_depth=3):
    ignore_patterns = ignore_patterns or []
    root = os.path.abspath(root)

    def should_ignore(path):
        rel = os.path.relpath(path, root)
        parts = rel.split(os.sep)
        for pat in ignore_patterns:
            if fnmatch.fnmatch(rel, pat) or any(fnmatch.fnmatch(p, pat) for p in parts):
                return True
        return False

    lines = [os.path.basename(root) or "."]
    def walk(dirpath, prefix="", depth=0):
        if depth >= max_depth:
            return
        try:
            entries = sorted(os.listdir(dirpath))
        except Exception:
            return
        # filter ignores
        filt = []
        for name in entries:
            p = os.path.join(dirpath, name)
            if should_ignore(p):
                continue
            filt.append(name)
        total = len(filt)
        for i, name in enumerate(filt):
            p = os.path.join(dirpath, name)
            connector = "└── " if i == total - 1 else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if os.path.isdir(p):
                extension = "    " if i == total - 1 else "│   "
                walk(p, prefix + extension, depth + 1)
    walk(root)
    return "\n".join(lines)


def render(lab_yml_path: pathlib.Path, out_dir: pathlib.Path):
    data = yaml.safe_load(lab_yml_path.read_text(encoding="utf-8"))
    repo_tree_cfg = (data or {}).get("repo_tree", {})
    
    if repo_tree_cfg.get("enabled"):
        root = repo_tree_cfg.get("root", ".")
        ignore = repo_tree_cfg.get("ignore", [])
        max_depth = int(repo_tree_cfg.get("max_depth", 3))
        # Important: render.py runs from the lab repo’s root in CI, so cwd = repo root
        data["file_tree"] = build_tree(root=root, ignore_patterns=ignore, max_depth=max_depth)
    else:
        data["file_tree"] = None

    for name in ["README.md.j2", "INSTRUCTIONS.md.j2"]:
        tpl = env.get_template(name)
        out = tpl.render(**data)
        (out_dir / name.replace(".j2", "")).write_text(out, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/render.py path/to/lab.yml path/to/target/repo")
        sys.exit(2)
    lab_yml = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    render(lab_yml, out_dir)
