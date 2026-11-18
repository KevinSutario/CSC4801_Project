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
diff --git a/docs/plan/01-REQUIREMENTS.md b/docs/plan/01-REQUIREMENTS.md
index 308e183..fc96831 100644
--- a/docs/plan/01-REQUIREMENTS.md
+++ b/docs/plan/01-REQUIREMENTS.md
@@ -8,6 +8,9 @@ Every graded requirement, where its rule text lives, which task builds it, and w
   states them.
 - **BLOCKED**: the rule is defined only in the brief, and the brief has not been pasted in yet.
   No agent may write logic for a BLOCKED item. Tasks that need it stop at the test-writing step.
+- **NEEDS DECISION**: the brief states the rule, but the task card's default or design contradicts
+  it. The orchestrator decides (and logs it in `docs/state/DECISIONS.md`) before the card is
+  dispatched.
 
 ## How to unblock
 
@@ -16,6 +19,20 @@ Every graded requirement, where its rule text lives, which task builds it, and w
 3. Answer the open questions listed for that row, using only the brief.
 4. Change the status to READY and log it in `docs/state/DECISIONS.md`.
 
+T-BRIEF did steps 1 to 3 on 2026-11-11 from `docs/BRIEF.md`. Every quote below is verbatim from the
+brief's `REQUIREMENTS.md` part; the section name is given each time. "NOT IN BRIEF" means the brief
+says nothing about it and the task card's default stands, marked `DEFAULT (not in brief)` on the
+card. Step 4's DECISIONS.md entry is the orchestrator's.
+
+## Requirement ids the brief defines
+
+FP-ARCH-1, FP-AUTH-1, FP-AUTH-2, FP-AUTH-3, FP-CAN-1, FP-CAN-2, FP-CAN-3, FP-EMP-1, FP-EMP-2,
+FP-EMP-3, FP-MATCH-1, FP-MATCH-2 (optional), FP-SCHED-1, FP-SCHED-2, FP-SCHED-3, FP-SEC-1, FP-SEC-2,
+FP-SEC-3, FP-SEC-4, FP-PROC-1, FP-DOC-1, FP-DOC-2, FP-DOC-3, FP-TEST-1, FP-SUB-1.
+
+The brief's FP-TEST-1 names the functional set that needs student-written unit tests:
+> FP-AUTH-1 through FP-AUTH-3, FP-CAN-1 through FP-CAN-3, FP-EMP-1 through FP-EMP-3, FP-MATCH-1, and FP-SCHED-1 through FP-SCHED-3 (plus FP-MATCH-2 if implemented).
+
 ## Requirement table
 
 The test names come from the course template. Keep them exactly. Tests live in per-task files
@@ -25,76 +42,269 @@ The test names come from the course template. Keep them exactly. Tests live in p
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-AUTH-1 | Registration and session lifecycle; invalid registration | READY (limits from brief) | T05 | `test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`, `::test_fp_auth_1_invalid_registration` |
+| FP-AUTH-1 | Registration and session lifecycle; invalid registration | READY (brief gives no limits; T05 defaults, marked DEFAULT) | T05 | `test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`, `::test_fp_auth_1_invalid_registration` |
 | FP-AUTH-2 | Salted hash and password verification | READY | T05 | `test_auth.py::test_fp_auth_2_salted_hash_and_password_verification` |
-| FP-AUTH-3 | Authorization and missing object | READY (status codes from brief) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |
+| FP-AUTH-3 | Authorization and missing object | NEEDS DECISION (codes quoted; cards use 404 where the brief says 403) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |
+
+Rule text (brief section "2. Roles and authentication"):
 
