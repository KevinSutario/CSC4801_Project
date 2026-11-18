# 10 · Review protocol: three reviewers and a judge

Every review uses the same shape: **three reviewers do the same review independently, then one
judge checks every finding against the code and keeps only the bugs that are really there.**

A single flash-model reviewer misses a lot and invents some. Three independent reviews catch more
real bugs. The judge throws away the invented ones, so fixes are only spent on real problems.

## When a review runs (triggers)

| Trigger | When | What is reviewed | Packet command |
|---|---|---|---|
| **A. Task review** | an implementer finished a task and its check passed | the task branch against `dev` | `python scripts/make_packet.py task T07` |
| **B. Merge review** | merging a task into `dev` after `dev` has changed since the task started (another agent's work went in), or any Phase 3 task that joins two lanes | the integration branch `int/T07` against `dev`, plus the files of the lanes it joins | `python scripts/make_packet.py merge T07` |
| **C. Phase review** | all tasks in a phase are merged | everything changed in the phase, split into chunks by package | `python scripts/make_packet.py phase 2` |

## Step by step (the orchestrator runs this, via `/review-task`)

1. **Make the packet.** The command writes `reviews/<id>/packet-1.md` (and `packet-2.md`... if the
   diff is over 400 changed lines; it splits by file). A packet holds: the task card, the
   requirement rows, the security checklist, the diff, the check output and the scope output.
2. **Spawn three `reviewer` subagents at the same time**, one per packet. All three get the same prompt:
   ```
   You are reviewer <n> of 3 for <id>. Review packet: <absolute path to packet-1.md>.
   The code is in worktree <absolute path>. You may open any file in that worktree to check a claim.
   Do not edit anything. Follow your agent instructions and return findings in the exact format.
   ```
   The `<n>` only changes which checklist section the reviewer starts from (1: correctness first,
   2: security first, 3: tests first). The review itself is the same.
3. **Save the three replies** as `reviews/<id>/r1.md`, `r2.md`, `r3.md`. Do not edit them.
4. **Spawn the `review-judge`** with:
   ```
   You are the judge for <id>. Packet: <path>. Worktree: <path>.
   Findings: <path>/r1.md, r2.md, r3.md. Repro folder: <worktree>/tests/repro/
   Follow your agent instructions. Return the verdict in the exact format.
   ```
5. **Save the verdict** as `reviews/<id>/verdict.md`, and copy the judge's repro tests from
   `<worktree>/tests/repro/` to `reviews/<id>/repro/` so they are kept. (`tests/repro/` is
   gitignored and not run by the gate.)
6. **Act on it:**
   - `PASS` (no confirmed findings): go to merge.
   - `FIX`: spawn an `implementer` on the same worktree with the card plus this line:
     `Fix the CONFIRMED findings in <path>/verdict.md, in order. For each, first move its repro test
     into the right test file as a regression test, see it fail, then fix.` Then run trigger A again
     with **only the judge** checking each fixed finding plus `python scripts/check.py`. If the fix
     diff is over 80 lines, run all three reviewers again.
   - `UNCLEAR` items: ask Kevin. Do not fix guesses.
   - After 3 rounds, stop and ask Kevin.

## What reviewers check (same list for all three)

1. **Requirement**: does the code do what the card and the brief rule say? Every acceptance item?
2. **Contract**: names, signatures, routes and templates exactly as in `07-CONTRACTS.md`?
3. **Invented things**: every function, method, column, config key and Flask API used actually
   exists. Name the file or documentation for each one you are unsure of.
4. **Security**: the 12-line checklist in `04-AUTH-SECURITY.md`.
5. **Edge cases**: empty, whitespace only, too long, zero, negative, None, wrong type, duplicate,
   someone else's id, missing id, already deleted, timezone and DST.
6. **Transactions**: every write inside `transaction()`? Booking uses `immediate=True`?
7. **Tests**: are the template test names present? Do tests check failure paths? Would the test
   fail if the code were wrong (try it in your head: remove a line, does a test catch it)?
   Any test weakened, skipped or deleted?
8. **Scope**: any change outside the Owns list, any reformatting or refactoring not asked for?
9. **Performance**: queries inside loops over many rows (N+1)? Loading every row where one is needed?

## Reviewer output format (exact)

```
REVIEWER: <n>
CHECKED: <list of checklist numbers you covered>
FINDINGS: <count>

F1
severity: critical | major | minor
category: security | functional | performance | test-gap | contract | scope
where: app/jobs/service.py:42
claim: <one sentence: what is wrong>
trigger: <exact input or steps that make it go wrong>
expected: <what should happen>
actual: <what the code does instead>
evidence: <the code lines, quoted>

F2 ...
```
Rules: at most 10 findings, worst first. Only problems you can trigger or point to in a quoted line.
No style opinions. If you found nothing, write `FINDINGS: 0` and still list what you checked.

## What the judge does

The judge is the higher-level agent. It trusts nothing it has not checked itself.

1. **Group** findings from r1, r2 and r3 that have the same root cause. Note how many reviewers
   found each group (1, 2 or 3).
2. **Verify each group, one at a time:**
   - Open the quoted lines. If the code does not say what the reviewer quoted: REJECTED.
   - If it can be tested: write a small test in `<worktree>/tests/repro/test_<group>.py` that
     should fail if the bug is real. It can use the normal fixtures from `tests/conftest.py`. Run it:
     `cd <worktree> && python -m pytest tests/repro/test_<group>.py -q -p no:cacheprovider`
     Fails as predicted: CONFIRMED. Passes: REJECTED.
   - If it cannot be tested (docs, missing test, contract name): check by reading, quote the proof,
     then CONFIRMED or REJECTED.
   - If it still cannot decide: UNCLEAR, with the exact question for Kevin.
3. **Severity**: the judge sets the final severity. Being found by 3 reviewers does not make a
   bug real, and being found by 1 does not make it fake. Only the proof counts.
4. **Mutation spot-check** (trigger C only): in a scratch copy of the worktree (`../ks-mut`), make 3
   small breaking changes in the phase's most important logic (flip a comparison, remove an
   ownership check, drop a tie-breaker). Run the tests. Any change no test catches becomes a
   CONFIRMED `test-gap` finding.
