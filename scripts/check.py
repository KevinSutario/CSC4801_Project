"""The gate. Every agent runs this before saying a task is done.

Usage:
    python scripts/check.py            lint + unit tests + contracts
    python scripts/check.py --release  same, and fail if any test is skipped

Exit code 0 means pass. Anything else means fail.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(label: str, cmd: list[str]) -> tuple[int, str]:
    print(f"\n=== {label}: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.rstrip())
    return proc.returncode, out


def main() -> int:
    release = "--release" in sys.argv[1:]
    failures: list[str] = []

    code, _ = run("lint", [sys.executable, "-m", "ruff", "check", "."])
    if code != 0:
        failures.append("lint (try: python -m ruff check . --fix, then fix the rest)")

    code, out = run("tests", [sys.executable, "-m", "pytest", "tests/unit", "-q", "-rs",
                              "-p", "no:cacheprovider"])
    if code != 0:
        failures.append("tests")
    skipped = re.search(r"(\d+) skipped", out)
    n_skipped = int(skipped.group(1)) if skipped else 0
    if release and n_skipped:
        failures.append(f"release: {n_skipped} skipped test(s) left")
    xfailed = re.search(r"(\d+) xfailed", out)
    if release and xfailed:
        failures.append(f"release: {xfailed.group(1)} xfail test(s) left (open bugs)")

    if os.path.isdir(os.path.join(ROOT, "app")):
        code, _ = run("contracts", [sys.executable, os.path.join("scripts", "check_contracts.py")])
        if code != 0:
            failures.append("contracts")
    else:
        print("\n=== contracts: skipped (no app/ folder yet)")

    print("\n" + "=" * 60)
    if failures:
        print("CHECK FAILED: " + "; ".join(failures))
        return 1
    note = f" ({n_skipped} skipped placeholder tests)" if n_skipped else ""
    print("CHECK PASSED" + note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
