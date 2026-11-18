TASK: B2
COMMIT: `aedea37`
FILES CHANGED: `scripts/check.py`, `tests/unit/test_check.py`, `tests/unit/test_check_scope.py`

TESTS ADDED:
- `test_gate_fails_when_no_tests_are_collected`
- `test_gate_passes_with_clean_lint_and_passing_test`
- `test_gate_fails_when_lint_fails`
- `test_gate_fails_when_a_test_fails`
- `test_scope_accepts_owned_changes` — 4 Git states
- `test_scope_rejects_unowned_changes` — 4 Git states

FAILING EVIDENCE:
- Before the fix, empty-suite repro failed at `assert result.returncode != 0`: pytest reported `no tests ran`, but gate returned 0 and printed `CHECK PASSED`.
- After the one-line fix: regression passed.
- Isolated lint mutation: both clean-gate and lint-failure tests failed as expected.
- Isolated scope mutation: rejection test failed because unowned changes printed `SCOPE OK for B2`.
- Temporary mutations were removed; tracked source was never mutated for these checks.

CHECK OUTPUT:
```text
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
................................                                         [100%]
32 passed in 1.78s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

SCOPE CHECK:
```text
SCOPE OK for B2
```

STATUS: done
OPEN QUESTIONS: none

BUG:
- Symptom: an empty unit-test suite passed the gate; lint and scope rejection lacked regression coverage.
- Cause: pytest exit code 5 was explicitly accepted; existing tests did not exercise lint or ownership failures.
- Fix: reject every nonzero pytest exit code; add real CLI regression tests.
- Guarded by: the six test functions listed above, totaling 12 cases.
- Other hits: `git grep` found the exit-code-5 acceptance only in `scripts/check.py:38`. Other comparisons at lines 33 and 50 already reject nonzero statuses; `scripts/check_scope.py:73` already rejects outside files.

JOURNAL:
- Gate now rejects pytest’s “no tests collected” exit status.
- Added isolated real gate tests for empty, passing, lint-failing, and test-failing suites.
- Added scope CLI tests covering owned/unowned unstaged, staged, committed, and untracked files.
- Both surviving Phase 0 mutations are caught; gate passes with 32 tests and task scope passes.
