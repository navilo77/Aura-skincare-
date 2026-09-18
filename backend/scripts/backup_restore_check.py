"""Backup and restore verification helpers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]


def run_command(
    command: list[str], check: bool = True
) -> subprocess.CompletedProcess:
    return subprocess.run(
        command, cwd=BACKEND_DIR, capture_output=True, text=True, check=check
    )


def check_alembic() -> None:
    if run_command(["uv", "run", "alembic", "--version"], check=False).returncode != 0:
        raise SystemExit("Alembic is not available via uv.")


def main() -> int:
    print("Backup/restore precheck:")
    try:
        check_alembic()
        print("- alembic: OK")
    except SystemExit as exc:
        print(str(exc))
        return 1
    print("Backup/restore tooling is available.")
    print("Note: Supabase Cloud manages automated backups.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
