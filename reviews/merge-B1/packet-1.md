# Review packet merge-B1 (1 of 1)

Worktree: /Users/mac/ks-int

Files in this packet: scripts/make_packet.py, tests/unit/test_make_packet.py

## Review type: merge

## Task card

# B1 · Phase 0 review packets must not require phase--1

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| 0 | tooling | T00 | no | READY |

## Goal
`python scripts/make_packet.py phase 0` currently fails with an ambiguous `phase--1..dev` revision. Generate complete Phase 0 packets without inventing a predecessor tag. Keep phase 1 and later comparisons against their predecessor tags.

## Requirement
Tooling only; no business rule or course brief is needed. Phase 0 contains initial repository tooling and setup; review the whole repository at `dev` against Git's empty tree because there is no preceding phase. Later phases retain the existing tag baseline.

## Owns
- `scripts/make_packet.py`
- `tests/unit/test_make_packet.py`

## May read
- `CLAUDE.md`
- `docs/tasks/B1.md`
- `scripts/make_packet.py`
- `scripts/check.py`
- `scripts/check_scope.py`
- `pytest.ini`
- `ruff.toml`
- `requirements-dev.txt`
- `docs/plan/10-REVIEW-PROTOCOL.md`

## Contract
Keep `python scripts/make_packet.py phase <n>` and its existing packet naming/output. No new dependencies. Use the existing Git empty-tree constant for phase 0; preserve missing-tag failures for later phases.

## Steps
1. Use the existing Python 3.12 environment at `/private/tmp/keystone-phase0-venv` via PATH. Set `PYTHONDONTWRITEBYTECODE=1` and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`.
2. Read before editing. Write an offline regression test using a temporary Git repository that invokes the real packet command for phase 0 with no tags. Show it failing with the actual missing-revision error.
3. State the root cause. Search for the same predecessor calculation elsewhere with `git grep`; report hits without changing unrelated code.
4. Make the smallest fix for phase 0. Test phase 1 still compares against phase-0 and fails clearly when that required tag is absent.
5. Run regression tests, `python scripts/check.py`, and `python scripts/check_scope.py B1`. Commit on `task/B1` only. Do not generate review packets in the main repo.

## Tests
- Real CLI generates phase-0 packets without a predecessor tag and includes the repository diff.
- Phase 1 uses phase-0 and preserves failure when its predecessor tag is absent.

## Done when
- Regression tests pass, full gate prints CHECK PASSED, and B1 scope passes.
- Reply includes actual failing/passing output, BUG and JOURNAL blocks.


## Changed files

```
 scripts/make_packet.py         |  2 +-
 tests/unit/test_make_packet.py | 78 ++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 79 insertions(+), 1 deletion(-)

```

## Check output (in the worktree)

```
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
....................                                                     [100%]
20 passed in 0.30s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for B1
```

## Security review checklist (reviewers tick every line)

1. Every new route has `@login_required` and the right `@role_required`, or a written reason why not.
2. Every POST form includes `csrf_field()`. No route skips the CSRF check.
3. Every service that loads an object by id also checks the actor owns it or may see it.
4. Missing and not-yours both give the agreed status code. Try an id that belongs to another user.
5. All SQL uses `?` placeholders. Search the diff for `f"`, `.format(`, `%` and `+` near `execute`.
6. No `|safe`, `Markup(` or `autoescape false` on anything a user typed.
7. Uploads: size cap, type check by content, random stored name, served only via the checked route.
8. Redirects use `url_for`, or a `next` value that passes the safe-redirect check.
9. No secret, password, token or traceback appears in logs, flash messages, audit detail or HTML.
10. Error responses use the error templates, with the right status code.
11. Sign-in clears the session first. Sign-out is POST with CSRF.
12. Role cannot be changed through any form field.



## Diff

