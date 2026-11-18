# Phase 0 round-two judge evidence

Snapshot: `5b8b3da6ae076e9e5fb61990e18a03e23108e07f` (current reviewer reports; reviewed sources match Phase 0 round-two packet snapshot).

Environment: `PATH=/private/tmp/keystone-phase0-venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`.

## Current findings and prior resolutions

- Rename finding: `python -m pytest tests/repro/test_round2_rename.py -q -p no:cacheprovider`: **2 failed** as predicted. Both staged and committed `git mv unowned.txt owned-new.txt` are accepted by the real scope CLI with `SCOPE OK for B3`, return code 0, despite the source path being unowned. This is one root cause reported by all three reviewers in packet 43.F1.
- Prior G1: `python -m pytest tests/repro/test_g1.py -q -p no:cacheprovider`: **1 passed**. Current `scripts/check.py:38` rejects every nonzero pytest code, including 5. B2 regression checks failure output and excludes CHECK PASSED.
- Prior G2: B2 adds real gate CLI tests for clean lint/pass and lint failure; the former lint mutation is caught, including semantic return-code assertions (see below).
- Prior G3: B2 adds owned/unowned real scope CLI tests in unstaged, staged, committed and untracked states; disabling rejection is caught.
- Full current gate: clean Ruff, **32 passed**, CHECK PASSED.
- Contract command: exit 0, `CONTRACTS: nothing to check yet`.

## Required mutation spot-check

Detached worktree `/private/tmp/keystone-phase0-round2-mut` at `5b8b3da`. Each mutation applied alone; after each, ran `python -m pytest tests/unit -q -x`, then `git checkout -- .`. The scratch worktree was removed afterward.

| Mutation | Result | Catching test |
|---|---|---|
| M1: `scripts/make_packet.py` phase baseline `phase == 0` -> `phase == 1` | CAUGHT: 1 failed, 16 passed | `test_phase_zero_without_tags_includes_whole_repository`: `AssertionError: git diff phase--1..dev failed` |
| M2: `scripts/check.py:33` lint condition `code != 0` -> `code == 0` | CAUGHT: 1 failed, 4 passed | `test_gate_fails_when_no_tests_are_collected` notices erroneous lint failure; focused semantic confirmation below |
| M3: `scripts/check_scope.py:73` `if outside:` -> `if False:` | CAUGHT: 1 failed, 12 passed | `test_scope_rejects_unowned_changes[unstaged]`: `AssertionError: SCOPE OK for B2` |

For M2, additionally ran the two dedicated lint tests while the mutation remained active: `test_gate_fails_when_lint_fails` and `test_gate_passes_with_clean_lint_and_passing_test`: **2 failed**. The lint-error case incorrectly returned 0/CHECK PASSED; the clean-lint case incorrectly returned 1/CHECK FAILED: lint. These failures confirm B2 repairs the prior lint regression gap.

No mutations survived. No tracked source, real tests, or state/docs in the main worktree were edited by this judge.
