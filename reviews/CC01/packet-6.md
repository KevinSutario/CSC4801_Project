# Review packet CC01 (6 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/tasks/T11.md, docs/tasks/T12.md, docs/tasks/T13.md

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
diff --git a/docs/tasks/T11.md b/docs/tasks/T11.md
index be134db..0ca46a2 100644
--- a/docs/tasks/T11.md
+++ b/docs/tasks/T11.md
@@ -2,7 +2,7 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | MATCH | T05, T-BRIEF | no | READY (every rule and example quoted from the brief) |
+| 2 | MATCH | T05 | no | READY (after T05; every rule and example quoted from the brief; D15) |
 
 ## Goal
 A pure, deterministic engine that scores a candidate against a job and ranks every job exactly as
@@ -35,13 +35,12 @@ Rule text (brief section "5. Matching contract", FP-MATCH-1 "Score definition"),
 Mapped to this card's placeholders (each is a quote from the block above):
 - Normalisation rule: "trimming surrounding whitespace, converting to lowercase, removing empty
   values, and removing duplicates". Nothing about punctuation or synonyms: NOT IN BRIEF, so do not
-  add them. OPEN QUESTION (for your reply, per Pitfalls): the provisional `normalise_skill` in
-  `07-CONTRACTS.md` is described as "strip, lower-case, collapse spaces"; "collapse spaces" is not
-  in the brief's rule. If T07 or T10 stored a skill containing internal double spaces under the
-  provisional rule, its stored form differs from the brief's normal form and those rows may need
-  re-normalising (a contract change, not part of this task). Do not assume the stored rows match.
+  add them. `normalise_skill` is strip and lower-case, nothing else (no inner-space collapsing);
+  T01 wrote it with this rule from the start (D18), so rows stored by T07 and T10 already match
+  and never need re-normalising. This task keeps the function and adds tests for it.
 - Score formula: "score = 100 when |R| = 0"; "score = floor(100 * |C intersection R| / |R|)
-  otherwise". "Resume text is not an input."
+  otherwise". "Resume text is not an input." Implemented as integer arithmetic:
+  `100 * len(common) // len(required)` (D15).
 - The floor: the `floor(...)` in the formula; "The result **MUST** be an integer from 0 through
   100." So `score()` returns an `int`.
 - Tie-breaker 1 (candidate dashboard, `rank`): "case-insensitive job title".
@@ -64,25 +63,33 @@ Mapped to this card's placeholders (each is a quote from the block above):
 
 ## Contract
 ```python
+# app/skills.py
+def normalise_skill(raw: str) -> str          # brief FP-MATCH-1: strip surrounding whitespace, lower-case; nothing else (no inner-space collapsing)
+def parse_skill_list(text: str) -> list[str]  # split on commas, normalise, drop empties, dedupe keeping order
+def get_or_create_skill_ids(conn: Conn, names: list[str]) -> list[int]   # names already normalised
+
 # app/matching/engine.py  (pure: import only app.skills and the standard library)
 def score(candidate_skills: set[str], job_skills: set[str]) -> dict
-    # {"score": <number>, "matched": sorted list, "missing": sorted list}
+    # {"score": int, "matched": sorted list, "missing": sorted list}
+    # score = 100 when the job has no skills, else 100 * len(common) // len(required)
 def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]
+    # sorted by score descending, then title.lower(), then id; new dicts; never mutates the input
 ```
 `app/matching/service.py` (database side) is T13's job, not this task's.
