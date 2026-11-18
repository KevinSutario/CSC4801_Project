# Review packet CC01 (1 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/plan/01-REQUIREMENTS.md, docs/plan/02-ARCHITECTURE.md, docs/plan/03-DATA-MODEL.md

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
diff --git a/docs/plan/01-REQUIREMENTS.md b/docs/plan/01-REQUIREMENTS.md
index 9444a8f..f886f2f 100644
--- a/docs/plan/01-REQUIREMENTS.md
+++ b/docs/plan/01-REQUIREMENTS.md
@@ -8,9 +8,8 @@ Every graded requirement, where its rule text lives, which task builds it, and w
   states them.
 - **BLOCKED**: the rule is defined only in the brief, and the brief has not been pasted in yet.
   No agent may write logic for a BLOCKED item. Tasks that need it stop at the test-writing step.
-- **NEEDS DECISION**: the brief states the rule, but the task card's default or design contradicts
-  it. The orchestrator decides (and logs it in `docs/state/DECISIONS.md`) before the card is
-  dispatched.
+- **READY (D<n>)**: the brief's rule contradicted the card's old default; decision D<n> in
+  `docs/state/DECISIONS.md` settled it and CC01 wrote the decided text into the plan and the card.
 
 ## How to unblock
 
@@ -22,7 +21,7 @@ Every graded requirement, where its rule text lives, which task builds it, and w
 T-BRIEF did steps 1 to 3 on 2026-11-11 from `docs/BRIEF.md`. Every quote below is verbatim from the
 brief's `REQUIREMENTS.md` part; the section name is given each time. "NOT IN BRIEF" means the brief
 says nothing about it and the task card's default stands, marked `DEFAULT (not in brief)` on the
-card. Step 4's DECISIONS.md entry is the orchestrator's.
+card. Step 4 was done by decisions D9 to D18 (2026-11-10 to 2026-11-12) and applied by CC01.
 
 ## Requirement ids the brief defines
 
@@ -44,7 +43,7 @@ The test names come from the course template. Keep them exactly. Tests live in p
 |---|---|---|---|---|
 | FP-AUTH-1 | Registration and session lifecycle; invalid registration | READY (brief gives no limits; T05 defaults, marked DEFAULT) | T05 | `test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`, `::test_fp_auth_1_invalid_registration` |
 | FP-AUTH-2 | Salted hash and password verification | READY | T05 | `test_auth.py::test_fp_auth_2_salted_hash_and_password_verification` |
