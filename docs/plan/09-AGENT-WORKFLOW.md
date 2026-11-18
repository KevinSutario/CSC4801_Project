# 09 · Agent workflow: dispatch, isolation, context, merging

This file is for the **orchestrator** (your main Claude Code session). Subagents do not need it.

## Who does what

| Agent | Defined in | Tools | Job | Writes to |
|---|---|---|---|---|
| Orchestrator | main session + `.claude/skills/` | all | picks tasks, makes worktrees, spawns agents, saves their reports, merges, updates state | `docs/state/*`, `reviews/*`, git branches |
| `implementer` | `.claude/agents/implementer.md` | Read, Edit, Write, Bash, Grep, Glob | builds one task card in one worktree | only its card's Owns files, on its task branch |
| `reviewer` | `.claude/agents/reviewer.md` | Read, Grep, Glob, Bash | reviews one packet, returns findings | nothing (returns text) |
| `review-judge` | `.claude/agents/review-judge.md` | Read, Grep, Glob, Bash, Write | checks every finding is real, with proof | `<worktree>/tests/repro/` (gitignored) and its verdict text |

Claude Code subagents cannot start other subagents. So **only the orchestrator spawns agents**,
including the three reviewers and the judge.

## The golden rules

1. **One task, one agent, one worktree, one branch.** Nobody shares a working folder.
2. **Owns lists never overlap** between tasks that run at the same time.
   `python scripts/check_scope.py --overlap T07 T09 T12` must print `OK` before you dispatch them together.
3. **Shared files are frozen after Phase 1** (`app/__init__.py`, `app/db.py`, `app/schema.sql`,
   `app/errors.py`, `app/security.py`, `app/audit.py`, `base.html`, `components/*`, `tests/conftest.py`).
   Only a contract change task may touch them.
4. **Only the orchestrator writes shared state** (`docs/state/*`, `reviews/*`). Agents return text;
   the orchestrator saves it. No two agents ever write the same file. The orchestrator commits these
   on `dev` right away (`git add docs/state reviews && git commit -m "state: ..."`), so the main
   folder stays clean for merges.
5. **The orchestrator never reads app code.** It reads cards, agent reports, check output and
   verdicts. This keeps its own context small and clear. Reading code is the reviewers' job.
6. **At most 3 agents run at once.** More than that and the model endpoint slows down, and you lose
   track.

## Folder layout on your computer

```
CSC4801_TeamA/           main worktree, always on branch dev, the orchestrator works here
ks-T07/                  worktree for task T07, branch task/T07  (sibling folder, created by /dispatch)
ks-T09/                  worktree for task T09, branch task/T09
ks-int/                  integration worktree for merge reviews, branch int/<id>
```
Worktrees live **next to** the repo folder (`../ks-T07`), never inside it.

## Branches

| Branch | Meaning | Who commits |
|---|---|---|
| `main` | what the auditors build. Updated only at phase gates. | orchestrator (merge) |
| `dev` | integrated, reviewed work | orchestrator (merge) |
| `task/Txx` | one task's work, from `dev` | the implementer |
| `int/Txx` | dev + one task, for a merge review | orchestrator |

Never rebase, reset or force-push. Merges only, with `--no-ff`.

## The task lifecycle

```
READY ──/dispatch──> RUNNING ──report──> CHECKED ──/review-task──> REVIEWED ──/merge──> MERGED
   ^                    │                    │                         │
   │                    └── blocked ──> BLOCKED (needs Kevin or the brief)
   │                                         └── fails ──> fix round (max 2) ──> REVIEWED
   └──────────── confirmed findings ──> FIXING ──> back to CHECKED
```

### 1. Pick tasks (`/orient`)
- Read `docs/state/STATUS.md` and the current phase in `08-TASKS.md`. Nothing else.
- A task is READY when: all its `Depends on` tasks are MERGED, it is not BLOCKED, and its Owns list
  does not overlap any RUNNING task.

### 2. Dispatch (`/dispatch T07`)
```
git worktree add ../ks-T07 -b task/T07 dev
python scripts/check_scope.py --overlap T07 <every RUNNING task>
```
Mark T07 RUNNING in STATUS.md. Then spawn the `implementer` subagent with exactly this prompt:

