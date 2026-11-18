# Review packet CC01 (7 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/tasks/T14.md, docs/tasks/T15.md

## Review type: task

## Task card

# CC01 · Contract changes from the brief (resume, statuses, slots, 403, deletion)

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| any | docs | T-BRIEF | no | READY. Runs alone. Docs and `scripts/contracts.json` only. No app code exists yet. |

## Goal
T-BRIEF quoted the brief into the cards and found that the plan's contracts, data model and several
card Steps contradict it. This card changes the frozen plan files and the affected cards so that every
later agent builds the brief's rules and never the old defaults. After this card, no card says
CONFLICT, SUPERSEDED, GAP or NEEDS DECISION any more: each such note is replaced by the decided text.

The decisions are already taken (by Kevin, logged as D9 to D18 in `docs/state/DECISIONS.md`). Do not
re-decide anything. Apply them exactly as written below.

## Requirement
All FP-* ids. Every rule below is quoted in `docs/plan/01-REQUIREMENTS.md`; this card only propagates
them. Where this card says DEFAULT (not in brief), keep that mark in the text you write.

## Owns
- `docs/plan/01-REQUIREMENTS.md`
- `docs/plan/02-ARCHITECTURE.md`
- `docs/plan/03-DATA-MODEL.md`
- `docs/plan/04-AUTH-SECURITY.md`
- `docs/plan/05-UX-FLOWS.md`
- `docs/plan/07-CONTRACTS.md`
- `docs/plan/11-TESTING.md`
- `docs/plan/12-DEPLOY.md`
- `scripts/contracts.json`
- `docs/tasks/T01.md`
- `docs/tasks/T04.md`
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
- `docs/tasks/T19.md`
- `docs/tasks/T21.md`

## May read
- `CLAUDE.md`
- `docs/BRIEF.md`
- `docs/state/DECISIONS.md` (D9 to D18)
- `docs/tasks/T-BRIEF.md`, `docs/tasks/TEMPLATE.md`
- every file listed under Owns
- `scripts/check_contracts.py` (to see how `contracts.json` is read; do not change it)

## The decisions, and what each changes

### D9 · Another user's object is 403, missing is 404 (FP-AUTH-3, FP-CAN-1, FP-EMP-2, FP-SEC-1)
- Every ownership helper raises `NotFound` when the row does not exist and `Forbidden` when it exists
  but belongs to someone else. Wrong role stays 403 (decorator). Signed out: GET redirects to login,
  other methods 401 (unchanged).
- `04-AUTH-SECURITY.md`: rewrite the Authorization bullets and checklist line 4 to say exactly that.
  Remove every "404 for both so ids cannot be probed" sentence.
- `07-CONTRACTS.md`: every comment that says "NotFound if not theirs" or "missing or not allowed"
  becomes "NotFound if missing; Forbidden if another user's".
- Cards T06, T08, T10, T12, T14, T15, T16: replace `NotFound` with `Forbidden` wherever the object
  belongs to another user, in Steps and Tests. Missing ids stay `NotFound`. T06's sweep expects:
  user B with A's id gives 403; missing id gives 404; wrong role gives 403; signed out gives redirect
  or 401. Delete every CONFLICT paragraph about 403 vs 404 once the text below it is fixed.

### D10 · The resume is raw text, one per candidate, owner-only (FP-CAN-1)
- `03-DATA-MODEL.md`: replace the `resumes` table with
  ```sql
  CREATE TABLE resumes (
    owner_id    INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    body        TEXT NOT NULL,
    updated_at  TEXT NOT NULL
  );
  ```
  Remove `resume_id` from `applications`. In "Audit actions" replace `resume.upload` and
  `resume.delete` with `resume.update`. Update the Relationships block and "Why these constraints"
  (drop the `stored_name` sentence).
- `07-CONTRACTS.md`, section "candidates: resume (T08)", becomes exactly:
  ```python
  def get_resume(conn: Conn, owner_id: int) -> dict | None      # keys: owner_id, body, updated_at
  def save_resume(conn: Conn, owner_id: int, body: str) -> None
      # strip; ValidationError({"body": ...}) if empty or over RESUME_MAX_CHARS; upsert; audit resume.update
  def get_resume_for_viewer(conn: Conn, viewer_id: int, candidate_id: int) -> dict
      # Forbidden unless viewer_id == candidate_id; then NotFound if that candidate has no resume
  RESUME_MAX_CHARS: int = 20000     # DEFAULT (not in brief)
  ```
  Routes: `candidates.resume` GET, POST `/candidate/resume` (candidate only: shows the current text
  in a textarea, POST replaces it); `candidates.resume_view` GET
  `/candidates/<int:candidate_id>/resume` (`@login_required`, any role: the owner sees their text,
  anyone else gets 403 through `get_resume_for_viewer`). Remove `resume_delete` and
  `resume_download`. Template `candidates/resume.html` only.
- `scripts/contracts.json` T08: names `app.candidates.resume_service:get_resume`,
  `:save_resume`, `:get_resume_for_viewer`, `:RESUME_MAX_CHARS`; endpoints
  `["candidates.resume", "GET POST", "/candidate/resume"]` and
  `["candidates.resume_view", "GET", "/candidates/<int:candidate_id>/resume"]`.
- `02-ARCHITECTURE.md`: rewrite the FP-CAN-1 flow lines (no files, no `send_file`, no `static/`
  sentence). Keep `UPLOAD_DIR` and `MAX_UPLOAD_MB` in the config table but add "(unused since CC01;
  kept so the Dockerfile and `.env.example` do not change)".
- `04-AUTH-SECURITY.md`: replace the "File uploads (resumes)" section with a two-line "Resumes"
  section: raw text, owner-only, 403 for everyone else, rendered escaped (FP-SEC-3). Checklist line 7
  becomes "No file is ever written from user input." Data privacy bullet: owner only.
