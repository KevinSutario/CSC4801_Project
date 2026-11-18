# Review packet B3 (1 of 1)

Worktree: /Users/mac/ks-B3

Files in this packet: scripts/check_scope.py, tests/unit/test_check_scope.py

## Review type: task

## Task card

# B3 · Check both paths of a rename against task ownership

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| 0 | tooling | T00, B1, B2 | no | READY |

## Goal
Resolve the Phase 0 round 2 scope finding: renaming an unowned tracked source file into an owned destination currently passes the scope checker. Both the removed source and added destination must be checked for unstaged, staged, and committed changes.

## Requirement
Tooling only. CLAUDE.md permits changes only to task Owns files, which includes removing or renaming a source path. No course brief is needed.

## Owns
- `scripts/check_scope.py`
- `tests/unit/test_check_scope.py`

## May read
- `CLAUDE.md`
- `.claude/agents/implementer.md`
- `docs/tasks/B3.md`
- `docs/tasks/TEMPLATE.md`
- `docs/plan/07-CONTRACTS.md`
- `scripts/check_scope.py`
- `scripts/check.py`
- `tests/unit/test_check_scope.py`
- `pytest.ini`
- `ruff.toml`
- `requirements-dev.txt`
- `reviews/phase-0/verdict.md`
- `reviews/phase-0/repro/test_round2_rename.py`
- `reviews/phase-0/repro/mutation-results-round2.md`

## Contract
Keep `python scripts/check_scope.py <task-id>`, its existing environment settings, and its ownership matching behavior. Include both rename paths in changed-file checks. Do not add dependencies or refactor unrelated tooling.

## Steps
1. Use `/private/tmp/keystone-phase0-venv/bin` on PATH, `PYTHONDONTWRITEBYTECODE=1`, and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`. Read the implementer instructions and files before editing; quote real signatures before calls.
2. Read the latest judge verdict and rename repro. Add regression coverage to the existing isolated Git fixture in `tests/unit/test_check_scope.py`; show staged and committed unowned-source-to-owned-destination renames fail the intended assertion before fixing.
3. State the cause and search for the same pattern with `git grep`; report other hits without fixing unrelated code.
4. Make the smallest change so all three diff sources check removed and added paths. Preserve normal owned changes and legitimate renames where both paths are owned. Cover an owned-source-to-unowned-destination rename too, using parameterization or fixture reuse where useful. Exercise real Git rename detection explicitly in fixtures so global configuration cannot hide the bug.
5. Keep the code and regression diff focused; avoid unrelated fixture restructuring. Do not weaken existing assertions or skip tests.
6. Run focused scope tests, `python scripts/check.py`, and `python scripts/check_scope.py B3`. Commit only Owns files on `task/B3`. Include failing and passing evidence, BUG and JOURNAL blocks.

## Tests
- Staged and committed unowned-source renames to owned destinations are rejected with the source path named.
- Renames where both paths are owned pass; an unowned destination is rejected.
- Existing owned/unowned change coverage remains green.

## Done when
- Regression tests, full gate, and B3 scope pass; no unrelated files change.


## Changed files

```
 scripts/check_scope.py         |  6 +++---
 tests/unit/test_check_scope.py | 34 ++++++++++++++++++++++++++++++++++
 2 files changed, 37 insertions(+), 3 deletions(-)

```

## Check output (in the worktree)

```
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
.........................................                                [100%]
41 passed in 3.00s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for B3
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
diff --git a/scripts/check_scope.py b/scripts/check_scope.py
index 8cc5b5e..e9fcb15 100644
--- a/scripts/check_scope.py
+++ b/scripts/check_scope.py
@@ -54,9 +54,9 @@ def git_lines(*args: str) -> list[str]:
 
 def changed_files() -> list[str]:
     files: set[str] = set()
-    files.update(git_lines("diff", "--name-only", f"{BASE}...HEAD"))
-    files.update(git_lines("diff", "--name-only"))
-    files.update(git_lines("diff", "--name-only", "--cached"))
+    files.update(git_lines("diff", "--no-renames", "--name-only", f"{BASE}...HEAD"))
+    files.update(git_lines("diff", "--no-renames", "--name-only"))
+    files.update(git_lines("diff", "--no-renames", "--name-only", "--cached"))
     files.update(git_lines("ls-files", "--others", "--exclude-standard"))
     return sorted(f.replace("\\", "/") for f in files)
 
diff --git a/tests/unit/test_check_scope.py b/tests/unit/test_check_scope.py
index 39797f0..8697b68 100644
--- a/tests/unit/test_check_scope.py
+++ b/tests/unit/test_check_scope.py
@@ -29,6 +29,7 @@ def scope_repo(tmp_path: Path) -> Path:
     git(tmp_path, "init", "--initial-branch=dev")
     git(tmp_path, "config", "user.name", "Scope test")
     git(tmp_path, "config", "user.email", "scope@example.invalid")
+    git(tmp_path, "config", "diff.renames", "true")
     git(tmp_path, "add", ".")
     git(tmp_path, "commit", "-m", "Fixture baseline")
     git(tmp_path, "checkout", "-b", "task/B2")
@@ -70,3 +71,36 @@ def test_scope_rejects_unowned_changes(scope_repo: Path, state: str) -> None:
     assert "SCOPE FAILED for B2" in result.stdout
     assert name in result.stdout
     assert "SCOPE OK" not in result.stdout
+
+
+@pytest.mark.parametrize("state", ["unstaged", "staged", "committed"])
+@pytest.mark.parametrize("source,destination,outside", [
+    ("unowned.txt", "owned-new.txt", "unowned.txt"),
+    ("owned.txt", "owned-new.txt", None),
+    ("owned.txt", "unowned-new.txt", "unowned-new.txt"),
+])
+def test_scope_checks_both_rename_paths(
+    scope_repo: Path, state: str, source: str, destination: str, outside: str | None,
+) -> None:
+    if state == "unstaged":
+        (scope_repo / source).rename(scope_repo / destination)
+        git(scope_repo, "add", "--intent-to-add", destination)
+    else:
+        git(scope_repo, "mv", source, destination)
+        if state == "committed":
+            git(scope_repo, "commit", "-m", "Rename fixture file")
+    diff_args = {"committed": ["dev...HEAD"], "staged": ["--cached"], "unstaged": []}[state]
+    diff = subprocess.run(
+        ["git", "diff", "--name-status", *diff_args], cwd=scope_repo,
+        capture_output=True, text=True, check=True,
+    )
+    assert f"R100\t{source}\t{destination}" in diff.stdout
+    result = run_scope(scope_repo)
+    if outside is None:
+        assert result.returncode == 0, result.stdout + result.stderr
+        assert "SCOPE OK for B2" in result.stdout
+    else:
+        assert result.returncode != 0, result.stdout + result.stderr
+        assert "SCOPE FAILED for B2" in result.stdout
+        assert outside in result.stdout
+        assert "SCOPE OK" not in result.stdout

```
