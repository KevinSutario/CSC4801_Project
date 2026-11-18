---
name: dispatch
description: Orchestrator step. Creates a worktree and branch for one Keystone task and starts an implementer subagent on it.
argument-hint: "[task-id]"
disable-model-invocation: true
---

Dispatch task $ARGUMENTS. You are the orchestrator. Do not read app code.

1. Check `docs/tasks/$ARGUMENTS.md` exists and does not say BLOCKED. Check its `Depends on` tasks
   are MERGED in `docs/state/STATUS.md`. If not, stop and say why.
2. Overlap check with every RUNNING task:
   `python scripts/check_scope.py --overlap $ARGUMENTS <running ids>`. Must print OK.
3. Create the worktree next to the repo:
   `git worktree add ../ks-$ARGUMENTS -b task/$ARGUMENTS dev`
   Get its absolute path with `cd ../ks-$ARGUMENTS && pwd`.
4. In `docs/state/STATUS.md`, set the task to RUNNING with the worktree path and the time. Commit:
   `git add docs/state && git commit -m "state: dispatch $ARGUMENTS"`.
5. Spawn the `implementer` subagent with exactly this prompt (fill the two values):
   ```
   You are the implementer for task $ARGUMENTS.
   Worktree: <absolute path>. Start every shell command with: cd "<absolute path>" &&
   Read, in order: <absolute path>/CLAUDE.md, then <absolute path>/docs/tasks/$ARGUMENTS.md.
   Then read only the files listed under "May read" in that card.
   Follow the card's steps. Commit on branch task/$ARGUMENTS when python scripts/check.py passes.
   Finish with the reply format in CLAUDE.md.
   ```
   Do not add anything else. If several tasks are dispatched together, spawn them in parallel.
6. When it replies, save the reply to `reviews/$ARGUMENTS/implementer.md`. Then run yourself:
   `cd ../ks-$ARGUMENTS && python scripts/check.py && python scripts/check_scope.py $ARGUMENTS`
   - Both pass: set CHECKED in STATUS.md and tell Kevin "ready for /review-task $ARGUMENTS".
   - Fail: spawn one new implementer with the same prompt plus
     `Previous attempt failed. Output: <paste>. Fix only that.` A second failure: BLOCKED, ask Kevin.
   - Reply says blocked or CONTRACT CHANGE NEEDED: set BLOCKED with the reason. See
     `docs/plan/09-AGENT-WORKFLOW.md`, "Contract change requests".
