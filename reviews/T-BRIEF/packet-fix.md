# Review packet T-BRIEF (1 of 3)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-T-BRIEF

Files in this packet: docs/plan/01-REQUIREMENTS.md, docs/tasks/T05.md

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

## Fix-round diff (47701ca..b1aa462), applying reviews/T-BRIEF/verdict.md items 1 to 10

```diff
diff --git a/docs/plan/01-REQUIREMENTS.md b/docs/plan/01-REQUIREMENTS.md
index fc96831..9444a8f 100644
--- a/docs/plan/01-REQUIREMENTS.md
+++ b/docs/plan/01-REQUIREMENTS.md
@@ -78,8 +78,8 @@ Open questions for the brief, answered:
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-CAN-1 | Profile and private resume rules | NEEDS DECISION (profile part READY; resume part: the brief requires a raw-text resume and owner-only access, T08 builds PDF upload with employer access) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
-| FP-CAN-2 | Recommendations preserve fields and rank all jobs | READY (after T11) | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
+| FP-CAN-1 | Profile and private resume rules | NEEDS DECISION (profile part: the brief's editable profile includes "a display name" and no card lets the candidate edit it, so `save_profile` needs a contract change or a new owner; resume part: the brief requires a raw-text resume and owner-only access, T08 builds PDF upload with employer access) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
+| FP-CAN-2 | Recommendations preserve fields and rank all jobs | NEEDS DECISION (rule quoted; the brief lists "all current (not deleted) jobs", the plan's "closed" job state in T10/T13 hides jobs that are not deleted; also after T11) | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
 | FP-CAN-3 | Pending duplicate and application owner | NEEDS DECISION (status names and re-apply rule differ from T14 defaults) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
 
 Rule text (brief section "3. Candidate workflow"):
@@ -105,7 +105,10 @@ Open questions, answered:
   employer with an application open it contradicts this.)
 - FP-CAN-2: which fields must each recommendation show? "a visible match score", "the job title,
   employer/company, required skills, and a way to view the description". Do zero-score jobs appear?
-  "list all current (not deleted) jobs", so yes. Closed (not deleted) jobs: NOT IN BRIEF.
+  "list all current (not deleted) jobs", so yes. Closed (not deleted) jobs: CONFLICT. The brief's
+  only exclusion is "deleted"; T10's "closed" state and T13's `list_open_jobs` hide jobs that are
+  not deleted. Decision needed before T10 and T13 run (drop "closed", list closed jobs, or document
+  why closed is not "current").
 - FP-CAN-3: application status list? From FP-EMP-3: "exactly these statuses: `Pending`,
   `Interviewing`, `Rejected`, or `Accepted`". New application: "status `Pending`". Can a candidate
   re-apply after a rejection or withdrawal? "apply to a job once"; "A duplicate application by the
@@ -187,16 +190,16 @@ Open questions, answered:
   ID".
 - Worked examples? The four-row table above, copied verbatim into T11.
 
-FP-MATCH-2 "Optional AI enhancement" is optional and not planned:
-> Teams **MAY** add an LLM-generated explanation or secondary recommendation, but it earns no substitute credit and **MUST NOT** alter the required score or ordering.
+FP-MATCH-2 "Optional AI enhancement" is optional and not planned (full paragraph):
+> Teams **MAY** add an LLM-generated explanation or secondary recommendation, but it earns no substitute credit and **MUST NOT** alter the required score or ordering. If user-controlled text is sent to an LLM, it **MUST** be treated as untrusted data, **MUST NOT** reveal prompts or secrets, and the data flow **MUST** be documented in `SPEC.md`. An optional AI enhancement is part of the peer-audit scope.
 
 ### Scheduling (FP-SCHED)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
 | FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rule quoted; T12's "15 to 240 minutes" default superseded by "30-minute") | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
-| FP-SCHED-2 | Eligible and ineligible booking | READY (rule quoted; needs the `uq_booking_application` contract change and the status-name decision) | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
-| FP-SCHED-3 | Booking conflict contract | READY (contract quoted) | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
+| FP-SCHED-2 | Eligible and ineligible booking | NEEDS DECISION (rule quoted; the brief scopes slots to "the employer for the candidate's application", T16's steps and tests scope them to the job; also needs the `uq_booking_application` contract change and the status-name decision) | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
+| FP-SCHED-3 | Booking conflict contract | NEEDS DECISION (contract quoted; T17's "same candidate books twice" test needs a decided result, `Forbidden` or `Conflict`; T17 also depends on T16, which is NEEDS DECISION) | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
 
 Rule text (brief section "6. Applications and interview scheduling"):
 
diff --git a/docs/tasks/T06.md b/docs/tasks/T06.md
index ee7875d..34cc801 100644
--- a/docs/tasks/T06.md
+++ b/docs/tasks/T06.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | security | T10, T15, T16 | yes | READY after its dependencies (codes quoted from the brief; see CONFLICT under Requirement) |
+| 3 | security | T10, T15, T16 | yes | **BLOCKED** (NEEDS DECISION, same as the FP-AUTH-3 row in `01-REQUIREMENTS.md`): the feature cards raise `NotFound` (404) for another user's object where the brief says "authenticated user with the wrong role or owner: `403 Forbidden`", so Step 2's "expected code" for user B with A's id has no decided value; the orchestrator decides 403 vs 404 before dispatch (see CONFLICT under Requirement). Also waits for its dependencies |
 
 ## Goal
 Prove, route by route, that nobody can read or change what is not theirs, and that missing objects
@@ -31,7 +31,7 @@ Expected codes, from the quote: signed out: `401 Unauthorized` or redirect to lo
 wrong owner: `403 Forbidden`; missing object the caller could otherwise access: `404 Not Found`.
 
 CONFLICT (orchestrator decision needed, nothing below changed): the old default on this card said
-"another user's object 404", and the feature cards (T08, T10, T12, T14, T15) raise `NotFound` for
+"another user's object 404", and the feature cards (T08, T10, T12, T14, T15, T16) raise `NotFound` for
 another user's object. The brief says `403 Forbidden` for "the wrong role or owner". Either the
 feature cards change to `Forbidden` (a contract change) or the sweep records each 404 as a `BUG:`
 hole. Signed-out POST giving 401 and GET redirecting both satisfy the quote.
diff --git a/docs/tasks/T07.md b/docs/tasks/T07.md
index f3d5461..fe3a4bf 100644
--- a/docs/tasks/T07.md
+++ b/docs/tasks/T07.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | CAN | T05 | no | READY (rule quoted from the brief; limits are DEFAULT (not in brief); see GAP) |
+| 2 | CAN | T05 | no | **BLOCKED** (NEEDS DECISION, same as the FP-CAN-1 row in `01-REQUIREMENTS.md`): the brief says a candidate "**MUST** be able to view and edit only their own profile, including a display name", and no card lets the candidate edit the display name (the `save_profile` contract has no name field). Needs either a contract change to `save_profile` or a new owner; see GAP. Limits are DEFAULT (not in brief) |
 
 ## Goal
 A candidate can fill in and edit their profile and skills. The Today page welcomes them and shows
@@ -20,9 +20,11 @@ DEFAULT (not in brief): the brief sets no field limits. Keep: headline max 120,
 summary max 2000, timezone must be a valid IANA name (use `zoneinfo.available_timezones()`), skills:
 comma separated, at most 30, each 1 to 40 chars after normalising.
 
-GAP (listed in T-BRIEF's OPEN QUESTIONS, not changed here): the brief's editable profile includes
-"a display name". This card's form has headline, location, timezone, summary and skills; the display
-name is set once at registration (T05) and no card lets the candidate edit it.
+GAP (NEEDS DECISION; listed in T-BRIEF's OPEN QUESTIONS, not changed here): the brief's editable
+profile includes "a display name". This card's form has headline, location, timezone, summary and
+skills; the display name is set once at registration (T05) and no card lets the candidate edit it.
+Closing the gap means a contract change to `save_profile` (add a display-name parameter, and the
+form field in Step 4) or a new card that owns it. The orchestrator decides before dispatch.
 
 ## Owns
 - `app/candidates/profile_service.py`
diff --git a/docs/tasks/T10.md b/docs/tasks/T10.md
index 45b3ba2..3838073 100644
--- a/docs/tasks/T10.md
+++ b/docs/tasks/T10.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | EMP | T09 | no | READY (rules quoted from the brief; two defaults SUPERSEDED, see Requirement; 403 CONFLICT flagged) |
+| 2 | EMP | T09 | no | **BLOCKED** (NEEDS DECISION, same as the FP-EMP-2 row in `01-REQUIREMENTS.md`): Step 7 and the FP-EMP-2 test bullet still describe cascade delete, but the brief says deletion with dependents "**MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged"; Step 4 and the test bullet give `NotFound` (404) where the brief says the other employer "**MUST** receive `403`"; and "closed" jobs are a CONFLICT with FP-CAN-2 (see Requirement). The orchestrator decides and rewrites those lines before dispatch |
 
 ## Goal
 An employer can post, edit, close and delete jobs with required skills. Anyone signed in can view
@@ -21,15 +21,21 @@ SUPERSEDED by the quote (the old defaults said the opposite):
 - Delete: no cascade. If any application or interview slot exists, deletion fails with
   `409 Conflict` and changes nothing. Overrides Step 7's "confirm-delete page that states what else is
   deleted" and the test bullet "delete removes it plus its applications and slots". The orchestrator
-  should rewrite those lines; they are left as written here.
+  should rewrite those lines; they are left as written here, which is why the card is BLOCKED rather
+  than READY (a card whose Steps and Tests contradict its quoted rule is not buildable).
 
 CONFLICT (flagged, not changed): the brief says another employer gets `403`; Step 4 raises
 `NotFound` (404). See T06.
 
 DEFAULT (not in brief): title max 120 chars; description max 5000; location max 80; employment type
 one of `EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "internship")`; salary min and max
-optional whole numbers from 0 to 10_000_000, min <= max; at most 30 skills. "Closed" jobs are not in
-the brief at all (it says "current (not deleted) jobs" in FP-CAN-2); closing is a card feature.
+optional whole numbers from 0 to 10_000_000, min <= max; at most 30 skills.
+
+CONFLICT (flagged, not changed): "closed" jobs. FP-CAN-2 (brief section "3. Candidate workflow")
+says the candidate dashboard "**MUST** list all current (not deleted) jobs". A closed job is not
+deleted, so the brief requires it to be listed; this card's close feature, `list_open_jobs`, the
+Contract line "a closed job is 404 unless the viewer owns it" and the test bullets "excludes closed
+jobs" and "detail of a closed job: ... other users 404" hide it. See T13. Orchestrator decision.
 
 ## Owns
 - `app/jobs/service.py`
diff --git a/docs/tasks/T11.md b/docs/tasks/T11.md
index 555b4c3..be134db 100644
--- a/docs/tasks/T11.md
+++ b/docs/tasks/T11.md
@@ -35,7 +35,11 @@ Rule text (brief section "5. Matching contract", FP-MATCH-1 "Score definition"),
 Mapped to this card's placeholders (each is a quote from the block above):
 - Normalisation rule: "trimming surrounding whitespace, converting to lowercase, removing empty
   values, and removing duplicates". Nothing about punctuation or synonyms: NOT IN BRIEF, so do not
-  add them (T07 and T10 rows need no re-normalising).
+  add them. OPEN QUESTION (for your reply, per Pitfalls): the provisional `normalise_skill` in
+  `07-CONTRACTS.md` is described as "strip, lower-case, collapse spaces"; "collapse spaces" is not
+  in the brief's rule. If T07 or T10 stored a skill containing internal double spaces under the
+  provisional rule, its stored form differs from the brief's normal form and those rows may need
+  re-normalising (a contract change, not part of this task). Do not assume the stored rows match.
 - Score formula: "score = 100 when |R| = 0"; "score = floor(100 * |C intersection R| / |R|)
   otherwise". "Resume text is not an input."
 - The floor: the `floor(...)` in the formula; "The result **MUST** be an integer from 0 through
diff --git a/docs/tasks/T12.md b/docs/tasks/T12.md
index bedd45c..766caa0 100644
--- a/docs/tasks/T12.md
+++ b/docs/tasks/T12.md
@@ -25,8 +25,14 @@ is DEFAULT (not in brief)); booked slots are never listed as available.
 
 DEFAULT (not in brief): date `YYYY-MM-DD`, times `HH:MM` 24-hour; no overlap with another slot of
 the same job; storage in UTC with the entry zone recorded (the brief only requires "an unambiguous,
-documented timezone", so document it in SPEC.md). The brief says a slot has "one owner" and does not
-say whether a slot belongs to a job or to the employer; this card attaches slots to jobs (DEFAULT).
+documented timezone", so document it in SPEC.md). This card attaches slots to jobs (DEFAULT for
+storage). Note that FP-SCHED-1 says each slot "**MUST** have one owner" and FP-SCHED-2 (brief section
+"6. Applications and interview scheduling") scopes booking to the employer, not the job:
+> - the slot belongs to the employer for the candidate's application;
+
+So a slot's owner is the employer. Attaching slots to jobs is only acceptable if booking (T16)
+still allows any slot of the same employer; that is the T16 CONFLICT and the orchestrator's
+decision, not this card's.
 
 CONFLICT (flagged, not changed): the brief (FP-EMP-2, FP-AUTH-3) gives `403` for another
 employer's posting; the invalid-slots test bullet says `NotFound` for "someone else's job". See T06.
diff --git a/docs/tasks/T13.md b/docs/tasks/T13.md
index afbed2e..11c1b1c 100644
--- a/docs/tasks/T13.md
+++ b/docs/tasks/T13.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | READY after T11 is merged (rule quoted from the brief; fields SUPERSEDE the default) |
+| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | **BLOCKED** (NEEDS DECISION, same as the FP-CAN-2 row in `01-REQUIREMENTS.md`): the brief says the dashboard "**MUST** list all current (not deleted) jobs", but the Contract (`list_open_jobs`) and the test bullet exclude T10's "closed" jobs, which are not deleted (CONFLICT, see Requirement). Also waits for T11 to merge |
 
 ## Goal
 A candidate sees every open job ranked for them, each with its score and which skills matched and
@@ -22,8 +22,12 @@ brief).
 
 Answers for the test bullets:
 - Zero-score jobs: "list all current (not deleted) jobs", so a zero-overlap job is present.
-- Closed jobs: NOT IN BRIEF. The brief knows only "current (not deleted)"; closing is a T10 card
-  feature. Excluding closed jobs is DEFAULT (not in brief).
+- Closed jobs: CONFLICT (flagged, not changed; orchestrator decision needed). The brief says "list
+  all current (not deleted) jobs". A job that T10 has "closed" is not deleted, so the brief requires
+  it on the dashboard; this card's Contract (`rank(skills, list_open_jobs(conn))`) and the test
+  bullet "5 open jobs and 1 closed; result has exactly the 5" hide it. Either the "closed" state is
+  dropped from the plan, or closed jobs are listed, or the orchestrator documents why "closed"
+  counts as not "current". Not a default this card can pick.
 - "Candidate and employer views **MUST** call the same implementation." (FP-MATCH-1)
 
 ## Owns
diff --git a/docs/tasks/T15.md b/docs/tasks/T15.md
index ea285ee..e949188 100644
--- a/docs/tasks/T15.md
+++ b/docs/tasks/T15.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | EMP + CAN + MATCH | T11, T14 | yes | **BLOCKED** on the T14 status-name decision (rules quoted; order and fields SUPERSEDE the defaults) |
+| 3 | EMP + CAN + MATCH | T11, T14 | yes | **BLOCKED** on the T14 status-name decision and on the resume-access CONFLICT (rules quoted; order and fields SUPERSEDE the defaults; see Requirement) |
 
 ## Goal
 An employer sees the applicants for one of their jobs, with the fields and order the brief requires,
@@ -22,9 +22,19 @@ SUPERSEDED by the quotes (old defaults were different):
 - Order: score high to low, then case-insensitive candidate display name, then candidate ID. The
   old default "then `applied_at` oldest first, then `application_id`" is wrong.
 - Fields: each row must show "candidate identity, skills, match score, application status, and
-  interview booking (if any)". The old field list lacks the candidate's skills list and the booking.
-  Keeping `matched`, `missing`, `headline`, `applied_at`, `resume_id` as extras is DEFAULT (not in
-  brief); `resume_id` conflicts with the T08 CONFLICT (resumes are owner-only in the brief).
+  interview booking (if any)". The old field list lacked the candidate's skills list and the booking.
+  The keys `list_applicants` returns, the list Step 2 and the test mean by "the listed keys":
+  `application_id`, `candidate_id`, `candidate_name`, `headline`, `skills` (the candidate's
+  normalised skill names, sorted), `score`, `matched`, `missing`, `status`, `applied_at`, `booking`
+  (the booked slot's `starts_at`/`ends_at` as a dict, or `None`), `resume_id`.
+  Of these the brief requires identity (`candidate_id`, `candidate_name`), `skills`, `score`,
+  `status` and `booking`; the exact key names and the extras `headline`, `matched`, `missing`,
+  `applied_at` are DEFAULT (not in brief).
+  CONFLICT (flagged, not changed): `resume_id`, and the resume link in Step 4, exist only so the
+  employer can open the candidate's resume. The brief (FP-CAN-1, "3. Candidate workflow") says
+  "Resume contents are private: only the owning candidate may read or modify them. Any other
+  candidate or employer **MUST** receive `403` through a direct URL/API request." Same CONFLICT as
+  T08; orchestrator decision.
 - Statuses: exactly `Pending`, `Interviewing`, `Rejected`, `Accepted` (see T14 CONFLICT).
 - Transitions: NOT IN BRIEF; "set an application to one of exactly these statuses". See T14.
 - Also FP-SCHED-2: "If a booked application later leaves `Interviewing`, its booking **MUST** remain
@@ -70,7 +80,8 @@ field), all `@role_required("employer")`.
    `new_status` not in `TRANSITIONS[current]`: `ValidationError`. Update and audit
    `application.status` with detail `"<old> -> <new>"`.
 4. Applicants page: table (fields above; date with `format_local` in UTC unless the brief says
-   otherwise), resume link to `/resumes/<id>`, one link per allowed next status to the confirm page.
+   otherwise), resume link to `/resumes/<id>` (CONFLICT: the brief gives employers `403` on resumes;
+   see Requirement), one link per allowed next status to the confirm page.
 5. Confirm-status page: `confirm_box` "Change <name>'s application from <old> to <new>?", POST form.
 
 ## Tests (`tests/unit/test_emp_applicants.py`; remove the skip)
diff --git a/docs/tasks/T16.md b/docs/tasks/T16.md
index d3c07cf..c85ba85 100644
--- a/docs/tasks/T16.md
+++ b/docs/tasks/T16.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | READY (eligibility rule quoted from the brief; needs the `uq_booking_application` contract change first) |
+| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | **BLOCKED** (NEEDS DECISION, same as the FP-SCHED-2 row in `01-REQUIREMENTS.md`) for three reasons: (1) the brief's eligibility is employer-level, "the slot belongs to the employer for the candidate's application", while Steps 3-4 and the ineligible test scope slots to the application's job (CONFLICT, see Requirement); (2) the T14 status-name decision (the rule needs the literal `Interviewing`); (3) the `uq_booking_application` index is an unmade contract change |
 
 ## Goal
 An eligible candidate sees the open slots for their application, in their time zone, and books one
@@ -24,8 +24,14 @@ interview scheduling", FP-SCHED-2 "Booking eligibility"):
 Worked examples: none in the brief for FP-SCHED-2.
 
 - Who is eligible: the five bullets above, all true. Status is the literal `Interviewing` (see the
-  T14 CONFLICT on status names). Note the brief ties the slot to "the employer for the candidate's
-  application", not to the job; this card's slots hang off jobs (T12 DEFAULT), which is narrower.
+  T14 CONFLICT on status names).
+- CONFLICT (flagged, not changed; orchestrator decision needed): the brief's rule is "if and only
+  if", and its second bullet is "the slot belongs to the employer for the candidate's application".
+  Step 3 ("slots of the application's job"), Step 4 ("belongs to the same job (`NotFound`)") and the
+  "slot of a different job" case in `test_fp_sched_2_ineligible_booking` all scope the slot to the
+  job, which refuses a booking the brief says **MUST** be allowed (a slot of the same employer on a
+  different job). T12 attaches slots to jobs; whether booking checks the job or the employer is a
+  contract decision, not a card default.
 - Can one application hold more than one booking: no, "the application has no existing booking".
   Request the `uq_booking_application` index through a contract change before building.
 - Leaving `Interviewing` later: the booking stays and the slot stays unavailable.
@@ -63,8 +69,10 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
 1. Tests first, using the brief's rule and examples.
 2. `is_eligible`: `get_own_application` (raises `NotFound` for others), then the brief's rule.
 3. `list_bookable_slots`: future, unbooked slots of the application's job, start ascending.
+   (CONFLICT: the brief scopes slots to the employer, not the job; see Requirement.)
 4. `book_slot` (simple version; T17 hardens it): own application (`NotFound`), eligible
-   (`Forbidden`), slot exists and belongs to the same job (`NotFound`), inside
+   (`Forbidden`), slot exists and belongs to the same job (`NotFound`) (CONFLICT: brief says "belongs
+   to the employer for the candidate's application"; see Requirement), inside
    `transaction(conn, immediate=True)`: insert booking, audit `booking.create`.
 5. Detail page: application status, then either "Book an interview" with slots shown by
    `format_local(..., candidate timezone from get_profile)` and the zone name, or the booked slot, or
@@ -76,7 +84,8 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
 - `test_fp_sched_2_eligible_booking`: eligible candidate books; booking row exists; slot no longer
   listed as bookable; detail page shows the booked time in the candidate's zone.
 - `test_fp_sched_2_ineligible_booking`: parametrised: status not eligible, another candidate's
-  application, slot of a different job, missing slot, missing application. Each refused with the
+  application, slot of a different job (CONFLICT: under the brief a slot of the same employer's
+  other job is bookable; see Requirement), missing slot, missing application. Each refused with the
   right error and no booking row.
 - employer GET of the detail page gives 403
 
diff --git a/docs/tasks/T17.md b/docs/tasks/T17.md
index 5e3c1ec..78a4fc6 100644
--- a/docs/tasks/T17.md
+++ b/docs/tasks/T17.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED | T16, T-BRIEF | no | READY (conflict contract quoted from the brief) |
+| 3 | SCHED | T16, T-BRIEF | no | **BLOCKED** (conflict contract quoted from the brief): (1) the Goal and the last test bullet cover "one person books twice", which the brief does not define as a conflict case; by FP-SCHED-2 the second attempt is ineligible ("the application has no existing booking"), and the result the test must assert (`Forbidden` from the eligibility check, or the `Slot already booked` `Conflict`) is a decision the orchestrator makes against `07-CONTRACTS.md`, not a card default (see Requirement); (2) T16, which this card hardens, is BLOCKED |
 
 ## Goal
 When two people try to book the same slot, or one person books twice, the result is exactly the
@@ -22,8 +22,13 @@ Worked examples: none in the brief beyond the scenario in the second paragraph.
 - What the losing user sees next: NOT IN BRIEF. DEFAULT: re-render `scheduling/book.html` with the
   message, status 409.
 - Same candidate booking the same slot twice: NOT IN BRIEF as a conflict case. By FP-SCHED-2 the
-  second attempt is ineligible ("the application has no existing booking"); whether it must use the
-  `Slot already booked` message: unknown.
+  second attempt is ineligible ("the application has no existing booking"), so the brief's own
+  classification is "ineligible booking" (FP-SCHED-2: "Ineligible bookings **MUST** fail without
+  partially changing either record"), not the FP-SCHED-3 conflict. NEEDS DECISION (this is why the
+  card is BLOCKED): the test bullet "gets the contract result (or what the brief says)" needs one
+  decided outcome. The T-BRIEF reviewer proposed `Forbidden` (the error T16 Step 4 raises for an
+  ineligible booking) and cited `07-CONTRACTS.md`; that file is outside this task's May read, so it
+  is recorded here as a proposal, not a DEFAULT. The orchestrator decides and logs it.
 - Mechanism: "a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an
   equivalent database mechanism"; Step 2's `BEGIN IMMEDIATE` plus the unique index on `slot_id`
   satisfies this. "An in-process check alone is insufficient."
```

## Check output (orchestrator ran it)

CHECK PASSED; SCOPE OK for T-BRIEF