-`rank` input jobs are dicts shaped like `jobs.service.list_open_jobs` output (each has `id`,
+`rank` input jobs are dicts shaped like `jobs.service.list_jobs` output (each has `id`,
 `title`, `skills` as a list of normalised names, `created_at`, and more). Build such dicts by hand
 in tests; this task uses no database. Output: new dicts with every original key unchanged, plus `score`, `matched`, `missing`.
 
 ## Steps
 1. Tests first: one parametrised test case per brief example, inputs and outputs exactly as written,
    with a `# brief: <section>` comment. Run them. See them fail.
-2. `normalise_skill`: replace the provisional body with the brief's rule. Keep the signature.
-3. `score`: the brief's formula and floor. Use `fractions` or integers if the brief's numbers need
-   exact arithmetic; never compare floats with `==`.
-4. `rank`: `sorted()` with a key tuple built from the score and the two tie-breakers in the brief's
-   order. Add a final key `job["id"]` so equal items are always in the same order (unless the brief
-   defines the last tie-breaker as something else). Copy each dict (`dict(job)`), never mutate.
+2. `normalise_skill`: keep T01's body (strip, lower-case, nothing else) and the signature. Add tests
+   for it: `"  Python "` gives `"python"`; `"Data  Science"` keeps its inner double space;
+   `parse_skill_list("Python, SQL, python, , sql ")` gives `["python", "sql"]`.
+3. `score`: the brief's formula and floor as integer arithmetic, `100 * len(common) //
+   len(required)`; never floats.
+4. `rank`: `sorted()` with the key tuple `(-score, title.lower(), id)`, the brief's order. Copy
+   each dict (`dict(job)`), never mutate.
 5. Property tests (fixed seed `random.Random(1234)`, 200 rounds): `rank` returns every job exactly
    once; the input list and dicts are unchanged afterwards; running twice gives the same order.
 
@@ -99,6 +106,5 @@ in tests; this task uses no database. Output: new dicts with every original key
 - every brief example is a test case
 
 ## Pitfalls
-- T07 and T10 already store skills with the provisional rule. If the brief's rule differs (for
-  example synonyms), say so in your reply under OPEN QUESTIONS: existing rows may need re-normalising,
-  which is a contract change, not part of this task.
+- Do not change what `normalise_skill` does. T07 and T10 rows are stored under the same rule and
+  must keep matching. Collapsing inner spaces, synonyms or punctuation handling are not in the brief.
diff --git a/docs/tasks/T12.md b/docs/tasks/T12.md
index 766caa0..51243dd 100644
--- a/docs/tasks/T12.md
+++ b/docs/tasks/T12.md
@@ -2,40 +2,33 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | SCHED | T05 | no | READY (rules quoted from the brief; duration default SUPERSEDED; the rest DEFAULT (not in brief)) |
+| 2 | SCHED | T05 | no | READY (after T05; rules quoted from the brief; slots employer-owned and exactly 30 minutes by D13; codes by D9; the rest DEFAULT (not in brief)) |
 
 ## Goal
-Employers add interview slots for their jobs in their own time zone. Slots are stored in UTC and
-shown correctly in any time zone. Invalid slots are rejected.
+Employers add 30-minute interview slots in their own time zone, from their home page. Slots belong
+to the employer, not to a job. They are stored in UTC and shown correctly in any time zone. Invalid
+slots are rejected; a booked slot cannot be deleted.
 
 ## Requirement
 FP-SCHED-1: slot creation, timezones and deletion; invalid slots. Rule text (brief section
 "6. Applications and interview scheduling", FP-SCHED-1 "Availability"):
 > An employer **MUST** be able to create and delete future, 30-minute availability slots. Each slot **MUST** have one owner and an exact start and end time with an unambiguous, documented timezone. The system **MUST** reject invalid durations, end-before-start values, and deletion of a booked slot. Booked slots **MUST NOT** be shown as available.
 
-Worked examples: none in the brief for FP-SCHED-1.
+Ownership scope, from FP-SCHED-2 (same brief section):
+> - the slot belongs to the employer for the candidate's application;
 
-SUPERSEDED by the quote: slot length is exactly 30 minutes ("30-minute availability slots";
-"reject invalid durations"). The old default "length 15 to 240 minutes" is wrong. The test bullets
-"too short, too long" still apply (29 and 31 minutes are invalid durations).
+Worked examples: none in the brief for FP-SCHED-1.
 
-Required by the quote, matching the old defaults: end after start; start in the future; a booked
-slot cannot be deleted (`Conflict("This slot is booked and cannot be deleted.")`, message wording
-is DEFAULT (not in brief)); booked slots are never listed as available.
+Decided (D13): a slot's one owner is the employer (`interview_slots.employer_id`; there is no
+`job_id`). Duration is exactly 30 minutes: 29 and 31 minutes are "invalid durations". Start must be
+in the future. End must be after start. Deleting a booked slot raises `Conflict` (HTTP 409 is
+DEFAULT (not in brief); message `"This slot is booked and cannot be deleted."` is DEFAULT (not in
+brief)). Booked slots are never listed as available. Another employer's slot: `Forbidden`; a
+missing slot: `NotFound` (D9).
 
 DEFAULT (not in brief): date `YYYY-MM-DD`, times `HH:MM` 24-hour; no overlap with another slot of
-the same job; storage in UTC with the entry zone recorded (the brief only requires "an unambiguous,
-documented timezone", so document it in SPEC.md). This card attaches slots to jobs (DEFAULT for
-storage). Note that FP-SCHED-1 says each slot "**MUST** have one owner" and FP-SCHED-2 (brief section
-"6. Applications and interview scheduling") scopes booking to the employer, not the job:
-> - the slot belongs to the employer for the candidate's application;
-
-So a slot's owner is the employer. Attaching slots to jobs is only acceptable if booking (T16)
-still allows any slot of the same employer; that is the T16 CONFLICT and the orchestrator's
-decision, not this card's.
-
-CONFLICT (flagged, not changed): the brief (FP-EMP-2, FP-AUTH-3) gives `403` for another
-employer's posting; the invalid-slots test bullet says `NotFound` for "someone else's job". See T06.
+the same employer; storage in UTC with the entry zone recorded in `created_tz` (the brief only
+requires "an unambiguous, documented timezone", so document it in SPEC.md).
 
 ## Owns
 - `app/timeutil.py`
@@ -47,18 +40,38 @@ employer's posting; the invalid-slots test bullet says `NotFound` for "someone e
 
 ## May read
 - `CLAUDE.md`
-- `docs/plan/07-CONTRACTS.md` (sections: scheduling, jobs)
-- `docs/plan/03-DATA-MODEL.md` (tables: interview_slots, bookings, jobs, companies)
+- `docs/plan/07-CONTRACTS.md` (sections: scheduling)
+- `docs/plan/03-DATA-MODEL.md` (tables: interview_slots, bookings)
 - `app/audit.py`, `app/db.py`, `app/errors.py`, `app/scheduling/__init__.py`,
   `app/templates/components/*`, `tests/conftest.py`
 
 ## Contract
-`app/timeutil.py` and `app/scheduling/slots.py` exactly as in `07-CONTRACTS.md`. Routes
-`scheduling.slots` GET/POST `/employer/jobs/<int:job_id>/slots`, `scheduling.delete_slot` POST
-`/employer/slots/<int:slot_id>/delete`, both `@role_required("employer")`.
-
-Ownership of the job: query `jobs JOIN companies` where `companies.owner_id = ?` directly in
-`slots.py`. Do not import `app.jobs.service` (another lane).
+`app/timeutil.py` exactly as in `07-CONTRACTS.md`:
+```python
+def validate_tz(name: str) -> str                   # ValueError if not an IANA zone
+def local_to_utc(date_str: str, time_str: str, tz_name: str) -> str   # "YYYY-MM-DD","HH:MM" -> UTC iso
+def utc_to_local(utc_iso: str, tz_name: str) -> datetime
+def format_local(utc_iso: str, tz_name: str) -> str  # "Mon 30 Nov 2026, 10:00 (Asia/Hong_Kong)"
+def parse_iso(utc_iso: str) -> datetime              # aware UTC
+COMMON_TIMEZONES: tuple[str, ...]                    # for the select box
+```
+`app/scheduling/slots.py`:
+```python
+def create_slot(conn: Conn, employer_id: int, date_str: str, start_str: str, end_str: str,
+                tz_name: str) -> int
+    # ValidationError: bad date or time, unknown zone, DST gap, end not after start,
+    # duration not exactly 30 minutes, start not in the future, overlap with the employer's own slot
+    # (overlap rule is DEFAULT (not in brief))
+def delete_slot(conn: Conn, employer_id: int, slot_id: int) -> None
+    # NotFound if missing; Forbidden if another employer's; Conflict if booked (409 is DEFAULT (not in brief))
+def list_slots_for_employer(conn: Conn, employer_id: int) -> list[dict]   # adds "booked": bool; start ascending
+```
+Routes `scheduling.slots` GET/POST `/employer/slots`, `scheduling.delete_slot` POST
+`/employer/slots/<int:slot_id>/delete`, both `@role_required("employer")`. Template
+`scheduling/slots.html`. The page is linked from the employer home (`employers.home`, T09 owns that
+template; add the link there only if T09 has not, otherwise report it).
+
+No job ownership query: slots are not attached to jobs. Do not import `app.jobs.service`.
 
 ## Steps
 1. Tests first.
@@ -67,13 +80,18 @@ Ownership of the job: query `jobs JOIN companies` where `companies.owner_id = ?`
    the zone, convert to UTC, then convert back and compare with the input; if different, the time does
    not exist (DST gap): `ValueError`. Output format `%Y-%m-%dT%H:%M:%SZ`. `COMMON_TIMEZONES`: UTC,
    Asia/Hong_Kong, Asia/Shanghai, Asia/Jakarta, Asia/Singapore, Europe/London, America/New_York.
-3. `create_slot`: validate every field (collect errors), check job ownership (`NotFound`), future
-   start (compare with `now_iso()` as strings is fine: same format), overlap query
-   (`starts_at < ? AND ends_at > ?`), insert, audit `slot.create`.
-4. `delete_slot`: ownership via slot's job; booked: `Conflict`; else delete, audit `slot.delete`.
-5. `list_slots_for_job`: one query with `LEFT JOIN bookings`, `booked` as bool, ordered by start.
+3. `create_slot`: validate every field (collect errors): date and time formats, zone, DST gap, end
+   after start, `parse_iso(ends_at) - parse_iso(starts_at) == timedelta(minutes=30)` exactly, start
+   after `now_iso()` (comparing strings of the same format is fine), overlap query on the employer's
+   own slots (`employer_id = ? AND starts_at < ? AND ends_at > ?`). Insert with `employer_id`,
+   `starts_at`, `ends_at`, `created_tz`, `created_at`; audit `slot.create`.
+4. `delete_slot`: `SELECT` the slot by id; no row: `NotFound`; `employer_id` differs: `Forbidden`;
+   a `bookings` row for it: `Conflict`; else delete, audit `slot.delete`.
+5. `list_slots_for_employer`: one query with `LEFT JOIN bookings`, `booked` as bool, ordered by
+   `starts_at`.
 6. Page: add-slot form (date, start, end, time zone select defaulting to the employer's last used
-   zone or UTC), list in the chosen zone using `format_local`, delete button only on open slots.
+   zone or UTC), list in the chosen zone using `format_local` ("Mon 30 Nov, 10:00 to 10:30
+   (Asia/Hong_Kong)"), delete button only on unbooked slots, booked ones marked "Booked".
 
 ## Tests
 `tests/unit/test_timeutil.py`:
@@ -83,12 +101,18 @@ Ownership of the job: query `jobs JOIN companies` where `companies.owner_id = ?`
 - `validate_tz("Mars/Base")` raises
 
 `tests/unit/test_sched_slots.py` (remove both skips):
-- `test_fp_sched_1_slot_creation_timezones_and_deletion`: create in Hong Kong time, stored UTC is
-  right, listed with `booked False`; delete works; booked slot delete gives `Conflict` (insert a
-  booking with SQL).
-- `test_fp_sched_1_invalid_slots`: parametrised: bad date, bad time, end before start, too short,
-  too long, in the past, overlapping, unknown zone, someone else's job (`NotFound`).
-- candidate POST to the slots page gives 403
+- `test_fp_sched_1_slot_creation_timezones_and_deletion`: create `2030-01-07 10:00` to `10:30` in
+  `Asia/Hong_Kong`; stored `starts_at` is `2030-01-07T02:00:00Z` and `ends_at`
+  `2030-01-07T02:30:00Z`; listed with `booked False`; after `make_booking` it is listed with
+  `booked True`; delete of an unbooked slot works; delete of the booked slot gives `Conflict` and
+  the slot and booking still exist.
+- `test_fp_sched_1_invalid_slots`: parametrised: bad date, bad time, end before start, 29 minutes,
+  31 minutes, in the past, overlapping the employer's own slot, unknown zone; each raises
+  `ValidationError` and inserts no row. Plus: deleting another employer's slot gives `Forbidden`,
+  a missing slot `NotFound`, a booked slot `Conflict`.
+- an overlapping slot of a different employer is allowed
+- candidate POST to `/employer/slots` gives 403; employer B POST delete on A's slot gives 403;
+  missing slot id gives 404
 
 ## Done when
 - check and scope pass
diff --git a/docs/tasks/T13.md b/docs/tasks/T13.md
index 11c1b1c..634e6ec 100644
--- a/docs/tasks/T13.md
+++ b/docs/tasks/T13.md
@@ -2,10 +2,10 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | **BLOCKED** (NEEDS DECISION, same as the FP-CAN-2 row in `01-REQUIREMENTS.md`): the brief says the dashboard "**MUST** list all current (not deleted) jobs", but the Contract (`list_open_jobs`) and the test bullet exclude T10's "closed" jobs, which are not deleted (CONFLICT, see Requirement). Also waits for T11 to merge |
+| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | READY (after T07, T10, T11; no closed state by D18, ranking by D15) |
 
 ## Goal
-A candidate sees every open job ranked for them, each with its score and which skills matched and
+A candidate sees every job ranked for them, each with its score and which skills matched and
 which are missing.
 
 ## Requirement
@@ -22,12 +22,8 @@ brief).
 
 Answers for the test bullets:
 - Zero-score jobs: "list all current (not deleted) jobs", so a zero-overlap job is present.
-- Closed jobs: CONFLICT (flagged, not changed; orchestrator decision needed). The brief says "list
-  all current (not deleted) jobs". A job that T10 has "closed" is not deleted, so the brief requires
-  it on the dashboard; this card's Contract (`rank(skills, list_open_jobs(conn))`) and the test
-  bullet "5 open jobs and 1 closed; result has exactly the 5" hide it. Either the "closed" state is
-  dropped from the plan, or closed jobs are listed, or the orchestrator documents why "closed"
-  counts as not "current". Not a default this card can pick.
+- There is no closed state (D18): every job that exists is current, so the dashboard lists every
+  job (`list_jobs`). A job with no required skills scores 100 (FP-MATCH-1).
 - "Candidate and employer views **MUST** call the same implementation." (FP-MATCH-1)
 
 ## Owns
@@ -45,23 +41,23 @@ Answers for the test bullets:
 
 ## Contract
 ```python
-def recommend_for(conn, candidate_id: int) -> list[dict]          # rank(skills, list_open_jobs(conn))
-def score_candidate_for_job(conn, candidate_id: int, job_id: int) -> dict   # engine.score for one job
+def recommend_for(conn, candidate_id: int) -> list[dict]          # rank(skills, list_jobs(conn))
+def score_candidate_for_job(conn, candidate_id: int, job_id: int) -> dict   # engine.score for one job; NotFound if the job is missing
 ```
 Route `matching.recommendations` GET `/candidate/recommendations`, `@role_required("candidate")`.
 
 ## Steps
 1. Tests first.
-2. `recommend_for`: `set(get_profile(conn, candidate_id)["skills"])`, `list_open_jobs(conn)`, `rank`.
-3. `score_candidate_for_job`: `get_job` (NotFound if missing or closed), then `engine.score`.
+2. `recommend_for`: `set(get_profile(conn, candidate_id)["skills"])`, `list_jobs(conn)`, `rank`.
+3. `score_candidate_for_job`: `get_job` (NotFound if missing), then `engine.score`.
 4. Page: one card per job in the returned order, `score_bar`, "Matched:" and "Missing:" lists,
-   link to `/jobs/<id>`. Empty states from `05-UX-FLOWS.md` (no skills; no open jobs).
+   link to `/jobs/<id>`. Empty states from `05-UX-FLOWS.md` (no skills; no jobs).
 
 ## Tests (`tests/unit/test_can_recommend.py`; remove the skip)
-- `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs`: 5 open jobs and 1 closed;
-  result has exactly the 5 (or what the brief says about closed ones); every key from
-  `list_open_jobs` is present with the same value; order equals `engine.rank` on the same input; a
-  zero-overlap job is still present (unless the brief says otherwise).
+- `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs`: 6 jobs from two employers,
+  one with no required skills; the result has exactly the 6; every key from `list_jobs` is present
+  with the same value; order equals `engine.rank` on the same input; a zero-overlap job is still
+  present; the job with no required skills scores 100.
 - page shows jobs in the same order as the service (check the titles' positions in the HTML)
 - candidate with no skills sees the empty-state text
 - employer GET gives 403

```
