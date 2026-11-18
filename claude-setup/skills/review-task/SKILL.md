---
name: review-task
description: Orchestrator step. Runs the three-reviewer plus judge review for a Keystone task, merge or phase, and acts on the verdict.
argument-hint: "[task|merge|phase|audit] [id or area]"
disable-model-invocation: true
---

Review: $ARGUMENTS. Follow `docs/plan/10-REVIEW-PROTOCOL.md`. You are the orchestrator: do not
review code yourself.

1. Make the packet: `python scripts/make_packet.py $ARGUMENTS`. It prints the packet path(s) and
   the worktree path.
2. For each packet, spawn **three `reviewer` subagents in parallel**, n = 1, 2, 3, with:
   ```
   You are reviewer <n> of 3 for <id>. Review packet: <packet path>.
   The code is in worktree <worktree path>. You may open any file in that worktree to check a claim.
   Do not edit anything. Follow your agent instructions and return findings in the exact format.
   ```
3. Save the replies, unedited, to `reviews/<id>/r1.md`, `r2.md`, `r3.md` (add `-p2` for packet 2).
4. Spawn one `review-judge` with:
   ```
   You are the judge for <id>. Packet: <packet path>. Worktree: <worktree path>.
   Findings: reviews/<id>/r1.md, r2.md, r3.md (absolute paths). Repro folder: <worktree path>/tests/repro/
   This is a <task|merge|phase> review. Follow your agent instructions. Return the verdict in the exact format.
   ```
5. Save it to `reviews/<id>/verdict.md`. Copy `<worktree>/tests/repro/*` to `reviews/<id>/repro/`.
6. Act on RESULT:
   - PASS: set REVIEWED in STATUS.md. Tell Kevin "ready for /merge <id>".
   - FIX: spawn an `implementer` on the same worktree with the normal dispatch prompt plus:
     `Fix the CONFIRMED findings in <abs path>/reviews/<id>/verdict.md, in order. For each, first move
     its repro test into the right test file as a regression test, see it fail, then fix.`
     Then re-run step 4 with only the judge (tell it: "re-check round: verify each CONFIRMED item is
     fixed and python scripts/check.py passes"). If the fix diff is over 80 lines, redo steps 1 to 5.
   - UNCLEAR: show Kevin the questions. Wait.
   - Round 3 still FIX: stop and ask Kevin.
7. Append one line to `docs/state/JOURNAL.md`: `<date> <id> review: <RESULT>, <n> confirmed, <n> rejected`.
