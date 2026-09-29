import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
checks = [
    ([sys.executable, "scripts/check_size.py"], root),
    ([sys.executable, "scripts/check_docs.py"], root),
    ([sys.executable, "scripts/schema.py"], root),
    ([sys.executable, "-m", "ruff", "check", "apps/api", "scripts"], root),
    ([sys.executable, "-m", "ruff", "format", "--check", "apps/api", "scripts"], root),
    ([sys.executable, "-m", "pytest", "-q"], root / "apps/api"),
]
for command, directory in checks:
    print("RUN:", " ".join(command), flush=True)
    subprocess.run(command, cwd=directory, check=True)
