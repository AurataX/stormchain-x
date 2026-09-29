from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".css", ".sql", ".toml"}
EXCLUDED = {".venv", ".git", "node_modules", "__pycache__", ".next"}


def violations():
    for path in ROOT.rglob("*"):
        if set(path.relative_to(ROOT).parts) & EXCLUDED:
            continue
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if path.name == "schema.sql":
            continue
        count = len(path.read_text(encoding="utf-8").split())
        if count > 250:
            yield f"{path.relative_to(ROOT)}: {count} words (maximum 250)"


if __name__ == "__main__":
    errors = list(violations())
    print("\n".join(errors) if errors else "Source-size gate passed (250 words).")
    raise SystemExit(bool(errors))