-Open questions for the brief:
-- FP-AUTH-1: allowed roles at sign-up? Password length and rules? Email format rules? Session lifetime?
-- FP-AUTH-3: for another user's object, return 403 or 404? For a missing object, 404?
+FP-AUTH-1 "Accounts":
+> The system **MUST** support exactly two application roles: `Candidate` and `Employer`. A user **MUST** be able to register, log in, and log out. Email or username identifiers **MUST** be unique.
+
+FP-AUTH-2 "Credential storage":
+> Passwords **MUST** be stored with an established password-hashing function. Plain text, reversible encryption, and a general-purpose fast hash such as unsalted SHA-256 do not satisfy this requirement. Authentication secrets **MUST NOT** be returned by an API or rendered in the UI.
+
+FP-AUTH-3 "Server-side authorization":
+> Every protected operation **MUST** enforce role and ownership on the server; hiding a button in the UI is not sufficient. The observable response contract is:
+>
+> - unauthenticated request: `401 Unauthorized` or redirect to login;
+> - authenticated user with the wrong role or owner: `403 Forbidden`; and
+> - missing object that the caller would otherwise be allowed to access: `404 Not Found`.
+>
+> For non-HTTP frameworks, the UI and service layer **MUST** provide equivalent, clearly distinguishable outcomes.
+
+Open questions for the brief, answered:
+- FP-AUTH-1: allowed roles at sign-up? "exactly two application roles: `Candidate` and
+  `Employer`". Password length and rules? NOT IN BRIEF. Email format rules? NOT IN BRIEF (only
+  "Email or username identifiers **MUST** be unique"). Session lifetime? NOT IN BRIEF.
+- FP-AUTH-3: for another user's object, return 403 or 404? "authenticated user with the wrong role
+  or owner: `403 Forbidden`". For a missing object, 404? "missing object that the caller would
+  otherwise be allowed to access: `404 Not Found`". Signed out: "`401 Unauthorized` or redirect to
+  login".
+- CONFLICT: T06's default and the feature cards T08, T10, T12, T14, T15, T16 return 404 (`NotFound`)
+  for another user's object. The brief says 403. Decision needed before those cards run.
 
 ### Candidate (FP-CAN)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-CAN-1 | Profile and private resume rules | READY (limits from brief) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
-| FP-CAN-2 | Recommendations preserve fields and rank all jobs | BLOCKED on FP-MATCH-1 | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
-| FP-CAN-3 | Pending duplicate and application owner | READY (statuses from brief) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
+| FP-CAN-1 | Profile and private resume rules | NEEDS DECISION (profile part READY; resume part: the brief requires a raw-text resume and owner-only access, T08 builds PDF upload with employer access) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
+| FP-CAN-2 | Recommendations preserve fields and rank all jobs | READY (after T11) | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
+| FP-CAN-3 | Pending duplicate and application owner | NEEDS DECISION (status names and re-apply rule differ from T14 defaults) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
+
+Rule text (brief section "3. Candidate workflow"):
 
-Open questions:
-- FP-CAN-1: required profile fields? Resume file types and size limit? Who may see a resume
-  (only the owner, or also employers the candidate applied to)?
-- FP-CAN-2: which fields must each recommendation show? Do zero-score jobs appear?
-- FP-CAN-3: application status list? Can a candidate re-apply after a rejection or withdrawal?
+FP-CAN-1 "Candidate profile and resume":
+> A candidate **MUST** be able to view and edit only their own profile, including a display name and a list of technical skills. Skills **MUST** be saved and available to the matching function.
+>
+> A candidate **MUST** be able to enter a raw-text resume. The application **MUST** persist the text and allow the owner to view and replace it. PDF upload and extraction are optional. Resume contents are private: only the owning candidate may read or modify them. Any other candidate or employer **MUST** receive `403` through a direct URL/API request.
+
+FP-CAN-2 "Recommendations":
+> A candidate dashboard **MUST** list all current (not deleted) jobs with a visible match score and sort them from highest to lowest score. The dashboard **MUST** include the job title, employer/company, required skills, and a way to view the description.
+
+FP-CAN-3 "Applications":
+> A candidate **MUST** be able to apply to a job once. A new application **MUST** have status `Pending`. A duplicate application by the same candidate to the same job **MUST** be rejected without creating another row. A candidate **MUST** be able to view the job, employer, current status, and interview booking (if any) for each of their own applications.
+>
+> A candidate **MUST NOT** be able to view another candidate's applications or change an application status.
+
+Open questions, answered:
+- FP-CAN-1: required profile fields? "a display name and a list of technical skills". Resume file
+  types and size limit? NOT IN BRIEF; the required resume is "a raw-text resume", and "PDF upload
+  and extraction are optional". Who may see a resume? "only the owning candidate may read or modify
+  them. Any other candidate or employer **MUST** receive `403`". (T08's default of letting an
+  employer with an application open it contradicts this.)
+- FP-CAN-2: which fields must each recommendation show? "a visible match score", "the job title,
+  employer/company, required skills, and a way to view the description". Do zero-score jobs appear?
+  "list all current (not deleted) jobs", so yes. Closed (not deleted) jobs: NOT IN BRIEF.
+- FP-CAN-3: application status list? From FP-EMP-3: "exactly these statuses: `Pending`,
+  `Interviewing`, `Rejected`, or `Accepted`". New application: "status `Pending`". Can a candidate
+  re-apply after a rejection or withdrawal? "apply to a job once"; "A duplicate application by the
+  same candidate to the same job **MUST** be rejected without creating another row". No exception
+  for status is given; "withdrawal" does not exist in the brief. HTTP code for the duplicate: NOT IN
+  BRIEF.
 
 ### Employer (FP-EMP)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
 | FP-EMP-1 | Company profile | READY | T09 | `test_emp_company.py::test_fp_emp_1_company_profile` |
