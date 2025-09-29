import re, sys, pathlib, yaml

root = pathlib.Path(sys.argv[1])  # path to a lab repo
readme_p = root / "README.md"
instr_p = root / "INSTRUCTIONS.md"
readme = readme_p.read_text(encoding="utf-8", errors="ignore") if readme_p.exists() else ""
instr  = instr_p.read_text(encoding="utf-8", errors="ignore") if instr_p.exists() else ""

def find(pat, s):
    m = re.search(pat, s, re.I|re.M|re.S)
    return m.group(1).strip() if m else None

data = {
  "title": find(r"^#\s*(.+)$", readme) or root.name,
  "course": find(r"\*\*Course:\*\*\s*(.+)", readme) or "Software Defined Networking",
  "module": find(r"\*\*Module:\*\*\s*([^\n|]+)", readme) or "Module",
  "lab_number": find(r"Lab\s*#?:\s*([0-9]+)", readme) or None,
  "time_estimate": find(r"Estimated Time:\s*([^\n]+)", readme) or "60–90 min",
  "objectives": re.findall(r"^-\s+(.+)$", (find(r"## Objectives(.*?)(?:\n##|\Z)", readme) or ""), re.M),
  "python_version": "3.11",
  "accounts": ["GitHub", "Cisco DevNet"],
  "devices": ["Cisco DevNet Always-On Catalyst"],
  "deliverables": {
    "readme_summary": "README present and consistent",
    "instructions_summary": "INSTRUCTIONS present and consistent"
  },
  "grading": {
    "total_points": 75,
    "rows": []
  },
  "tips": [],
  "autograder": {
    "log_path": "logs/lab.log",
    "required_markers": []
  },
  "license": "© 2025 — Classroom use",
  "steps": []
}

# Grading table harvest (Step | Requirement | Points)
grading_block = find(r"## Grading Breakdown(.*?)(?:\n##|\Z)", readme) or ""
for line in grading_block.splitlines():
    cells = [c.strip("| ").strip() for c in line.split("|")]
    if len(cells) >= 4 and cells[1] and cells[1].lower() != 'step':
        pts = re.sub(r"[^\d]", "", cells[3])
        if pts.isdigit():
            data["grading"]["rows"].append({"step": cells[1], "requirement": cells[2], "points": int(pts)})

# Steps from INSTRUCTIONS (## Step N — Title)
for m in re.finditer(r"##\s*Step\s*\d+\s*[—-]\s*(.+?)\n(.*?)(?=\n##|\Z)", instr, re.S):
    step_title, body = m.groups()
    def pick(lbl):
        mm = re.search(fr"\*\*{lbl}:\*\*\s*(.+?)(?:\n\n|\Z)", body, re.S)
        return mm.group(1).strip() if mm else "—"
    data["steps"].append({
        "title": step_title.strip(),
        "goal": pick("Goal"),
        "actions": pick("What to do"),
        "done_when": pick("You’re done when"),
        "log_marker": pick("Log marker to add"),
    })

out = root / "lab.yml"
out.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
print(f"Wrote {out}")
