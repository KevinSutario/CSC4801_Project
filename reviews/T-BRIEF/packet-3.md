# Review packet T-BRIEF (3 of 3)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-T-BRIEF

Files in this packet: docs/tasks/T15.md, docs/tasks/T16.md, docs/tasks/T17.md

## Review type: task

## Task card

# T-BRIEF · Fill rules from the course brief

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| any | docs | `docs/BRIEF.md` filled by Kevin | no | BLOCKED until docs/BRIEF.md has the brief |

## Goal
Copy every business rule the app needs from the brief into the plan, word for word, so no later
agent has to guess. Docs only. No code.

## Requirement
All FP-* ids.

## Owns
- `docs/plan/01-REQUIREMENTS.md`
- `docs/tasks/T05.md`
- `docs/tasks/T06.md`
- `docs/tasks/T07.md`
- `docs/tasks/T08.md`
- `docs/tasks/T09.md`
- `docs/tasks/T10.md`
- `docs/tasks/T11.md`
- `docs/tasks/T12.md`
- `docs/tasks/T13.md`
- `docs/tasks/T14.md`
- `docs/tasks/T15.md`
- `docs/tasks/T16.md`
- `docs/tasks/T17.md`

## May read
- `CLAUDE.md`
- `docs/BRIEF.md`
- every file listed under Owns

## Steps
1. Read `docs/BRIEF.md` fully. List every requirement id it defines.
2. In `01-REQUIREMENTS.md`, for each FP-* row: add a "Rule text" block under the table section,
   quoting the brief exactly, with the brief's section name. Answer each "Open questions" item with a
   quote, or write `NOT IN BRIEF`.
3. For FP-MATCH-1 and FP-SCHED-1 to 3: copy every worked example from the brief exactly (inputs and
   expected outputs) into the matching task card under `## Requirement`.
4. In each task card listed under Owns: replace every "(from the brief)" placeholder with the quoted
   rule. If a rule is `NOT IN BRIEF`, write the default already in the card and mark it
   `DEFAULT (not in brief)`.
5. If the brief has a requirement that no card covers: do not invent a card. List it under
   OPEN QUESTIONS in your reply.
6. Set Status to READY on every card whose rules are now complete. Leave BLOCKED where a rule the
   card needs is still missing, with the reason.

## Done when
- Every FP-* row has rule text or `NOT IN BRIEF`.
- No card still says "(from the brief)" without a quote or a DEFAULT mark.
- `python scripts/check_scope.py T-BRIEF` passes.

## Pitfalls
- Never paraphrase a rule. Quote it. A paraphrase is how a requirement gets silently changed.
- Do not change any card's Owns, Contract or test names.


## Changed files

```
 docs/plan/01-REQUIREMENTS.md | 296 ++++++++++++++++++++++++++++++++++++-------
 docs/tasks/T05.md            |  20 ++-
 docs/tasks/T06.md            |  31 ++++-
 docs/tasks/T07.md            |  20 ++-
 docs/tasks/T08.md            |  21 ++-
 docs/tasks/T09.md            |  12 +-
 docs/tasks/T10.md            |  28 +++-
 docs/tasks/T11.md            |  44 +++++--
 docs/tasks/T12.md            |  27 +++-
 docs/tasks/T13.md            |  21 ++-
 docs/tasks/T14.md            |  36 +++++-
 docs/tasks/T15.md            |  33 ++++-
 docs/tasks/T16.md            |  30 ++++-
 docs/tasks/T17.md            |  24 +++-
 14 files changed, 530 insertions(+), 113 deletions(-)

```

## Check output (in the worktree)

```
=== lint: C:\Users\sutar\AppData\Local\Programs\Python\Python311\python.exe -m ruff check .
All checks passed!

=== tests: C:\Users\sutar\AppData\Local\Programs\Python\Python311\python.exe -m pytest tests/unit -q -rs -p no:cacheprovider
.........................................                                [100%]
41 passed in 14.02s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for T-BRIEF
```

## Security review checklist (reviewers tick every line)

