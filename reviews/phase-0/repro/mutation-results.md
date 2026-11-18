# Phase 0 mutation spot-check

Detached scratch worktree: `/private/tmp/keystone-phase0-ks-mut`, created from HEAD `6c899eb`.
All mutations were made one at a time, undone using `git checkout -- .`, and the scratch worktree was removed afterward. No app code or real tests in the main worktree were edited.

Environment for all tests:
`PATH=/private/tmp/keystone-phase0-venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`

Baseline: `python -m pytest tests/unit -q -x -p no:cacheprovider`: **20 passed**.
Mutation command: `python -m pytest tests/unit -q -x`.

| ID | Mutation | Observed result | Interpretation |
|---|---|---|---|
| M1 | `scripts/make_packet.py`: changed `base = EMPTY_TREE if phase == 0 else ...` to `phase == 1` | `1 failed, 4 passed`; `test_phase_zero_without_tags_includes_whole_repository` failed with `AssertionError: git diff phase--1..dev failed` | CAUGHT |
| M2 / G2 | `scripts/check.py:33`: changed lint `if code != 0:` to `if code == 0:` | `20 passed` | SURVIVED: no unit test catches a reversed lint-failure gate |
| M3 / G3 | `scripts/check_scope.py:73`: changed `if outside:` to `if False:` | `20 passed` | SURVIVED: no unit test catches acceptance of out-of-scope files |

Extra phase check: `python scripts/check_contracts.py` exited 0 with `CONTRACTS: nothing to check yet`.

G1: `python -m pytest tests/repro/test_g1.py -q -p no:cacheprovider` failed as predicted:
`AssertionError` at `assert result.returncode != 0, output`; subprocess returned 0 and printed `CHECK PASSED` after real pytest printed `no tests ran in 0.00s`. This repro copies only the gate and Ruff config to a temporary directory, leaving `tests/unit` present but empty.
