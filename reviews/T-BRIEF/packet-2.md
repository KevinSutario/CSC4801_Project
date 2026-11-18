# Review packet T-BRIEF (2 of 3)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-T-BRIEF

Files in this packet: docs/tasks/T06.md, docs/tasks/T07.md, docs/tasks/T08.md, docs/tasks/T09.md, docs/tasks/T10.md, docs/tasks/T11.md, docs/tasks/T12.md, docs/tasks/T13.md, docs/tasks/T14.md

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
diff --git a/docs/tasks/T06.md b/docs/tasks/T06.md
index 742b7c3..ee7875d 100644
--- a/docs/tasks/T06.md
+++ b/docs/tasks/T06.md
@@ -2,16 +2,39 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | security | T10, T15, T16 | yes | READY after its dependencies (status codes from the brief) |
+| 3 | security | T10, T15, T16 | yes | READY after its dependencies (codes quoted from the brief; see CONFLICT under Requirement) |
 
 ## Goal
 Prove, route by route, that nobody can read or change what is not theirs, and that missing objects
 give 404. This task only writes tests. Holes it finds are reported, not fixed here.
 
 ## Requirement
-FP-AUTH-3: authorization and missing object. Rule text: (from the brief)
-Default until the brief says otherwise: wrong role 403; another user's object 404; missing object 404;
-signed out GET redirects to sign-in, signed out POST 401.
+FP-AUTH-3: authorization and missing object. Rule text (brief section "2. Roles and
+authentication", FP-AUTH-3 "Server-side authorization"):
+> Every protected operation **MUST** enforce role and ownership on the server; hiding a button in the UI is not sufficient. The observable response contract is:
+>
+> - unauthenticated request: `401 Unauthorized` or redirect to login;
+> - authenticated user with the wrong role or owner: `403 Forbidden`; and
+> - missing object that the caller would otherwise be allowed to access: `404 Not Found`.
+>
+> For non-HTTP frameworks, the UI and service layer **MUST** provide equivalent, clearly distinguishable outcomes.
+
+The brief also names the boundaries this sweep must cover (section "7. Security requirements",
+FP-SEC-1 "Object access"):
+> Changing an object ID in a request **MUST NOT** bypass FP-AUTH-3. Unit tests of the authorization logic **MUST** cover these representative boundaries:
+>
+> 1. one candidate cannot read or modify another candidate's resume or application;
+> 2. one employer cannot modify another employer's job or read its applicant list;
+> 3. a candidate cannot book a slot using another candidate's application.
+
+Expected codes, from the quote: signed out: `401 Unauthorized` or redirect to login; wrong role or
+wrong owner: `403 Forbidden`; missing object the caller could otherwise access: `404 Not Found`.
+
+CONFLICT (orchestrator decision needed, nothing below changed): the old default on this card said
+"another user's object 404", and the feature cards (T08, T10, T12, T14, T15) raise `NotFound` for
+another user's object. The brief says `403 Forbidden` for "the wrong role or owner". Either the
+feature cards change to `Forbidden` (a contract change) or the sweep records each 404 as a `BUG:`
+hole. Signed-out POST giving 401 and GET redirecting both satisfy the quote.
 
 ## Owns
 - `tests/unit/test_auth.py`
diff --git a/docs/tasks/T07.md b/docs/tasks/T07.md
index 640b050..f3d5461 100644
--- a/docs/tasks/T07.md
+++ b/docs/tasks/T07.md
@@ -2,17 +2,27 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | CAN | T05 | no | READY (limits from the brief, defaults below) |
+| 2 | CAN | T05 | no | READY (rule quoted from the brief; limits are DEFAULT (not in brief); see GAP) |
 
 ## Goal
 A candidate can fill in and edit their profile and skills. The Today page welcomes them and shows
 what to do next.
 
 ## Requirement
-FP-CAN-1 (profile part). Rule text: (from the brief)
-Defaults: headline max 120, location max 80, summary max 2000, timezone must be a valid IANA name
-(use `zoneinfo.available_timezones()`), skills: comma separated, at most 30, each 1 to 40 chars
-after normalising.
+FP-CAN-1 (profile part). Rule text (brief section "3. Candidate workflow", FP-CAN-1 "Candidate
+profile and resume", first paragraph):
+> A candidate **MUST** be able to view and edit only their own profile, including a display name and a list of technical skills. Skills **MUST** be saved and available to the matching function.
+
+Skill normalisation is the brief's FP-MATCH-1 rule (owned by T11, `app/skills.py`):
+> Normalize candidate and required skills by trimming surrounding whitespace, converting to lowercase, removing empty values, and removing duplicates.
+
+DEFAULT (not in brief): the brief sets no field limits. Keep: headline max 120, location max 80,
+summary max 2000, timezone must be a valid IANA name (use `zoneinfo.available_timezones()`), skills:
+comma separated, at most 30, each 1 to 40 chars after normalising.
+
+GAP (listed in T-BRIEF's OPEN QUESTIONS, not changed here): the brief's editable profile includes
+"a display name". This card's form has headline, location, timezone, summary and skills; the display
+name is set once at registration (T05) and no card lets the candidate edit it.
 
 ## Owns
 - `app/candidates/profile_service.py`
diff --git a/docs/tasks/T08.md b/docs/tasks/T08.md
index d2b32bb..bf4c88a 100644
--- a/docs/tasks/T08.md
+++ b/docs/tasks/T08.md
@@ -2,17 +2,28 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | CAN | T07 | no | READY (rules from the brief, defaults below) |
+| 2 | CAN | T07 | no | **BLOCKED**: rule quoted, but the card's design contradicts it (see CONFLICT); orchestrator decision needed |
 
 ## Goal
 A candidate can upload a resume, see and delete their resumes, and download them. Nobody else can,
 except as the brief allows.
 
 ## Requirement
-FP-CAN-1 (private resume rules). Rule text: (from the brief)
-Defaults: PDF only (extension `.pdf` and content starting with `%PDF-`), size limit
-`MAX_UPLOAD_MB`, at most 5 resumes per candidate. Who may view: the owner; and an employer who owns a
-job that has an application using this resume.
+FP-CAN-1 (private resume rules). Rule text (brief section "3. Candidate workflow", FP-CAN-1
+"Candidate profile and resume", second paragraph):
+> A candidate **MUST** be able to enter a raw-text resume. The application **MUST** persist the text and allow the owner to view and replace it. PDF upload and extraction are optional. Resume contents are private: only the owning candidate may read or modify them. Any other candidate or employer **MUST** receive `403` through a direct URL/API request.
+
+CONFLICT (three points; orchestrator decision needed; Steps and Tests below are unchanged):
+1. The required resume is raw text that the owner can view and replace. This card builds PDF upload
+   only, which the brief calls optional. No card builds a raw-text resume.
+2. The brief gives no employer any access ("only the owning candidate may read or modify them").
+   The old default let an employer with an application open it, and the FP-CAN-1 test bullet expects
+   that employer to get 200. The brief says that employer gets `403`.
+3. The refusal code is `403`. The card returns 404 (`NotFound`) "so ids cannot be probed".
+
+DEFAULT (not in brief), only relevant if the optional PDF upload is kept: PDF only (extension
+`.pdf` and content starting with `%PDF-`), size limit `MAX_UPLOAD_MB`, at most 5 resumes per
+candidate.
 
 ## Owns
 - `app/candidates/resume_service.py`
diff --git a/docs/tasks/T09.md b/docs/tasks/T09.md
index 0e7f5c3..fff230c 100644
--- a/docs/tasks/T09.md
+++ b/docs/tasks/T09.md
@@ -2,15 +2,21 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | EMP | T05 | no | READY (limits from the brief, defaults below) |
+| 2 | EMP | T05 | no | READY (rule quoted from the brief; limits are DEFAULT (not in brief)) |
 
 ## Goal
 An employer can create and edit one company profile, and has a home page.
 
 ## Requirement
-FP-EMP-1: company profile. Rule text: (from the brief)
-Defaults: name required, 1 to 120 chars; industry max 80; location max 80; website optional, if given
+FP-EMP-1: company profile. Rule text (brief section "4. Employer workflow", FP-EMP-1 "Company
+profile"):
+> An employer **MUST** be able to view and edit a company profile containing at least a company name and description.
+
+DEFAULT (not in brief): the brief sets no limits and names only "company name and description".
+Keep: name required, 1 to 120 chars; industry max 80; location max 80; website optional, if given
 must start with `https://` or `http://` and be max 200 chars; description max 4000.
+Escaping of company text is also required by FP-SEC-3 (brief section "7. Security requirements"):
+> User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML.
 
 ## Owns
 - `app/employers/service.py`
diff --git a/docs/tasks/T10.md b/docs/tasks/T10.md
index 0c268a3..45b3ba2 100644
--- a/docs/tasks/T10.md
+++ b/docs/tasks/T10.md
@@ -2,18 +2,34 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | EMP | T09 | no | READY (rules from the brief, defaults below) |
+| 2 | EMP | T09 | no | READY (rules quoted from the brief; two defaults SUPERSEDED, see Requirement; 403 CONFLICT flagged) |
 
 ## Goal
 An employer can post, edit, close and delete jobs with required skills. Anyone signed in can view
 an open job's detail page.
 
 ## Requirement
-FP-EMP-2: job validation and deletion. Rule text: (from the brief)
-Defaults: title 1 to 120 chars; description 1 to 5000; location max 80; employment type one of
-`EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "internship")`; salary min and max
-optional whole numbers from 0 to 10_000_000, min <= max; skills 1 to 30. Delete: also deletes its
-applications, slots and bookings (database cascade) unless the brief says otherwise.
+FP-EMP-2: job validation and deletion. Rule text (brief section "4. Employer workflow", FP-EMP-2
+"Job postings"):
+> An employer **MUST** be able to create, view, edit, and delete their own job postings. Each posting **MUST** contain a non-empty title and description plus a required-skills list; the list may be empty. An employer **MUST** receive `403` when attempting to edit, delete, or manage applicants for another employer's posting.
+>
+> A job with no applications or interview slots **MUST** be deletable. If either kind of dependent record exists, deletion **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged.
+
+SUPERSEDED by the quote (the old defaults said the opposite):
+- Skills: "the list may be empty". The old default "skills 1 to 30" is wrong; a job with no skills
+  is valid. (FP-MATCH-1 scores such a job 100 for every candidate.)
+- Delete: no cascade. If any application or interview slot exists, deletion fails with
+  `409 Conflict` and changes nothing. Overrides Step 7's "confirm-delete page that states what else is
+  deleted" and the test bullet "delete removes it plus its applications and slots". The orchestrator
+  should rewrite those lines; they are left as written here.
+
+CONFLICT (flagged, not changed): the brief says another employer gets `403`; Step 4 raises
+`NotFound` (404). See T06.
+
+DEFAULT (not in brief): title max 120 chars; description max 5000; location max 80; employment type
+one of `EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "internship")`; salary min and max
+optional whole numbers from 0 to 10_000_000, min <= max; at most 30 skills. "Closed" jobs are not in
+the brief at all (it says "current (not deleted) jobs" in FP-CAN-2); closing is a card feature.
 
 ## Owns
 - `app/jobs/service.py`
diff --git a/docs/tasks/T11.md b/docs/tasks/T11.md
index a260e8a..555b4c3 100644
--- a/docs/tasks/T11.md
+++ b/docs/tasks/T11.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | MATCH | T05, T-BRIEF | no | **BLOCKED**: rules only in the brief |
+| 2 | MATCH | T05, T-BRIEF | no | READY (every rule and example quoted from the brief) |
 
 ## Goal
 A pure, deterministic engine that scores a candidate against a job and ranks every job exactly as
@@ -11,13 +11,41 @@ the brief says, and the brief's skill normalisation.
 ## Requirement
 FP-MATCH-1: skill-overlap examples, normalization and floor; both tie-breakers.
 
-Rule text (T-BRIEF fills these; until then this card is BLOCKED):
-- Normalisation rule: (from the brief)
-- Score formula: (from the brief)
-- The floor: (from the brief)
-- Tie-breaker 1: (from the brief)
-- Tie-breaker 2: (from the brief)
-- Worked examples, verbatim: (from the brief)
+Rule text (brief section "5. Matching contract", FP-MATCH-1 "Score definition"), in full:
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
+Mapped to this card's placeholders (each is a quote from the block above):
+- Normalisation rule: "trimming surrounding whitespace, converting to lowercase, removing empty
+  values, and removing duplicates". Nothing about punctuation or synonyms: NOT IN BRIEF, so do not
+  add them (T07 and T10 rows need no re-normalising).
+- Score formula: "score = 100 when |R| = 0"; "score = floor(100 * |C intersection R| / |R|)
+  otherwise". "Resume text is not an input."
+- The floor: the `floor(...)` in the formula; "The result **MUST** be an integer from 0 through
+  100." So `score()` returns an `int`.
+- Tie-breaker 1 (candidate dashboard, `rank`): "case-insensitive job title".
+- Tie-breaker 2: "and then stable job ID". (Employer applicant lists, T15: "case-insensitive
+  candidate display name and then stable candidate ID".)
+- Worked examples, verbatim: the four-row table above. Inputs are comma-separated skill lists as
+  written; expected scores 100, 50, 0, 100.
+- "Candidate and employer views **MUST** call the same implementation."
 
 ## Owns
 - `app/skills.py`
diff --git a/docs/tasks/T12.md b/docs/tasks/T12.md
index a48466d..bedd45c 100644
--- a/docs/tasks/T12.md
+++ b/docs/tasks/T12.md
@@ -2,17 +2,34 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | SCHED | T05 | no | READY (rules from the brief, defaults below) |
+| 2 | SCHED | T05 | no | READY (rules quoted from the brief; duration default SUPERSEDED; the rest DEFAULT (not in brief)) |
 
 ## Goal
 Employers add interview slots for their jobs in their own time zone. Slots are stored in UTC and
 shown correctly in any time zone. Invalid slots are rejected.
 
 ## Requirement
-FP-SCHED-1: slot creation, timezones and deletion; invalid slots. Rule text: (from the brief)
-Defaults: date `YYYY-MM-DD`, times `HH:MM` 24-hour; end after start; length 15 to 240 minutes;
-start must be in the future; no overlap with another slot of the same job; a booked slot cannot be
-deleted (`Conflict("This slot is booked and cannot be deleted.")`).
+FP-SCHED-1: slot creation, timezones and deletion; invalid slots. Rule text (brief section
+"6. Applications and interview scheduling", FP-SCHED-1 "Availability"):
+> An employer **MUST** be able to create and delete future, 30-minute availability slots. Each slot **MUST** have one owner and an exact start and end time with an unambiguous, documented timezone. The system **MUST** reject invalid durations, end-before-start values, and deletion of a booked slot. Booked slots **MUST NOT** be shown as available.
+
+Worked examples: none in the brief for FP-SCHED-1.
+
+SUPERSEDED by the quote: slot length is exactly 30 minutes ("30-minute availability slots";
+"reject invalid durations"). The old default "length 15 to 240 minutes" is wrong. The test bullets
+"too short, too long" still apply (29 and 31 minutes are invalid durations).
+
+Required by the quote, matching the old defaults: end after start; start in the future; a booked
+slot cannot be deleted (`Conflict("This slot is booked and cannot be deleted.")`, message wording
+is DEFAULT (not in brief)); booked slots are never listed as available.
+
+DEFAULT (not in brief): date `YYYY-MM-DD`, times `HH:MM` 24-hour; no overlap with another slot of
+the same job; storage in UTC with the entry zone recorded (the brief only requires "an unambiguous,
+documented timezone", so document it in SPEC.md). The brief says a slot has "one owner" and does not
+say whether a slot belongs to a job or to the employer; this card attaches slots to jobs (DEFAULT).
+
+CONFLICT (flagged, not changed): the brief (FP-EMP-2, FP-AUTH-3) gives `403` for another
+employer's posting; the invalid-slots test bullet says `NotFound` for "someone else's job". See T06.
 
 ## Owns
 - `app/timeutil.py`
diff --git a/docs/tasks/T13.md b/docs/tasks/T13.md
index 87d927b..afbed2e 100644
--- a/docs/tasks/T13.md
+++ b/docs/tasks/T13.md
@@ -2,16 +2,29 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | BLOCKED until T11 is merged |
+| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | READY after T11 is merged (rule quoted from the brief; fields SUPERSEDE the default) |
 
 ## Goal
 A candidate sees every open job ranked for them, each with its score and which skills matched and
 which are missing.
 
 ## Requirement
-FP-CAN-2: recommendations preserve fields and rank all jobs. Rule text: (from the brief)
-Which fields each card shows: (from the brief). Default: title, company name, location, employment
-type, salary range or "Not stated", score, matched, missing.
+FP-CAN-2: recommendations preserve fields and rank all jobs. Rule text (brief section
+"3. Candidate workflow", FP-CAN-2 "Recommendations"):
+> A candidate dashboard **MUST** list all current (not deleted) jobs with a visible match score and sort them from highest to lowest score. The dashboard **MUST** include the job title, employer/company, required skills, and a way to view the description.
+
+Which fields each card shows (from the quote): "the job title, employer/company, required skills,
+and a way to view the description", plus "a visible match score". Order: "from highest to lowest
+score", ties by FP-MATCH-1: "case-insensitive job title and then stable job ID". The old default
+list (title, company name, location, employment type, salary range or "Not stated", score, matched,
+missing) must at least add the full required-skills list; the extra fields are DEFAULT (not in
+brief).
+
+Answers for the test bullets:
+- Zero-score jobs: "list all current (not deleted) jobs", so a zero-overlap job is present.
+- Closed jobs: NOT IN BRIEF. The brief knows only "current (not deleted)"; closing is a T10 card
+  feature. Excluding closed jobs is DEFAULT (not in brief).
+- "Candidate and employer views **MUST** call the same implementation." (FP-MATCH-1)
 
 ## Owns
 - `app/matching/service.py`
diff --git a/docs/tasks/T14.md b/docs/tasks/T14.md
index 16be56d..d74d006 100644
--- a/docs/tasks/T14.md
+++ b/docs/tasks/T14.md
@@ -2,19 +2,41 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | CAN + EMP | T08, T10 | yes | READY (statuses from the brief, defaults below) |
+| 3 | CAN + EMP | T08, T10 | yes | **BLOCKED**: rules quoted, but the status names and the re-apply default contradict the brief (see CONFLICT); contract decision needed |
 
 ## Goal
 A candidate applies to an open job through a confirm screen that shows exactly what will be shared,
 and can see all their applications. A second pending application to the same job is refused.
 
 ## Requirement
-FP-CAN-3: pending duplicate and application owner. Rule text: (from the brief)
-Defaults: `STATUSES = ("pending", "interview", "rejected", "hired", "withdrawn")`;
-`TRANSITIONS = {"pending": ("interview", "rejected"), "interview": ("hired", "rejected"),
-"rejected": (), "hired": (), "withdrawn": ()}`; re-applying is allowed only when no application to
-that job is `pending`; duplicate pending gives `Conflict("You already have a pending application
-for this job.")` and HTTP 409. Cover note max 2000 chars.
+FP-CAN-3: pending duplicate and application owner. Rule text (brief section "3. Candidate
+workflow", FP-CAN-3 "Applications"):
+> A candidate **MUST** be able to apply to a job once. A new application **MUST** have status `Pending`. A duplicate application by the same candidate to the same job **MUST** be rejected without creating another row. A candidate **MUST** be able to view the job, employer, current status, and interview booking (if any) for each of their own applications.
+>
+> A candidate **MUST NOT** be able to view another candidate's applications or change an application status.
+
+Status list (brief section "4. Employer workflow", FP-EMP-3 "Applicant management"):
+> The employer who owns the job **MUST** be able to set an application to one of exactly these statuses: `Pending`, `Interviewing`, `Rejected`, or `Accepted`. Other employers and candidates **MUST NOT** be able to change the status.
+
+CONFLICT (orchestrator decision needed; `app/applications/statuses.py` values are a contract):
+1. Statuses: the brief has exactly four, `Pending`, `Interviewing`, `Rejected`, `Accepted`. The old
+   default had five, `("pending", "interview", "rejected", "hired", "withdrawn")`. `withdrawn` is
+   not in the brief; `interview` and `hired` are named differently. FP-SCHED-2 keys eligibility on
+   the literal status `Interviewing` and FP-DOC-3 seeds "applications covering all four statuses".
+2. Re-applying: the brief says "apply to a job once" and rejects "a duplicate application by the
+   same candidate to the same job" with no exception for status. The old default allowed re-applying
+   once no application is `pending`, and the test bullet "after setting the first to `rejected` with
+   SQL, apply again works" expects that. Under the quote, that re-apply must be rejected.
+3. Transitions: NOT IN BRIEF. The brief only says the owner can "set an application to one of
+   exactly these statuses". The default `TRANSITIONS` table restricts moves the brief does not
+   restrict (for example `Rejected` back to `Pending`); whether that is acceptable: unknown.
+
+DEFAULT (not in brief): duplicate gives `Conflict(...)` and HTTP 409 (the brief gives no code or
+message for FP-CAN-3 duplicates); cover note max 2000 chars; resume attached to an application
+(the brief's resume is private to the candidate, see T08 CONFLICT).
+
+CONFLICT (flagged, not changed): the brief gives `403` for another candidate's application
+(FP-AUTH-3, FP-SEC-1 boundary 1); Step 3 raises `NotFound`. See T06.
 
 ## Owns
 - `app/applications/statuses.py`

```