5. **Never edit app code or real tests.** Only files in `tests/repro/`.

## Judge output format (exact)

```
JUDGE: <id>
RESULT: PASS | FIX | UNCLEAR

| Group | Found by | Category | Severity | Verdict | Proof |
|---|---|---|---|---|---|
| G1 (r1.F2, r3.F1) | 2 | security | critical | CONFIRMED | tests/repro/test_g1.py fails: AssertionError ... |
| G2 (r2.F4) | 1 | functional | minor | REJECTED | line 42 already strips input: "title = title.strip()" |

FIX LIST (CONFIRMED only, in this order):
1. G1: <what to fix, where, which repro test proves it>
2. ...

QUESTIONS FOR KEVIN (UNCLEAR only):
1. ...
```

## Merge review (trigger B) extra checks

- Do both sides still use the shared contracts the same way (same function names, same status values)?
- Do the joined features work together? The judge writes at least one repro test that goes through
  both features (for example: employer posts a job, candidate applies, employer sees the applicant).
- Did the merge itself change any line that neither branch changed? (It should not.)

## Phase review (trigger C) extra checks

- Read `01-REQUIREMENTS.md`: is every requirement in this phase built and tested?
- `python scripts/check_contracts.py` passes.
- The security checklist across the whole phase, not only one task.
- The mutation spot-check above.

## Bugs found later (Week 12 audit and phase 5)

Each confirmed audit issue becomes a card `docs/tasks/B<issue number>.md` from `TEMPLATE.md`, using
the bug steps in `CLAUDE.md`: failing test first, fix, log in `docs/state/BUGS.md`, then trigger A.