1. Every new route has `@login_required` and the right `@role_required`, or a written reason why not.
2. Every POST form includes `csrf_field()`. No route skips the CSRF check.
3. Every service that loads an object by id also checks the actor owns it or may see it.
4. Missing and not-yours both give the agreed status code. Try an id that belongs to another user.
5. All SQL uses `?` placeholders. Search the diff for `f"`, `.format(`, `%` and `+` near `execute`.
6. No `|safe`, `Markup(` or `autoescape false` on anything a user typed.
7. Uploads: size cap, type check by content, random stored name, served only via the checked route.
8. Redirects use `url_for`, or a `next` value that passes the safe-redirect check.
9. No secret, password, token or traceback appears in logs, flash messages, audit detail or HTML.
10. Error responses use the error templates, with the right status code.
11. Sign-in clears the session first. Sign-out is POST with CSRF.
12. Role cannot be changed through any form field.



## Diff

```diff
diff --git a/docs/tasks/T15.md b/docs/tasks/T15.md
index d1f5c3d..ea285ee 100644
--- a/docs/tasks/T15.md
+++ b/docs/tasks/T15.md
@@ -2,18 +2,39 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | EMP + CAN + MATCH | T11, T14 | yes | READY (fields and order from the brief, defaults below) |
+| 3 | EMP + CAN + MATCH | T11, T14 | yes | **BLOCKED** on the T14 status-name decision (rules quoted; order and fields SUPERSEDE the defaults) |
 
 ## Goal
 An employer sees the applicants for one of their jobs, with the fields and order the brief requires,
 and moves an application through allowed statuses via a confirm screen.
 
 ## Requirement
-FP-EMP-3: applicant fields, order, status and role. Rule text: (from the brief)
-Defaults: fields `application_id, candidate_name, headline, score, matched, missing, status,
-applied_at, resume_id`; order by score high to low, then `applied_at` oldest first, then
-`application_id`; only an employer who owns the job may see or change; transitions from
-`statuses.TRANSITIONS`; an invalid transition gives `ValidationError({"status": ...})`.
+FP-EMP-3: applicant fields, order, status and role. Rule text (brief section "4. Employer
+workflow", FP-EMP-3 "Applicant management"):
+> For each owned job, an employer **MUST** be able to view its applicants sorted by match score from highest to lowest. Each row **MUST** show candidate identity, skills, match score, application status, and interview booking (if any).
+>
+> The employer who owns the job **MUST** be able to set an application to one of exactly these statuses: `Pending`, `Interviewing`, `Rejected`, or `Accepted`. Other employers and candidates **MUST NOT** be able to change the status.
+
+Tie-breakers (brief section "5. Matching contract", FP-MATCH-1):
+> Sort by descending score. [...] break employer applicant ties by case-insensitive candidate display name and then stable candidate ID.
+
+SUPERSEDED by the quotes (old defaults were different):
+- Order: score high to low, then case-insensitive candidate display name, then candidate ID. The
+  old default "then `applied_at` oldest first, then `application_id`" is wrong.
+- Fields: each row must show "candidate identity, skills, match score, application status, and
+  interview booking (if any)". The old field list lacks the candidate's skills list and the booking.
+  Keeping `matched`, `missing`, `headline`, `applied_at`, `resume_id` as extras is DEFAULT (not in
+  brief); `resume_id` conflicts with the T08 CONFLICT (resumes are owner-only in the brief).
+- Statuses: exactly `Pending`, `Interviewing`, `Rejected`, `Accepted` (see T14 CONFLICT).
+- Transitions: NOT IN BRIEF; "set an application to one of exactly these statuses". See T14.
+- Also FP-SCHED-2: "If a booked application later leaves `Interviewing`, its booking **MUST** remain
+  associated with the application and the slot **MUST** remain unavailable." So changing status
+  never touches bookings.
+
+CONFLICT (flagged, not changed): the brief gives `403` for another employer ("manage applicants for
+another employer's posting", FP-EMP-2); Steps 2 and 3 use `get_owned_job` / `NotFound`. See T06.
+
+DEFAULT (not in brief): dates shown with `format_local` in UTC.
 
 ## Owns
 - `app/applications/review_service.py`
diff --git a/docs/tasks/T16.md b/docs/tasks/T16.md
index bc13476..d3c07cf 100644
--- a/docs/tasks/T16.md
+++ b/docs/tasks/T16.md
@@ -2,18 +2,36 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | **BLOCKED**: eligibility rule only in the brief |
+| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | READY (eligibility rule quoted from the brief; needs the `uq_booking_application` contract change first) |
 
 ## Goal
 An eligible candidate sees the open slots for their application, in their time zone, and books one
 through a confirm screen. Ineligible candidates cannot book.
 
 ## Requirement
-FP-SCHED-2: eligible and ineligible booking. Rule text: (from the brief)
-- Who is eligible: (from the brief). Likely shape: own application, for this slot's job, in status
-  (from the brief).
-- Can one application hold more than one booking: (from the brief). If no, add the
-  `uq_booking_application` index through a contract change request first.
+FP-SCHED-2: eligible and ineligible booking. Rule text (brief section "6. Applications and
+interview scheduling", FP-SCHED-2 "Booking eligibility"):
+> The system **MUST** allow a candidate to book a slot if and only if all of the following are true:
+>
+> - the candidate owns the application;
+> - the slot belongs to the employer for the candidate's application;
+> - the application status is `Interviewing`;
+> - the slot is in the future and is not already booked; and
+> - the application has no existing booking.
+>
+> A successful booking **MUST** link the candidate's application to the slot and be visible to both that candidate and the owning employer. Ineligible bookings **MUST** fail without partially changing either record. If a booked application later leaves `Interviewing`, its booking **MUST** remain associated with the application and the slot **MUST** remain unavailable.
+
+Worked examples: none in the brief for FP-SCHED-2.
+
+- Who is eligible: the five bullets above, all true. Status is the literal `Interviewing` (see the
+  T14 CONFLICT on status names). Note the brief ties the slot to "the employer for the candidate's
+  application", not to the job; this card's slots hang off jobs (T12 DEFAULT), which is narrower.
+- Can one application hold more than one booking: no, "the application has no existing booking".
+  Request the `uq_booking_application` index through a contract change before building.
+- Leaving `Interviewing` later: the booking stays and the slot stays unavailable.
+- Refusal code for another candidate's application: `403` (FP-AUTH-3, FP-SEC-1 boundary 3 "a
+  candidate cannot book a slot using another candidate's application"). Step 2 says `NotFound`;
+  flagged, not changed. See T06.
 
 ## Owns
 - `app/scheduling/booking.py`
diff --git a/docs/tasks/T17.md b/docs/tasks/T17.md
index 3151835..5e3c1ec 100644
--- a/docs/tasks/T17.md
+++ b/docs/tasks/T17.md
@@ -2,17 +2,31 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED | T16, T-BRIEF | no | **BLOCKED**: conflict contract only in the brief |
+| 3 | SCHED | T16, T-BRIEF | no | READY (conflict contract quoted from the brief) |
 
 ## Goal
 When two people try to book the same slot, or one person books twice, the result is exactly the
 brief's conflict contract, and the database never holds a double booking.
 
 ## Requirement
-FP-SCHED-3: booking conflict contract. Rule text, verbatim: (from the brief)
-- Status code: (from the brief)
-- Message or body: (from the brief)
-- What the losing user sees next: (from the brief)
+FP-SCHED-3: booking conflict contract. Rule text, verbatim (brief section "6. Applications and
+interview scheduling", FP-SCHED-3 "Atomic concurrency"):
+> Booking **MUST** be atomic at the database layer. Use a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an equivalent database mechanism. An in-process check alone is insufficient.
+>
+> When two eligible candidates concurrently attempt to book the same slot, exactly one attempt **MUST** succeed, the other **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message `Slot already booked`, and the database **MUST** contain exactly one booking afterward. Students **MUST** write unit tests for the booking conflict-handling logic. Database atomicity is verified through implementation review and the running system; students are not required to provide a synchronized multi-client test.
+
+Worked examples: none in the brief beyond the scenario in the second paragraph.
+
+- Status code: "HTTP `409` or a clearly documented equivalent".
+- Message or body: the message `Slot already booked` (exact text).
+- What the losing user sees next: NOT IN BRIEF. DEFAULT: re-render `scheduling/book.html` with the
+  message, status 409.
+- Same candidate booking the same slot twice: NOT IN BRIEF as a conflict case. By FP-SCHED-2 the
+  second attempt is ineligible ("the application has no existing booking"); whether it must use the
+  `Slot already booked` message: unknown.
+- Mechanism: "a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an
+  equivalent database mechanism"; Step 2's `BEGIN IMMEDIATE` plus the unique index on `slot_id`
+  satisfies this. "An in-process check alone is insufficient."
 
 ## Owns
 - `app/scheduling/booking.py`

```
