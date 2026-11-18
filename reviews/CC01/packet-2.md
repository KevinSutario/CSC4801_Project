# Review packet CC01 (2 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/plan/04-AUTH-SECURITY.md, docs/plan/05-UX-FLOWS.md

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
diff --git a/docs/plan/04-AUTH-SECURITY.md b/docs/plan/04-AUTH-SECURITY.md
index 6ce5edc..eeb3c9d 100644
--- a/docs/plan/04-AUTH-SECURITY.md
+++ b/docs/plan/04-AUTH-SECURITY.md
@@ -9,7 +9,7 @@ marks. This file is the spec, and it doubles as the checklist every reviewer use
 |---|---|
 | Accounts | email + password + role (`candidate` or `employer`), chosen at sign-up |
 | Password hashing | `werkzeug.security.generate_password_hash(password)` (salted, scrypt by default). Verify with `check_password_hash`. Never store or log the password. |
-| Password rules | from the brief; default minimum 8 characters, maximum 128 |
+| Password rules | minimum 8 characters, maximum 128, DEFAULT (not in brief) |
 | Email | stripped and lower-cased; basic format check; unique (case-insensitive) |
 | Sign-up errors | field messages, HTTP 400, form refilled except password |
 | Duplicate email | same generic message as other errors where the brief allows, to limit account probing |
@@ -17,20 +17,25 @@ marks. This file is the spec, and it doubles as the checklist every reviewer use
 | Sign in | `session.clear()` first (stops session fixation), then set values and a new CSRF token |
 | Sign out | POST only, with CSRF. `session.clear()`. |
 | Cookie flags | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, `SESSION_COOKIE_SECURE` on when served over HTTPS |
-| Session lifetime | from the brief; default `PERMANENT_SESSION_LIFETIME` 8 hours |
+| Session lifetime | `PERMANENT_SESSION_LIFETIME` 8 hours, DEFAULT (not in brief) |
 | Brute force | per email and per IP: 5 failed logins in 10 minutes blocks the next try for 10 minutes (in-memory dict, fine for one process). Message does not say whether the email exists. |
 | Current user | `security.load_user` runs before every request: reads `session["user_id"]`, loads the row, puts it on `g.user`. A deleted user means the session is cleared. |
 
 ## Authorization
 
-- `@login_required`: no user, redirect to sign-in (GET) or 401 (POST).
-- `@role_required("employer")` or `("candidate")`: wrong role gives 403.
+The response contract is the brief's FP-AUTH-3 (D9):
+
+- Signed out: `@login_required` redirects to sign-in on GET and returns 401 on every other method.
+- Wrong role: `@role_required("employer")` or `("candidate")` gives 403.
 - **Object ownership is checked in the service, every time**, with the actor id passed in.
   Never trust an id from the form or URL on its own.
-- Missing object gives 404. Another user's object gives 403 or 404, as the brief says
-  (FP-AUTH-3). Until the brief says otherwise, use **404** for both, so ids cannot be probed.
+- Every ownership helper raises `NotFound` (404) when the row does not exist and `Forbidden` (403)
+  when it exists but belongs to someone else. Brief FP-AUTH-3: "authenticated user with the wrong
+  role or owner: `403 Forbidden`"; "missing object that the caller would otherwise be allowed to
+  access: `404 Not Found`". The same rule is repeated in FP-CAN-1 (resume) and FP-EMP-2 (jobs).
 - Ownership helpers (in services): `get_owned_job(conn, employer_id, job_id)`,
-  `get_owned_slot(...)`, `get_own_application(...)`, `can_view_resume(conn, viewer, resume_id)`.
+  `delete_slot(conn, employer_id, slot_id)`, `get_own_application(conn, candidate_id,
+  application_id)`, `get_resume_for_viewer(conn, viewer_id, candidate_id)`.
 
 ## Request security
 
@@ -49,22 +54,17 @@ marks. This file is the spec, and it doubles as the checklist every reviewer use
 | Mass assignment | Services take named fields only. Never `**request.form`. `role` is never editable after sign-up. |
 | Integer ids | Route converters `<int:job_id>`, so non-numbers give 404. |
 
-## File uploads (resumes)
+## Resumes
 
