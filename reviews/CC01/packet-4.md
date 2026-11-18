# Review packet CC01 (4 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/tasks/T04.md, docs/tasks/T05.md, docs/tasks/T06.md, docs/tasks/T07.md

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
diff --git a/docs/tasks/T04.md b/docs/tasks/T04.md
index b48e0ad..49d01bc 100644
--- a/docs/tasks/T04.md
+++ b/docs/tasks/T04.md
@@ -5,8 +5,8 @@
 | 1 | foundation | T03 | no | READY |
 
 ## Goal
-Every later task can create test users, companies, jobs, applications and slots in one line, sign
-in, and post forms with a CSRF token. Every template test name exists as a skipped placeholder, so
+Every later task can create test users, companies, jobs, applications, slots and bookings in one
+line, sign in, and post forms with a CSRF token. Every template test name exists as a skipped placeholder, so
 progress is visible and nothing passes by accident.
 
 ## Owns
@@ -39,13 +39,30 @@ progress is visible and nothing passes by accident.
   `app/skills.py`
 
 ## Contract
-The fixtures and signatures in `07-CONTRACTS.md`, section `tests/conftest.py`.
+The fixtures and signatures in `07-CONTRACTS.md`, section `tests/conftest.py`:
+```python
+make_candidate(email="cand@example.com", password="Passw0rd!", name="Mei Lin Tan",
+               skills=("python", "sql")) -> int          # user id
+make_employer(email="emp@example.com", password="Passw0rd!", name="Daniel Wong") -> int
+make_company(employer_id: int, name="Harbourline Logistics") -> int
+make_job(employer_id: int, title="Data Analyst", skills=("python",), **cols) -> int
+make_application(candidate_id: int, job_id: int, status="pending") -> int
+make_slot(employer_id: int, starts_at="2030-01-07T02:00:00Z",
+          ends_at="2030-01-07T02:30:00Z", created_tz="UTC") -> int
+make_booking(application_id: int, slot_id: int) -> int
+login(client, email, password) -> Response
+login_as(client, user_id: int, role: str) -> None
+csrf_post(client, url, data: dict, **kwargs) -> Response
+```
+Jobs have no open/closed flag (D18) and slots belong to the employer, not to a job (D13).
 
 ## Steps
 1. Factories insert with plain SQL inside `transaction(conn)`. Passwords hashed with
    `werkzeug.security.generate_password_hash`. `make_candidate` also inserts a `candidate_profiles`
    row (timezone `UTC`) and its skills via `app.skills.get_or_create_skill_ids`. `make_job` creates a
-   company for the employer if none exists. All times use `now_iso()` except slot times.
+   company for the employer if none exists. `make_slot` inserts an `interview_slots` row with
+   `employer_id` only (no job). `make_booking` inserts a `bookings` row. All times use `now_iso()`
+   except slot times.
 2. Each factory fixture returns a function, so a test can call it many times. Emails default to
    unique values when called again (append a counter) so two calls never clash.
 3. `login_as(client, user_id, role)`: sets `user_id`, `role` and a fresh `csrf` in the session.
@@ -63,8 +80,9 @@ The fixtures and signatures in `07-CONTRACTS.md`, section `tests/conftest.py`.
    `pass` bodies this way. Create the other files with a module docstring naming the owner task.
 7. Delete `tests/unit/test_workflows.py` and `tests/unit/test_scheduling.py` after their names exist
    in the new files.
-8. `tests/unit/test_conftest.py`: each factory works twice in one test; `login_as` then GET `/`
-   redirects by role; `csrf_post` to `/nowhere` gives 404, not 403.
+8. `tests/unit/test_conftest.py`: each factory works twice in one test (`make_booking` twice needs
+   two applications and two slots); `login_as` then GET `/` redirects by role; `csrf_post` to
+   `/nowhere` gives 404, not 403.
 
 ## Done when
 - check passes, showing the placeholder tests as skipped
diff --git a/docs/tasks/T05.md b/docs/tasks/T05.md
index b808b76..3ecb56b 100644
--- a/docs/tasks/T05.md
+++ b/docs/tasks/T05.md
@@ -18,9 +18,9 @@ People can create an account as a candidate or an employer, sign in, and sign ou
   name limit and no session lifetime. Keep these defaults: email lower-cased, max 254 chars, must
   match `^[^@\s]+@[^@\s]+\.[^@\s]+$`; password 8 to 128 chars; display name 1 to 80 chars after
   strip; role `candidate` or `employer`.