- `05-UX-FLOWS.md`: journey line "Upload resume [C01] (PDF, private)" becomes "Resume [C01] (raw
  text, private to you)"; screen row "Resume upload and list" becomes "Resume (view and replace)";
  Confirm application box no longer lists a resume file: "This will be sent to <company>: your
  name, your skills, your cover note. Not shared: your resume, your email address, your other
  applications." Applicants table: drop "resume link".
- `11-TESTING.md` FP-CAN-1 row: "profile saves and reloads; skills normalised and deduped; resume
  text saved and replaced; owner can read it; another candidate and an employer get 403 by direct
  URL".
- `T08.md`: rewrite Goal, Contract, Steps, Tests for the raw-text design. Tests keep the template name
  `test_fp_can_1_profile_and_private_resume_rules` and must cover: save then get returns the text;
  replace overwrites (one row); empty and over-limit rejected; owner GET `/candidates/<own id>/resume`
  200 with the text escaped; another candidate 403; an employer 403; owner with no resume 404;
  `<script>alert(1)</script>` in the body is not emitted as markup. Owns: `app/candidates/resume_service.py`,
  `app/candidates/routes_resume.py`, `app/templates/candidates/resume.html`, `tests/unit/test_can_resume.py`.
  May read drops the "File uploads" section. Remove the DEFAULT paragraph about PDFs.
- `T14.md`: `apply` has no `resume_id` (see D11); the confirm page has no resume select.
- `T15.md`: no `resume_id` field, no resume link.
- `T19.md`: remove `scripts/demo_resume.pdf` from Owns and Steps; seed Mei Lin's resume with
  `save_resume(conn, user_id, "Demo resume. Fictional person.")`.
- `T21.md` Step 3: scheduling and resume sections cite D10 to D14.

### D11 · Four statuses, any change allowed, apply once ever (FP-CAN-3, FP-EMP-3, FP-SCHED-2)
- Stored values are lower-case: `("pending", "interviewing", "rejected", "accepted")`. Labels are the
  brief's spellings `Pending`, `Interviewing`, `Rejected`, `Accepted`. There are no transition rules:
  the owning employer may set any status other than the current one.
- `03-DATA-MODEL.md` `applications`: `status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN
  ('pending', 'interviewing', 'rejected', 'accepted'))`; replace the partial unique index with
  `CREATE UNIQUE INDEX uq_application ON applications (job_id, candidate_id);` and fix its comment
  ("one application per candidate per job, ever").
- `07-CONTRACTS.md` `app/applications/statuses.py`:
  ```python
  STATUSES: tuple[str, ...] = ("pending", "interviewing", "rejected", "accepted")   # brief FP-EMP-3, stored lower-case
  TRANSITIONS: dict[str, tuple[str, ...]]   # every status -> the other three (brief has no transition rules)
  LABELS: dict[str, str]                    # "pending" -> "Pending", and so on
  ```
  `apply(conn: Conn, candidate_id: int, job_id: int, cover_note: str) -> int`
  (`Conflict("You have already applied to this job.")` for any existing application, whatever its
  status; message is DEFAULT (not in brief)). `list_for_candidate` returns, per row, at least
  `id, job_id, job_title, company_name, status, created_at, booking` where `booking` is
  `None` or `{"slot_id", "starts_at", "ends_at"}`.
- `T14.md`: rewrite the Requirement CONFLICT block into the decided text; Steps and Tests: no
  re-apply after rejection (the test asserts the second apply is refused even after the first is set
  to `rejected` with SQL); the unique index is `uq_application`; drop every `resume_id` mention; mine
  page shows the booking time when there is one. Status is BLOCKED no more: READY.
