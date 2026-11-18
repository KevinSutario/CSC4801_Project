# Review packet CC01 (5 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/tasks/T08.md, docs/tasks/T09.md, docs/tasks/T10.md

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
diff --git a/docs/tasks/T08.md b/docs/tasks/T08.md
index bf4c88a..fe403c2 100644
--- a/docs/tasks/T08.md
+++ b/docs/tasks/T08.md
@@ -1,29 +1,26 @@
-# T08 Â· Resume upload, list, delete, private download
+# T08 Â· Raw-text resume: view, replace, owner-only
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | CAN | T07 | no | **BLOCKED**: rule quoted, but the card's design contradicts it (see CONFLICT); orchestrator decision needed |
+| 2 | CAN | T07 | no | READY (after T07; design decided by D10, codes by D9) |
 
 ## Goal
-A candidate can upload a resume, see and delete their resumes, and download them. Nobody else can,
-except as the brief allows.
+A candidate can enter a raw-text resume, see it, and replace it. Only the owner can read it: any
+other candidate or employer who requests it by direct URL gets 403.
 
 ## Requirement
 FP-CAN-1 (private resume rules). Rule text (brief section "3. Candidate workflow", FP-CAN-1
 "Candidate profile and resume", second paragraph):
 > A candidate **MUST** be able to enter a raw-text resume. The application **MUST** persist the text and allow the owner to view and replace it. PDF upload and extraction are optional. Resume contents are private: only the owning candidate may read or modify them. Any other candidate or employer **MUST** receive `403` through a direct URL/API request.
 
-CONFLICT (three points; orchestrator decision needed; Steps and Tests below are unchanged):
-1. The required resume is raw text that the owner can view and replace. This card builds PDF upload
-   only, which the brief calls optional. No card builds a raw-text resume.
-2. The brief gives no employer any access ("only the owning candidate may read or modify them").
-   The old default let an employer with an application open it, and the FP-CAN-1 test bullet expects
-   that employer to get 200. The brief says that employer gets `403`.
-3. The refusal code is `403`. The card returns 404 (`NotFound`) "so ids cannot be probed".
+FP-SEC-3 applies to the rendered text (brief section "7. Security requirements", FP-SEC-3
+"Cross-site scripting"):
+> User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML.
 
-DEFAULT (not in brief), only relevant if the optional PDF upload is kept: PDF only (extension
-`.pdf` and content starting with `%PDF-`), size limit `MAX_UPLOAD_MB`, at most 5 resumes per
-candidate.
+Decided (D10): the resume is raw text, one row per candidate (`resumes.owner_id` is the primary
+key), replaced in place. No PDF upload is built. No employer has any access.
+
+DEFAULT (not in brief): `RESUME_MAX_CHARS = 20000` after strip.
 
 ## Owns
 - `app/candidates/resume_service.py`
@@ -33,56 +30,68 @@ candidate.
 
 ## May read
 - `CLAUDE.md`
-- `docs/plan/04-AUTH-SECURITY.md` (section: File uploads)
+- `docs/plan/04-AUTH-SECURITY.md` (sections: Authorization, Resumes)
 - `docs/plan/07-CONTRACTS.md` (sections: candidates: resume)
-- `docs/plan/03-DATA-MODEL.md` (tables: resumes, applications, jobs, companies)
+- `docs/plan/03-DATA-MODEL.md` (table: resumes)
 - `app/audit.py`, `app/db.py`, `app/errors.py`, `app/security.py`, `app/candidates/__init__.py`,
   `app/candidates/profile_service.py`, `app/templates/components/*`, `tests/conftest.py`
 
 ## Contract
 ```python
-def save_resume(conn, upload_dir: str, owner_id: int, file) -> int
-def list_resumes(conn, owner_id: int) -> list[dict]
-def delete_resume(conn, upload_dir: str, owner_id: int, resume_id: int) -> None
-def can_view_resume(conn, viewer_id: int, viewer_role: str, resume_id: int) -> bool
-def get_resume_for_download(conn, viewer_id: int, viewer_role: str, resume_id: int) -> dict
+def get_resume(conn: Conn, owner_id: int) -> dict | None      # keys: owner_id, body, updated_at
+def save_resume(conn: Conn, owner_id: int, body: str) -> None
+    # strip; ValidationError({"body": ...}) if empty or over RESUME_MAX_CHARS; upsert; audit resume.update
+def get_resume_for_viewer(conn: Conn, viewer_id: int, candidate_id: int) -> dict
+    # Forbidden unless viewer_id == candidate_id; then NotFound if that candidate has no resume
+RESUME_MAX_CHARS: int = 20000     # DEFAULT (not in brief)
 ```
