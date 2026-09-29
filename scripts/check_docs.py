import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
documents = [root / name for name in ("AGENTS.md", "CLAUDE.md", "README.md")]
documents.extend((root / "docs").rglob("*.md"))
missing = []
for document in documents:
    for target in re.findall(
        r"\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")
    ):
        if target.startswith(("http:", "https:", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if not (document.parent / path).exists():
            missing.append(f"{document.relative_to(root)} -> {target}")
if missing:
    raise SystemExit("Broken documentation links:\n" + "\n".join(missing))
print(f"Documentation links passed ({len(documents)} documents).")