- `T15.md`: status READY; `set_status` accepts any status in `STATUSES` other than the current one
  (`ValidationError({"status": ...})` otherwise); changing status never touches bookings (quote
  FP-SCHED-2's last sentence). `list_applicants` returns dicts with exactly these keys, written into
  `07-CONTRACTS.md` and the card: `application_id, candidate_id, candidate_name, headline,
  skills (list[str], sorted), score, matched, missing, status, applied_at, booking` where `booking`
  is `None` or `{"slot_id", "starts_at", "ends_at"}`. Step 2 adds one query for the bookings of
  those applications (joined to `interview_slots`), so the query count stays fixed. May read adds
  `docs/plan/03-DATA-MODEL.md (tables: applications, bookings, interview_slots)`.
- `T01.md` test bullet "two pending applications" becomes "two applications for the same job and
  candidate raise IntegrityError"; add "two bookings for the same application raise IntegrityError".

### D12 · Job delete with dependants is 409 and changes nothing; empty skills allowed (FP-EMP-2)
- `03-DATA-MODEL.md` `applications.job_id ... ON DELETE RESTRICT`. Comment: deletion is refused in the
  service first (409), the constraint is the backstop.
- `07-CONTRACTS.md` jobs: `delete_job`: "Forbidden if another employer's; Conflict if the job has any
  application (interview slots are employer-owned since CC01, so applications and their bookings are
  the only dependants); deletes nothing in that case". Add a helper
  `def count_dependants(conn: Conn, job_id: int) -> int` to `app/jobs/service.py` and to
  `contracts.json` T10 names.
- `T10.md`: skills 0 to 30; Step 7 confirm-delete page says either "This job has no applications and
  can be deleted" or "This job has N applications and cannot be deleted" (no delete button then);
  `jobs.delete` POST returns 409 via `Conflict`; the FP-EMP-2 test asserts that after a refused
  delete the job and its applications are unchanged. Delete the SUPERSEDED and CONFLICT paragraphs
  once applied.

### D13 · Slots belong to the employer, are exactly 30 minutes and in the future; one booking per application (FP-SCHED-1, FP-SCHED-2)
- `03-DATA-MODEL.md` `interview_slots`: drop `job_id`; keep `employer_id`; replace `ix_slots_job` with
  `CREATE INDEX ix_slots_employer ON interview_slots (employer_id, starts_at);`. Add
  `CREATE UNIQUE INDEX uq_booking_application ON bookings (application_id);` (no longer a comment).
  Fix the Relationships block: `users (employer) 1 ─ * interview_slots 1 ─ 0..1 bookings 1 ─ 1 applications`.
- `07-CONTRACTS.md` scheduling (T12):
  ```python
  def create_slot(conn: Conn, employer_id: int, date_str: str, start_str: str, end_str: str,
                  tz_name: str) -> int
      # ValidationError: bad date or time, unknown zone, DST gap, end not after start,
      # duration not exactly 30 minutes, start not in the future, overlap with the employer's own slot
      # (overlap rule is DEFAULT (not in brief))
  def delete_slot(conn: Conn, employer_id: int, slot_id: int) -> None
      # NotFound if missing; Forbidden if another employer's; Conflict if booked (409 is DEFAULT (not in brief))
  def list_slots_for_employer(conn: Conn, employer_id: int) -> list[dict]   # adds "booked": bool; start ascending
  ```
  Routes: `scheduling.slots` GET, POST `/employer/slots`; `scheduling.delete_slot` POST
  `/employer/slots/<int:slot_id>/delete`. Template `scheduling/slots.html`.
  Booking (T16, T17):
  ```python
  def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
      # the brief's five conditions except the slot ones: owns it, status interviewing, no booking yet
  def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
      # future, unbooked slots of the employer who owns the application's job; start ascending
  def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
      # NotFound: application or slot missing. Forbidden: application is another candidate's, or
      # status is not interviewing, or the application already has a booking, or the slot belongs
      # to another employer. Conflict("Slot already booked"): slot already booked (checked inside
      # BEGIN IMMEDIATE, and again from sqlite3.IntegrityError). Nothing is written on any failure.
  ```
- `scripts/contracts.json` T12: names `app.scheduling.slots:create_slot`, `:delete_slot`,
  `:list_slots_for_employer` (plus the unchanged `app.timeutil` names); endpoints
  `["scheduling.slots", "GET POST", "/employer/slots"]`,
  `["scheduling.delete_slot", "POST", "/employer/slots/<int:slot_id>/delete"]`.
- `tests/conftest.py` contract: `make_slot(employer_id: int, starts_at="2030-01-07T02:00:00Z",
  ends_at="2030-01-07T02:30:00Z", created_tz="UTC") -> int`; add
  `make_booking(application_id: int, slot_id: int) -> int`. `make_application` unchanged (status
  default `"pending"`). Update `T04.md` to match (Owns unchanged).
- `02-ARCHITECTURE.md` FP-SCHED flow: slots per employer; booking checks the five conditions.
- `05-UX-FLOWS.md`: employer journey "Interview slots [R13]" is reached from the employer home, route
  `/employer/slots`; screen row updated; slot label example uses a 30-minute range
  ("Mon 30 Nov, 10:00 to 10:30 (Asia/Hong_Kong)").
- `T12.md`: Goal, Contract, Steps, Tests rewritten for employer-owned slots: no job ownership query,
  no `job_id`; duration exactly 30 minutes (29 and 31 minutes are invalid); page reached from the
  employer home. Invalid-slot test cases: bad date, bad time, end before start, 29 minutes, 31
  minutes, in the past, overlapping own slot, unknown zone; plus deleting another employer's slot
  gives `Forbidden`, a missing slot `NotFound`, a booked slot `Conflict`. Remove the SUPERSEDED,
  DEFAULT-about-jobs and CONFLICT paragraphs once applied.
- `T16.md`: READY; "slot of a different job" becomes "slot of a different employer"; Step 2 uses the
  five conditions; the ineligible test is parametrised over: status not `interviewing`, another
  candidate's application (`Forbidden`), slot of another employer (`Forbidden`), application that
  already has a booking on a different slot (`Forbidden`), slot in the past (`Forbidden`), slot
  already booked by another application (`Conflict`), missing slot (`NotFound`), missing application
  (`NotFound`); each leaves no new booking row. `list_bookable_slots` never lists a past or booked
  slot. Remove the "request the index first" sentence (this card adds it).
- `T17.md`: READY; delete the sentence claiming `07-CONTRACTS.md` is outside the task's May read (it
  is listed there); message is exactly `Slot already booked`, status 409; the losing user sees
  `scheduling/book.html` re-rendered with that message (DEFAULT (not in brief)); same candidate
  booking twice is refused as `Forbidden` by the no-existing-booking condition (D14).
- `T06.md`: the sweep's list of routes with ids uses the new slot route and the resume view route; add
  FP-SEC-1's three boundaries as named cases.
- `T19.md` and `12-DEPLOY.md`: see D17.

### D14 · Conflict contract (FP-SCHED-3)
`Conflict("Slot already booked")`, HTTP 409, exactly one booking row afterwards, a `booking.conflict`
audit row written in a separate transaction after the rollback. Already in T17; make the message
literal everywhere it appears (`07-CONTRACTS.md`, T16, T17).

### D15 · Matching (FP-MATCH-1)
`07-CONTRACTS.md` `app/skills.py`: `normalise_skill` is no longer provisional. Its comment becomes
"brief FP-MATCH-1: strip surrounding whitespace, lower-case; nothing else (no inner-space
collapsing)". `parse_skill_list`: split on commas, normalise, drop empties, dedupe keeping order.
`T01.md` Step 6 and the `test_db.py` bullet, and `T11.md` Step 2 and Pitfalls, say the same (T11
keeps the function and adds tests; T07 and T10 rows never need re-normalising).
`07-CONTRACTS.md` engine: `score` returns `{"score": int, "matched": [...], "missing": [...]}` with
`score = 100` when the job has no skills, else `floor(100 * |C ∩ R| / |R|)` (integer arithmetic:
`100 * len(common) // len(required)`); `rank` sorts by score descending, then `title.lower()`, then
`id`. `T11.md` Contract block: same. `T13.md`: recommendations list every job (D18: there is no
closed state); the test asserts the order equals `engine.rank` and that a job with no required skills
scores 100.
`T15.md`: applicants sorted by score descending, then `display_name.lower()`, then `candidate_id`.

