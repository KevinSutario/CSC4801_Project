# 09 · Workflow: branches, ownership, merging

> Slimmed 2026-11-19 for a 3-person team. Was a heavy orchestrator+swarm protocol (int/ branches,
> six-state machine, merge reviews). Old version is in git history.

Three people, each owning a lane (`docs/state/DIVISION.md`). **P2 is the integration lead**: the only
one who merges into `dev` and writes `docs/state/*`.

## What stays (cheap, prevents real pain)

1. **One branch per task.** `git switch -c task/Txx dev`. Nobody commits on someone else's task branch.
2. **Owns lists never overlap** between tasks worked on at the same time.
   `python scripts/check_scope.py --overlap T07 T09 T12` prints `OK` before you start them together.
3. **Shared files freeze after Phase 1** (`app/__init__.py`, `app/db.py`, `app/schema.sql`,
   `app/errors.py`, `app/security.py`, `app/audit.py`, `base.html`, `components/*`,
   `tests/conftest.py`). Only a contract-change card (CCxx, run by P2) may touch them.
4. **Only P2 writes shared state** (`docs/state/*`) and merges `dev`. Everyone else hands off a branch.

## What's gone (was overhead for a swarm, not a team)

- No `int/Txx` integration branch and no separate "merge review" — merge straight onto `dev`.
- No six-state machine — states are `todo / doing / merged` (+ `blocked`).
- No JOURNAL or BUGS files — `git log` + `STATUS.md` cover it; a bug is a new `Bxx` card.
- Worktrees optional. A plain branch is fine; use a worktree only if you want two cards open at once.

## Branches

| Branch | Meaning | Who commits |
|---|---|---|
| `main` | what the graders build. Updated only at phase gates. | P2 (merge) |
| `dev` | integrated, reviewed work | P2 (merge) |
| `task/Txx` | one task, branched from `dev` | that task's owner |

Never rebase, reset or force-push. Merges only, `--no-ff`.

## A task, start to finish

1. **Claim** a card that is ready (all its `Depends on` are merged, not BLOCKED, Owns doesn't clash
   with anything in progress). Mark it `doing` — tell P2, who notes it in STATUS.md.
2. **Branch**: `git switch -c task/Txx dev`.
3. **Build** following the card. For logic, failing test first (CLAUDE.md rule 9). Change only Owns
   files.
4. **Gate**: `python scripts/check.py` must print CHECK PASSED, and `python scripts/check_scope.py Txx`
   must pass. Commit on `task/Txx`. Push the branch (or hand it to P2).
5. **Review**: one other person reviews per `10-REVIEW-PROTOCOL.md` (light or careful by card type).
6. **Merge (P2)**:
   ```
   git switch dev && git merge --no-ff task/Txx && python scripts/check.py
   ```
   If check passes, mark the card `merged` in STATUS.md and delete the task branch. If `dev` moved
   and the merge conflicts, resolve on `dev`, re-run check, and have the reviewer glance at the
   resolution.

## Phases (order still matters)

- **Phase 1** is strictly serial: T01 → T02 → T03 → T04 → T05, one at a time, because it builds the
  shared skeleton. After it merges, the shared files above are frozen.
- **Phase 2** runs up to 3 cards at once, one per person, non-overlapping Owns
  (batches {T07,T09,T12} then {T08,T10,T11}).
- **Phase 3** joins lanes; keep it to ~2 at once and watch the cross-lane dependencies in
  `08-TASKS.md`. T06 (authz sweep) goes last.
- **Phases 4–5** per `08-TASKS.md`.

### Phase gate (P2)
All the phase's cards merged → `python scripts/check.py` passes → `python scripts/check_contracts.py`
passes → each FP-* for the phase has a test (`01-REQUIREMENTS.md`). Then `git merge --no-ff dev` into
`main` and tag `phase-N`. For phase 4/5 also run `python scripts/check.py --release`.

## Contract changes (CCxx)

If a card needs a frozen shared file changed:
1. Stop; don't edit the shared file on a feature branch. Mark the card BLOCKED.
2. P2 writes a small `docs/tasks/CCnn.md` (from `TEMPLATE.md`) owning only that file + `07-CONTRACTS.md`,
   runs it alone, reviews it (careful), merges it.
3. Open task branches `git merge dev` (never rebase) to pick it up. Unblock.
4. Log it in `docs/state/DECISIONS.md`.

## Tooling is your choice

This workflow is tool-neutral. Build your cards by hand, or with any AI assistant (Claude, Cursor,
Copilot, Codex, Aider). The rules are the same for all of them and live in `AGENTS.md`; the
tool-specific files (`CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`) just point
there. Nothing in the running app or the gate depends on an AI tool.

If you do use an AI assistant on a card: give it the branch/worktree path, tell it to read `AGENTS.md`
then its task card, and to touch only the Owns files. You still review and hand off the result
yourself — the assistant is a helper, not a fourth teammate.

Claude Code users get extra convenience in `.claude/` (slash commands `/dispatch`, `/review-task`,
`/merge`, `/phase-gate`, `/orient`, `/bugfix`, and implementer/reviewer agents). These are **optional**
and Claude-only; the same steps can be run by hand or with another tool. They were built for the old
heavier protocol, so treat them as a starting point and follow the lean rules in this file where they
differ.
