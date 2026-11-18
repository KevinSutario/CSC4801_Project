JUDGE: phase-0
RESULT: FIX

| Group | Found by | Category | Severity | Verdict | Proof |
|---|---|---|---|---|---|
| G1 (r2.packet17.F1) | 1 | test-gap | major | CONFIRMED | `tests/repro/test_g1.py` fails: `AssertionError` at `assert result.returncode != 0`. Real pytest prints `no tests ran`; the gate returns 0 and prints `CHECK PASSED`. |
| G2 (judge.M2) | judge | test-gap | minor | CONFIRMED | Reversing the lint failure comparison in `scripts/check.py:33` survives: `20 passed`. |
| G3 (judge.M3) | judge | test-gap | minor | CONFIRMED | Removing scope rejection with `if False` in `scripts/check_scope.py:73` survives: `20 passed`. |

FIX LIST (CONFIRMED only, worst first):
1. G1: Required bug card `docs/tasks/B2.md`: make `scripts/check.py:main` reject pytest exit code 5. Promote `tests/repro/test_g1.py` into a regression test before fixing.
2. G2: Include in B2 regression coverage proving lint failure makes the gate fail and lint success permits it to continue.
3. G3: Include in B2 regression coverage proving `scripts/check_scope.py:check_task` rejects files outside the task’s Owns list.

QUESTIONS FOR KEVIN (UNCLEAR only):
None.

MUTATION RESULTS:
- Baseline: 20 passed.
- M1: Reversing the phase-zero baseline comparison was caught: 1 failed, 4 passed.
- M2: Reversing lint failure handling survived: 20 passed; G2 confirmed.
- M3: Disabling scope rejection survived: 20 passed; G3 confirmed.
- Every mutation was undone; the detached scratch worktree was removed. Evidence: `tests/repro/mutation-results.md`.
- Contract check exited 0: `CONTRACTS: nothing to check yet`.
