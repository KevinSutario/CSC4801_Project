---
name: merge
description: Orchestrator step. Merges a reviewed Keystone task into dev through an integration branch, running a merge review when other work has landed meanwhile.
argument-hint: "[task-id]"
disable-model-invocation: true
---

Merge task $ARGUMENTS. Never rebase, reset or force.

1. STATUS.md must say REVIEWED for $ARGUMENTS. The main folder must be on `dev`. Commit your own
   state first: `git add docs/state reviews && git commit -m "state: before merging $ARGUMENTS"`.
   Then `git status` must be clean. If anything else is uncommitted, stop and tell Kevin.
2. Integration branch:
   `git worktree add ../ks-int -b int/$ARGUMENTS dev`
   `cd ../ks-int && git merge --no-ff task/$ARGUMENTS -m "merge $ARGUMENTS"`
   If there is a merge conflict: `git merge --abort`, mark BLOCKED, tell Kevin. Do not resolve it yourself.
3. `cd ../ks-int && python scripts/check.py`. Must pass.
4. Merge review needed if either is true:
   - `git log --oneline task/$ARGUMENTS..dev` is not empty (dev moved since the task began), or
   - the task card says `Joins lanes: yes`.
   If needed: run `/review-task merge $ARGUMENTS` and continue only on PASS.
5. In the main folder: `git merge --no-ff int/$ARGUMENTS -m "$ARGUMENTS into dev"`, then
   `python scripts/check.py`. Must pass.
6. Clean up: `git worktree remove ../ks-int`, `git worktree remove ../ks-$ARGUMENTS`,
   `git branch -d int/$ARGUMENTS` (task branches are kept).
7. STATUS.md: MERGED. JOURNAL.md: append the `JOURNAL:` block from `reviews/$ARGUMENTS/implementer.md`.
   If the reply had a `BUG:` block, append it to `docs/state/BUGS.md`.
8. Say which tasks are now READY.