-Routes: `candidates.resume` GET/POST `/candidate/resume` (candidate only),
-`candidates.resume_delete` POST `/candidate/resume/<int:resume_id>/delete` (candidate only),
-`candidates.resume_download` GET `/resumes/<int:resume_id>` (any signed-in user; access checked).
+Routes: `candidates.resume` GET/POST `/candidate/resume` (`@login_required`,
+`@role_required("candidate")`: shows the current text in a textarea, POST replaces it);
+`candidates.resume_view` GET `/candidates/<int:candidate_id>/resume` (`@login_required`, any role:
+the owner sees their text, anyone else gets 403 through `get_resume_for_viewer`).
+Template: `candidates/resume.html` only.
 
 ## Steps
 1. Tests first.
-2. `save_resume`: no file or empty name: `ValidationError({"resume": "Choose a PDF file."})`.
-   Check extension lower-cased, read the first 5 bytes (`file.stream.read(5)` then `seek(0)`),
-   check count limit. Stored name `secrets.token_hex(16) + ".pdf"`, path
-   `os.path.join(upload_dir, stored_name)`. Save, then insert the row in a transaction with
-   `os.path.getsize`. If the insert fails, delete the file. Audit `resume.upload`.
-3. `delete_resume`: owner only (else `NotFound`); delete row in a transaction, then the file
-   (ignore a missing file). Audit `resume.delete`.
-4. `can_view_resume` and `get_resume_for_download`: rules above, in SQL with `?` placeholders.
-   Missing or not allowed: `NotFound` (404, so ids cannot be probed).
-5. Download route: `send_file(path, as_attachment=True, download_name=<secure_filename of original
-   name or "resume.pdf">, mimetype="application/pdf")`.
-6. Over-size uploads: Flask raises 413 before the route runs; the 413 error page handles it.
-7. Page: upload form (`enctype="multipart/form-data"`), list with name, size, date, download and
-   delete (delete is a POST form with `csrf_field()`). Privacy line: "Only you and employers you
-   apply to can open your resume."
+2. `get_resume`: `SELECT owner_id, body, updated_at FROM resumes WHERE owner_id = ?`; `dict(row)` or
+   `None`.
+3. `save_resume`: `body.strip()`; empty gives `ValidationError({"body": "Enter your resume."})`,
+   longer than `RESUME_MAX_CHARS` gives `ValidationError({"body": "Resume is too long (max 20000
+   characters)."})`. In one transaction: `INSERT INTO resumes (owner_id, body, updated_at) VALUES
+   (?, ?, ?) ON CONFLICT(owner_id) DO UPDATE SET body = excluded.body, updated_at =
+   excluded.updated_at`, then `audit.log_event(conn, owner_id, "resume.update", "resume",
+   owner_id)`.
+4. `get_resume_for_viewer`: the ownership check comes first, in Python, with no query:
+   `if viewer_id != candidate_id: raise Forbidden`. Then `get_resume`; `None` raises `NotFound`.
+   (Order matters: another user must get 403 even when the target has no resume, so ids cannot be
+   probed for "has a resume".)
+5. `candidates.resume` GET: render the page with the current text (empty textarea if none) and
+   `updated_at`. POST: `save_resume`; on `ValidationError` re-render with the error and the typed
+   text, status 400; on success flash "Resume saved" and redirect to `candidates.resume`.
+6. `candidates.resume_view` GET: `get_resume_for_viewer(conn, g.user["id"], candidate_id)`, render
+   the same template in read-only mode (`<pre>` or a `white-space: pre-wrap` block; the text goes
+   through Jinja autoescape, never `|safe`).
+7. Page: textarea named `body`, `csrf_field()`, a "Save resume" button, the privacy line
+   "Only you can read this resume." and, below the form, the current text rendered escaped.
 
 ## Tests (`tests/unit/test_can_resume.py`; remove the skip on the template test)
 - `test_fp_can_1_profile_and_private_resume_rules`: profile saved (through `profile_service`);