```diff
diff --git a/scripts/make_packet.py b/scripts/make_packet.py
index 61291a1..65244ea 100644
--- a/scripts/make_packet.py
+++ b/scripts/make_packet.py
@@ -151,7 +151,7 @@ def main() -> int:
         return 0
 
     phase = int(ident)
-    base = f"phase-{phase - 1}"
+    base = EMPTY_TREE if phase == 0 else f"phase-{phase - 1}"
     diff = git("diff", f"{base}..dev")
     stat = git("diff", "--stat", f"{base}..dev")
     header = (
diff --git a/tests/unit/test_make_packet.py b/tests/unit/test_make_packet.py
new file mode 100644
index 0000000..fe8f131
--- /dev/null
+++ b/tests/unit/test_make_packet.py
@@ -0,0 +1,78 @@
+"""Offline regression tests for phase review packet baselines."""
+
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+import pytest
+
+
+SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "make_packet.py"
+EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
+
+
+def git(repo: Path, *args: str) -> str:
+    return subprocess.run(
+        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
+    ).stdout
+
+
+@pytest.fixture
+def packet_repo(tmp_path: Path) -> Path:
+    repo = tmp_path / "repo"
+    (repo / "scripts").mkdir(parents=True)
+    shutil.copyfile(SCRIPT, repo / "scripts" / "make_packet.py")
+    git(repo, "init", "--initial-branch=dev")
+    git(repo, "config", "user.name", "Packet test")
+    git(repo, "config", "user.email", "packet@example.invalid")
+    (repo / "README.md").write_text("Initial repository content\n", encoding="utf-8")
+    git(repo, "add", ".")
+    git(repo, "commit", "-m", "Initial repository")
+    return repo
+
+
+def run_phase(repo: Path, phase: int) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [sys.executable, "scripts/make_packet.py", "phase", str(phase)],
+        cwd=repo, capture_output=True, text=True,
+    )
+
+
+def test_phase_zero_without_tags_includes_whole_repository(packet_repo: Path) -> None:
+    assert git(packet_repo, "tag") == ""
+    result = run_phase(packet_repo, 0)
+    assert result.returncode == 0, result.stderr
+    packets = sorted((packet_repo / "reviews" / "phase-0").glob("packet-*.md"))
+    assert packets
+    text = "\n".join(packet.read_text(encoding="utf-8") for packet in packets)
+    assert f"Compare: {EMPTY_TREE}..dev" in text
+    assert "diff --git a/README.md b/README.md" in text
+    assert "+Initial repository content" in text
+    assert "diff --git a/scripts/make_packet.py b/scripts/make_packet.py" in text
+    assert "new file mode" in text
+    assert f"PACKET: {packets[0]}" in result.stdout
+    assert f"WORKTREE: {packet_repo}" in result.stdout
+
+
+def test_phase_one_compares_against_phase_zero_tag(packet_repo: Path) -> None:
+    git(packet_repo, "tag", "phase-0")
+    (packet_repo / "phase-one.txt").write_text("Phase one content\n", encoding="utf-8")
+    git(packet_repo, "add", "phase-one.txt")
+    git(packet_repo, "commit", "-m", "Phase one")
+    result = run_phase(packet_repo, 1)
+    assert result.returncode == 0, result.stderr
+    packet = packet_repo / "reviews" / "phase-1" / "packet-1.md"
+    text = packet.read_text(encoding="utf-8")
+    assert "Compare: phase-0..dev" in text
+    assert "+Phase one content" in text
+    assert "diff --git a/README.md" not in text
+    assert "diff --git a/scripts/make_packet.py" not in text
+
+
+def test_phase_one_requires_phase_zero_tag(packet_repo: Path) -> None:
+    result = run_phase(packet_repo, 1)
+    assert result.returncode != 0
+    assert "git diff phase-0..dev failed:" in result.stderr
+    assert "unknown revision or path not in the working tree" in result.stderr
+    assert not (packet_repo / "reviews" / "phase-1").exists()

```