### D16 · Candidate display name is editable (FP-CAN-1)
`07-CONTRACTS.md` profile: `get_profile` also returns `display_name`;
`save_profile(conn: Conn, candidate_id: int, display_name: str, headline: str, location: str,
timezone: str, summary: str, skills_text: str) -> None` updates `users.display_name` (1 to 80
chars after strip, DEFAULT (not in brief)) in the same transaction. `T07.md`: add the field to the
form, Steps and Tests; delete the GAP paragraph. `T15.md` and `T13.md` need no change.

### D17 · Seed data (FP-DOC-3)
`12-DEPLOY.md` "Demo data" and `T19.md` Step 2 state the mandatory minimum, quoting FP-DOC-3:
- candidates: `meilin@demo.keystone` (skills Python, SQL), `arjun@demo.keystone` (skills Python),
  `sofia@demo.keystone` (skills Rust); employers `daniel@demo.keystone` (Harbourline Logistics),
  `priya@demo.keystone` (Tidewater Freight). One demo password for all, documented as demo-only.
- jobs: Harbourline "Data Analyst" requires Python, SQL; Tidewater "Graduate Trainee" requires no
  skills. These give the four FP-MATCH-1 examples: Mei Lin 100 and Arjun 50 and Sofia 0 on Data
  Analyst, everyone 100 on Graduate Trainee. T19 may add more jobs after these.
- applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates eligible
  to race for one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee `accepted`;
  Sofia on Graduate Trainee `rejected`.
- slots: Daniel has one future 30-minute slot, unbooked, created in `Asia/Hong_Kong`; Priya has one in
  `Europe/London`.
- `tests/unit/test_seed.py` asserts the counts above and that the four example scores come out of
  `engine.score` on the seeded rows.
Update the demo-account table (five accounts) and the `seed.py` sentence (no uploads folder).

### D18 · No closed state for jobs; things kept as DEFAULT (not in brief)
- Jobs have no open/closed flag. Remove `is_open` from `03-DATA-MODEL.md` (column, index comments),
  from `07-CONTRACTS.md` (`update_job` loses `is_open: bool`; `list_open_jobs` is renamed
  `list_jobs(conn: Conn) -> list[dict]`, "every job with company_name and skills"; `make_job` loses
  `is_open=1`; `get_job` is "NotFound if missing" only), from `scripts/contracts.json` (T10 name
  `app.jobs.service:list_jobs` replaces `list_open_jobs`), from `02-ARCHITECTURE.md` and
  `05-UX-FLOWS.md` wherever "open job" or "close" appears, and from cards T04, T10 (no close action,
  no "closed job 404" tests; `jobs.detail` is `@login_required` and shows any job), T13 (Contract,
  Step 3 `get_job` becomes "NotFound if missing" only, and the test bullet), T14 (apply to any
  existing job; a missing job is 404), T19. The word "open" in "open slots" stays.
- Roles are stored `candidate` and `employer`; pages show `Candidate` and `Employer`.
- Password rules, email format, session lifetime, field length limits, slot overlap policy, display
  timezone and the HTTP code for deleting a booked slot stay as the cards' defaults, each marked
  DEFAULT (not in brief).

### FP-SEC tests (FP-SEC-1 to FP-SEC-4, FP-TEST-1)
Add these names to the "Test files and owners" table in `07-CONTRACTS.md` and to the owning cards'
Tests sections:
- `tests/unit/test_auth.py::test_fp_sec_2_sql_metacharacters_stay_bound` (T05): register and
  authenticate with the email `x'); DROP TABLE users; --@example.com` and the display name
  `Robert'); DELETE FROM users; --`; the users table still exists and holds the rows; the literal
  strings are stored.
- `tests/unit/test_emp_company.py::test_fp_sec_3_script_tag_is_escaped` (T09): company name and
  description `<script>alert(1)</script>` render as `&lt;script&gt;` and the raw tag never appears
  in the response.
- `tests/unit/test_db.py::test_fp_sec_4_tests_use_isolated_database` (T01): the `app` fixture's
  `DATABASE` is under `tmp_path` and differs between two tests.
- `tests/unit/test_authz_sweep.py::test_fp_sec_1_object_access_boundaries` (T06): the three brief
  boundaries, each as a named case.
`11-TESTING.md` requirement table: add four FP-SEC rows.

## Steps
1. Read `docs/state/DECISIONS.md` D9 to D18 and this card fully. Read every Owns file before editing it.
2. `03-DATA-MODEL.md` (D10 to D13). Keep the SQL block valid: run it once through
   `python -c "import sqlite3; sqlite3.connect(':memory:').executescript(open('x.sql').read())"` on a
   copy of the block in a temporary file outside the repo, then delete the file.
3. `07-CONTRACTS.md`, then `scripts/contracts.json` to match it exactly. Run
   `python -c "import json; json.load(open('scripts/contracts.json'))"`.
4. `04-AUTH-SECURITY.md`, `02-ARCHITECTURE.md`, `05-UX-FLOWS.md`, `11-TESTING.md`, `12-DEPLOY.md`.
5. Cards, in this order: T01, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17,
   T19, T21. In each: apply the decisions, then delete the CONFLICT, SUPERSEDED, GAP and
   "orchestrator decision needed" paragraphs that T-BRIEF left, keeping the brief quotes. Set every
   Status to READY (with its "after <deps>" note). Keep every Owns list unchanged except T19 (drop
   the PDF). Keep every template test name unchanged.
6. `01-REQUIREMENTS.md`: change each NEEDS DECISION to READY with "(D<n>)" and make the Tests column
   list the new FP-SEC test names in a new FP-SEC table.
7. `grep -rn "CONFLICT\|SUPERSEDED\|NEEDS DECISION\|GAP (\|resume_id\|job_id\b.*slot\|demo_resume\|withdrawn\|hired\|uq_pending" docs/tasks docs/plan scripts/contracts.json`
   must find nothing except historical mentions in `docs/BRIEF.md` (none expected) and this card.