-| FP-EMP-2 | Job validation and deletion | READY (limits from brief) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
-| FP-EMP-3 | Applicant fields, order, status and role | READY (order from brief) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
+| FP-EMP-2 | Job validation and deletion | NEEDS DECISION (rule quoted; T10's cascade-delete default and "skills 1 to 30" are superseded; steps and tests mention the old default) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
+| FP-EMP-3 | Applicant fields, order, status and role | NEEDS DECISION (rule quoted; T15's order and field defaults superseded; depends on the FP-CAN-3 status-name decision) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
+
+Rule text (brief section "4. Employer workflow"):
+
+FP-EMP-1 "Company profile":
+> An employer **MUST** be able to view and edit a company profile containing at least a company name and description.
 
-Open questions:
-- FP-EMP-2: required job fields and limits? On delete, what happens to its applications and slots?
-- FP-EMP-3: which applicant fields are shown? Sort order? Which status changes are allowed?
+FP-EMP-2 "Job postings":
+> An employer **MUST** be able to create, view, edit, and delete their own job postings. Each posting **MUST** contain a non-empty title and description plus a required-skills list; the list may be empty. An employer **MUST** receive `403` when attempting to edit, delete, or manage applicants for another employer's posting.
+>
+> A job with no applications or interview slots **MUST** be deletable. If either kind of dependent record exists, deletion **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged.
+
+FP-EMP-3 "Applicant management":
+> For each owned job, an employer **MUST** be able to view its applicants sorted by match score from highest to lowest. Each row **MUST** show candidate identity, skills, match score, application status, and interview booking (if any).
+>
+> The employer who owns the job **MUST** be able to set an application to one of exactly these statuses: `Pending`, `Interviewing`, `Rejected`, or `Accepted`. Other employers and candidates **MUST NOT** be able to change the status.
+
+Open questions, answered:
+- FP-EMP-2: required job fields and limits? "a non-empty title and description plus a
+  required-skills list; the list may be empty". Length limits: NOT IN BRIEF. On delete, what happens
+  to its applications and slots? Nothing: "If either kind of dependent record exists, deletion
+  **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and
+  dependent records unchanged." (T10's cascade default is wrong.)
+- FP-EMP-3: which applicant fields are shown? "candidate identity, skills, match score, application
+  status, and interview booking (if any)". Sort order? "sorted by match score from highest to
+  lowest"; ties (FP-MATCH-1): "case-insensitive candidate display name and then stable candidate
+  ID". Which status changes are allowed? Any of "exactly these statuses: `Pending`, `Interviewing`,
+  `Rejected`, or `Accepted`"; a transition table is NOT IN BRIEF.
 
 ### Matching (FP-MATCH)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | **BLOCKED** | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |
+| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | READY (every rule and example quoted) | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |
+
+Rule text (brief section "5. Matching contract", FP-MATCH-1 "Score definition"):
+> The required match score is a deterministic skill-overlap score. Resume text is not an input. Normalize candidate and required skills by trimming surrounding whitespace, converting to lowercase, removing empty values, and removing duplicates. Let `C` and `R` be the resulting candidate-skill and required-skill sets:
+>
+> ```text
+> score = 100                                      when |R| = 0
+> score = floor(100 * |C intersection R| / |R|)   otherwise
+> ```
+>
+> The result **MUST** be an integer from 0 through 100. Candidate and employer views **MUST** call the same implementation. Sort by descending score. Break candidate dashboard ties by case-insensitive job title and then stable job ID; break employer applicant ties by case-insensitive candidate display name and then stable candidate ID.
+>
+> The seed data and unit tests **MUST** include these examples:
+>
+> | Candidate skills | Required skills | Expected score |
+> |---|---|---:|
+> | `Python, SQL` | `Python, SQL` | 100 |
+> | `Python` | `Python, SQL` | 50 |
+> | `Rust` | `Python, SQL` | 0 |
+> | any skills | empty list | 100 |
+>
+> `SPEC.md` **MUST** identify the matching implementation and describe how skills are stored. It may cite this formula rather than inventing another scoring oracle.
+
+Open questions, answered:
+- How is a skill normalised? "trimming surrounding whitespace, converting to lowercase, removing
+  empty values, and removing duplicates". Punctuation and synonyms: NOT IN BRIEF (so none).
+- Score formula? "score = 100 when |R| = 0"; "score = floor(100 * |C intersection R| / |R|)
+  otherwise". Fraction of the job's required skills, not Jaccard.
+- "The floor"? The `floor(...)` in the formula: "The result **MUST** be an integer from 0 through
+  100."
+- The two tie-breakers, in order? Candidate dashboard: "case-insensitive job title and then stable
+  job ID". Employer applicants: "case-insensitive candidate display name and then stable candidate
+  ID".
+- Worked examples? The four-row table above, copied verbatim into T11.
 
-Open questions (the brief must answer every one before T11 starts):
-- How is a skill normalised (case, whitespace, punctuation, synonyms)?
-- What is the score formula (overlap count, fraction of job skills, Jaccard)?
-- What is "the floor" (a minimum score, or rounding down)?
-- What are the two tie-breakers, in order?
-- Do the brief's worked examples exist? Copy every one, inputs and expected outputs, verbatim.
+FP-MATCH-2 "Optional AI enhancement" is optional and not planned:
+> Teams **MAY** add an LLM-generated explanation or secondary recommendation, but it earns no substitute credit and **MUST NOT** alter the required score or ordering.
 
 ### Scheduling (FP-SCHED)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rules from brief) | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
-| FP-SCHED-2 | Eligible and ineligible booking | **BLOCKED** | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
-| FP-SCHED-3 | Booking conflict contract | **BLOCKED** | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
+| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rule quoted; T12's "15 to 240 minutes" default superseded by "30-minute") | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
+| FP-SCHED-2 | Eligible and ineligible booking | READY (rule quoted; needs the `uq_booking_application` contract change and the status-name decision) | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
+| FP-SCHED-3 | Booking conflict contract | READY (contract quoted) | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
 
-Open questions:
-- FP-SCHED-1: slot length limits? Can slots overlap for one employer? Slots in the past? Which
-  timezone is shown to whom? Can a booked slot be deleted?
-- FP-SCHED-2: who is eligible to book (an application in which status, for which job)?
-- FP-SCHED-3: exactly what happens when two people book the same slot, or one person books twice?
-  What status code and message? This is a "contract", so the brief likely states it word for word.
+Rule text (brief section "6. Applications and interview scheduling"):
+
+FP-SCHED-1 "Availability":
+> An employer **MUST** be able to create and delete future, 30-minute availability slots. Each slot **MUST** have one owner and an exact start and end time with an unambiguous, documented timezone. The system **MUST** reject invalid durations, end-before-start values, and deletion of a booked slot. Booked slots **MUST NOT** be shown as available.
+
+FP-SCHED-2 "Booking eligibility":
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
+FP-SCHED-3 "Atomic concurrency":
+> Booking **MUST** be atomic at the database layer. Use a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an equivalent database mechanism. An in-process check alone is insufficient.
+>
+> When two eligible candidates concurrently attempt to book the same slot, exactly one attempt **MUST** succeed, the other **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message `Slot already booked`, and the database **MUST** contain exactly one booking afterward. Students **MUST** write unit tests for the booking conflict-handling logic. Database atomicity is verified through implementation review and the running system; students are not required to provide a synchronized multi-client test.
+
+Open questions, answered:
+- FP-SCHED-1: slot length limits? "30-minute availability slots"; "reject invalid durations". Can
+  slots overlap for one employer? NOT IN BRIEF. Slots in the past? "future ... slots". Which
+  timezone is shown to whom? NOT IN BRIEF beyond "an exact start and end time with an unambiguous,
+  documented timezone". Can a booked slot be deleted? No: "reject ... deletion of a booked slot".
+- FP-SCHED-2: who is eligible to book? The five bullets quoted above, all true: owns the
+  application; slot belongs to that application's employer; status `Interviewing`; slot in the
+  future and not booked; application has no existing booking.
+- FP-SCHED-3: two people book the same slot? "exactly one attempt **MUST** succeed, the other
+  **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message
+  `Slot already booked`, and the database **MUST** contain exactly one booking afterward". One person
+  books twice? NOT IN BRIEF as a conflict case; by FP-SCHED-2 the second attempt is ineligible ("the
+  application has no existing booking"). What the losing user sees next: NOT IN BRIEF.
+
+### Security (FP-SEC), required unit tests
+
+These four ids are graded and each demands at least one named unit test, but no task card carries
+them as its Requirement. Where they land today: FP-SEC-1 overlaps the T06 sweep; FP-SEC-2 and
+FP-SEC-3 have no owning test name; FP-SEC-4 is covered by `tests/conftest.py` if it uses an isolated
+database. Listed under T-BRIEF's OPEN QUESTIONS.
+
+Rule text (brief section "7. Security requirements"):
+
+FP-SEC-1 "Object access":
+> Changing an object ID in a request **MUST NOT** bypass FP-AUTH-3. Unit tests of the authorization logic **MUST** cover these representative boundaries:
+>
+> 1. one candidate cannot read or modify another candidate's resume or application;
+> 2. one employer cannot modify another employer's job or read its applicant list;
+> 3. a candidate cannot book a slot using another candidate's application.
+>
+> Unit tests for each functional requirement are additionally required by FP-TEST-1; code review and demonstration supplement that evidence.
+
+FP-SEC-2 "SQL injection":
+> All database access involving user-controlled values **MUST** use parameterized queries, a correctly used ORM, or an equivalent safe API. Concatenating raw user input into a query is prohibited. At least one unit test **MUST** pass SQL metacharacters to the query-building or data-access logic and verify that the input remains a bound value rather than executable SQL. Code review and the running system verify the use of safe database APIs.
+
+FP-SEC-3 "Cross-site scripting":
+> User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML. If the design intentionally supports formatted HTML, it **MUST** use an allow-list sanitizer. At least one unit test **MUST** pass `<script>alert(1)</script>` to the rendering or sanitization logic and verify that it is not emitted as executable markup.
+
+FP-SEC-4 "Secrets and test isolation":
+> The repository **MUST** contain no real secrets or personal data. Unit tests **MUST** use isolated fixtures or test doubles and **MUST NOT** call real third-party services. Any test that uses a database **MUST** use an isolated test database. `.env.example` **MUST** contain placeholders only.
 
 ### Non-functional and delivery
 
-| Item | Source | Task |
-|---|---|---|
-| README requirement-test table | template README | T21 |
-| SPEC.md sections | template SPEC.md | T21 |
-| INSTALL.md sections, demo accounts, reset command | template INSTALL.md | T19, T21 |
-| Docker build and start | template Dockerfile | T20 |
-| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | T02, T05, T06, phase 5 |
-| Performance on small fixtures | audit labels `type:performance` | `11-TESTING.md`, phase 5 |
-| Optional AI features | template SPEC.md | not planned (optional) |
+| Item | Source | Brief id | Task |
+|---|---|---|---|
+| Full-stack, runs from a clean checkout via `INSTALL.md`, no paid credentials | brief section 1 | FP-ARCH-1 | T19, T20, T21 |
+| README requirement-test table | template README | FP-DOC-2 | T21 |
+| SPEC.md sections | template SPEC.md | FP-PROC-1 | T21 |
+| INSTALL.md sections, demo accounts, reset command | template INSTALL.md | FP-DOC-1, FP-DOC-3 | T19, T21 |
+| Docker build and start | template Dockerfile | FP-SUB-1 (Dockerfile part) | T20 |
+| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | FP-SEC-1 to FP-SEC-4 | T02, T05, T06, phase 5 |
+| One command runs all unit tests, nonzero exit on failure | brief section 9 | FP-TEST-1 | `scripts/check.py` |
+| Performance on small fixtures | audit labels `type:performance` | none | `11-TESTING.md`, phase 5 |
+| Optional AI features | template SPEC.md | FP-MATCH-2 | not planned (optional) |
+
+Rule text that sets concrete content (brief section "9. Documentation, data, tests, and CI"):
+
+FP-DOC-3 "Deterministic demo data" (for T19):
+> One documented command **MUST** reset and seed a local database. Seed data **MUST** include at least:
+>
+> - two candidates and two employers;
+> - two jobs with required skills;
+> - the four matching examples required by FP-MATCH-1;
+> - applications covering all four statuses; and
+> - two `Interviewing` candidates eligible to race for the same available slot.
+>
+> Seed credentials **MUST** be clearly marked as local/demo credentials.
+
+FP-TEST-1 "Automated verification", the coverage list:
+> The unit tests **MUST** cover:
+>
+> - the unauthenticated, forbidden, and missing-object outcomes in FP-AUTH-3;
+> - the four skill-overlap examples and both tie-breaking rules;
+> - the representative authorization boundaries in FP-SEC-1;
+> - the SQL-injection case in FP-SEC-2;
+> - the XSS case in FP-SEC-3; and
+> - the booking conflict-handling logic in FP-SCHED-3.
+
+FP-PROC-1 "Living specification", first sentence:
+> `SPEC.md` **MUST** describe the architecture, data model and relationships, authentication/authorization design, API routes or server actions, major UI screens, matching contract, booking transaction, and security controls.
+
+FP-DOC-1 "Installation", first sentence:
+> `INSTALL.md` **MUST** list prerequisite versions, exact install commands, environment variables, database setup/migrations, seed command, run command, test command, `Dockerfile` build and start commands, and troubleshooting for any non-obvious dependency.
+
+FP-DOC-2 "Repository README", first two sentences:
+> `README.md` **MUST** give a short product overview, architecture summary, quick-start link to `INSTALL.md`, demo account credentials for seeded non-production users, unit-test command, document index, and known limitations. It **MUST** include a requirementâ€“test mapping table covering every requirement ID in this document, with implementation file(s) and named student-written unit tests for each functional requirement.
+
+FP-SUB-1 "Submission protocol", first sentence:
+> Each team **MUST** submit a permanent GitHub commit URL on `main`, and the repository at that commit **MUST** build and run entirely from its own `Dockerfile`.
diff --git a/docs/tasks/T05.md b/docs/tasks/T05.md
index 2be4c93..b808b76 100644
--- a/docs/tasks/T05.md
+++ b/docs/tasks/T05.md
@@ -2,17 +2,25 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 1 | foundation | T04 | no | READY (limits from the brief, defaults below) |
+| 1 | foundation | T04 | no | READY (rules quoted from the brief; limits are DEFAULT (not in brief)) |
 
 ## Goal
 People can create an account as a candidate or an employer, sign in, and sign out, safely.
 
 ## Requirement
-- FP-AUTH-1: registration and session lifecycle; invalid registration. Rule text: (from the brief)
-- FP-AUTH-2: salted hash and password verification. Rule text: (from the brief)
-- Defaults until the brief says otherwise: email lower-cased, max 254 chars, must match
-  `^[^@\s]+@[^@\s]+\.[^@\s]+$`; password 8 to 128 chars; display name 1 to 80 chars after strip;
-  role `candidate` or `employer`.
+- FP-AUTH-1: registration and session lifecycle; invalid registration. Rule text (brief section
+  "2. Roles and authentication", FP-AUTH-1 "Accounts"):
+  > The system **MUST** support exactly two application roles: `Candidate` and `Employer`. A user **MUST** be able to register, log in, and log out. Email or username identifiers **MUST** be unique.
+- FP-AUTH-2: salted hash and password verification. Rule text (brief section "2. Roles and
+  authentication", FP-AUTH-2 "Credential storage"):
+  > Passwords **MUST** be stored with an established password-hashing function. Plain text, reversible encryption, and a general-purpose fast hash such as unsalted SHA-256 do not satisfy this requirement. Authentication secrets **MUST NOT** be returned by an API or rendered in the UI.
+- DEFAULT (not in brief): the brief sets no email format or length, no password rules, no display
+  name limit and no session lifetime. Keep these defaults: email lower-cased, max 254 chars, must
+  match `^[^@\s]+@[^@\s]+\.[^@\s]+$`; password 8 to 128 chars; display name 1 to 80 chars after
+  strip; role `candidate` or `employer`.
+- Note: the brief writes the two roles as `Candidate` and `Employer`; the contract stores
+  `candidate` and `employer`. Whether the stored spelling must match the brief: unknown (listed in
+  T-BRIEF's OPEN QUESTIONS). Not changed here.
 
 ## Owns
 - `app/auth/service.py`

```
