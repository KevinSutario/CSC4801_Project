# Review packet merge-B2 (1 of 1)

Worktree: /Users/mac/ks-int

Files in this packet: scripts/check.py, tests/unit/test_check.py, tests/unit/test_check_scope.py

## Review type: merge

## Task card

# B2 · Fail empty test gates and guard lint/scope rejection

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| 0 | tooling | T00, B1 | no | READY |

## Goal
Resolve the three confirmed Phase 0 findings in `reviews/phase-0/verdict.md`. A gate with an existing but empty `tests/unit` currently prints CHECK PASSED because it accepts pytest exit code 5; it must fail. Regression tests must also catch broken lint failure propagation and a scope checker that accepts unowned files.

## Requirement
Tooling only; no course brief or business rule is needed. The Phase 0 gate and Owns enforcement must reject failures, and tests must detect the judge's lint and scope mutations.

## Owns
- `scripts/check.py`
- `tests/unit/test_check.py`
- `tests/unit/test_check_scope.py`

## May read
- `CLAUDE.md`
- `.claude/agents/implementer.md`
- `docs/tasks/B2.md`
- `docs/plan/07-CONTRACTS.md`
- `docs/plan/10-REVIEW-PROTOCOL.md`
- `scripts/check.py`
- `scripts/check_scope.py`
- `pytest.ini`
- `ruff.toml`
- `requirements-dev.txt`
- `tests/unit/test_make_packet.py`
- `reviews/phase-0/verdict.md`
- `reviews/phase-0/repro/test_g1.py`
- `reviews/phase-0/repro/mutation-results.md`

## Contract
Preserve the documented `python scripts/check.py` and `python scripts/check_scope.py <task-id>` CLIs. Do not add dependencies or change application contracts. Preserve the scope checker behavior; the confirmed scope issue is missing regression coverage.

## Steps
1. Use `/private/tmp/keystone-phase0-venv/bin` on PATH, `PYTHONDONTWRITEBYTECODE=1`, and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`. Read the implementer instructions and every file before editing; quote real signatures before calling existing functions.
2. Read the confirmed verdict and repro evidence. Port the empty-suite repro into `tests/unit/test_check.py` and show it failing for the predicted reason. Exercise the real gate in an isolated temporary fixture so that the test cannot recursively launch itself.
3. State the root cause and search for the same mistake using `git grep`; report other hits without changing unrelated files.
4. Make the smallest change so pytest exit code 5 fails the gate. Add meaningful tests for a clean gate, a failing lint run, and a failing test run. Exercise actual gate behavior; avoid assertions that merely mirror implementation text.
5. Add a scope regression using an isolated temporary Git repository and task card: an owned change passes, an unowned change fails. Do not alter `scripts/check_scope.py`.
6. Demonstrate the lint and scope tests fail for the judge's corresponding mutations in an isolated temporary copy. Keep all temporary mutations outside tracked source; restore any scratch copy afterward. Do not weaken or skip existing tests.
7. Run the focused regressions, full `python scripts/check.py`, and `python scripts/check_scope.py B2`. Commit only Owns files on `task/B2`.

## Tests
- An empty unit-test suite fails the real gate and never prints CHECK PASSED.
- Clean lint plus passing tests succeeds; lint failure and test failure each fail the gate.
- An owned change passes the real scope CLI; an unowned change fails.
- The Phase 0 lint and scope mutations are detected by the new regressions.

## Done when
- All three confirmed groups have regression coverage, the full gate passes, and scope prints OK.
- Reply includes actual failing/passing evidence plus BUG and JOURNAL blocks.

## Pitfalls
- Gate subprocess tests must use isolated fixtures instead of launching the full repository gate recursively.
- Repro archives are evidence; do not edit them. Only the orchestrator updates state and review files.


## Changed files

```
 scripts/check.py               |  2 +-
 tests/unit/test_check.py       | 76 ++++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_check_scope.py | 72 +++++++++++++++++++++++++++++++++++++++
 3 files changed, 149 insertions(+), 1 deletion(-)

```

## Check output (in the worktree)

```
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
................................                                         [100%]
32 passed in 1.68s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for B2
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
diff --git a/scripts/check.py b/scripts/check.py
index 81f9389..72f9d7e 100644
--- a/scripts/check.py
+++ b/scripts/check.py
@@ -35,7 +35,7 @@ def main() -> int:
 
     code, out = run("tests", [sys.executable, "-m", "pytest", "tests/unit", "-q", "-rs",
                               "-p", "no:cacheprovider"])
-    if code not in (0, 5):
+    if code != 0:
         failures.append("tests")
     skipped = re.search(r"(\d+) skipped", out)
     n_skipped = int(skipped.group(1)) if skipped else 0