-- `MAX_CONTENT_LENGTH` set from `MAX_UPLOAD_MB`; larger uploads give 413 with a friendly page.
-- Allowed types from the brief; default PDF only. Check the extension **and** the first bytes
-  (`%PDF-`).
-- Stored as `secrets.token_hex(16) + ".pdf"` under `UPLOAD_DIR`, outside `static/`.
-- `original_name` is for display only. It passes through `werkzeug.utils.secure_filename` and is
-  never used as a path.
-- Download route checks `can_view_resume`, then `send_file(path, as_attachment=True,
-  download_name=original_name, mimetype="application/pdf")`.
-- Deleting a resume removes the row and the file.
+- The resume is raw text in `resumes.body` (brief FP-CAN-1, D10): one per candidate, owner-only,
+  no file is ever written from user input.
+- Only the owner may read or replace it; every other user (candidate or employer) gets 403 by
+  direct URL through `get_resume_for_viewer`. It is rendered escaped by Jinja autoescape (FP-SEC-3).
 
 ## Data privacy
 
-- A resume is private to its owner, plus anyone the brief allows (likely the employer of a job
-  the candidate applied to).
+- A resume is private to its owner only (brief FP-CAN-1: "only the owning candidate may read or
+  modify them").
 - Employers see applicants only for their own jobs.
 - The audit log never stores passwords, tokens or file contents.
 - Demo data uses fake people and companies only.
@@ -74,10 +74,11 @@ marks. This file is the spec, and it doubles as the checklist every reviewer use
 1. Every new route has `@login_required` and the right `@role_required`, or a written reason why not.
 2. Every POST form includes `csrf_field()`. No route skips the CSRF check.
 3. Every service that loads an object by id also checks the actor owns it or may see it.
-4. Missing and not-yours both give the agreed status code. Try an id that belongs to another user.
+4. A missing object gives 404 and another user's object gives 403 (FP-AUTH-3, D9). Try an id that
+   belongs to another user and an id that does not exist.
 5. All SQL uses `?` placeholders. Search the diff for `f"`, `.format(`, `%` and `+` near `execute`.
 6. No `|safe`, `Markup(` or `autoescape false` on anything a user typed.
-7. Uploads: size cap, type check by content, random stored name, served only via the checked route.
+7. No file is ever written from user input.
 8. Redirects use `url_for`, or a `next` value that passes the safe-redirect check.
 9. No secret, password, token or traceback appears in logs, flash messages, audit detail or HTML.
 10. Error responses use the error templates, with the right status code.
diff --git a/docs/plan/05-UX-FLOWS.md b/docs/plan/05-UX-FLOWS.md
index aab0f17..5864ab4 100644
--- a/docs/plan/05-UX-FLOWS.md
+++ b/docs/plan/05-UX-FLOWS.md
@@ -10,8 +10,7 @@ Screens follow the Keystone design canvas (web-only cut). The canvas ID in brack
    change an applicant's status, delete a job, book a slot) goes through a **confirm screen**
    showing exactly what will happen, to whom, and what will be shared.
 2. **Explain every score.** A match score always shows which skills matched and which did not.
-3. **Private by default.** Say plainly who can see what ("Only you and employers you apply to can
-   open this resume").
+3. **Private by default.** Say plainly who can see what ("Only you can read this resume").
 4. **Plain, short words.** Sentence case. Verb-first buttons: "Save profile", "Apply to this job".
 5. **Every list has an empty state** that tells the user what to do next.
 
@@ -27,15 +26,15 @@ Screens follow the Keystone design canvas (web-only cut). The canvas ID in brack
 
 ```
 Landing [P01] -> Create account [P02] (role = candidate)
-  -> Profile [C22/C03]: headline, location, timezone, summary, skills (comma separated)
-  -> Upload resume [C01] (PDF, private)
+  -> Profile [C22/C03]: display name, headline, location, timezone, summary, skills (comma separated)
+  -> Resume [C01] (raw text, private to you)
   -> Today [C06]: profile completeness, top 3 recommendations, application statuses
-  -> Recommendations [C07]: every open job, ranked, each with score + matched / missing skills
+  -> Recommendations [C07]: every job, ranked, each with score + matched / missing skills
   -> Job detail [C08]: full job, company card, "Apply to this job"
-  -> Confirm application [C11]: shows job, resume to be shared, cover note -> Submit
-  -> Applications [C12]: list with status badges
+  -> Confirm application [C11]: shows job, what will be shared, cover note -> Submit
+  -> Applications [C12]: list with status badges and booking time where there is one
   -> Application detail: status; if eligible, list of open slots in her timezone
-  -> Confirm booking -> Booked (or conflict message per brief)
+  -> Confirm booking -> Booked (or "Slot already booked", 409)
 ```
 
 ## Journey: employer
@@ -45,10 +44,11 @@ Landing -> Create account (role = employer)
   -> Company [R03 area]: name, industry, location, website, description
   -> Jobs [R03]: list, "Post a job"
   -> New job [R05]: title, description, location, type, salary range, skills
-  -> Job applicants [R06/R10]: applicants in the brief's order, each with match score, skills,
-     resume link, status; actions per allowed status change
+  -> Job applicants [R06/R10]: applicants sorted by score, each with match score, skills,
+     status, booking (if any); set any of the four statuses
   -> Confirm status change -> Updated
-  -> Interview slots [R13]: add slot (date, start, end, timezone), list, delete unbooked slot
+  -> Interview slots [R13] (from the employer home, `/employer/slots`): add a 30-minute slot
+     (date, start, end, timezone), list, delete unbooked slot
 ```
 
 ## Screen list
@@ -60,7 +60,7 @@ Landing -> Create account (role = employer)
 | Sign in | `GET/POST /auth/login` | `auth/login.html` | T05 | P02 |
 | Candidate Today | `GET /candidate/` | `candidates/today.html` | T07 | C06 |
 | Candidate profile | `GET/POST /candidate/profile` | `candidates/profile.html` | T07 | C22 |
-| Resume upload and list | `GET/POST /candidate/resume` | `candidates/resume.html` | T08 | C01 |
+| Resume (view and replace) | `GET/POST /candidate/resume`, `GET /candidates/<id>/resume` | `candidates/resume.html` | T08 | C01 |
 | Recommendations | `GET /candidate/recommendations` | `matching/recommendations.html` | T13 | C07 |
 | Job detail | `GET /jobs/<id>` | `jobs/detail.html` | T10 | C08 |
 | Confirm application | `GET /jobs/<id>/apply` | `applications/confirm.html` | T14 | C11 |
@@ -72,7 +72,7 @@ Landing -> Create account (role = employer)
 | New or edit job | `GET/POST /employer/jobs/new`, `/employer/jobs/<id>/edit` | `jobs/form.html` | T10 | R05 |
 | Confirm job delete | `GET /employer/jobs/<id>/delete` | `jobs/confirm_delete.html` | T10 | none |
 | Applicants | `GET /employer/jobs/<id>/applicants` | `applications/applicants.html` | T15 | R06, R10 |
-| Interview slots | `GET/POST /employer/jobs/<id>/slots` | `scheduling/slots.html` | T12 | R13 |
+| Interview slots | `GET/POST /employer/slots` | `scheduling/slots.html` | T12 | R13 |
 | Activity log | `GET /activity` | `activity/list.html` | T18 | A02 |
 | Errors | 400, 403, 404, 405, 409, 413, 500 | `errors/<code>.html` | T03 | none |
 
@@ -80,19 +80,18 @@ Landing -> Create account (role = employer)
 
 **Recommendations card** (FP-CAN-2): job title, company name, location, employment type, salary
 range (or "Not stated"), score shown as a number plus a 5-segment bar, "Matched: Python, SQL",
-"Missing: dbt". Every open job appears, including weak matches, unless the brief says otherwise.
-Ranking and tie-breaks come from the brief only.
+"Missing: dbt". Every job appears, including weak matches (brief FP-CAN-2: "all current (not
+deleted) jobs"; there is no closed state, D18). Ranking and tie-breaks are the brief's FP-MATCH-1.
 
 **Applicants table** (FP-EMP-3): candidate name, headline, match score, matched skills, applied
-date (shown in the employer's timezone), status badge, resume link, actions. Columns and order
-from the brief.
+date (shown in the employer's timezone), status badge, booking time (if any), actions. Sorted by
+score descending, then case-insensitive display name, then candidate id (brief FP-MATCH-1).
 
 **Confirm application** (Keystone approval pattern): a box titled "This will be sent to
-<company>", listing the resume file name, the cover note, and "Not shared: your other
-applications, your email address" (adjust to the brief's privacy rules). Buttons: primary
-"Submit application", secondary "Back to job".
+<company>: your name, your skills, your cover note. Not shared: your resume, your email address,
+your other applications." Buttons: primary "Submit application", secondary "Back to job".
 
-**Slot times**: always show the timezone label, for example "Mon 30 Nov, 10:00 to 10:45 (Asia/Hong_Kong)".
+**Slot times**: always show the timezone label, for example "Mon 30 Nov, 10:00 to 10:30 (Asia/Hong_Kong)".
 
 ## Forms
 
@@ -107,7 +106,7 @@ applications, your email address" (adjust to the brief's privacy rules). Buttons
 | Where | Text | Action |
 |---|---|---|
 | Recommendations, no skills | "Add your skills to see how jobs match you." | Edit profile |
-| Recommendations, no open jobs | "No open jobs right now. Check back soon." | none |
+| Recommendations, no jobs | "No jobs right now. Check back soon." | none |
 | My applications | "You have not applied to any jobs yet." | See recommendations |
 | My jobs | "You have not posted a job yet." | Post a job |
 | Applicants | "No one has applied to this job yet." | none |

```
