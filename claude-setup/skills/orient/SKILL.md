---
name: orient
description: Orchestrator start-of-session step. Loads project state and proposes which Keystone tasks to run next. Read-only.
disable-model-invocation: true
allowed-tools: Read, Glob, Bash(git status:*), Bash(git branch:*), Bash(git worktree list:*), Bash(git log:*), Bash(python scripts/check_scope.py:*)
---

You are the orchestrator. Do not read app code.

1. Read `CLAUDE.md`, `docs/state/STATUS.md`, and only the current phase section of
   `docs/plan/08-TASKS.md`.
2. Run `git status`, `git branch --show-current` (must be `dev`), `git worktree list`.
3. List: tasks RUNNING, CHECKED (waiting for review), REVIEWED (waiting for merge), BLOCKED and why.
4. List READY tasks: every `Depends on` task is MERGED, not BLOCKED, and not waiting for the brief.
5. Pick up to 3 READY tasks that can run together. Check with
   `python scripts/check_scope.py --overlap <ids...>` (include RUNNING tasks). It must print OK.
6. Reply:
   ```
   PHASE: <n>
   RUNNING: ...    CHECKED: ...    REVIEWED: ...    BLOCKED: ...
   PROPOSE: dispatch <ids>, because <one line each>
   NEXT ACTION FOR KEVIN: <approve, or answer a blocker>
   ```
Do not dispatch anything until Kevin says yes.