8. `python scripts/check.py`, `python scripts/check_scope.py CC01`, commit.

## Done when
- check and scope pass
- the grep in step 7 is clean
- `scripts/contracts.json` parses and matches `07-CONTRACTS.md` name for name
- no card says BLOCKED for a reason this card resolves

## Pitfalls
- Do not change `app/`: it does not exist yet. T01 to T05 will build from the files you change.
- Do not rename template test names. Do not change any Owns list except T19's PDF line.
- Do not soften a brief rule back toward an old default because it is more convenient.
- `check_contracts.py` reads `contracts.json` by task id; keep every task key present even if empty.


## Changed files

```
 docs/plan/01-REQUIREMENTS.md  |  80 ++++++++++++++------------
 docs/plan/02-ARCHITECTURE.md  |  48 +++++++++-------
 docs/plan/03-DATA-MODEL.md    |  55 +++++++++---------
 docs/plan/04-AUTH-SECURITY.md |  43 +++++++-------
 docs/plan/05-UX-FLOWS.md      |  43 +++++++-------
 docs/plan/07-CONTRACTS.md     | 128 ++++++++++++++++++++++++++++--------------
 docs/plan/11-TESTING.md       |  22 +++++---
 docs/plan/12-DEPLOY.md        |  31 ++++++----
 docs/tasks/T01.md             |  19 +++++--
 docs/tasks/T04.md             |  30 ++++++++--
 docs/tasks/T05.md             |  10 +++-
 docs/tasks/T06.md             |  58 +++++++++++++------
 docs/tasks/T07.md             |  53 +++++++++--------
 docs/tasks/T08.md             | 107 +++++++++++++++++++----------------
 docs/tasks/T09.md             |  10 +++-
 docs/tasks/T10.md             | 113 ++++++++++++++++++++++++-------------
 docs/tasks/T11.md             |  42 ++++++++------
 docs/tasks/T12.md             | 108 +++++++++++++++++++++--------------
 docs/tasks/T13.md             |  30 +++++-----
 docs/tasks/T14.md             | 122 ++++++++++++++++++++++++----------------
 docs/tasks/T15.md             |  96 +++++++++++++++++--------------
 docs/tasks/T16.md             |  93 ++++++++++++++++++------------
 docs/tasks/T17.md             |  63 ++++++++++++---------
 docs/tasks/T19.md             |  59 ++++++++++++++-----
 docs/tasks/T21.md             |   8 ++-
 scripts/contracts.json        |  23 +++-----
 26 files changed, 904 insertions(+), 590 deletions(-)

```

## Check output (in the worktree)

