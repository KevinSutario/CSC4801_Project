# Keystone: rules for every agent

You are working on Keystone, a job platform for the CSC4801 final project.
Read this file fully at the start of every task. It is short on purpose.

## Who you are

- **Orchestrator**: the main session. You plan, dispatch, review and merge. You do not write app code.
- **Subagent**: you were started with a task card or a review packet. Do only that. Nothing else.

If you are a subagent, your prompt names your task card (for example `docs/tasks/T07.md`) and your
worktree folder. Read the card. It tells you every file you may read and every file you may change.

## Hard rules

1. **Stay inside your worktree.** Every command starts with `cd <your worktree> &&`. Never edit files
   in the main repo folder or in another task's worktree.
2. **Only change files listed under "Owns" in your task card.** Need another file changed? Stop and
   report. `python scripts/check_scope.py <task-id>` must pass before you finish.
3. **Read before you write.** Never edit a file you have not opened in this session. Before calling a
   function you did not write, quote its real signature from its file.
4. **Never invent.** No made-up functions, routes, columns, config keys, Flask APIs, or library
   methods. Check `docs/plan/07-CONTRACTS.md` or the code. If it is not there, stop and ask.
5. **Rules come from the brief.** Business rules (matching, scheduling, validation limits) come from
   `docs/BRIEF.md` only. If your card says BLOCKED, or the brief section is empty, stop and report.
6. **No new dependencies.** Only what is in `requirements.lock` and `requirements-dev.txt`.
7. **Prove it.** Run `python scripts/check.py` and paste the real output before you say done. The
   words "done", "fixed" and "should work" are banned unless passing output is right above them.
8. **Two strikes then stop.** If the same error survives two fix attempts, stop and report: the exact
   error, what you tried, your two best guesses, what you need.
9. **Never weaken a test** to get green. No skipping, deleting or loosening assertions.
10. **Test first for logic.** Write the failing test, show it failing, then write the code.
11. **No git history changes.** No rebase, reset, force push, or branch deletion. Commit only on your
    own task branch. Never push. Never merge (the orchestrator merges).

## Fixing a bug

1. Write a test that fails because of the bug. Run it. Show it failing.
2. State the cause in one sentence (the mechanism, not the symptom).
3. Search for the same mistake elsewhere: `git grep -n "<pattern>"`. List the hits. Do not fix them
   in this change; report them.
4. Fix the cause with the smallest change. Show the test passing, then `python scripts/check.py`.
5. Put a `BUG:` block in your final reply (symptom, cause, test name, other hits). The orchestrator
   copies it into `docs/state/BUGS.md`.

## Stack (do not change)

- Python 3.12, Flask 3.1, Jinja2, SQLite via the standard `sqlite3` module, waitress, pytest.
- Server-rendered HTML forms. No JavaScript framework. No ORM.
- Times stored as UTC ISO-8601 strings. Converted with `zoneinfo` (needs the `tzdata` package).

## Commands (use exactly these)

```
python scripts/check.py              # the gate: lint + all tests. Must pass.
python -m pytest tests/unit/test_X.py::test_name -q    # one test
python scripts/check_scope.py T07    # are my changes inside my Owns list?
python -m flask --app app run --debug   # local run (never in Docker)
python scripts/seed.py --reset       # demo data (after task T19 exists)
```

## Where things are

- `docs/BRIEF.md`: the course brief, the source of truth for rules
- `docs/plan/`: the plan. `07-CONTRACTS.md` is the frozen list of names and signatures
- `docs/tasks/`: one card per task
- `docs/state/STATUS.md`: what is done, running, next (orchestrator updates it)
- `docs/state/JOURNAL.md`, `DECISIONS.md`, `BUGS.md`: logs
- `reviews/`: review packets, findings and verdicts

## Reply format when you finish a task

```
TASK: T07
FILES CHANGED: <paths>
TESTS ADDED: <test names>
CHECK OUTPUT: <paste the last 15 lines of python scripts/check.py>
SCOPE CHECK: <paste output of check_scope.py>
STATUS: done | blocked | failing
OPEN QUESTIONS: <or "none">
```

Write `unknown` instead of guessing anything.
