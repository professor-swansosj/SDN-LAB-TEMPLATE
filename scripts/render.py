import sys, yaml, pathlib
from jinja2 import Environment, FileSystemLoader, StrictUndefined

root = pathlib.Path(__file__).resolve().parents[1]
templates_dir = root / "templates"
env = Environment(
    loader=FileSystemLoader(str(templates_dir)),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)

def render(lab_yml_path: pathlib.Path, out_dir: pathlib.Path):
    data = yaml.safe_load(lab_yml_path.read_text(encoding="utf-8"))
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
