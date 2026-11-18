REVIEWER: 2
CHECKED: 1 (requirement and contract: each fix-list item 1 to 10 checked against the worktree at b1aa462 and every quote re-checked against docs/BRIEF.md), 2 (security checklist: docs-only change, no routes, SQL, templates or uploads; only the 403/404 lines of FP-AUTH-3 are relevant and are covered in F1), 3 (tests and edges: no test files changed; `git diff 47701ca..b1aa462 --stat` touches only the 10 files in the packet, all inside the Owns list; `git grep "(from the brief)"` finds no placeholder in any card; Owns, Contract and test names unchanged in every card)

Fix-list verification, item by item (against the worktree files, not the packet):
1. T10 BLOCKED with all three reasons, agrees with `docs/plan/01-REQUIREMENTS.md:124`. Applied.
2. T16 BLOCKED with three reasons; Steps 3-4 and the "slot of a different job" test case marked CONFLICT; `docs/tasks/T12.md:29-31` now quotes `BRIEF.md:115` verbatim; FP-SCHED-2 row NEEDS DECISION. Applied.
3. `T13.md:25-30`, `T10.md:34-38`, `01-REQUIREMENTS.md:108-111` say CONFLICT; FP-CAN-2 row NEEDS DECISION. Applied.
4. `T15.md:26-32` gives one definitive key list including `skills` and `booking`, marked DEFAULT. Applied (see F2).
5. `T07.md:5` BLOCKED; FP-CAN-1 row names the display-name gap. Applied.
6. `T06.md:5` BLOCKED matching `01-REQUIREMENTS.md:47`; `T06.md:34` lists T16. Applied.
7. `T15.md:33-37` and `T15.md:83-84` label `resume_id` and the link CONFLICT. Applied.
8. `T17.md:5` BLOCKED with the reason; `T17.md:24-31` explains. Applied (see F3).
9. `01-REQUIREMENTS.md:193-194` quotes the full FP-MATCH-2 paragraph; verbatim against `BRIEF.md:102`. Applied.
10. `T11.md:36-42` drops the "no re-normalising" claim and records the collapse-spaces OPEN QUESTION. Applied.

FINDINGS: 3

F1
severity: major
category: contract
where: docs/tasks/T12.md:5
claim: The fix round made the 404-vs-403 contradiction a BLOCKED reason on T10 and T06, and the plan says the decision is needed before T12 runs, but T12 stays READY with the identical contradiction in its Step 3 and test bullet.
trigger: Orchestrator dispatches every card whose Status is READY after this merge; T12 is dispatched; the T12 agent follows Step 3 and the invalid-slots test bullet and builds `NotFound` (404) for another employer's job.
expected: T12 status is BLOCKED / NEEDS DECISION like T10 (same conflict, same brief line), or the plan row at `01-REQUIREMENTS.md:74-75` stops naming T12 as needing the decision first.
actual: `T12.md:5` says `READY (rules quoted from the brief; duration default SUPERSEDED; the rest DEFAULT (not in brief))`; `T12.md:37-38` says `CONFLICT (flagged, not changed): the brief (FP-EMP-2, FP-AUTH-3) gives 403 for another employer's posting; the invalid-slots test bullet says NotFound for "someone else's job". See T06.`; `T12.md:70` `check job ownership (NotFound)`; `T12.md:90` `someone else's job (NotFound)`. Meanwhile `01-REQUIREMENTS.md:74-75`: `CONFLICT: T06's default and the feature cards T08, T10, T12, T14, T15, T16 return 404 (NotFound) for another user's object. The brief says 403. Decision needed before those cards run.` and `T10.md:5` cites exactly this as a BLOCKED reason.
evidence: quoted lines above; `docs/BRIEF.md:66` `An employer **MUST** receive 403 when attempting to edit, delete, or manage applicants for another employer's posting.`

F2
severity: minor
category: performance
where: docs/tasks/T15.md:76-78
claim: Fix item 4 added a `booking` key to every applicant row but left Step 2's query plan at two queries (applications, skills), so the card now instructs a result it gives no query for, and the obvious way to fill it is one booking lookup per applicant, which the card's own query-count test forbids.
trigger: T15 agent follows Step 2 literally, then needs `booking` for each of 30 applicants and does a per-row SELECT on `bookings JOIN interview_slots`; the test `query count stays fixed for 30 applicants (set_trace_callback)` fails, or the agent omits `booking` and the "keys are exactly the listed fields" assertion fails.
expected: Step 2 names a third single query (or a LEFT JOIN in the first) for bookings and slots, matching the new key list.
actual: `T15.md:27-29` `... status, applied_at, booking (the booked slot's starts_at/ends_at as a dict, or None), resume_id.`; `T15.md:76-78` `list_applicants: get_owned_job first. One query for the applications with candidate name and headline, one query for all those candidates' skills; ...`; `T15.md:92` `query count stays fixed for 30 applicants (set_trace_callback)`. T15's May read (`T15.md:56-62`) still has no file that defines `bookings` or `interview_slots` (verdict item 11, deferred to CC01).
evidence: quoted above

F3
severity: minor
category: contract
where: docs/tasks/T17.md:29-31
claim: The new T17 text says `07-CONTRACTS.md` is "outside this task's May read", which is true of T-BRIEF but false of T17, the card the sentence sits in; T17's own May read includes that file, so the proposal is wrongly downgraded and a T17 agent is told it may not open a file it may open.
trigger: T17 agent reads its card to decide what the same-candidate-twice test must assert; line 30 tells it `07-CONTRACTS.md` is out of bounds, line 45 lists it under May read.
expected: The sentence names T-BRIEF as the task whose May read excludes the file, or simply cites `07-CONTRACTS.md:277`, which already answers the question for T17.
actual: `T17.md:29-31` `The T-BRIEF reviewer proposed Forbidden (the error T16 Step 4 raises for an ineligible booking) and cited 07-CONTRACTS.md; that file is outside this task's May read, so it is recorded here as a proposal, not a DEFAULT.` versus `T17.md:45` `- docs/plan/07-CONTRACTS.md (section: scheduling)`.
evidence: quoted above; `docs/plan/07-CONTRACTS.md:276-277` `def book_slot(...)` / `# Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief`
