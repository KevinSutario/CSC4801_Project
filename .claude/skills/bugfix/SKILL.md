---
name: bugfix
description: Orchestrator step. Turns a bug report (from a review, from Kevin, or a Week 12 audit issue) into a bug card and runs it through dispatch and review.
argument-hint: "[short bug description or audit issue number]"
disable-model-invocation: true
---

Bug: $ARGUMENTS

1. Make a card `docs/tasks/B<next number or issue number>.md` from `docs/tasks/TEMPLATE.md`:
   - Goal: the wrong behaviour and the expected behaviour, with exact steps.
   - Owns: only the files that must change, and the test file for that area. Find them from
     `docs/plan/07-CONTRACTS.md`, not by reading code.
   - Steps: the "Fixing a bug" steps from CLAUDE.md.
   - For an audit issue: the issue link and commit SHA, and the label it will get (`audit:repair`).
2. Commit the card on `dev` (docs only).
3. `/dispatch B<n>`, then `/review-task task B<n>`, then `/merge B<n>`.
4. Append to `docs/state/BUGS.md`: symptom, cause, regression test, other places with the same mistake.