-- Note: the brief writes the two roles as `Candidate` and `Employer`; the contract stores
-  `candidate` and `employer`. Whether the stored spelling must match the brief: unknown (listed in
-  T-BRIEF's OPEN QUESTIONS). Not changed here.
+- Roles are stored `candidate` and `employer`; pages show `Candidate` and `Employer` (D18).
+- FP-SEC-2 (brief section "7. Security requirements", FP-SEC-2 "SQL injection"):
+  > All database access involving user-controlled values **MUST** use parameterized queries, a correctly used ORM, or an equivalent safe API. Concatenating raw user input into a query is prohibited. At least one unit test **MUST** pass SQL metacharacters to the query-building or data-access logic and verify that the input remains a bound value rather than executable SQL.
 
 ## Owns
 - `app/auth/service.py`
@@ -76,6 +76,10 @@ Routes: `auth.register` GET/POST `/auth/register`, `auth.login` GET/POST `/auth/
 - `test_fp_auth_2_salted_hash_and_password_verification`: stored hash differs from the password and
   starts with a known Werkzeug method prefix; two users with the same password have different
   hashes; `authenticate` true for right, None for wrong password and for unknown email.
+- `test_fp_sec_2_sql_metacharacters_stay_bound` (FP-SEC-2): register and then authenticate with
+  the email `x'); DROP TABLE users; --@example.com` and the display name
+  `Robert'); DELETE FROM users; --`; afterwards the `users` table still exists (query
+  `sqlite_master`) and holds the rows; the literal strings are stored unchanged (email lower-cased).
 - extra: login with `next=//evil.com` redirects to `/`; with `next=/candidate/profile` goes there.
 - extra: 6th bad login for the same email gives 429.
 - extra: logout via GET gives 405; logout POST without token gives 403.
diff --git a/docs/tasks/T06.md b/docs/tasks/T06.md
index 34cc801..9f249db 100644
--- a/docs/tasks/T06.md
+++ b/docs/tasks/T06.md
@@ -2,11 +2,11 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | security | T10, T15, T16 | yes | **BLOCKED** (NEEDS DECISION, same as the FP-AUTH-3 row in `01-REQUIREMENTS.md`): the feature cards raise `NotFound` (404) for another user's object where the brief says "authenticated user with the wrong role or owner: `403 Forbidden`", so Step 2's "expected code" for user B with A's id has no decided value; the orchestrator decides 403 vs 404 before dispatch (see CONFLICT under Requirement). Also waits for its dependencies |
+| 3 | security | T10, T15, T16 | yes | READY (after T10, T15, T16; codes decided by D9) |
 
 ## Goal
-Prove, route by route, that nobody can read or change what is not theirs, and that missing objects
-give 404. This task only writes tests. Holes it finds are reported, not fixed here.
+Prove, route by route, that nobody can read or change what is not theirs (403), and that missing
+objects give 404. This task only writes tests. Holes it finds are reported, not fixed here.
 
 ## Requirement
 FP-AUTH-3: authorization and missing object. Rule text (brief section "2. Roles and
@@ -27,14 +27,10 @@ FP-SEC-1 "Object access"):
 > 2. one employer cannot modify another employer's job or read its applicant list;
 > 3. a candidate cannot book a slot using another candidate's application.
 
-Expected codes, from the quote: signed out: `401 Unauthorized` or redirect to login; wrong role or
-wrong owner: `403 Forbidden`; missing object the caller could otherwise access: `404 Not Found`.
-
-CONFLICT (orchestrator decision needed, nothing below changed): the old default on this card said
-"another user's object 404", and the feature cards (T08, T10, T12, T14, T15, T16) raise `NotFound` for
-another user's object. The brief says `403 Forbidden` for "the wrong role or owner". Either the
-feature cards change to `Forbidden` (a contract change) or the sweep records each 404 as a `BUG:`
-hole. Signed-out POST giving 401 and GET redirecting both satisfy the quote.
+Expected codes (D9, exactly the quote): signed out: redirect to login on GET, `401` on other
+methods; wrong role: `403`; another user's object: `403` (every ownership helper raises `Forbidden`);
+missing object: `404` (`NotFound`). Every feature card (T08, T10, T12, T14, T15, T16) builds these
+codes, so a different code is a hole in that feature, not a disagreement about the rule.
 
 ## Owns
 - `tests/unit/test_auth.py`
@@ -49,19 +45,45 @@ hole. Signed-out POST giving 401 and GET redirecting both satisfy the quote.
 
 ## Steps
 1. From `scripts/contracts.json`, list every endpoint with a path parameter. For each, write down:
-   the role that may use it, how to make an object owned by user A, and the URL.
+   the role that may use it, how to make an object owned by user A, and the URL. The list includes
+   at least: `candidates.resume_view` (`/candidates/<int:candidate_id>/resume`), `jobs.edit`,
+   `jobs.confirm_delete`, `jobs.delete`, `jobs.detail`, `applications.confirm`,
+   `applications.submit`, `applications.applicants`, `applications.confirm_status`,
+   `applications.set_status`, `scheduling.delete_slot` (`/employer/slots/<int:slot_id>/delete`),
+   `scheduling.application_detail`, `scheduling.confirm_booking`, `scheduling.book`. (The slots
+   page itself is `/employer/slots` with no id since D13; it belongs in step 3.)
 2. `test_authz_sweep.py`: one parametrised test over that list. For each route: user B (same role)
-   with A's id: expected code; right role, missing id (999999): 404; wrong role: 403; signed out:
-   redirect or 401. Use factories and `login_as`. POSTs use `csrf_post`.
+   with A's id: 403; right role, missing id (999999): 404; wrong role: 403; signed out: redirect
+   (GET) or 401 (other methods). Use factories and `login_as`. POSTs use `csrf_post`. For
+   `jobs.detail` and `candidates.resume_view` (any signed-in role) the "wrong role" case does not
+   apply; `candidates.resume_view` with another user's id is 403 for both a candidate and an
+   employer.
 3. A second parametrised test: every route without a path parameter, wrong role gives 403 and signed
    out redirects or 401.
-4. `test_auth.py`: remove the skip on `test_fp_auth_3_authorization_and_missing_object` and make it a
-   short, readable version of the sweep for the main cases (employer B edits A's job; candidate B reads
-   A's application; candidate opens an employer page; missing job).
-5. Run. Every failing case is a real hole: list each in your reply under `BUG:` with the route and
+4. `test_fp_sec_1_object_access_boundaries` in `test_authz_sweep.py` (FP-SEC-1): the brief's three
+   boundaries as named parametrised cases (`pytest.param(..., id=...)`):
+   - `candidate_resume`: candidate B GET `/candidates/<A>/resume` is 403; and
+     `candidate_application`: candidate B GET `/candidate/applications/<A's application>` is 403;
+   - `employer_job`: employer B POST `/employer/jobs/<A's job>/edit` is 403 and the job is
+     unchanged; and `employer_applicants`: employer B GET `/employer/jobs/<A's job>/applicants` is
+     403;
+   - `candidate_booking`: candidate B POST `/candidate/applications/<A's application>/book/<slot>`
+     is 403 and no booking row exists.
+5. `test_auth.py`: remove the skip on `test_fp_auth_3_authorization_and_missing_object` and make it a
+   short, readable version of the sweep for the main cases (employer B edits A's job: 403; candidate B
+   reads A's application: 403; candidate opens an employer page: 403; missing job: 404; signed out:
+   redirect or 401).
+6. Run. Every failing case is a real hole: list each in your reply under `BUG:` with the route and
    what happened. Mark those cases `@pytest.mark.xfail(strict=True, reason="B<n>: <route>")` so the
    gate passes and the hole stays visible. The bug cards remove the xfail when fixed.
 
+## Tests
+- `tests/unit/test_authz_sweep.py::test_fp_sec_1_object_access_boundaries` (FP-SEC-1): the three
+  boundaries above, each as a named case.
+- `tests/unit/test_authz_sweep.py`: the two parametrised sweeps (steps 2 and 3).
+- `tests/unit/test_auth.py::test_fp_auth_3_authorization_and_missing_object` (FP-AUTH-3).
+
 ## Done when
 - check and scope pass
 - every endpoint with an id appears in the sweep
+- the three FP-SEC-1 boundaries appear by name
diff --git a/docs/tasks/T07.md b/docs/tasks/T07.md
index fe3a4bf..0a85a15 100644
--- a/docs/tasks/T07.md
+++ b/docs/tasks/T07.md
@@ -2,11 +2,11 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 2 | CAN | T05 | no | **BLOCKED** (NEEDS DECISION, same as the FP-CAN-1 row in `01-REQUIREMENTS.md`): the brief says a candidate "**MUST** be able to view and edit only their own profile, including a display name", and no card lets the candidate edit the display name (the `save_profile` contract has no name field). Needs either a contract change to `save_profile` or a new owner; see GAP. Limits are DEFAULT (not in brief) |
+| 2 | CAN | T05 | no | READY (after T05; display name added by D16; limits are DEFAULT (not in brief)) |
 
 ## Goal
-A candidate can fill in and edit their profile and skills. The Today page welcomes them and shows
-what to do next.
+A candidate can fill in and edit their profile, including their display name, and their skills.
+The Today page welcomes them and shows what to do next.
 
 ## Requirement
 FP-CAN-1 (profile part). Rule text (brief section "3. Candidate workflow", FP-CAN-1 "Candidate
@@ -16,15 +16,13 @@ profile and resume", first paragraph):
 Skill normalisation is the brief's FP-MATCH-1 rule (owned by T11, `app/skills.py`):
 > Normalize candidate and required skills by trimming surrounding whitespace, converting to lowercase, removing empty values, and removing duplicates.
 
-DEFAULT (not in brief): the brief sets no field limits. Keep: headline max 120, location max 80,
-summary max 2000, timezone must be a valid IANA name (use `zoneinfo.available_timezones()`), skills:
-comma separated, at most 30, each 1 to 40 chars after normalising.
+DEFAULT (not in brief): the brief sets no field limits. Keep: display name 1 to 80 chars after
+strip, headline max 120, location max 80, summary max 2000, timezone must be a valid IANA name
+(use `zoneinfo.available_timezones()`), skills: comma separated, at most 30, each 1 to 40 chars
+after normalising.
 
-GAP (NEEDS DECISION; listed in T-BRIEF's OPEN QUESTIONS, not changed here): the brief's editable
-profile includes "a display name". This card's form has headline, location, timezone, summary and
-skills; the display name is set once at registration (T05) and no card lets the candidate edit it.
-Closing the gap means a contract change to `save_profile` (add a display-name parameter, and the
-form field in Step 4) or a new card that owns it. The orchestrator decides before dispatch.
+The display name is editable here (D16): `save_profile` updates `users.display_name` in the same
+transaction as the profile row.
 
 ## Owns
 - `app/candidates/profile_service.py`
@@ -43,29 +41,36 @@ form field in Step 4) or a new card that owns it. The orchestrator decides befor
 ## Contract
 ```python
 def get_profile(conn, candidate_id: int) -> dict
-    # headline, location, timezone, summary, skills: list[str] (sorted), updated_at (None if never saved)
-def save_profile(conn, candidate_id: int, headline: str, location: str, timezone: str,
-                 summary: str, skills_text: str) -> None
+    # display_name, headline, location, timezone, summary, skills: list[str] (sorted),
+    # updated_at (None if never saved)
+def save_profile(conn, candidate_id: int, display_name: str, headline: str, location: str,
+                 timezone: str, summary: str, skills_text: str) -> None
+    # also updates users.display_name in the same transaction (D16)
 ```
 Routes: `candidates.today` GET `/candidate/`, `candidates.profile` GET/POST `/candidate/profile`.
 Both `@login_required` and `@role_required("candidate")`.
 
 ## Steps
 1. Tests first.
-2. `get_profile`: read `candidate_profiles` (create nothing; if the row is missing return defaults),
-   join skills.
-3. `save_profile`: strip all text, validate (collect all errors), `parse_skill_list`, then in one
-   transaction: upsert profile (`INSERT ... ON CONFLICT(user_id) DO UPDATE`), delete old
-   `candidate_skills`, insert new ones via `get_or_create_skill_ids`, audit `profile.update`.
-4. Profile page: form with the five fields (timezone as a `select_field` of
+2. `get_profile`: read `users.display_name` and `candidate_profiles` (create nothing; if the
+   profile row is missing return defaults), join skills.
+3. `save_profile`: strip all text, validate (collect all errors, including `display_name` 1 to 80
+   chars), `parse_skill_list`, then in one transaction: `UPDATE users SET display_name = ?`, upsert
+   profile (`INSERT ... ON CONFLICT(user_id) DO UPDATE`), delete old `candidate_skills`, insert new
+   ones via `get_or_create_skill_ids`, audit `profile.update`.
+4. Profile page: form with the six fields (display name first; timezone as a `select_field` of
    `sorted(zoneinfo.available_timezones())`), current skills shown as badges, errors per field.
 5. Today page: "Good morning, <display name>" style heading, a card listing what is missing
    (no skills, no resume, no summary) with links to `/candidate/profile` and `/candidate/resume`.
    T18 adds widgets later; leave a `{% block today_widgets %}{% endblock %}`.
 
 ## Tests (`tests/unit/test_can_profile.py`)
-- save then get returns the same values; skills normalised, deduped, sorted
-- each limit: one character over gives a field error; nothing saved
+- save then get returns the same values, including the new display name; skills normalised,
+  deduped, sorted
+- after `save_profile` with a new display name, `users.display_name` holds it and `g.user` on the
+  next request shows it (GET `/candidate/` greets by the new name)
+- each limit: one character over gives a field error; nothing saved (display name: empty and 81
+  chars rejected, and `users.display_name` unchanged)
 - invalid timezone `Mars/Base` rejected
 - skills text with 31 skills rejected
 - saving again replaces skills (old ones gone)
@@ -76,5 +81,5 @@ Both `@login_required` and `@role_required("candidate")`.
 - check and scope pass
 
 ## Pitfalls
-- `app/skills.py` is provisional and owned by T11. Do not edit it. Use simple test skills like
-  "Python" and "sql" whose normal form will not change.
+- `app/skills.py` is owned by T11. Do not edit it. It already implements the brief's rule (strip,
+  lower-case, nothing else), so rows saved here never need re-normalising.

```
