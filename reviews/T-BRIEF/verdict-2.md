JUDGE: T-BRIEF (re-check round, commit b1aa462)
RESULT: FIX

Docs-only task: no repro tests written (nothing executable). Everything below was verified by reading the worktree files (HEAD = `b1aa462 T-BRIEF: Fill rules from the course brief (fix verdict items 1-10)`), not the packet.

Gate: `python scripts/check.py` prints `All checks passed!`, `41 passed in 19.57s`, `CHECK PASSED`. `python scripts/check_scope.py T-BRIEF` prints `SCOPE OK for T-BRIEF`. `git diff 47701ca..b1aa462 --stat` touches exactly 10 files, all in Owns. `git grep "(from the brief)"` hits only `docs/tasks/T-BRIEF.md` (the instructions themselves).

Previous fix list (verdict.md items 1 to 10), each verified fixed:
1. G1 T10: `T10.md:5` now `**BLOCKED** (NEEDS DECISION, same as the FP-EMP-2 row ...)` naming cascade/409, 404/403 and closed jobs; `:21-25` explains Steps/Tests left as written is why it is BLOCKED. FIXED.
2. G2+G5 T16/T12/plan: `T16.md:5` BLOCKED with three numbered reasons; `:71-72`, `:73-76`, `:86-89` carry CONFLICT marks on Steps 3-4 and the "slot of a different job" case; `T12.md:31` quotes `> - the slot belongs to the employer for the candidate's application;` (verbatim `BRIEF.md:115`); `01-REQUIREMENTS.md:201` FP-SCHED-2 NEEDS DECISION. FIXED.
3. G3 closed jobs: `T13.md:25-30`, `T10.md:34-38`, `01-REQUIREMENTS.md:108-111` all say CONFLICT; `01-REQUIREMENTS.md:82` FP-CAN-2 NEEDS DECISION; `T13.md:5` BLOCKED. FIXED.
4. G7 T15 key list: `T15.md:26-32` lists `application_id, candidate_id, candidate_name, headline, skills, score, matched, missing, status, applied_at, booking, resume_id` with the DEFAULT mark. FIXED (see new G2 for a leftover).
5. G9 T07: `T07.md:5` BLOCKED on the display-name gap; `01-REQUIREMENTS.md:81` FP-CAN-1 names it. FIXED.
6. G4+G14 T06: `T06.md:5` BLOCKED matching `01-REQUIREMENTS.md:47`; `T06.md:34` list now `(T08, T10, T12, T14, T15, T16)`. FIXED.
7. G8 T15 resume: `T15.md:33-37` CONFLICT paragraph quoting FP-CAN-1; `T15.md:83-84` Step 4 link marked CONFLICT; `:5` status updated. FIXED.
8. G17 T17: `T17.md:5` BLOCKED with the same-candidate-twice reason; `:24-31` explains; `01-REQUIREMENTS.md:202` FP-SCHED-3 NEEDS DECISION. FIXED (see new G3 for a wrong sentence inside the new text).
9. G13 FP-MATCH-2: `01-REQUIREMENTS.md:193-194` quotes the full paragraph, verbatim against `BRIEF.md:102`. FIXED.
10. G11 T11: `T11.md:38-42` drops "need no re-normalising", adds the OPEN QUESTION on "collapse spaces" (matches `07-CONTRACTS.md:94`). FIXED.

New findings:

| Group | Found by | Category | Severity | Verdict | Proof |
|---|---|---|---|---|---|
| G1 (r1.F1, r2.F1, r3.F2): T12 stays READY while the plan says the 403/404 decision is needed before T12 runs, T10 is BLOCKED for the identical conflict, and T12's own text makes its job-attached design hinge on the T16 decision | 3 | contract | minor | CONFIRMED | `T12.md:5` `READY (...)`; `T12.md:33-35` "Attaching slots to jobs is only acceptable if booking (T16) still allows any slot of the same employer; that is the T16 CONFLICT and the orchestrator's decision, not this card's."; `T12.md:37-38` CONFLICT 403 vs NotFound; `T12.md:70`, `:90` NotFound; `01-REQUIREMENTS.md:74-75` "Decision needed before those cards run."; `T10.md:5` cites the same line as a BLOCKED reason; `01-REQUIREMENTS.md:200` FP-SCHED-1 READY. Minor because CC01 (dev) D9 and D13 rewrite T12's Goal, Contract, Steps and Tests for employer-owned slots and `Forbidden`. |
| G2 (r1.F2, r2.F2): restored key list adds `booking` but Step 2 names no query that produces it, and the test fixes the query count | 2 | contract | minor | CONFIRMED | `T15.md:28-29`, `:76-78`, `:92`; May read has no file defining `bookings`/`interview_slots`. Contained: T15 is BLOCKED. CC01: "Step 2 adds one query for the bookings of those applications (joined to `interview_slots`) ... May read adds `docs/plan/03-DATA-MODEL.md (tables: applications, bookings, interview_slots)`." |
| G3 (r1.F3, r2.F3, r3.F1): T17's new text says `07-CONTRACTS.md` is "outside this task's May read", false for T17, which lists that file | 3 | contract | minor | CONFIRMED | `T17.md:29-31` versus `T17.md:45`; `07-CONTRACTS.md:277` is inside the scheduling section. True of T-BRIEF's May read, not T17's. CC01 sets T17 READY with the `Forbidden` default (D14). |
| G4 (r1.F4): T13's closed-jobs CONFLICT block names the Contract line and the test bullet but not Step 3, which also hides closed jobs | 1 | contract | minor | CONFIRMED | `T13.md:25-30` names only the Contract and the test bullet; `T13.md:56` "`get_job` (NotFound if missing or closed)" unmarked. Contained: T13 is BLOCKED. CC01 D18 removes the closed state everywhere. |

FIX LIST (CONFIRMED only, worst first):
1. G1: `docs/tasks/T12.md:5` set Status to BLOCKED / NEEDS DECISION with two reasons, and set `01-REQUIREMENTS.md:200` FP-SCHED-1 to NEEDS DECISION; or, since CC01 rewrites T12 entirely, merge as is and let CC01 land first (T12 must not be dispatched before CC01).
2. G3: `docs/tasks/T17.md:30` change "outside this task's May read" to "outside T-BRIEF's May read" (or cite `07-CONTRACTS.md:277` directly).
3. G2: `docs/tasks/T15.md:76-78` Step 2 add a third single query for the `booking` key, and add `03-DATA-MODEL.md (tables: bookings, interview_slots)` to May read. Already specified in CC01.
4. G4: `docs/tasks/T13.md:56` add a CONFLICT mark on Step 3's "NotFound if missing or closed". Already covered by CC01 D18.

All four are minor leftovers that CC01 on dev already rewrites. If the orchestrator prefers, merging b1aa462 and running CC01 next resolves every item above without another T-BRIEF fix round; the one real hazard is G1, because T12 is the only READY phase-2 card carrying an undecided rule and must not be dispatched before CC01 merges.

QUESTIONS FOR KEVIN (UNCLEAR only):
none

Orchestrator decision (D19): merged as is; all four items carried into docs/tasks/CC01.md; no phase-2 card is dispatched before CC01 merges.
