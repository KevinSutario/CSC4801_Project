"""Scope checks for task cards.

Usage:
    python scripts/check_scope.py T07
        Every file changed on this branch (committed, staged, unstaged or new) must match a
        pattern in the "## Owns" section of docs/tasks/T07.md. Compares against branch "dev".

    python scripts/check_scope.py --overlap T07 T09 T12
        Prints OK if no two of these cards own the same file or pattern.

Owns entries are bullet lines with a path in backticks, for example:
    - `app/jobs/service.py`
    - `app/templates/jobs/*`
"""

from __future__ import annotations

import fnmatch
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("SCOPE_BASE", "dev")


def owns(task_id: str) -> list[str]:
    path = os.path.join(ROOT, "docs", "tasks", f"{task_id}.md")
    if not os.path.exists(path):
        sys.exit(f"No card: docs/tasks/{task_id}.md")
    patterns: list[str] = []
    in_owns = False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("## "):
                in_owns = line.strip().lower() == "## owns"
                continue
            if in_owns:
                m = re.match(r"\s*-\s*`([^`]+)`", line)
                if m:
                    patterns.append(m.group(1).strip().replace("\\", "/"))
    if not patterns:
        sys.exit(f"Card {task_id} has no '## Owns' entries")
    return patterns


def git_lines(*args: str) -> list[str]:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def changed_files() -> list[str]:
    files: set[str] = set()
    files.update(git_lines("diff", "--no-renames", "--name-only", f"{BASE}...HEAD"))
    files.update(git_lines("diff", "--no-renames", "--name-only"))
    files.update(git_lines("diff", "--no-renames", "--name-only", "--cached"))
    files.update(git_lines("ls-files", "--others", "--exclude-standard"))
    return sorted(f.replace("\\", "/") for f in files)


def matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/"):
        return path.startswith(pattern)
    return path == pattern or fnmatch.fnmatch(path, pattern)


def check_task(task_id: str) -> int:
    patterns = owns(task_id)
    outside = [f for f in changed_files() if not any(matches(f, p) for p in patterns)]
    if outside:
        print(f"SCOPE FAILED for {task_id}. These files are not in its Owns list:")
        for f in outside:
            print(f"  {f}")
        print("Undo those changes, or stop and report CONTRACT CHANGE NEEDED.")
        return 1
    print(f"SCOPE OK for {task_id}")
    return 0


def check_overlap(task_ids: list[str]) -> int:
    cards = {t: owns(t) for t in task_ids}
    tracked = git_lines("ls-files")
    problems: list[str] = []
    ids = list(cards)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            for pa in cards[a]:
                for pb in cards[b]:
                    same = pa == pb or matches(pa, pb) or matches(pb, pa)
                    shared = [f for f in tracked if matches(f, pa) and matches(f, pb)]
                    if same or shared:
                        problems.append(f"{a} `{pa}` overlaps {b} `{pb}`")
    if problems:
        print("OVERLAP FOUND. Do not run these tasks at the same time:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("OK: no overlap between " + ", ".join(ids))
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--overlap":
        if len(args) < 2:
            print("OK: only one task")
            return 0
        return check_overlap(args[1:])
    return check_task(args[0])


if __name__ == "__main__":
    sys.exit(main())
