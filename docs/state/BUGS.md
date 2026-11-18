# Bug log

One entry per bug, including small ones. Newest at the bottom.

Template:

## B<n>: <one line symptom>
- Found by: test | review (reviews/<id>/verdict.md) | Kevin | audit issue #<n>
- Class: auth | ownership | validation | csrf | xss | injection | upload | timezone | transaction | ordering | performance | other
- Cause: <one sentence, the mechanism>
- Fix: <file and what changed>
- Guarded by: <tests/unit/file.py::test_name>
- Same cause elsewhere: <list, or "checked, none">

## B1: Phase 0 review packet requests nonexistent phase--1 tag
- Found by: `python scripts/make_packet.py phase 0` during the Phase 0 gate.
- Class: other
- Cause: The packet baseline unconditionally subtracted one from the phase number.
- Fix: `scripts/make_packet.py` uses the existing empty-tree constant for Phase 0; later phases retain predecessor tags.
- Guarded by: `tests/unit/test_make_packet.py::test_phase_zero_without_tags_includes_whole_repository`, `test_phase_one_compares_against_phase_zero_tag`, `test_phase_one_requires_phase_zero_tag`.
- Same cause elsewhere: checked, none; other search hits were status/card text and packet naming.

## B2: Empty test suite passed the gate; lint and scope rejection lacked regression coverage
- Found by: Phase 0 review (`reviews/phase-0/verdict-round1.md`), including judge mutation checks.
- Class: other
- Cause: pytest exit code 5 was explicitly accepted; existing tests did not exercise lint or ownership failures.
- Fix: `scripts/check.py` rejects every nonzero pytest status; real CLI regressions exercise gate failure and scope enforcement.
- Guarded by: `tests/unit/test_check.py::test_gate_fails_when_no_tests_are_collected`, `test_gate_passes_with_clean_lint_and_passing_test`, `test_gate_fails_when_lint_fails`, `test_gate_fails_when_a_test_fails`; `tests/unit/test_check_scope.py::test_scope_accepts_owned_changes`, `test_scope_rejects_unowned_changes` (four Git states each).
- Same cause elsewhere: exit-code-5 acceptance appeared only in `scripts/check.py:38`; other lint/contract comparisons already reject nonzero status, and scope rejection already worked. Both mutation gaps now covered.

## B3: Rename from unowned source into owned destination passed scope checking
- Found by: all three Phase 0 round 2 reviewers; judge confirmed staged and committed repros (`reviews/phase-0/verdict-round2.md`).
- Class: other
- Cause: Git's rename-aware `--name-only` output omitted the removed source path.
- Fix: `scripts/check_scope.py` adds `--no-renames` to committed, unstaged, and staged diffs.
- Guarded by: `tests/unit/test_check_scope.py::test_scope_checks_both_rename_paths` (9 cases; explicit R100 detection across three Git states and ownership directions).
- Same cause elsewhere: checked, only the three affected diff commands at `scripts/check_scope.py:57–59`.