-| FP-AUTH-3 | Authorization and missing object | NEEDS DECISION (codes quoted; cards use 404 where the brief says 403) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |
+| FP-AUTH-3 | Authorization and missing object | READY (D9: another user's object 403, missing 404, applied to every card) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |
 
 Rule text (brief section "2. Roles and authentication"):
 
@@ -71,16 +70,16 @@ Open questions for the brief, answered:
   or owner: `403 Forbidden`". For a missing object, 404? "missing object that the caller would
   otherwise be allowed to access: `404 Not Found`". Signed out: "`401 Unauthorized` or redirect to
   login".
-- CONFLICT: T06's default and the feature cards T08, T10, T12, T14, T15, T16 return 404 (`NotFound`)
-  for another user's object. The brief says 403. Decision needed before those cards run.
+- Decided (D9): every ownership helper raises `Forbidden` (403) for another user's object and
+  `NotFound` (404) for a missing one. Cards T06, T08, T10, T12, T14, T15, T16 say so.
 
 ### Candidate (FP-CAN)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-CAN-1 | Profile and private resume rules | NEEDS DECISION (profile part: the brief's editable profile includes "a display name" and no card lets the candidate edit it, so `save_profile` needs a contract change or a new owner; resume part: the brief requires a raw-text resume and owner-only access, T08 builds PDF upload with employer access) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
-| FP-CAN-2 | Recommendations preserve fields and rank all jobs | NEEDS DECISION (rule quoted; the brief lists "all current (not deleted) jobs", the plan's "closed" job state in T10/T13 hides jobs that are not deleted; also after T11) | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
-| FP-CAN-3 | Pending duplicate and application owner | NEEDS DECISION (status names and re-apply rule differ from T14 defaults) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
+| FP-CAN-1 | Profile and private resume rules | READY (D16: display name editable in `save_profile`; D10: raw-text resume, owner-only, 403 for everyone else) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
+| FP-CAN-2 | Recommendations preserve fields and rank all jobs | READY (D18: no closed state, every job is current; D15: ranking) | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
+| FP-CAN-3 | Pending duplicate and application owner | READY (D11: four statuses, apply once ever) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
 
 Rule text (brief section "3. Candidate workflow"):
 
@@ -101,28 +100,27 @@ Open questions, answered:
 - FP-CAN-1: required profile fields? "a display name and a list of technical skills". Resume file
   types and size limit? NOT IN BRIEF; the required resume is "a raw-text resume", and "PDF upload
   and extraction are optional". Who may see a resume? "only the owning candidate may read or modify
-  them. Any other candidate or employer **MUST** receive `403`". (T08's default of letting an
-  employer with an application open it contradicts this.)
+  them. Any other candidate or employer **MUST** receive `403`". Decided (D10): raw text, one per
+  candidate, owner-only; no employer access. Display name editable (D16).
 - FP-CAN-2: which fields must each recommendation show? "a visible match score", "the job title,
   employer/company, required skills, and a way to view the description". Do zero-score jobs appear?
-  "list all current (not deleted) jobs", so yes. Closed (not deleted) jobs: CONFLICT. The brief's
-  only exclusion is "deleted"; T10's "closed" state and T13's `list_open_jobs` hide jobs that are
-  not deleted. Decision needed before T10 and T13 run (drop "closed", list closed jobs, or document
-  why closed is not "current").
+  "list all current (not deleted) jobs", so yes. Closed (not deleted) jobs: decided (D18), there is
+  no closed state; every job that exists is listed (`list_jobs`).
 - FP-CAN-3: application status list? From FP-EMP-3: "exactly these statuses: `Pending`,
   `Interviewing`, `Rejected`, or `Accepted`". New application: "status `Pending`". Can a candidate
   re-apply after a rejection or withdrawal? "apply to a job once"; "A duplicate application by the
   same candidate to the same job **MUST** be rejected without creating another row". No exception
-  for status is given; "withdrawal" does not exist in the brief. HTTP code for the duplicate: NOT IN
-  BRIEF.
+  for status is given; no other status exists in the brief. Decided (D11): re-applying is refused
+  for any existing application, whatever its status. HTTP code for the duplicate: NOT IN BRIEF;
+  `Conflict`, 409, is DEFAULT.
 
 ### Employer (FP-EMP)
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
 | FP-EMP-1 | Company profile | READY | T09 | `test_emp_company.py::test_fp_emp_1_company_profile` |
-| FP-EMP-2 | Job validation and deletion | NEEDS DECISION (rule quoted; T10's cascade-delete default and "skills 1 to 30" are superseded; steps and tests mention the old default) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
-| FP-EMP-3 | Applicant fields, order, status and role | NEEDS DECISION (rule quoted; T15's order and field defaults superseded; depends on the FP-CAN-3 status-name decision) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
+| FP-EMP-2 | Job validation and deletion | READY (D12: 409 and nothing changed when applications exist, empty skills allowed; D9: 403 for another employer; D18: no closed state) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
+| FP-EMP-3 | Applicant fields, order, status and role | READY (D11: four statuses, any change; D15: order; D10: no resume access) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
 
 Rule text (brief section "4. Employer workflow"):
 
@@ -144,7 +142,9 @@ Open questions, answered:
   required-skills list; the list may be empty". Length limits: NOT IN BRIEF. On delete, what happens
   to its applications and slots? Nothing: "If either kind of dependent record exists, deletion
   **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and
-  dependent records unchanged." (T10's cascade default is wrong.)
+  dependent records unchanged." Decided (D12): `delete_job` raises `Conflict` (409) when any
+  application exists and deletes nothing; slots are employer-owned (D13) so applications are the
+  only dependants.
 - FP-EMP-3: which applicant fields are shown? "candidate identity, skills, match score, application
   status, and interview booking (if any)". Sort order? "sorted by match score from highest to
   lowest"; ties (FP-MATCH-1): "case-insensitive candidate display name and then stable candidate
@@ -155,7 +155,7 @@ Open questions, answered:
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | READY (every rule and example quoted) | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |
+| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | READY (every rule and example quoted; D15) | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |
 
 Rule text (brief section "5. Matching contract", FP-MATCH-1 "Score definition"):
 > The required match score is a deterministic skill-overlap score. Resume text is not an input. Normalize candidate and required skills by trimming surrounding whitespace, converting to lowercase, removing empty values, and removing duplicates. Let `C` and `R` be the resulting candidate-skill and required-skill sets:
@@ -197,9 +197,9 @@ FP-MATCH-2 "Optional AI enhancement" is optional and not planned (full paragraph
 
 | ID | What the template says | Status | Task | Tests |
 |---|---|---|---|---|
-| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rule quoted; T12's "15 to 240 minutes" default superseded by "30-minute") | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
-| FP-SCHED-2 | Eligible and ineligible booking | NEEDS DECISION (rule quoted; the brief scopes slots to "the employer for the candidate's application", T16's steps and tests scope them to the job; also needs the `uq_booking_application` contract change and the status-name decision) | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
-| FP-SCHED-3 | Booking conflict contract | NEEDS DECISION (contract quoted; T17's "same candidate books twice" test needs a decided result, `Forbidden` or `Conflict`; T17 also depends on T16, which is NEEDS DECISION) | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
+| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (D13: employer-owned, exactly 30 minutes, future) | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
+| FP-SCHED-2 | Eligible and ineligible booking | READY (D13: slots scoped to the employer, `uq_booking_application` added; D11: status `interviewing`) | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
+| FP-SCHED-3 | Booking conflict contract | READY (D14: `Conflict("Slot already booked")`, 409; same candidate twice is `Forbidden`) | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
 
 Rule text (brief section "6. Applications and interview scheduling"):
 
@@ -223,25 +223,33 @@ FP-SCHED-3 "Atomic concurrency":
 > When two eligible candidates concurrently attempt to book the same slot, exactly one attempt **MUST** succeed, the other **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message `Slot already booked`, and the database **MUST** contain exactly one booking afterward. Students **MUST** write unit tests for the booking conflict-handling logic. Database atomicity is verified through implementation review and the running system; students are not required to provide a synchronized multi-client test.
 
 Open questions, answered:
-- FP-SCHED-1: slot length limits? "30-minute availability slots"; "reject invalid durations". Can
-  slots overlap for one employer? NOT IN BRIEF. Slots in the past? "future ... slots". Which
-  timezone is shown to whom? NOT IN BRIEF beyond "an exact start and end time with an unambiguous,
-  documented timezone". Can a booked slot be deleted? No: "reject ... deletion of a booked slot".
+- FP-SCHED-1: slot length limits? "30-minute availability slots"; "reject invalid durations".
+  Decided (D13): exactly 30 minutes. Can slots overlap for one employer? NOT IN BRIEF (no overlap
+  is DEFAULT). Slots in the past? "future ... slots". Which timezone is shown to whom? NOT IN BRIEF
+  beyond "an exact start and end time with an unambiguous, documented timezone". Can a booked slot
+  be deleted? No: "reject ... deletion of a booked slot" (409 is DEFAULT).
 - FP-SCHED-2: who is eligible to book? The five bullets quoted above, all true: owns the
   application; slot belongs to that application's employer; status `Interviewing`; slot in the
-  future and not booked; application has no existing booking.
+  future and not booked; application has no existing booking. Decided (D13): slots belong to the
+  employer (no `job_id`), one booking per application (`uq_booking_application`).
 - FP-SCHED-3: two people book the same slot? "exactly one attempt **MUST** succeed, the other
   **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message
   `Slot already booked`, and the database **MUST** contain exactly one booking afterward". One person
   books twice? NOT IN BRIEF as a conflict case; by FP-SCHED-2 the second attempt is ineligible ("the
-  application has no existing booking"). What the losing user sees next: NOT IN BRIEF.
+  application has no existing booking"); decided (D14): `Forbidden`. What the losing user sees next:
+  NOT IN BRIEF; the booking page re-rendered with the message, 409, is DEFAULT.
 
 ### Security (FP-SEC), required unit tests
 
-These four ids are graded and each demands at least one named unit test, but no task card carries
-them as its Requirement. Where they land today: FP-SEC-1 overlaps the T06 sweep; FP-SEC-2 and
-FP-SEC-3 have no owning test name; FP-SEC-4 is covered by `tests/conftest.py` if it uses an isolated
-database. Listed under T-BRIEF's OPEN QUESTIONS.
+| ID | What the brief requires | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-SEC-1 | Object access: the three representative boundaries | READY (D9; assigned by CC01) | T06 | `test_authz_sweep.py::test_fp_sec_1_object_access_boundaries` |
+| FP-SEC-2 | SQL injection: metacharacters stay a bound value | READY (assigned by CC01) | T05 | `test_auth.py::test_fp_sec_2_sql_metacharacters_stay_bound` |
+| FP-SEC-3 | XSS: `<script>alert(1)</script>` is not emitted as markup | READY (assigned by CC01) | T09 | `test_emp_company.py::test_fp_sec_3_script_tag_is_escaped` |
+| FP-SEC-4 | Secrets and test isolation: isolated test database | READY (assigned by CC01) | T01 | `test_db.py::test_fp_sec_4_tests_use_isolated_database` |
+
+These four ids are graded and each demands at least one named unit test. CC01 assigned each to the
+card above (D18); the names are also in `07-CONTRACTS.md`, "Test files and owners".
 
 Rule text (brief section "7. Security requirements"):
 
@@ -272,7 +280,7 @@ FP-SEC-4 "Secrets and test isolation":
 | SPEC.md sections | template SPEC.md | FP-PROC-1 | T21 |
 | INSTALL.md sections, demo accounts, reset command | template INSTALL.md | FP-DOC-1, FP-DOC-3 | T19, T21 |
 | Docker build and start | template Dockerfile | FP-SUB-1 (Dockerfile part) | T20 |
-| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | FP-SEC-1 to FP-SEC-4 | T02, T05, T06, phase 5 |
+| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | FP-SEC-1 to FP-SEC-4 | T01, T02, T05, T06, T09, phase 5 (named tests in the FP-SEC table above) |
 | One command runs all unit tests, nonzero exit on failure | brief section 9 | FP-TEST-1 | `scripts/check.py` |
 | Performance on small fixtures | audit labels `type:performance` | none | `11-TESTING.md`, phase 5 |
 | Optional AI features | template SPEC.md | FP-MATCH-2 | not planned (optional) |
diff --git a/docs/plan/02-ARCHITECTURE.md b/docs/plan/02-ARCHITECTURE.md
index 18a7137..1ce6f25 100644
--- a/docs/plan/02-ARCHITECTURE.md
+++ b/docs/plan/02-ARCHITECTURE.md
@@ -23,7 +23,7 @@ app/
   errors.py              ServiceError classes + HTTP error handlers
   security.py            csrf, security headers, login_required, role_required, rate limit
   audit.py               log_event(conn, actor_id, action, object_type, object_id, detail)
-  timeutil.py            pure: to_utc(), from_utc(), validate_tz()
+  timeutil.py            pure: local_to_utc(), utc_to_local(), validate_tz()
   auth/        routes.py service.py
   candidates/  routes.py service.py        profile, skills, resume
   employers/   routes.py service.py        company profile
@@ -90,27 +90,30 @@ logout POST -> session.clear() -> redirect to sign in
 
 ### Candidate profile and resume (FP-CAN-1)
 ```
-profile form -> candidates.service.save_profile -> upsert candidate_profiles
+profile form (display name, headline, ..., skills) -> candidates.profile_service.save_profile
+  -> UPDATE users.display_name + upsert candidate_profiles, one transaction
 skills field "Python, SQL"  -> normalise_skill() each -> replace candidate_skills rows
-resume upload -> size and type check -> random file name -> save under instance/uploads/
-  -> INSERT resumes (owner_id, stored_name, original_name, size, mime)
-resume download GET /resumes/<id> -> can_view_resume(viewer, resume) -> send_file as attachment
+resume textarea POST /candidate/resume -> resume_service.save_resume(conn, owner_id, body)
+  -> strip, length check -> upsert resumes (owner_id, body, updated_at) -> audit resume.update
+resume view GET /candidates/<candidate_id>/resume -> get_resume_for_viewer(viewer, candidate)
+  -> Forbidden unless viewer is the owner -> NotFound if no resume -> render escaped
 ```
-Resume files are **never** under `static/`. They are only served through the checked route.
+The resume is raw text only (brief FP-CAN-1, D10). No file is written from user input.
 
 ### Jobs and company (FP-EMP-1, FP-EMP-2)
 ```
 company form -> employers.service.save_company -> upsert companies (one per employer)
 job form -> jobs.service.create_job / update_job -> validate -> INSERT jobs + job_skills
-delete POST -> jobs.service.delete_job -> ownership -> rules from brief for linked rows
+delete POST -> jobs.service.delete_job -> NotFound / Forbidden -> count_dependants > 0?
+  -> Conflict (409), nothing changed; else DELETE jobs (job_skills cascade)
 ```
 
 ### Recommendations (FP-CAN-2, FP-MATCH-1)
 ```
 GET /candidate/recommendations
   -> matching.service.recommend_for(conn, candidate_id)
-       -> load candidate skills (normalised) and ALL open jobs with their skills
-       -> matching.engine.rank(candidate_skills, jobs)   pure function, rules from BRIEF
+       -> load candidate skills (normalised) and ALL jobs with their skills (no closed state, D18)
+       -> matching.engine.rank(candidate_skills, jobs)   pure function, brief FP-MATCH-1
        -> return every job with its score and its fields unchanged
   -> template lists them in ranked order
 ```
@@ -118,20 +121,25 @@ GET /candidate/recommendations
 ### Applying and applicants (FP-CAN-3, FP-EMP-3)
 ```
 confirm page (shows exactly what will be sent) -> POST apply
-  -> applications.service.apply -> duplicate pending check -> INSERT applications
-employer applicants page -> applications.service.list_applicants(conn, employer_id, job_id)
-  -> ownership -> ordered per brief -> fields per brief
-status change POST -> applications.service.set_status -> allowed transitions -> audit
+  -> applications.service.apply -> already applied (any status)? Conflict -> INSERT applications
+employer applicants page -> applications.review_service.list_applicants(conn, employer_id, job_id)
+  -> NotFound / Forbidden -> ordered by score desc, name, candidate id -> fields per brief
+status change POST -> applications.review_service.set_status -> any of the four statuses other
+  than the current one -> bookings untouched -> audit
 ```
 
 ### Slots and booking (FP-SCHED)
 ```
-employer slot form (local date, time, timezone) -> timeutil.to_utc -> scheduling.service.create_slot
-candidate booking POST -> scheduling.service.book_slot
+employer slot form (local date, start, end, timezone) -> timeutil.local_to_utc
+  -> scheduling.slots.create_slot(conn, employer_id, ...)   slots belong to the employer, not a job
+  -> exactly 30 minutes, in the future, no overlap with own slots -> INSERT interview_slots
+candidate booking POST -> scheduling.booking.book_slot
   -> BEGIN IMMEDIATE (one writer at a time)
-  -> eligibility check (brief) -> slot still free? -> INSERT bookings (UNIQUE slot_id)
-  -> COMMIT, or on IntegrityError: conflict result defined by the brief
-display -> timeutil.from_utc(utc, viewer_tz)
+  -> the brief's five conditions: owns the application; slot belongs to the employer of the
+     application's job; status interviewing; slot in the future and unbooked; no existing booking
+  -> INSERT bookings (UNIQUE slot_id, UNIQUE application_id)
+  -> COMMIT, or on IntegrityError: Conflict("Slot already booked"), 409, audit booking.conflict
+display -> timeutil.utc_to_local(utc, viewer_tz)
 ```
 
 ## Configuration
@@ -140,8 +148,8 @@ display -> timeutil.from_utc(utc, viewer_tz)
 |---|---|---|
 | `SECRET_KEY` | random per start (sessions end on restart) | session signing key |
 | `DATABASE` | `instance/keystone.sqlite3` | SQLite file path |
-| `UPLOAD_DIR` | `instance/uploads` | resume storage, outside static |
-| `MAX_UPLOAD_MB` | value from brief, else 2 | upload size cap |
+| `UPLOAD_DIR` | `instance/uploads` | (unused since CC01; kept so the Dockerfile and `.env.example` do not change) |
+| `MAX_UPLOAD_MB` | 2 | (unused since CC01; kept so the Dockerfile and `.env.example` do not change) |
 | `PORT` | 8080 | waitress port in Docker |
 
 Tests use `create_app({"TESTING": True, "DATABASE": tmp_path, "UPLOAD_DIR": tmp_path, "SECRET_KEY": "test"})`.
diff --git a/docs/plan/03-DATA-MODEL.md b/docs/plan/03-DATA-MODEL.md
index b54351d..bdc98a3 100644
--- a/docs/plan/03-DATA-MODEL.md
+++ b/docs/plan/03-DATA-MODEL.md
@@ -51,14 +51,11 @@ CREATE TABLE candidate_skills (
 );
 
 CREATE TABLE resumes (
-  id             INTEGER PRIMARY KEY,
-  owner_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
-  stored_name    TEXT NOT NULL UNIQUE,   -- random hex, never user supplied
-  original_name  TEXT NOT NULL,          -- shown only, never used as a path
-  mime_type      TEXT NOT NULL,
-  size_bytes     INTEGER NOT NULL CHECK (size_bytes > 0),
-  uploaded_at    TEXT NOT NULL
+  owner_id    INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
+  body        TEXT NOT NULL,
+  updated_at  TEXT NOT NULL
 );
+-- one raw-text resume per candidate, owner-only (FP-CAN-1, D10)
 
 CREATE TABLE companies (
   id           INTEGER PRIMARY KEY,
@@ -80,7 +77,6 @@ CREATE TABLE jobs (
   employment_type TEXT NOT NULL DEFAULT '',          -- (brief) allowed values
   salary_min   INTEGER,                              -- (brief) required or optional
   salary_max   INTEGER,
-  is_open      INTEGER NOT NULL DEFAULT 1 CHECK (is_open IN (0, 1)),
   created_at   TEXT NOT NULL,
   updated_at   TEXT NOT NULL,
   CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max)
@@ -94,22 +90,23 @@ CREATE TABLE job_skills (
 
 CREATE TABLE applications (
   id            INTEGER PRIMARY KEY,
-  job_id        INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,   -- (brief) delete rule
+  -- FP-EMP-2: deleting a job with applications is refused in the service first (409 Conflict);
+  -- the RESTRICT constraint is the backstop (D12)
+  job_id        INTEGER NOT NULL REFERENCES jobs(id) ON DELETE RESTRICT,
   candidate_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
-  resume_id     INTEGER REFERENCES resumes(id) ON DELETE SET NULL,
-  status        TEXT NOT NULL DEFAULT 'pending',     -- (brief) allowed values
+  -- FP-EMP-3: exactly these four, stored lower-case (D11)
+  status        TEXT NOT NULL DEFAULT 'pending'
+                CHECK (status IN ('pending', 'interviewing', 'rejected', 'accepted')),
   cover_note    TEXT NOT NULL DEFAULT '',
   created_at    TEXT NOT NULL,
   updated_at    TEXT NOT NULL
 );
--- one pending application per candidate per job (FP-CAN-3)
-CREATE UNIQUE INDEX uq_pending_application
-  ON applications (job_id, candidate_id) WHERE status = 'pending';
+-- one application per candidate per job, ever (FP-CAN-3, D11)
+CREATE UNIQUE INDEX uq_application ON applications (job_id, candidate_id);
 
 CREATE TABLE interview_slots (
   id           INTEGER PRIMARY KEY,
-  job_id       INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
-  employer_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+  employer_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,   -- the slot's one owner (FP-SCHED-1, D13)
   starts_at    TEXT NOT NULL,      -- UTC
   ends_at      TEXT NOT NULL,      -- UTC
   created_tz   TEXT NOT NULL,      -- the IANA zone the employer entered it in
@@ -123,8 +120,8 @@ CREATE TABLE bookings (
   application_id  INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
   booked_at       TEXT NOT NULL
 );
--- (brief) if one application may hold only one booking, add:
--- CREATE UNIQUE INDEX uq_booking_application ON bookings (application_id);
+-- one booking per application (FP-SCHED-2 "the application has no existing booking", D13)
+CREATE UNIQUE INDEX uq_booking_application ON bookings (application_id);
 
 CREATE TABLE audit_log (
   id           INTEGER PRIMARY KEY,
@@ -139,7 +136,7 @@ CREATE TABLE audit_log (
 CREATE INDEX ix_jobs_company ON jobs (company_id);
 CREATE INDEX ix_applications_job ON applications (job_id);
 CREATE INDEX ix_applications_candidate ON applications (candidate_id);
-CREATE INDEX ix_slots_job ON interview_slots (job_id, starts_at);
+CREATE INDEX ix_slots_employer ON interview_slots (employer_id, starts_at);
 CREATE INDEX ix_audit_actor ON audit_log (actor_id, created_at);
 ```
 
@@ -148,23 +145,29 @@ CREATE INDEX ix_audit_actor ON audit_log (actor_id, created_at);
 ```
 users (candidate) 1 â”€ 1 candidate_profiles
 users (candidate) 1 â”€ * candidate_skills * â”€ 1 skills
-users (candidate) 1 â”€ * resumes
+users (candidate) 1 â”€ 0..1 resumes
 users (employer)  1 â”€ 1 companies 1 â”€ * jobs 1 â”€ * job_skills * â”€ 1 skills
 jobs 1 â”€ * applications * â”€ 1 users (candidate)
-jobs 1 â”€ * interview_slots 1 â”€ 0..1 bookings * â”€ 1 applications
+users (employer) 1 â”€ * interview_slots 1 â”€ 0..1 bookings 1 â”€ 1 applications
 users 1 â”€ * audit_log
 ```
 
 ## Why these constraints
 
-- `uq_pending_application` makes the duplicate-pending rule (FP-CAN-3) hold even if two requests
-  race. The service still checks first, to give a friendly message.
+- `uq_application` makes the apply-once rule (FP-CAN-3, D11) hold even if two requests race, for
+  every status, so a rejected candidate cannot re-apply. The service still checks first, to give a
+  friendly message.
 - `bookings.slot_id UNIQUE` makes double booking impossible at the database level (FP-SCHED-3).
   The service uses `BEGIN IMMEDIATE` and turns the `IntegrityError` into the brief's conflict result.
-- `stored_name` is random, so a user can never choose a file path (path traversal).
+- `uq_booking_application` makes "the application has no existing booking" (FP-SCHED-2) hold at the
+  database level too.
+- `applications.job_id ON DELETE RESTRICT` is the backstop for FP-EMP-2: `delete_job` refuses with
+  409 first and deletes nothing; if that check were ever bypassed the database still refuses.
+- `resumes.owner_id` is the primary key: one raw-text resume per candidate, replaced in place (D10).
+  No file is ever written from user input.
 
 ## Audit actions (fixed list)
 
-`user.register`, `user.login`, `user.login_failed`, `profile.update`, `resume.upload`,
-`resume.delete`, `company.update`, `job.create`, `job.update`, `job.delete`, `application.submit`,
+`user.register`, `user.login`, `user.login_failed`, `profile.update`, `resume.update`,
+`company.update`, `job.create`, `job.update`, `job.delete`, `application.submit`,
 `application.status`, `slot.create`, `slot.delete`, `booking.create`, `booking.conflict`.

```
