# Keystone: rules for everyone

Keystone is a job platform for the CSC4801 final project. Read this file at the start of a task.
It is short on purpose.

**This is the canonical rules file.** It is tool-neutral: it applies to every person and to any AI
coding assistant (Claude, Cursor, Copilot, Codex, Aider, or none). Tool-specific files
(`CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`) are thin pointers to this one —
do not put rules in them.

> Process note: this is a 3-person team, not a swarm of agents. The heavy agent protocol was
> slimmed on 2026-11-19 (see `docs/state/DECISIONS.md`, D20). The three lanes and owners are in
> `docs/state/DIVISION.md`.

## Who you are

- **Owner**: one of the three people (P1/P2/P3 in `docs/state/DIVISION.md`). You build your own task
  cards on your own branch. You may use any AI assistant to help, but you own the result.
- **Integration lead (P2)**: also the only one who merges into `dev` and writes `docs/state/*`.
- **AI assistant** (optional): if you have one build a card, give it this file and the card's Owns
  list, nothing else. The assistant is a helper, not a fourth teammate.

## Hard rules (these stay strict — they are cheap and they save rework)

1. **Only change files listed under "Owns" in your task card.** Need another file changed? Stop and
   ask the owner of that file. `python scripts/check_scope.py <task-id>` must pass before you finish.
2. **Read before you write.** Never edit a file you have not opened. Before calling a function you did
   not write, quote its real signature from its file.
3. **Never invent.** No made-up functions, routes, columns, config keys, Flask APIs, or library
   methods. Check `docs/plan/07-CONTRACTS.md` or the code. If it is not there, stop and ask.
4. **Rules come from the brief.** Business rules (matching, scheduling, validation limits) come from
   `docs/BRIEF.md` only. If your card says BLOCKED, or the brief section is empty, stop and ask P2.
5. **No new dependencies.** Only what is in `requirements.lock` and `requirements-dev.txt`.
6. **Prove it.** Run `python scripts/check.py` and paste the real output before you say done. The
   words "done", "fixed" and "should work" are banned unless passing output is right above them.
7. **Two strikes then stop.** If the same error survives two fix attempts, stop and ask: the exact
   error, what you tried, your two best guesses, what you need.
8. **Never weaken a test** to get green. No skipping, deleting or loosening assertions.
9. **Test first for logic.** For matching, scheduling and any non-trivial rule: write the failing
   test, show it failing, then write the code. (Plain CRUD + templates don't need test-first.)
10. **No history rewrites.** No rebase, reset, force push, or branch deletion. Work on your own
    `task/Txx` branch. Only P2 merges into `dev`.

## The lean flow (full detail in `docs/plan/09-AGENT-WORKFLOW.md`)

- **One branch per task.** `git switch -c task/Txx dev`, work, commit. Worktrees optional.
- **Review = one non-author peer reads it**, light or careful by card type (`10-REVIEW-PROTOCOL.md`).
- **Merge straight onto `dev`** (P2, `--no-ff`). No `int/` branch.
- **States**: `TODO → DOING → MERGED` (+ `BLOCKED`).
- **Logs**: `STATUS.md` + `git log`. `DECISIONS.md` for real decisions. A bug is a new `Bxx` card.

## Fixing a bug

1. Write a test that fails because of the bug. Run it. Show it failing.
2. State the cause in one sentence (the mechanism, not the symptom).
3. Check for the same mistake elsewhere: `git grep -n "<pattern>"`. Note the hits.
4. Fix the cause with the smallest change. Show the test passing, then `python scripts/check.py`.

## Stack (do not change)

- Python 3.12, Flask 3.1, Jinja2, SQLite via the standard `sqlite3` module, waitress, pytest.
- Server-rendered HTML forms. No JavaScript framework. No ORM.
- Times stored as UTC ISO-8601 strings. Converted with `zoneinfo` (needs the `tzdata` package).

Nothing in the running application depends on any AI tool: `flask run`, `python scripts/check.py`,
`docker build` all work on their own.

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
- `docs/state/DIVISION.md`: who owns which task (P1/P2/P3)
- `docs/state/STATUS.md`: what is done, doing, next (P2 updates it)
- `docs/state/DECISIONS.md`: decisions worth remembering
- `reviews/`: short peer-review notes

## Reply / hand-off format when you finish a task

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
