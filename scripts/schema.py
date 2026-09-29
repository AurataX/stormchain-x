import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from sqlalchemy.dialects import postgresql  # noqa: E402
from sqlalchemy.schema import CreateIndex, CreateTable  # noqa: E402

from app.models import Base  # noqa: E402


def render():
    dialect = postgresql.dialect()
    statements = [
        "-- Generated from SQLAlchemy metadata. Run python scripts/schema.py --write."
    ]
    for table in Base.metadata.sorted_tables:
        statements.append(
            str(CreateTable(table).compile(dialect=dialect)).strip() + ";"
        )
        for index in sorted(table.indexes, key=lambda item: item.name):
            statements.append(
                str(CreateIndex(index).compile(dialect=dialect)).strip() + ";"
            )
    statements.append(
        (ROOT / "apps/api/database/postgis.sql").read_text(encoding="utf-8").strip()
    )
    return "\n\n".join(statements) + "\n"


if __name__ == "__main__":
    path = ROOT / "apps/api/database/schema.sql"
    expected = render()
    if "--write" in sys.argv:
        path.write_text(expected, encoding="utf-8")
    elif not path.exists() or path.read_text(encoding="utf-8") != expected:
        raise SystemExit(
            "Schema drift: run python scripts/schema.py --write and review."
        )
    print("Schema matches models.")
