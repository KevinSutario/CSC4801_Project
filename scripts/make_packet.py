"""Build review packets for the three reviewers and the judge.

Usage (run from the main repo folder, on branch dev):
    python scripts/make_packet.py task T07
        task branch task/T07 against dev, worktree ../ks-T07
    python scripts/make_packet.py merge T07
        integration branch int/T07 against dev, worktree ../ks-int
    python scripts/make_packet.py phase 2
        everything since tag phase-1 on dev, split by file
    python scripts/make_packet.py audit security
        whole app on main, one audit area (T22), worktree ../ks-audit.
        Areas: security, functional, performance, delivery

Writes reviews/<id>/packet-<k>.md and prints each path plus the worktree path.
A packet holds at most about 400 changed lines; bigger diffs are split by file.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_LINES = 400
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
AUDIT_AREAS = {
    "security": ["app/security.py", "app/errors.py", "app/auth", "app/candidates/resume_service.py",
                 "app/candidates/routes_resume.py", "app/*/routes*.py", "app/templates"],
    "functional": ["app", "tests/unit", "docs/BRIEF.md"],
    "performance": ["app/jobs", "app/matching", "app/applications", "app/scheduling",
                    "app/schema.sql"],
    "delivery": ["README.md", "SPEC.md", "INSTALL.md", "Dockerfile", ".dockerignore", "wsgi.py",
                 ".env.example", "scripts/seed.py", "requirements.lock"],
}


def git(*args: str, cwd: str = ROOT) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def read(rel: str) -> str:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return f"(missing: {rel})"
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def security_checklist() -> str:
    text = read("docs/plan/04-AUTH-SECURITY.md")
    marker = "## Security review checklist"
    return text[text.find(marker):] if marker in text else "(checklist not found)"


def run_in(cwd: str, cmd: list[str]) -> str:
    if not os.path.isdir(cwd):
        return f"(worktree {cwd} not found)"
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return "\n".join(out.strip().splitlines()[-40:])


def split_by_file(diff: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^(?=diff --git )", diff)
    files = []
    for part in parts:
        if not part.strip():
            continue
        m = re.match(r"diff --git a/(\S+) ", part)
        files.append((m.group(1) if m else "?", part))
    return files


def chunk(files: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    chunks: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    size = 0
    for name, part in sorted(files, key=lambda f: f[0]):
        n = part.count("\n")
        if current and size + n > MAX_LINES:
            chunks.append(current)
            current, size = [], 0
        current.append((name, part))
        size += n
    if current:
        chunks.append(current)
    return chunks or [[]]


def write_packets(review_id: str, header: str, diff: str, worktree: str) -> None:
    out_dir = os.path.join(ROOT, "reviews", review_id)
    os.makedirs(out_dir, exist_ok=True)
    chunks = chunk(split_by_file(diff))
    for k, files in enumerate(chunks, start=1):
        names = ", ".join(n for n, _ in files) or "(no changes)"
        body = "".join(p for _, p in files)
        path = os.path.join(out_dir, f"packet-{k}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"# Review packet {review_id} ({k} of {len(chunks)})\n\n")
            fh.write(f"Worktree: {worktree}\n\nFiles in this packet: {names}\n\n")
            fh.write(header)
            fh.write("\n\n## Diff\n\n```diff\n" + body + "\n```\n")
        print(f"PACKET: {path}")
    print(f"WORKTREE: {worktree}")


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in ("task", "merge", "phase", "audit"):
        print(__doc__)
        return 2
    mode, ident = sys.argv[1], sys.argv[2]
    parent = os.path.dirname(ROOT)

    if mode in ("task", "merge"):
        branch = f"task/{ident}" if mode == "task" else f"int/{ident}"
        worktree = os.path.join(parent, f"ks-{ident}" if mode == "task" else "ks-int")
        review_id = ident if mode == "task" else f"merge-{ident}"
        diff = git("diff", f"dev...{branch}")
        stat = git("diff", "--stat", f"dev...{branch}")
        header = (
            f"## Review type: {mode}\n\n"
            f"## Task card\n\n{read(f'docs/tasks/{ident}.md')}\n\n"
            f"## Changed files\n\n```\n{stat}\n```\n\n"
            f"## Check output (in the worktree)\n\n```\n"
            f"{run_in(worktree, [sys.executable, 'scripts/check.py'])}\n```\n\n"
            f"## Scope check\n\n```\n"
            f"{run_in(worktree, [sys.executable, 'scripts/check_scope.py', ident])}\n```\n\n"
            f"{security_checklist()}\n"
        )
        write_packets(review_id, header, diff, worktree)
        return 0

    if mode == "audit":
        if ident not in AUDIT_AREAS:
            sys.exit("area must be one of: " + ", ".join(AUDIT_AREAS))
        worktree = os.path.join(parent, "ks-audit")
        paths = AUDIT_AREAS[ident]
        diff = git("diff", EMPTY_TREE, "main", "--", *paths)
        header = (
            f"## Review type: audit ({ident}), whole app on main\n\n"
            f"Every line shows as added because this compares against an empty tree.\n\n"
            f"## Requirements\n\n{read('docs/plan/01-REQUIREMENTS.md')}\n\n"
            f"{security_checklist()}\n"
        )
        write_packets(f"T22-{ident}", header, diff, worktree)
        return 0

    phase = int(ident)
    base = EMPTY_TREE if phase == 0 else f"phase-{phase - 1}"
    diff = git("diff", f"{base}..dev")
    stat = git("diff", "--stat", f"{base}..dev")
    header = (
        f"## Review type: phase {phase}\n\n"
        f"Compare: {base}..dev\n\n"
        f"## Requirements\n\n{read('docs/plan/01-REQUIREMENTS.md')}\n\n"
        f"## Changed files (whole phase)\n\n```\n{stat}\n```\n\n"
        f"{security_checklist()}\n"
    )
    write_packets(f"phase-{phase}", header, diff, ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
