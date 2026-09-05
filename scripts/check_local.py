#!/usr/bin/env python3
"""Run repository checks locally; never invoke GitHub Actions or install packages."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    commands = [[sys.executable, str(ROOT / "scripts" / name)] for name in (
        "validate_repository.py", "validate_accuracy_invariants.py", "validate_semianalysis_profile.py")]
    commands.append([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"])
    failed = []
    for command in commands:
        print("RUN:", " ".join(command), flush=True)
        try:
            result = subprocess.run(command, cwd=ROOT, check=False, timeout=120)
            if result.returncode:
                failed.append(command[-1])
        except (OSError, subprocess.TimeoutExpired):
            failed.append(command[-1])
    if failed:
        print("FAIL: one or more local checks failed or did not run", file=sys.stderr)
        return 1
    print("PASS: local repository checks only; no live provider assessment performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