```
=== lint: C:\Users\sutar\AppData\Local\Programs\Python\Python311\python.exe -m ruff check .
All checks passed!

=== tests: C:\Users\sutar\AppData\Local\Programs\Python\Python311\python.exe -m pytest tests/unit -q -rs -p no:cacheprovider
.........................................                                [100%]
41 passed in 13.49s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for CC01
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
diff --git a/docs/tasks/T14.md b/docs/tasks/T14.md
index d74d006..8f08dad 100644
--- a/docs/tasks/T14.md
+++ b/docs/tasks/T14.md
@@ -2,15 +2,16 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | CAN + EMP | T08, T10 | yes | **BLOCKED**: rules quoted, but the status names and the re-apply default contradict the brief (see CONFLICT); contract decision needed |
+| 3 | CAN + EMP | T08, T10 | yes | READY (after T08, T10; statuses and apply-once by D11, codes by D9, no resume on applications by D10) |
 
 ## Goal
-A candidate applies to an open job through a confirm screen that shows exactly what will be shared,
-and can see all their applications. A second pending application to the same job is refused.
+A candidate applies to a job through a confirm screen that shows exactly what will be shared, and
+can see all their applications with their status and booking. A candidate can apply to a job once,
+ever: a second application is refused without a row, whatever the first one's status.
 
 ## Requirement
-FP-CAN-3: pending duplicate and application owner. Rule text (brief section "3. Candidate
-workflow", FP-CAN-3 "Applications"):
+FP-CAN-3: duplicate and application owner. Rule text (brief section "3. Candidate workflow",
+FP-CAN-3 "Applications"):
 > A candidate **MUST** be able to apply to a job once. A new application **MUST** have status `Pending`. A duplicate application by the same candidate to the same job **MUST** be rejected without creating another row. A candidate **MUST** be able to view the job, employer, current status, and interview booking (if any) for each of their own applications.
 >
 > A candidate **MUST NOT** be able to view another candidate's applications or change an application status.
@@ -18,25 +19,21 @@ workflow", FP-CAN-3 "Applications"):
 Status list (brief section "4. Employer workflow", FP-EMP-3 "Applicant management"):
 > The employer who owns the job **MUST** be able to set an application to one of exactly these statuses: `Pending`, `Interviewing`, `Rejected`, or `Accepted`. Other employers and candidates **MUST NOT** be able to change the status.
 
-CONFLICT (orchestrator decision needed; `app/applications/statuses.py` values are a contract):
-1. Statuses: the brief has exactly four, `Pending`, `Interviewing`, `Rejected`, `Accepted`. The old
-   default had five, `("pending", "interview", "rejected", "hired", "withdrawn")`. `withdrawn` is
-   not in the brief; `interview` and `hired` are named differently. FP-SCHED-2 keys eligibility on
-   the literal status `Interviewing` and FP-DOC-3 seeds "applications covering all four statuses".
-2. Re-applying: the brief says "apply to a job once" and rejects "a duplicate application by the
-   same candidate to the same job" with no exception for status. The old default allowed re-applying
-   once no application is `pending`, and the test bullet "after setting the first to `rejected` with
-   SQL, apply again works" expects that. Under the quote, that re-apply must be rejected.
-3. Transitions: NOT IN BRIEF. The brief only says the owner can "set an application to one of
-   exactly these statuses". The default `TRANSITIONS` table restricts moves the brief does not
-   restrict (for example `Rejected` back to `Pending`); whether that is acceptable: unknown.
+Decided (D11):
+1. Statuses: exactly four, stored lower-case `("pending", "interviewing", "rejected", "accepted")`,
+   shown with the brief's spellings `Pending`, `Interviewing`, `Rejected`, `Accepted`. A new
+   application is `pending`.
+2. Apply once, ever: a second application by the same candidate to the same job is refused with
+   `Conflict` and no row, whatever the first one's status (including `rejected`). The unique index
+   `uq_application (job_id, candidate_id)` has no WHERE clause.
+3. Transitions: the brief has none. `TRANSITIONS` maps every status to the other three; the owning
+   employer may set any status other than the current one (T15).
+4. Another candidate's application: `Forbidden` (403); a missing one: `NotFound` (404) (D9).
+5. No resume on an application (D10): the resume is private to the candidate and is never shared
+   with the employer.
 
-DEFAULT (not in brief): duplicate gives `Conflict(...)` and HTTP 409 (the brief gives no code or
-message for FP-CAN-3 duplicates); cover note max 2000 chars; resume attached to an application
-(the brief's resume is private to the candidate, see T08 CONFLICT).
-
-CONFLICT (flagged, not changed): the brief gives `403` for another candidate's application
-(FP-AUTH-3, FP-SEC-1 boundary 1); Step 3 raises `NotFound`. See T06.
+DEFAULT (not in brief): the duplicate message is `Conflict("You have already applied to this
+job.")`, HTTP 409; cover note max 2000 chars.
 
 ## Owns
 - `app/applications/statuses.py`
@@ -48,42 +45,71 @@ CONFLICT (flagged, not changed): the brief gives `403` for another candidate's a
 
 ## May read
 - `CLAUDE.md`
-- `docs/plan/07-CONTRACTS.md` (sections: applications, jobs, candidates: resume)
+- `docs/plan/07-CONTRACTS.md` (sections: applications, jobs, scheduling)
 - `docs/plan/05-UX-FLOWS.md` (sections: Confirm application, Empty states)
-- `docs/plan/03-DATA-MODEL.md` (table: applications and its unique index)
-- `app/jobs/service.py`, `app/candidates/resume_service.py`, `app/audit.py`, `app/db.py`,
-  `app/errors.py`, `app/applications/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
+- `docs/plan/03-DATA-MODEL.md` (tables: applications and its unique index, bookings, interview_slots)
+- `app/jobs/service.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
+  `app/applications/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
 
 ## Contract
-The `applications` T14 parts of `07-CONTRACTS.md`. Routes: `applications.confirm` GET and
-`applications.submit` POST `/jobs/<int:job_id>/apply`, `applications.mine` GET
-`/candidate/applications`, all `@role_required("candidate")`.
+```python
+# app/applications/statuses.py
+STATUSES: tuple[str, ...] = ("pending", "interviewing", "rejected", "accepted")   # brief FP-EMP-3, stored lower-case
+TRANSITIONS: dict[str, tuple[str, ...]]   # every status -> the other three (brief has no transition rules)
+LABELS: dict[str, str]                    # "pending" -> "Pending", and so on
+
+# app/applications/service.py
+def apply(conn: Conn, candidate_id: int, job_id: int, cover_note: str) -> int
+    # NotFound if the job is missing; Conflict("You have already applied to this job.") for any
+    # existing application by this candidate to this job, whatever its status; no row in that case
+def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
+    # per row at least: id, job_id, job_title, company_name, status, created_at, booking
+    # where booking is None or {"slot_id", "starts_at", "ends_at"}
+def get_own_application(conn: Conn, candidate_id: int, application_id: int) -> dict
+    # NotFound if missing; Forbidden if another user's
+```
+Routes: `applications.confirm` GET and `applications.submit` POST `/jobs/<int:job_id>/apply`,
+`applications.mine` GET `/candidate/applications`, all `@role_required("candidate")`.
 
 ## Steps
 1. Tests first.
-2. `apply`: job must exist and be open (`get_job`; closed: `NotFound`). `resume_id`, if given, must
-   belong to the candidate (`list_resumes`; else `ValidationError({"resume": ...})`). Check for an
-   existing pending application first (friendly `Conflict`), then insert inside
-   `transaction(conn, immediate=True)` and also catch `sqlite3.IntegrityError` from the unique index
-   as the same `Conflict` (two clicks at once). Audit `application.submit`.
-3. `get_own_application`: by id and candidate id; else `NotFound`.
-4. `list_for_candidate`: one query joining jobs and companies, newest first.
-5. Confirm page uses `confirm_box`: the job and company, a resume select (or "No resume, apply without
-   one"), cover note, and "Shared with <company>: the selected resume, your name, your cover note.
-   Not shared: your email, your other applications." Primary button "Submit application".
+2. `apply`: job must exist (`get_job`; missing: `NotFound`). Validate the cover note. Check for any
+   existing application by this candidate to this job first (friendly `Conflict`), then insert
+   with status `pending` inside `transaction(conn, immediate=True)` and also catch
+   `sqlite3.IntegrityError` from `uq_application` as the same `Conflict` (two clicks at once).
+   Audit `application.submit`.
+3. `get_own_application`: `SELECT` by id; no row: `NotFound`; `candidate_id` differs: `Forbidden`.
+4. `list_for_candidate`: one query joining jobs and companies, plus one `LEFT JOIN bookings JOIN
+   interview_slots` (or a second query grouped in Python) so each row carries `booking`; newest
+   first.
+5. Confirm page uses `confirm_box`: the job and company, the cover note field, and "This will be
+   sent to <company>: your name, your skills, your cover note. Not shared: your resume, your email
+   address, your other applications." Primary button "Submit application".
 6. Submit: success redirects to `/candidate/applications` with flash "Application sent to <company>";
    `Conflict` re-renders the confirm page with the message and status 409.
-7. Mine page: table with job, company, date, status badge (`LABELS`), link to
+7. Mine page: table with job, company, date, status badge (`LABELS`), booking time when there is
+   one (via `format_local` in the candidate's profile timezone) or "No interview booked", link to
    `/candidate/applications/<id>` (T16 builds it).
 
 ## Tests (`tests/unit/test_can_apply.py`; remove the skip)
-- `test_fp_can_3_pending_duplicate_and_application_owner`: apply once works; second apply to the
-  same job gives `Conflict` and still one row; after setting the first to `rejected` with SQL, apply
-  again works (or what the brief says); candidate B cannot `get_own_application` A's (`NotFound`).
-- applying to a closed job: `NotFound`; to a missing job: 404 via the route
-- someone else's resume id rejected
-- the confirm page shows the company name and the privacy lines
-- employer POST to apply gives 403
+- `test_fp_can_3_pending_duplicate_and_application_owner`: apply once works and the row has status
+  `pending`; second apply to the same job gives `Conflict` and still one row; after setting the
+  first to `rejected` with SQL, apply again is still refused with `Conflict` and still one row;
+  candidate B calling `get_own_application` on A's raises `Forbidden`; a missing id raises
+  `NotFound`.
+- applying to a missing job: `NotFound` from the service and 404 via the route
+- `STATUSES == ("pending", "interviewing", "rejected", "accepted")`; `LABELS` gives the brief's
+  spellings; `TRANSITIONS[s]` is the other three for every `s`
+- `list_for_candidate` returns `booking None` without a booking and `{"slot_id", "starts_at",
+  "ends_at"}` after `make_booking`; the mine page shows the booking time
+- the confirm page shows the company name and the privacy lines, and no resume field
+- the route for a duplicate returns 409
+- employer POST to apply gives 403; candidate B GET `/candidate/applications/<A's id>` is 403 (T16's
+  route; include here only if T16 has merged, otherwise leave to T06)
 
 ## Done when
 - check and scope pass; then merge review
