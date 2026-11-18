TASK: B3
COMMIT: `549bc41`
FILES CHANGED: `scripts/check_scope.py`, `tests/unit/test_check_scope.py`
TESTS ADDED: `test_scope_checks_both_rename_paths` — 9 cases across three Git states and ownership directions.

FAILING EVIDENCE:
Before the fix, staged and committed unowned-source renames failed regression assertions: `AssertionError: SCOPE OK for B2` (2 failed, 7 passed).

CHECK OUTPUT:
```text
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
.........................................                                [100%]
41 passed in 3.06s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

SCOPE CHECK:
```text
SCOPE OK for B3
```

STATUS: done
OPEN QUESTIONS: none

BUG:
- Symptom: renaming an unowned source into an owned destination bypassed scope enforcement.
- Cause: Git’s rename-aware `--name-only` output omitted the removed source path.
- Fix: added `--no-renames` to committed, unstaged, and staged diffs.
- Guarded by: `test_scope_checks_both_rename_paths` (9 cases), with explicit Git rename detection and `R100` verification.
- Other hits: searched `git grep`; only the three affected commands in `scripts/check_scope.py:57–59`.

JOURNAL:
- Scope checking now includes both source and destination paths of renames.
- Regression coverage exercises unstaged, staged, and committed renames with unowned sources, fully owned paths, and unowned destinations.
- Unstaged fixtures use intent-to-add so actual rename detection is exercised.
- Full gate passes 41 tests; scope passes; worktree clean.
- Diff: 37 insertions, 3 deletions, below the 80-line re-review threshold.
