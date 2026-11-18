TASK: B1  
COMMIT: `6696ff2` on `task/B1`  
FILES CHANGED: `scripts/make_packet.py`, `tests/unit/test_make_packet.py`  
TESTS ADDED:

- `test_phase_zero_without_tags_includes_whole_repository`
- `test_phase_one_compares_against_phase_zero_tag`
- `test_phase_one_requires_phase_zero_tag`

FAILING OUTPUT:
```text
E AssertionError: git diff phase--1..dev failed: fatal: ambiguous argument 'phase--1..dev': unknown revision or path not in the working tree.
1 failed in 0.10s
```

REGRESSION OUTPUT:
```text
3 passed in 0.29s
```

CHECK OUTPUT:
```text
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
....................                                                     [100%]
20 passed in 0.32s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

SCOPE CHECK:
```text
SCOPE OK for B1
```

STATUS: done  
OPEN QUESTIONS: none

BUG:
- Symptom: Phase 0 packet generation failed without nonexistent `phase--1`.
- Cause: The baseline calculation unconditionally subtracted one from the phase.
- Test: `test_phase_zero_without_tags_includes_whole_repository`.
- Other hits: No other predecessor calculations. Search found references in `docs/state/STATUS.md:12`, `docs/tasks/B1.md:1,8`, and packet naming at `scripts/make_packet.py:164`.

JOURNAL:
- Phase 0 now uses the existing Git empty-tree constant.
- Phase 1 retains its `phase-0` baseline and missing-tag failure.
- CLI regression tests use temporary repositories; no main-repository packets generated.
- Committed passing changes; worktree clean.
