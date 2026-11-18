REVIEWER: 1
CHECKED: 1 (requirement and contract: every fix-list item 1 to 10 checked against the worktree at b1aa462; every new quote in the fix diff compared word for word with docs/BRIEF.md; Owns, Contract blocks and test names unchanged in the diff; `git grep "(from the brief)"` finds only T-BRIEF.md's own instructions; `python scripts/check_scope.py T-BRIEF` prints `SCOPE OK for T-BRIEF`), 2 (security checklist: docs-only change, no routes, SQL, templates or uploads; nothing applicable), 3 (tests and edges: no test files touched; checked that card test bullets still match 01-REQUIREMENTS test names).

Fix-list verification (all applied):
1. T10 status BLOCKED with cascade/409, 403/404 and closed-jobs reasons: `docs/tasks/T10.md:5`, `:21-25`, `:34-38`. Applied.
2. T16 BLOCKED with the three reasons (`T16.md:5`), CONFLICT marks on Steps 3-4 (`:71-76`) and the ineligible test case (`:86-89`); T12 now quotes BRIEF.md:115 verbatim (`T12.md:31`); FP-SCHED-2 row NEEDS DECISION (`01-REQUIREMENTS.md:201`). Applied.
3. "NOT IN BRIEF" replaced by CONFLICT in `T13.md:25-30`, `T10.md:34-38`, `01-REQUIREMENTS.md:108-111`; FP-CAN-2 row NEEDS DECISION (`:82`); T13 BLOCKED (`T13.md:5`). Applied.
4. T15 definitive key list restored with DEFAULT mark (`T15.md:26-32`). Applied (see F2 for a leftover).
5. T07 BLOCKED / NEEDS DECISION and FP-CAN-1 row updated (`T07.md:5`, `:23-27`; `01-REQUIREMENTS.md:81`). Applied.
6. T06 BLOCKED matching the FP-AUTH-3 row, T16 added to the list (`T06.md:5`, `:34`). Applied.
7. `resume_id` and the `/resumes/<id>` link relabelled CONFLICT (`T15.md:33-37`, `:82-84`), status line updated (`:5`). Applied.
8. T17 BLOCKED with the same-candidate-twice reason (`T17.md:5`, `:24-31`); FP-SCHED-3 row NEEDS DECISION (`01-REQUIREMENTS.md:202`). Applied (see F3).
9. FP-MATCH-2 full paragraph quoted (`01-REQUIREMENTS.md:193-194`), identical to BRIEF.md:102. Applied.
10. T11 "need no re-normalising" dropped, OPEN QUESTION added (`T11.md:38-42`); "strip, lower-case, collapse spaces" matches `07-CONTRACTS.md:94`. Applied.

FINDINGS: 4

F1
severity: minor
category: contract
where: docs/tasks/T12.md:5
claim: T12 stays READY although its own Requirement now says its slot-per-job design is only acceptable depending on an undecided orchestrator decision, the same inconsistency the verdict's G5 flagged for T16.
trigger: Dispatch T12 as READY; it builds `/employer/jobs/<int:job_id>/slots`, `list_slots_for_job(conn, employer_id, job_id)` and the DEFAULT "no overlap with another slot of the same job"; the orchestrator then decides the T16 CONFLICT as "slots belong to the employer, not a job" (one of the two options T12 itself names).
expected: Either T12 is BLOCKED / NEEDS DECISION alongside T16 and the FP-SCHED-2 row, or the card states that the job attachment is final for storage regardless of the booking decision.
actual: Status is `READY (rules quoted from the brief; duration default SUPERSEDED; the rest DEFAULT (not in brief))` while the Requirement says the design's acceptability hinges on a decision not yet made; the FP-SCHED-1 row in `01-REQUIREMENTS.md:200` is also READY.
evidence: `T12.md:33-35` "So a slot's owner is the employer. Attaching slots to jobs is only acceptable if booking (T16) still allows any slot of the same employer; that is the T16 CONFLICT and the orchestrator's decision, not this card's." `T12.md:26-27` "no overlap with another slot of the same job". `07-CONTRACTS.md:265-270` `create_slot(conn, employer_id, job_id, ...)`, `list_slots_for_job(conn, employer_id, job_id)`.

F2
severity: minor
category: contract
where: docs/tasks/T15.md:76-78
claim: The restored key list (fix item 4) adds `booking` and `skills`, but Step 2 still enumerates only two queries (applications with name and headline, candidates' skills) and no query for bookings, so an agent following Step 2 literally cannot fill the `booking` key the test demands.
trigger: T15 agent implements `list_applicants` exactly as Step 2 lists it (two queries), then writes the test "keys are exactly the listed fields" with `booking` for an applicant who has a booking row.
expected: Step 2 names where booking data comes from (a join or a third query on `bookings`/`interview_slots`), consistent with the "query count stays fixed" test bullet.
actual: `T15.md:76-78` "One query for the applications with candidate name and headline, one query for all those candidates' skills; score each ...; return dicts with exactly the listed keys." No source for `booking` (`starts_at`/`ends_at`); `T15.md:56-62` May read lists no file defining `bookings` (the verdict's G16 follow-up, still open). Contained for now because T15 is BLOCKED.
evidence: `T15.md:28-29` "`booking` (the booked slot's `starts_at`/`ends_at` as a dict, or `None`)"; `T15.md:76-78` quoted above; `T15.md:92` "query count stays fixed for 30 applicants".

F3
severity: minor
category: contract
where: docs/tasks/T17.md:29-31
claim: The card tells its reader that `07-CONTRACTS.md` is "outside this task's May read", which is false for T17 (the card the reader is executing), and it downgrades the contract's own stated behaviour (`Forbidden if not eligible`) to "a proposal".
trigger: T17 agent reads line 30 and, per hard rule 4 ("Never invent ... Check 07-CONTRACTS.md"), opens `07-CONTRACTS.md` section scheduling, which its May read (`T17.md:45`) allows; it finds `book_slot ... # Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief` and now has two contradicting instructions about whether that line is binding.
expected: Either "outside T-BRIEF's May read" (accurate), or, since the contract already answers it, a `DEFAULT (not in brief)`: same candidate twice is ineligible, `Forbidden`, which is the option the verdict's item 8 offered.
actual: `T17.md:29-31` "The T-BRIEF reviewer proposed `Forbidden` ... and cited `07-CONTRACTS.md`; that file is outside this task's May read, so it is recorded here as a proposal, not a DEFAULT." versus `T17.md:45` "- `docs/plan/07-CONTRACTS.md` (section: scheduling)" and `07-CONTRACTS.md:277` "# Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief".
evidence: lines quoted above.

F4
severity: minor
category: contract
where: docs/tasks/T13.md:56
claim: The closed-jobs CONFLICT block names the Contract line and the test bullet but not Step 3, which also hides closed jobs (`get_job` NotFound if closed), so one of the three places the decision must rewrite is unflagged.
trigger: Orchestrator decides "list closed jobs" for FP-CAN-2, rewrites the Contract and test bullet named in the CONFLICT, dispatches T13; the agent implements Step 3 as written and `score_candidate_for_job` raises `NotFound` for a closed job that the dashboard now lists.
expected: Step 3 carries the same CONFLICT mark (as T16 Steps 3-4 do after fix item 2), or the CONFLICT block lists it.
actual: `T13.md:25-30` CONFLICT names only "this card's Contract (`rank(skills, list_open_jobs(conn))`) and the test bullet"; `T13.md:56` "`score_candidate_for_job`: `get_job` (NotFound if missing or closed), then `engine.score`." is unmarked.
evidence: lines quoted above.

No new verbatim-quote errors, no scope, Owns, Contract or test-name changes found in the fix diff. Files checked: docs/plan/01-REQUIREMENTS.md, docs/tasks/T06.md, T07.md, T10.md, T11.md, T12.md, T13.md, T15.md, T16.md, T17.md, docs/BRIEF.md, docs/plan/07-CONTRACTS.md.
