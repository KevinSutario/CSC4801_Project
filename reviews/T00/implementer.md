TASK: T00
FILES CHANGED: none; verification commit `fe889b2` on `task/T00`
TESTS ADDED: none
CHECK OUTPUT:
```text
=== lint: /Users/mac/ks-T00/.venv/bin/python -m ruff check .
All checks passed!

=== tests: /Users/mac/ks-T00/.venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
.................                                                        [100%]
17 passed in 0.01s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```
SCOPE CHECK:
```text
SCOPE OK for T00
OK: no overlap between T07, T09, T12
```
STATUS: done
OPEN QUESTIONS: none. Used isolated Python 3.12.14 environment; dependency installation passed. Required ignored paths and `tzdata==2026.5` verified.

JOURNAL:
- Verified T00 using an isolated Python 3.12.14 virtual environment because the shell lacked `python`.
- Installed pinned dependencies, including `tzdata==2026.5`; confirmed all required ignore patterns.
- Gate passed with Ruff clean and 17 tests passing; T00 scope and T07/T09/T12 overlap checks passed.
- Sandbox initially blocked Ruff’s cache; approved rerun passed. Recorded verification commit `fe889b2` with no tracked file changes.