```
You are the implementer for task T07.
Worktree: <absolute path to ks-T07>. Start every shell command with: cd "<that path>" &&
Read, in order: <worktree>/CLAUDE.md, then <worktree>/docs/tasks/T07.md.
Then read only the files listed under "May read" in that card.
Follow the card's steps. Commit on branch task/T07 when python scripts/check.py passes.
Finish with the reply format in CLAUDE.md.
```
Do not add anything else to the prompt. Everything the agent needs is in the card. That is the
point: a fresh agent with a small, exact context.

### 3. Check the report
In the task's worktree run, yourself:
```
cd ../ks-T07 && python scripts/check.py && python scripts/check_scope.py T07
```
- Both pass: CHECKED.
- Either fails: spawn a new `implementer` with the same prompt plus one line:
  `Previous attempt failed. Output: <paste the failing output>. Fix only that.`
  Two failed rounds: mark BLOCKED, log it, and ask Kevin.

### 4. Review (`/review-task T07`)
See `10-REVIEW-PROTOCOL.md`. Three reviewers in parallel, then the judge.

### 5. Merge (`/merge T07`)
```
git worktree add ../ks-int -b int/T07 dev        (reuse ks-int if free)
cd ../ks-int && git merge --no-ff task/T07
python scripts/check.py
```
- If `dev` changed since T07 started (another task merged), this is a **merge of two agents' work**:
  run the merge review (`10-REVIEW-PROTOCOL.md`, trigger B) on `int/T07` before going on.
- Then, in the main folder: `git merge --no-ff int/T07` into `dev`, run `python scripts/check.py`
  again, mark MERGED, append the task's journal lines to `docs/state/JOURNAL.md`.
- Remove worktrees: `git worktree remove ../ks-T07` and `git worktree remove ../ks-int`.

### 6. Phase gate (`/phase-gate 2`)
All tasks in the phase MERGED, then the phase review (trigger C), then
`python scripts/check.py --release` if it is phase 4 or 5, then merge `dev` into `main` and tag
`phase-2`.

## Keeping every agent in its best state (context management)

| Risk | What we do |
|---|---|
| Long sessions make the model forget rules | Every implementer and reviewer is a **fresh subagent**. The orchestrator `/clear`s after every phase gate, and whenever its context is about half full, after updating STATUS.md. Then it runs `/orient`. |
| Agent wanders around the repo | The card's **May read** list. Reviewers get one packet file. |
| Agent changes other people's files | **Owns** list + `check_scope.py` + separate worktrees |
| Agent invents functions | `07-CONTRACTS.md` + `python scripts/check_contracts.py` in the gate |
| Two agents disturb each other | Separate folders, separate branches, non-overlapping Owns, temp databases in tests, only the orchestrator writes shared files |
| Rules drift | Business rules only from `docs/BRIEF.md`; BLOCKED items stop work |
| Orchestrator overloaded | It never reads code; it reads short reports. STATUS.md is its memory. |
| Agent stuck in a loop | Two-strikes rule in CLAUDE.md; orchestrator caps fix rounds at 2 |

## Contract change requests

When an implementer reports `CONTRACT CHANGE NEEDED`:
1. Do not let it edit the shared file. Mark its task BLOCKED.
2. Write a small card `docs/tasks/CCnn.md` (copy `TEMPLATE.md`) that owns only the shared file and
   `07-CONTRACTS.md`.
3. Wait until no other task is RUNNING. Run CCnn alone, review it (trigger A), merge it.
4. In every open task worktree: `git merge dev` (a merge, never a rebase). Then unblock.
5. Log it in `docs/state/DECISIONS.md`.

## When the brief arrives

1. Paste it into `docs/BRIEF.md`.
2. Run one `implementer` on card `T-BRIEF` (in `08-TASKS.md`). It fills the rule text and open
   questions in `01-REQUIREMENTS.md` and the BLOCKED sections of task cards, citing brief sections.
3. Review it with trigger A. Merge. Now BLOCKED tasks can run.

## Daily routine for Kevin

1. Open Claude Code in `CSC4801_TeamA` (on `dev`). Run `/orient`.
2. Approve the tasks it proposes. It runs `/dispatch` for each.
3. When agents report, it runs `/review-task`, then `/merge`.
4. At the end of a phase it runs `/phase-gate`.
5. Before stopping: it updates STATUS.md. Then `/clear`.
