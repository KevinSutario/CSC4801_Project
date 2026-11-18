---
name: phase-gate
description: Orchestrator step. Closes a Keystone phase with a phase review, release checks, a merge to main and a tag.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

Close phase $ARGUMENTS.

1. Every task of phase $ARGUMENTS in `docs/plan/08-TASKS.md` is MERGED in STATUS.md. If not, stop.
2. In the main folder on `dev`: `python scripts/check.py` and `python scripts/check_contracts.py`.
3. Phase review: `/review-task phase $ARGUMENTS`. The packet tool splits it by package. Continue only
   when every chunk's verdict is PASS (fixes go through bug cards `docs/tasks/Bxx.md`).
4. Phase 4 and 5 only: `python scripts/check.py --release` (fails on any skipped test), then the
   fresh-clone Docker check in `docs/plan/12-DEPLOY.md`. Ask Kevin to do the browser sign-in check.
5. Ask Kevin to approve. Then:
   `git checkout main && git merge --no-ff dev -m "phase $ARGUMENTS" && git tag phase-$ARGUMENTS && git checkout dev`
   Pushing is Kevin's call: ask before `git push origin main dev --tags`.
6. STATUS.md: phase $ARGUMENTS closed, next phase open. Then tell Kevin to run `/clear` and `/orient`.