-  PDF upload works; `.txt` rejected; a file named `.pdf` without `%PDF-` rejected; owner can
-  download (200, `Content-Disposition: attachment`); another candidate gets 404; an unrelated
-  employer gets 404; an employer whose job has an application with this resume gets 200 (create the
-  application with `make_application` and SQL to set `resume_id`).
-- upload over the size limit returns 413 (set `MAX_UPLOAD_MB` small in a test app)
-- delete removes the row and the file; deleting someone else's gives 404
-- stored file name is never the uploaded name; `../../evil.pdf` as a name is stored safely
-- sixth resume rejected
+  `save_resume` then `get_resume` returns the text; saving again overwrites (still one row in
+  `resumes`); empty body and `RESUME_MAX_CHARS + 1` chars raise `ValidationError` on `body` and
+  change nothing; owner GET `/candidates/<own id>/resume` is 200 and shows the text escaped;
+  another candidate GET gives 403; an employer GET gives 403; owner with no resume GET gives 404;
+  a body of `<script>alert(1)</script>` is rendered as `&lt;script&gt;` and the raw tag never
+  appears in the response (FP-SEC-3).
+- `get_resume_for_viewer` with another user's id raises `Forbidden` even when that user has no
+  resume
+- POST `/candidate/resume` via `csrf_post` saves and redirects with a flash; an employer session
+  POST gives 403; signed out GET redirects to login
+- an audit row `resume.update` exists after a save
 
 ## Done when
 - check and scope pass
 
 ## Pitfalls
-- Never build a path from `original_name`.
-- Never put uploads under `static/`.
+- Never use `|safe` or `Markup()` on the resume text.
+- No file is written anywhere. `UPLOAD_DIR` exists in config but this task does not use it.
+- `Forbidden` before `NotFound` in `get_resume_for_viewer` (step 4).
diff --git a/docs/tasks/T09.md b/docs/tasks/T09.md
index fff230c..bf8a85f 100644
--- a/docs/tasks/T09.md
+++ b/docs/tasks/T09.md
@@ -15,8 +15,9 @@ profile"):
 DEFAULT (not in brief): the brief sets no limits and names only "company name and description".
 Keep: name required, 1 to 120 chars; industry max 80; location max 80; website optional, if given
 must start with `https://` or `http://` and be max 200 chars; description max 4000.
-Escaping of company text is also required by FP-SEC-3 (brief section "7. Security requirements"):
-> User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML.
+Escaping of company text is also required by FP-SEC-3 (brief section "7. Security requirements",
+FP-SEC-3 "Cross-site scripting"); this card owns the FP-SEC-3 unit test:
+> User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML. If the design intentionally supports formatted HTML, it **MUST** use an allow-list sanitizer. At least one unit test **MUST** pass `<script>alert(1)</script>` to the rendering or sanitization logic and verify that it is not emitted as executable markup.
 
 ## Owns
 - `app/employers/service.py`