diff --git a/tests/unit/test_check.py b/tests/unit/test_check.py
new file mode 100644
index 0000000..5863bdf
--- /dev/null
+++ b/tests/unit/test_check.py
@@ -0,0 +1,76 @@
+"""CLI regression tests for the development gate."""
+
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+import pytest
+
+
+ROOT = Path(__file__).resolve().parents[2]
+
+
+@pytest.fixture
+def gate_repo(tmp_path: Path) -> Path:
+    scripts = tmp_path / "scripts"
+    scripts.mkdir()
+    shutil.copyfile(ROOT / "scripts" / "check.py", scripts / "check.py")
+    shutil.copyfile(ROOT / "ruff.toml", tmp_path / "ruff.toml")
+    (tmp_path / "tests" / "unit").mkdir(parents=True)
+    return tmp_path
+
+
+def run_gate(repo: Path) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [sys.executable, str(repo / "scripts" / "check.py")],
+        cwd=repo, capture_output=True, text=True, timeout=15,
+    )
+
+
+def write_test(repo: Path, assertion: str) -> None:
+    (repo / "tests" / "unit" / "test_example.py").write_text(
+        f"def test_example():\n    assert {assertion}\n", encoding="utf-8",
+    )
+
+
+def test_gate_fails_when_no_tests_are_collected(gate_repo: Path) -> None:
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert "no tests ran" in output, output
+    assert result.returncode != 0, output
+    assert "CHECK FAILED: tests" in output, output
+    assert "CHECK PASSED" not in output, output
+
+
+def test_gate_passes_with_clean_lint_and_passing_test(gate_repo: Path) -> None:
+    write_test(gate_repo, "True")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode == 0, output
+    assert "All checks passed!" in output, output
+    assert "1 passed" in output, output
+    assert "CHECK PASSED" in output, output
+
+
+def test_gate_fails_when_lint_fails(gate_repo: Path) -> None:
+    write_test(gate_repo, "True")
+    (gate_repo / "bad_lint.py").write_text("import os\n", encoding="utf-8")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode != 0, output
+    assert "F401" in output, output
+    assert "1 passed" in output, output
+    assert "CHECK FAILED: lint" in output, output
+    assert "CHECK PASSED" not in output, output
+
+
+def test_gate_fails_when_a_test_fails(gate_repo: Path) -> None:
+    write_test(gate_repo, "1 == 2")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode != 0, output
+    assert "All checks passed!" in output, output
+    assert "1 failed" in output, output
+    assert "CHECK FAILED: tests" in output, output
+    assert "CHECK PASSED" not in output, output
diff --git a/tests/unit/test_check_scope.py b/tests/unit/test_check_scope.py
new file mode 100644
index 0000000..39797f0
--- /dev/null
+++ b/tests/unit/test_check_scope.py
@@ -0,0 +1,72 @@
+"""CLI regression tests for task ownership enforcement."""
+
+import os
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+import pytest
+
+
+SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_scope.py"
+
+
+def git(repo: Path, *args: str) -> None:
+    subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)
+
+
+@pytest.fixture
+def scope_repo(tmp_path: Path) -> Path:
+    (tmp_path / "scripts").mkdir()
+    (tmp_path / "docs" / "tasks").mkdir(parents=True)
+    shutil.copyfile(SCRIPT, tmp_path / "scripts" / "check_scope.py")
+    (tmp_path / "docs" / "tasks" / "B2.md").write_text(
+        "# Fixture task\n\n## Owns\n- `owned.txt`\n- `owned-new.txt`\n", encoding="utf-8",
+    )
+    for name in ("owned.txt", "unowned.txt"):
+        (tmp_path / name).write_text("original\n", encoding="utf-8")
+    git(tmp_path, "init", "--initial-branch=dev")
+    git(tmp_path, "config", "user.name", "Scope test")
+    git(tmp_path, "config", "user.email", "scope@example.invalid")
+    git(tmp_path, "add", ".")
+    git(tmp_path, "commit", "-m", "Fixture baseline")
+    git(tmp_path, "checkout", "-b", "task/B2")
+    return tmp_path
+
+
+def change_file(repo: Path, name: str, state: str) -> str:
+    if state == "untracked":
+        name = name.replace(".txt", "-new.txt")
+    (repo / name).write_text("changed\n", encoding="utf-8")
+    if state in ("staged", "committed"):
+        git(repo, "add", name)
+    if state == "committed":
+        git(repo, "commit", "-m", "Change fixture file")
+    return name
+
+
+def run_scope(repo: Path) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [sys.executable, "scripts/check_scope.py", "B2"],
+        cwd=repo, capture_output=True, text=True,
+        env={**os.environ, "SCOPE_BASE": "dev"}, timeout=15,
+    )
+
+
+@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
+def test_scope_accepts_owned_changes(scope_repo: Path, state: str) -> None:
+    change_file(scope_repo, "owned.txt", state)
+    result = run_scope(scope_repo)
+    assert result.returncode == 0, result.stdout + result.stderr
+    assert "SCOPE OK for B2" in result.stdout
+
+
+@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
+def test_scope_rejects_unowned_changes(scope_repo: Path, state: str) -> None:
+    name = change_file(scope_repo, "unowned.txt", state)
+    result = run_scope(scope_repo)
+    assert result.returncode != 0, result.stdout + result.stderr
+    assert "SCOPE FAILED for B2" in result.stdout
+    assert name in result.stdout
+    assert "SCOPE OK" not in result.stdout

```