+
+## Pitfalls
+- An application never references a resume: the applications table has no resume column (D10).
+- The duplicate check is by `(job_id, candidate_id)` only; never filter by status.
diff --git a/docs/tasks/T15.md b/docs/tasks/T15.md
index e949188..c2ce9a7 100644
--- a/docs/tasks/T15.md
+++ b/docs/tasks/T15.md
@@ -2,11 +2,12 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | EMP + CAN + MATCH | T11, T14 | yes | **BLOCKED** on the T14 status-name decision and on the resume-access CONFLICT (rules quoted; order and fields SUPERSEDE the defaults; see Requirement) |
+| 3 | EMP + CAN + MATCH | T11, T14 | yes | READY (after T11, T14; statuses by D11, order by D15, codes by D9, no resume access by D10) |
 
 ## Goal
 An employer sees the applicants for one of their jobs, with the fields and order the brief requires,
-and moves an application through allowed statuses via a confirm screen.
+including each applicant's booking, and sets an application to any of the four statuses via a
+confirm screen. Changing a status never touches a booking.
 
 ## Requirement
 FP-EMP-3: applicant fields, order, status and role. Rule text (brief section "4. Employer
@@ -18,31 +19,24 @@ workflow", FP-EMP-3 "Applicant management"):
 Tie-breakers (brief section "5. Matching contract", FP-MATCH-1):
 > Sort by descending score. [...] break employer applicant ties by case-insensitive candidate display name and then stable candidate ID.
 
-SUPERSEDED by the quotes (old defaults were different):
-- Order: score high to low, then case-insensitive candidate display name, then candidate ID. The
-  old default "then `applied_at` oldest first, then `application_id`" is wrong.
-- Fields: each row must show "candidate identity, skills, match score, application status, and
-  interview booking (if any)". The old field list lacked the candidate's skills list and the booking.
-  The keys `list_applicants` returns, the list Step 2 and the test mean by "the listed keys":
-  `application_id`, `candidate_id`, `candidate_name`, `headline`, `skills` (the candidate's
-  normalised skill names, sorted), `score`, `matched`, `missing`, `status`, `applied_at`, `booking`
-  (the booked slot's `starts_at`/`ends_at` as a dict, or `None`), `resume_id`.
-  Of these the brief requires identity (`candidate_id`, `candidate_name`), `skills`, `score`,
-  `status` and `booking`; the exact key names and the extras `headline`, `matched`, `missing`,
-  `applied_at` are DEFAULT (not in brief).
-  CONFLICT (flagged, not changed): `resume_id`, and the resume link in Step 4, exist only so the
-  employer can open the candidate's resume. The brief (FP-CAN-1, "3. Candidate workflow") says
-  "Resume contents are private: only the owning candidate may read or modify them. Any other
-  candidate or employer **MUST** receive `403` through a direct URL/API request." Same CONFLICT as
-  T08; orchestrator decision.
-- Statuses: exactly `Pending`, `Interviewing`, `Rejected`, `Accepted` (see T14 CONFLICT).
-- Transitions: NOT IN BRIEF; "set an application to one of exactly these statuses". See T14.
-- Also FP-SCHED-2: "If a booked application later leaves `Interviewing`, its booking **MUST** remain
-  associated with the application and the slot **MUST** remain unavailable." So changing status
-  never touches bookings.
+Bookings survive status changes (brief section "6. Applications and interview scheduling",
+FP-SCHED-2, last sentence):
+> If a booked application later leaves `Interviewing`, its booking **MUST** remain associated with the application and the slot **MUST** remain unavailable.
 
-CONFLICT (flagged, not changed): the brief gives `403` for another employer ("manage applicants for
-another employer's posting", FP-EMP-2); Steps 2 and 3 use `get_owned_job` / `NotFound`. See T06.
+Decided:
+- Order (D15): score high to low, then `display_name.lower()`, then `candidate_id`.
+- Fields: `list_applicants` returns dicts with exactly these keys: `application_id`,
+  `candidate_id`, `candidate_name`, `headline`, `skills` (the candidate's normalised skill names,
+  `list[str]`, sorted), `score`, `matched`, `missing`, `status`, `applied_at`, `booking` (`None`
+  or `{"slot_id", "starts_at", "ends_at"}`). Of these the brief requires identity
+  (`candidate_id`, `candidate_name`), `skills`, `score`, `status` and `booking`; the exact key
+  names and the extras `headline`, `matched`, `missing`, `applied_at` are DEFAULT (not in brief).
+- No resume access (D10): the resume is private to the candidate. No resume key, no resume link.
+- Statuses (D11): exactly `pending`, `interviewing`, `rejected`, `accepted` (stored), shown as
+  `Pending`, `Interviewing`, `Rejected`, `Accepted`. No transition rules: `set_status` accepts any
+  status in `STATUSES` other than the current one.
+- Another employer's job or application: `Forbidden` (403); missing: `NotFound` (404) (D9).
+- Changing status never touches bookings.
 
 DEFAULT (not in brief): dates shown with `format_local` in UTC.
 
@@ -57,14 +51,22 @@ DEFAULT (not in brief): dates shown with `format_local` in UTC.
 - `CLAUDE.md`
 - `docs/plan/07-CONTRACTS.md` (sections: applications, matching, jobs)
 - `docs/plan/05-UX-FLOWS.md` (section: Applicants table)
+- `docs/plan/03-DATA-MODEL.md` (tables: applications, bookings, interview_slots)
 - `app/applications/statuses.py`, `app/matching/engine.py`, `app/jobs/service.py`,
   `app/timeutil.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
   `app/templates/components/*`, `tests/conftest.py`
 
 ## Contract
 ```python
-def list_applicants(conn, employer_id: int, job_id: int) -> list[dict]
-def set_status(conn, employer_id: int, application_id: int, new_status: str) -> None
+def list_applicants(conn: Conn, employer_id: int, job_id: int) -> list[dict]
+    # NotFound if the job is missing; Forbidden if another employer's. Each dict has exactly:
+    # application_id, candidate_id, candidate_name, headline, skills (list[str], sorted), score,
+    # matched, missing, status, applied_at, booking (None or {"slot_id", "starts_at", "ends_at"})
+    # sorted by score descending, then display_name.lower(), then candidate_id
+def set_status(conn: Conn, employer_id: int, application_id: int, new_status: str) -> None
+    # NotFound if missing; Forbidden if the application's job is another employer's;
+    # ValidationError({"status": ...}) unless new_status is in STATUSES and differs from the current
+    # one; never touches bookings
 ```
 Routes: `applications.applicants` GET `/employer/jobs/<int:job_id>/applicants`;
 `applications.confirm_status` GET and `applications.set_status` POST
@@ -73,23 +75,35 @@ field), all `@role_required("employer")`.
 
 ## Steps
 1. Tests first.
-2. `list_applicants`: `get_owned_job` first. One query for the applications with candidate name and
-   headline, one query for all those candidates' skills; score each with `engine.score` against the
-   job's skills; sort by the rule; return dicts with exactly the listed keys.
-3. `set_status`: load the application joined to its job's company; not the owner: `NotFound`.
-   `new_status` not in `TRANSITIONS[current]`: `ValidationError`. Update and audit
-   `application.status` with detail `"<old> -> <new>"`.
-4. Applicants page: table (fields above; date with `format_local` in UTC unless the brief says
-   otherwise), resume link to `/resumes/<id>` (CONFLICT: the brief gives employers `403` on resumes;
-   see Requirement), one link per allowed next status to the confirm page.
-5. Confirm-status page: `confirm_box` "Change <name>'s application from <old> to <new>?", POST form.
+2. `list_applicants`: `get_owned_job` first (`NotFound` / `Forbidden`). One query for the
+   applications with candidate name and headline, one query for all those candidates' skills, one
+   query for the bookings of those applications joined to `interview_slots` (so the query count
+   stays fixed); score each with `engine.score` against the job's skills; sort by
+   `(-score, candidate_name.lower(), candidate_id)`; return dicts with exactly the listed keys.
+3. `set_status`: load the application joined to its job's company; no row: `NotFound`; owner is not
+   `employer_id`: `Forbidden`. `new_status not in STATUSES` or equal to the current one:
+   `ValidationError({"status": ...})`. `UPDATE applications SET status = ?, updated_at = ?` only
+   (no statement touches `bookings`) and audit `application.status` with detail `"<old> -> <new>"`.
+4. Applicants page: table (fields above; date with `format_local` in UTC; booking shown as its
+   time or "No interview booked"), one link per other status to the confirm page. No resume link.
+5. Confirm-status page: `confirm_box` "Change <name>'s application from <Old> to <New>?" using
+   `LABELS`, POST form.
 
 ## Tests (`tests/unit/test_emp_applicants.py`; remove the skip)
 - `test_fp_emp_3_applicant_fields_order_status_and_role`: three applicants with different and equal
-  scores; keys are exactly the listed fields; order follows the rule including both ties; allowed
-  transition works and is audited; disallowed transition rejected; employer B gets `NotFound`;
-  candidate GET gives 403.
+  scores (two with the same score and names differing only by case, two with the same score and
+  the same name but different ids); keys are exactly the listed fields; order follows the rule
+  including both ties; a job with no required skills gives every applicant 100; `booking` is
+  `None` without a booking and the dict with `slot_id`, `starts_at`, `ends_at` after `make_booking`;
+  every status change to a different status works and is audited (`pending` to `accepted`,
+  `accepted` to `pending`, `interviewing` to `rejected`); setting the current status again raises
+  `ValidationError`; an unknown status raises `ValidationError`; employer B gets `Forbidden` for
+  both `list_applicants` and `set_status`; a missing job and a missing application give
+  `NotFound`; candidate GET gives 403.
+- after `make_booking` on an `interviewing` application, `set_status` to `rejected` leaves the
+  booking row unchanged and the slot still booked (FP-SCHED-2)
 - query count stays fixed for 30 applicants (`set_trace_callback`)
+- the applicants page shows no resume link and shows the booking time for a booked applicant
 
 ## Done when
 - check and scope pass; then merge review

```