@@ -56,7 +57,10 @@ Routes: `employers.home` GET `/employer/`, `employers.company` GET/POST `/employ
 - `javascript:alert(1)` as website rejected
 - candidate GET `/employer/company` gives 403
 - POST through the form works and redirects with a flash
-- a name with `<script>` is shown escaped on the page
+- `test_fp_sec_3_script_tag_is_escaped` (FP-SEC-3): save a company whose name and description are
+  both `<script>alert(1)</script>`; GET `/employer/company` and GET `/employer/` render them as
+  `&lt;script&gt;alert(1)&lt;/script&gt;` and the raw string `<script>alert(1)</script>` never
+  appears in either response body
 
 ## Done when
 - check and scope pass
diff --git a/docs/tasks/T10.md b/docs/tasks/T10.md
index 3838073..6777f91 100644
--- a/docs/tasks/T10.md
+++ b/docs/tasks/T10.md
@@ -1,12 +1,13 @@
-# T10 Â· Jobs: create, edit, close, delete, detail
+# T10 Â· Jobs: create, edit, delete, detail
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | EMP | T09 | no | **BLOCKED** (NEEDS DECISION, same as the FP-EMP-2 row in `01-REQUIREMENTS.md`): Step 7 and the FP-EMP-2 test bullet still describe cascade delete, but the brief says deletion with dependents "**MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged"; Step 4 and the test bullet give `NotFound` (404) where the brief says the other employer "**MUST** receive `403`"; and "closed" jobs are a CONFLICT with FP-CAN-2 (see Requirement). The orchestrator decides and rewrites those lines before dispatch |
+| 2 | EMP | T09 | no | READY (after T09; rules quoted from the brief; deletion decided by D12, codes by D9, no closed state by D18; limits are DEFAULT (not in brief)) |
 
 ## Goal
-An employer can post, edit, close and delete jobs with required skills. Anyone signed in can view
-an open job's detail page.
+An employer can post, edit and delete jobs with a required-skills list that may be empty. Deleting
+a job that has applications is refused with 409 and changes nothing. Anyone signed in can view any
+job's detail page.
 
 ## Requirement
 FP-EMP-2: job validation and deletion. Rule text (brief section "4. Employer workflow", FP-EMP-2
@@ -15,28 +16,22 @@ FP-EMP-2: job validation and deletion. Rule text (brief section "4. Employer wor
 >
 > A job with no applications or interview slots **MUST** be deletable. If either kind of dependent record exists, deletion **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged.
 
-SUPERSEDED by the quote (the old defaults said the opposite):
-- Skills: "the list may be empty". The old default "skills 1 to 30" is wrong; a job with no skills
-  is valid. (FP-MATCH-1 scores such a job 100 for every candidate.)
-- Delete: no cascade. If any application or interview slot exists, deletion fails with
-  `409 Conflict` and changes nothing. Overrides Step 7's "confirm-delete page that states what else is
-  deleted" and the test bullet "delete removes it plus its applications and slots". The orchestrator
-  should rewrite those lines; they are left as written here, which is why the card is BLOCKED rather
-  than READY (a card whose Steps and Tests contradict its quoted rule is not buildable).
-
-CONFLICT (flagged, not changed): the brief says another employer gets `403`; Step 4 raises
-`NotFound` (404). See T06.
+Decided:
+- Skills: "the list may be empty". A job with no skills is valid (FP-MATCH-1 scores it 100 for every
+  candidate). Skills 0 to 30 (30 is DEFAULT (not in brief)).
+- Delete (D12): no cascade. If the job has any application, `delete_job` raises `Conflict` (HTTP
+  409) and changes nothing. Interview slots belong to the employer, not to a job (D13), so
+  applications (and their bookings) are a job's only dependants. `applications.job_id` is
+  `ON DELETE RESTRICT` as the backstop.
+- Another employer's job: `Forbidden` (403) for edit, delete and applicants; a missing job is
+  `NotFound` (404) (D9).
+- No closed state (D18): jobs have no open/closed flag. Every job that exists is current and is
+  listed to candidates (FP-CAN-2 "all current (not deleted) jobs").
 
 DEFAULT (not in brief): title max 120 chars; description max 5000; location max 80; employment type
 one of `EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "internship")`; salary min and max
 optional whole numbers from 0 to 10_000_000, min <= max; at most 30 skills.
 
-CONFLICT (flagged, not changed): "closed" jobs. FP-CAN-2 (brief section "3. Candidate workflow")
-says the candidate dashboard "**MUST** list all current (not deleted) jobs". A closed job is not
-deleted, so the brief requires it to be listed; this card's close feature, `list_open_jobs`, the
-Contract line "a closed job is 404 unless the viewer owns it" and the test bullets "excludes closed
-jobs" and "detail of a closed job: ... other users 404" hide it. See T13. Orchestrator decision.
-
 ## Owns
 - `app/jobs/service.py`
 - `app/jobs/routes.py`
@@ -46,40 +41,82 @@ jobs" and "detail of a closed job: ... other users 404" hide it. See T13. Orches
 ## May read
 - `CLAUDE.md`
 - `docs/plan/07-CONTRACTS.md` (sections: jobs, employers, `app/skills.py`)
-- `docs/plan/03-DATA-MODEL.md` (tables: jobs, job_skills, companies, applications, interview_slots)
+- `docs/plan/03-DATA-MODEL.md` (tables: jobs, job_skills, companies, applications)
 - `docs/plan/05-UX-FLOWS.md` (screen list rows for jobs)
 - `app/employers/service.py`, `app/skills.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
   `app/jobs/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
 
 ## Contract
-The `jobs` section of `07-CONTRACTS.md`, exactly. Every employer route is
-`@role_required("employer")`. `jobs.detail` is `@login_required`; a closed job is 404 unless the
-viewer owns it.
+```python
+def create_job(conn: Conn, employer_id: int, title: str, description: str, location: str,
+               employment_type: str, salary_min: str, salary_max: str, skills_text: str) -> int
+def update_job(conn: Conn, employer_id: int, job_id: int, title: str, description: str,
+               location: str, employment_type: str, salary_min: str, salary_max: str,
+               skills_text: str) -> None
+    # NotFound if missing; Forbidden if another employer's
+def delete_job(conn: Conn, employer_id: int, job_id: int) -> None
+    # NotFound if missing; Forbidden if another employer's; Conflict if the job has any application;
+    # deletes nothing in that case
+def count_dependants(conn: Conn, job_id: int) -> int    # number of applications on the job
+def get_owned_job(conn: Conn, employer_id: int, job_id: int) -> dict
+    # NotFound if missing; Forbidden if another user's
+def get_job(conn: Conn, job_id: int) -> dict    # with company_name, skills; NotFound if missing
+def list_jobs_for_employer(conn: Conn, employer_id: int) -> list[dict]
+def list_jobs(conn: Conn) -> list[dict]         # every job with company_name and skills
+EMPLOYMENT_TYPES: tuple[str, ...]
+```
+Routes: `jobs.my_jobs` GET `/employer/jobs`; `jobs.new` GET, POST `/employer/jobs/new`; `jobs.edit`
+GET, POST `/employer/jobs/<int:job_id>/edit`; `jobs.confirm_delete` GET and `jobs.delete` POST
+`/employer/jobs/<int:job_id>/delete`; `jobs.detail` GET `/jobs/<int:job_id>`. Every employer route
+is `@role_required("employer")`. `jobs.detail` is `@login_required` and shows any job.
 
 ## Steps
 1. Tests first.
 2. A private `_validate(...)` returns cleaned values or raises `ValidationError` with all field
    errors. Salary: empty string means None; otherwise `int()` inside `try`; reject non-numbers.
+   `parse_skill_list` may return an empty list; that is valid.
 3. `create_job`: employer must have a company (`ValidationError({"company": "Create your company
    profile first."})`). Insert job and `job_skills` in one transaction. Audit `job.create`.
-4. `get_owned_job`: select where `jobs.id = ? AND companies.owner_id = ?`; none: `NotFound`.
-5. `update_job`, `delete_job`: use `get_owned_job` first. Audit `job.update`, `job.delete`.
-6. `list_open_jobs`: one query for jobs with company name, one query for all their skills, then group
-   in Python (no query per job).
-7. Routes and templates: list (with empty state), form (new and edit share `jobs/form.html`), a
-   confirm-delete page that states what else is deleted (counts of applications and slots), detail
-   page with skills as badges and a link "Apply to this job" to `/jobs/<id>/apply` (T14 builds it).
+4. `get_owned_job`: `SELECT ... FROM jobs JOIN companies ... WHERE jobs.id = ?`; no row: `NotFound`;
+   row whose `companies.owner_id != employer_id`: `Forbidden`.
+5. `update_job`: `get_owned_job` first; replace `job_skills`. Audit `job.update`.
+6. `count_dependants`: `SELECT COUNT(*) FROM applications WHERE job_id = ?`.
+7. `delete_job`: `get_owned_job` first; `count_dependants(conn, job_id) > 0` raises
+   `Conflict("This job has applications and cannot be deleted.")` (message is DEFAULT (not in
+   brief)) before any write; else delete inside a transaction (`job_skills` cascade), audit
+   `job.delete`. Catch `sqlite3.IntegrityError` from the RESTRICT backstop and raise the same
+   `Conflict`.
+8. `list_jobs`: one query for jobs with company name, one query for all their skills, then group in
+   Python (no query per job). `list_jobs_for_employer` the same, filtered by owner.
+9. Routes and templates: list (with empty state), form (new and edit share `jobs/form.html`), a
+   confirm-delete page that says either "This job has no applications and can be deleted" with the
+   delete button, or "This job has N applications and cannot be deleted" with no delete button;
+   `jobs.delete` POST on a job with applications returns 409 (let `Conflict` reach the error
+   handler, or re-render the confirm page with status 409); detail page with skills as badges (or
+   "No specific skills required") and a link "Apply to this job" to `/jobs/<id>/apply` (T14 builds
+   it).
 
 ## Tests (`tests/unit/test_emp_jobs.py`; remove the skip on the template test)
-- `test_fp_emp_2_job_validation_and_deletion`: parametrised invalid inputs each give the right field
-  error and no row; a valid job saved with normalised skills; delete removes it plus its
-  applications and slots; employer B deleting employer A's job gets `NotFound` and nothing is deleted.
+- `test_fp_emp_2_job_validation_and_deletion`: parametrised invalid inputs (empty title, empty
+  description, over-long fields, bad salary, min > max, 31 skills) each give the right field error
+  and no row; a valid job saved with normalised skills; a job with an empty skills list is saved
+  with no `job_skills` rows; delete removes a job with no applications (and its `job_skills`);
+  delete of a job with an application raises `Conflict`, and afterwards the job row, its skills and
+  its applications are unchanged (count and values); employer B deleting or editing employer A's
+  job gets `Forbidden` and nothing changes; a missing job gets `NotFound`.
 - no company yet: create gives the company error
-- `list_open_jobs` excludes closed jobs and includes skills for each
-- `list_open_jobs` runs a fixed number of queries no matter how many jobs (use
+- `list_jobs` includes every job with its skills (including a job with none)
+- `list_jobs` runs a fixed number of queries no matter how many jobs (use
   `conn.set_trace_callback` to count; 50 jobs, at most 3 queries)
-- detail of a closed job: owner 200, other users 404; missing job 404
+- detail of any job: owner 200, another employer 200, a candidate 200; missing job 404
+- `jobs.delete` POST for a job with an application returns 409 and the job still exists; employer
+  B POST gives 403
+- the confirm-delete page shows "cannot be deleted" and no delete button when applications exist
 - candidate POST to `/employer/jobs/new` gives 403
 
 ## Done when
 - check and scope pass
+
+## Pitfalls
+- Do not import `app.applications` (another lane); count applications with your own SQL.
+- `Forbidden` is for a job that exists and is not theirs; `NotFound` only when there is no row.

```
