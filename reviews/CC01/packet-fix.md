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

## Fix-round diff (7e800bd..96b0fcf, plan, cards and scripts only), applying reviews/CC01/verdict.md items 1 to 26

```diff
diff --git a/docs/plan/02-ARCHITECTURE.md b/docs/plan/02-ARCHITECTURE.md
index 1ce6f25..30ed693 100644
--- a/docs/plan/02-ARCHITECTURE.md
+++ b/docs/plan/02-ARCHITECTURE.md
@@ -24,14 +24,20 @@ app/
   security.py            csrf, security headers, login_required, role_required, rate limit
   audit.py               log_event(conn, actor_id, action, object_type, object_id, detail)
   timeutil.py            pure: local_to_utc(), utc_to_local(), validate_tz()
+  skills.py              normalise_skill(), parse_skill_list(), get_or_create_skill_ids()
+  core/        routes.py                   landing page
   auth/        routes.py service.py
-  candidates/  routes.py service.py        profile, skills, resume
+  candidates/  routes_profile.py profile_service.py     profile, skills
+               routes_resume.py  resume_service.py      raw-text resume
   employers/   routes.py service.py        company profile
   jobs/        routes.py service.py        job CRUD, job skills
   matching/    engine.py                   pure scoring + ranking (no db)
-               service.py                  loads data, calls engine
-  applications/ routes.py service.py       apply, list, status changes
-  scheduling/  routes.py service.py        slots, bookings
+               service.py routes.py        loads data, calls engine; recommendations page
+  applications/ statuses.py service.py routes_candidate.py      apply, list (candidate side)
+                review_service.py routes_employer.py            applicants, status changes
+  scheduling/  slots.py routes_employer.py                     employer slots
+               booking.py routes_candidate.py                  candidate booking
+  activity/    routes.py                   own audit events
   templates/
     base.html                layout, nav per role, flash messages, csrf meta
     components/              macros: button, card, badge, field, table, empty_state, confirm
@@ -130,9 +136,10 @@ status change POST -> applications.review_service.set_status -> any of the four
 
 ### Slots and booking (FP-SCHED)
 ```
-employer slot form (local date, start, end, timezone) -> timeutil.local_to_utc
-  -> scheduling.slots.create_slot(conn, employer_id, ...)   slots belong to the employer, not a job
-  -> exactly 30 minutes, in the future, no overlap with own slots -> INSERT interview_slots
+employer slot form (local date, start, end, timezone)
+  -> scheduling.slots.create_slot(conn, employer_id, date, start, end, tz)   slots belong to the employer, not a job
+       -> timeutil.local_to_utc for start and end (inside the service, not the route)
+       -> exactly 30 minutes, in the future, no overlap with own slots -> INSERT interview_slots
 candidate booking POST -> scheduling.booking.book_slot
   -> BEGIN IMMEDIATE (one writer at a time)
   -> the brief's five conditions: owns the application; slot belongs to the employer of the
diff --git a/docs/plan/03-DATA-MODEL.md b/docs/plan/03-DATA-MODEL.md
index bdc98a3..050679e 100644
--- a/docs/plan/03-DATA-MODEL.md
+++ b/docs/plan/03-DATA-MODEL.md
@@ -3,9 +3,9 @@
 This is the full schema. Task T01 writes it to `app/schema.sql` exactly. After Phase 1 it is
 **frozen**: a change needs a contract change request (see `09-AGENT-WORKFLOW.md`).
 
-Columns marked **(brief)** have limits or allowed values that come from `docs/BRIEF.md`. T01 uses
-the safe default shown; the task that owns the feature tightens validation in its service, not in
-the schema.
+Columns marked **DEFAULT (not in brief)** have limits or allowed values the brief does not set
+(see `01-REQUIREMENTS.md`). T01 uses the safe default shown; the task that owns the feature
+tightens validation in its service, not in the schema.
 
 ## Conventions
 
@@ -71,11 +71,11 @@ CREATE TABLE companies (
 CREATE TABLE jobs (
   id           INTEGER PRIMARY KEY,
   company_id   INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
-  title        TEXT NOT NULL,                       -- (brief) length limits
+  title        TEXT NOT NULL,                       -- DEFAULT (not in brief) length limits
   description  TEXT NOT NULL,
   location     TEXT NOT NULL DEFAULT '',
-  employment_type TEXT NOT NULL DEFAULT '',          -- (brief) allowed values
-  salary_min   INTEGER,                              -- (brief) required or optional
+  employment_type TEXT NOT NULL DEFAULT '',          -- DEFAULT (not in brief) allowed values
+  salary_min   INTEGER,                              -- DEFAULT (not in brief) optional
   salary_max   INTEGER,
   created_at   TEXT NOT NULL,
   updated_at   TEXT NOT NULL,
diff --git a/docs/plan/04-AUTH-SECURITY.md b/docs/plan/04-AUTH-SECURITY.md
index eeb3c9d..d74c3f4 100644
--- a/docs/plan/04-AUTH-SECURITY.md
+++ b/docs/plan/04-AUTH-SECURITY.md
@@ -36,6 +36,9 @@ The response contract is the brief's FP-AUTH-3 (D9):
 - Ownership helpers (in services): `get_owned_job(conn, employer_id, job_id)`,
   `delete_slot(conn, employer_id, slot_id)`, `get_own_application(conn, candidate_id,
   application_id)`, `get_resume_for_viewer(conn, viewer_id, candidate_id)`.
+- One carve-out: `get_resume_for_viewer` checks `Forbidden` before existence (D10). The resume is
+  keyed by the candidate's user id, so a viewer who is not that candidate gets 403 whether or not a
+  resume row exists; only the owner can ever see 404 (no resume yet). The T06 sweep encodes this.
 
 ## Request security
 
@@ -49,7 +52,7 @@ The response contract is the brief's FP-AUTH-3 (D9):
 | Content sniffing | `X-Content-Type-Options: nosniff` on every response |
 | CSP | `default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'` |
 | Referrer | `Referrer-Policy: same-origin` |
-| Debug leaks | `debug` off in Docker. Error handlers render plain pages for 400, 403, 404, 413, 500 without tracebacks. |
+| Debug leaks | `debug` off in Docker. Error handlers render plain pages for 400, 403, 404, 405, 409, 413, 500 without tracebacks. |
 | Secrets | `SECRET_KEY` from env only. Never committed. `.env` stays gitignored. |
 | Mass assignment | Services take named fields only. Never `**request.form`. `role` is never editable after sign-up. |
 | Integer ids | Route converters `<int:job_id>`, so non-numbers give 404. |
diff --git a/docs/plan/05-UX-FLOWS.md b/docs/plan/05-UX-FLOWS.md
index 5864ab4..6a2d87a 100644
--- a/docs/plan/05-UX-FLOWS.md
+++ b/docs/plan/05-UX-FLOWS.md
@@ -83,8 +83,9 @@ range (or "Not stated"), score shown as a number plus a 5-segment bar, "Matched:
 "Missing: dbt". Every job appears, including weak matches (brief FP-CAN-2: "all current (not
 deleted) jobs"; there is no closed state, D18). Ranking and tie-breaks are the brief's FP-MATCH-1.
 
-**Applicants table** (FP-EMP-3): candidate name, headline, match score, matched skills, applied
-date (shown in the employer's timezone), status badge, booking time (if any), actions. Sorted by
+**Applicants table** (FP-EMP-3): candidate name, headline, match score, skills (with matched and
+missing as the score explanation), applied date (shown in UTC, DEFAULT (not in brief)), status
+badge, booking time (if any), actions. Sorted by
 score descending, then case-insensitive display name, then candidate id (brief FP-MATCH-1).
 
 **Confirm application** (Keystone approval pattern): a box titled "This will be sent to
@@ -105,10 +106,13 @@ your other applications." Buttons: primary "Submit application", secondary "Back
 
 | Where | Text | Action |
 |---|---|---|
-| Recommendations, no skills | "Add your skills to see how jobs match you." | Edit profile |
 | Recommendations, no jobs | "No jobs right now. Check back soon." | none |
 | My applications | "You have not applied to any jobs yet." | See recommendations |
 | My jobs | "You have not posted a job yet." | Post a job |
 | Applicants | "No one has applied to this job yet." | none |
 | Slots | "No interview slots yet. Add one so applicants can book." | Add slot |
 | Activity | "Nothing here yet. Actions you take will show up here." | none |
+
+Not an empty state: a candidate with no skills still sees the full ranked list (brief FP-CAN-2
+"all current (not deleted) jobs"; every job scores 0 or 100 for them). The hint "Add your skills to
+see how jobs match you." (with an Edit profile link) is shown **above** the list, never instead of it.
diff --git a/docs/plan/07-CONTRACTS.md b/docs/plan/07-CONTRACTS.md
index 1e5363e..1f65ffd 100644
--- a/docs/plan/07-CONTRACTS.md
+++ b/docs/plan/07-CONTRACTS.md
@@ -64,6 +64,8 @@ def init_app(app: Flask) -> None
     # also handles HTTP 400, 403, 404, 405, 413, 500 with errors/<code>.html
 ```
 Routes catch `ValidationError` themselves and re-render the form with status 400.
+Every POST form includes `csrf_field()` (04-AUTH-SECURITY.md, "Request security"); no route skips
+the CSRF check.
 
 ### `app/security.py` (T02)
 ```python
@@ -249,9 +251,10 @@ LABELS: dict[str, str]                    # "pending" -> "Pending", and so on
 `app/applications/service.py` (T14)
 ```python
 def apply(conn: Conn, candidate_id: int, job_id: int, cover_note: str) -> int
-    # NotFound if the job is missing; Conflict("You have already applied to this job.") for any
-    # existing application by this candidate to this job, whatever its status (brief FP-CAN-3, D11;
-    # the message is DEFAULT (not in brief)); no row is created in that case
+    # NotFound if the job is missing; ValidationError({"cover_note": ...}) if the stripped note is
+    # over 2000 chars (DEFAULT (not in brief)); Conflict("You have already applied to this job.")
+    # for any existing application by this candidate to this job, whatever its status (brief
+    # FP-CAN-3, D11; the message is DEFAULT (not in brief)); no row is created in any of those cases
 def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
     # per row at least: id, job_id, job_title, company_name, status, created_at, booking
     # where booking is None or {"slot_id", "starts_at", "ends_at"}
@@ -306,14 +309,17 @@ def list_slots_for_employer(conn: Conn, employer_id: int) -> list[dict]   # adds
 `app/scheduling/booking.py` (T16, then T17)
 ```python
 def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
-    # the brief's five conditions except the slot ones: owns it, status interviewing, no booking yet
+    # loads the application with get_own_application (NotFound if missing, Forbidden if another
+    # candidate's), then returns True only if status is interviewing and it has no booking yet
 def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
     # future, unbooked slots of the employer who owns the application's job; start ascending
 def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
     # NotFound: application or slot missing. Forbidden: application is another candidate's, or
     # status is not interviewing, or the application already has a booking, or the slot belongs
-    # to another employer. Conflict("Slot already booked"): slot already booked (checked inside
-    # BEGIN IMMEDIATE, and again from sqlite3.IntegrityError). Nothing is written on any failure.
+    # to another employer, or the slot is in the past. Conflict("Slot already booked"): slot
+    # already booked (checked inside BEGIN IMMEDIATE, and again from sqlite3.IntegrityError).
+    # No booking row is written on any failure; on Conflict a booking.conflict audit row is
+    # written in a separate transaction after the rollback (D14).
     # (brief FP-SCHED-2, FP-SCHED-3; D13, D14)
 ```
 `app/scheduling/routes_employer.py` (T12): `scheduling.slots` GET, POST `/employer/slots`;
diff --git a/docs/plan/12-DEPLOY.md b/docs/plan/12-DEPLOY.md
index dd55895..d686984 100644
--- a/docs/plan/12-DEPLOY.md
+++ b/docs/plan/12-DEPLOY.md
@@ -40,12 +40,16 @@ and two `Interviewing` candidates eligible to race for the same available slot")
 | `arjun@demo.keystone` | same | candidate | skills Python |
 | `sofia@demo.keystone` | same | candidate | skills Rust |
 | `daniel@demo.keystone` | same | employer | Harbourline Logistics; job "Data Analyst" requiring Python, SQL; one future 30-minute slot, unbooked, created in `Asia/Hong_Kong` |
-| `priya@demo.keystone` | same | employer | Tidewater Freight; job "Graduate Trainee" requiring no skills; one future 30-minute slot, unbooked, created in `Europe/London` |
+| `priya@demo.keystone` | same | employer | Tidewater Freight; jobs "Logistics Coordinator" requiring SQL, Excel and "Graduate Trainee" requiring no skills; one future 30-minute slot, unbooked, created in `Europe/London` |
+
+Jobs (three mandatory): Harbourline "Data Analyst" requires Python, SQL; Tidewater "Logistics
+Coordinator" requires SQL, Excel (so "two jobs with required skills" holds on any reading of
+FP-DOC-3); Tidewater "Graduate Trainee" requires no skills. T19 may add more jobs after these.
 
 Applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates eligible to
 race for Daniel's one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee `accepted`;
 Sofia on Graduate Trainee `rejected`. These give the four FP-MATCH-1 examples: Mei Lin 100, Arjun 50
-and Sofia 0 on Data Analyst; everyone 100 on Graduate Trainee. T19 may add more jobs after these.
+and Sofia 0 on Data Analyst; everyone 100 on Graduate Trainee.
 
 One demo password is shared by all five accounts. It is documented in INSTALL.md and README "Demo
 Accounts" because the template asks for them, marked as local/demo-only (FP-DOC-3), and must not be
diff --git a/docs/tasks/T01.md b/docs/tasks/T01.md
index 9f313dc..086b9b3 100644
--- a/docs/tasks/T01.md
+++ b/docs/tasks/T01.md
@@ -111,9 +111,10 @@ Also create empty service modules, each holding only a module docstring naming i
   `normalise_skill("  Data  Science ")` returns `"data  science"` (inner spaces kept, brief FP-MATCH-1)
 - GET `/does-not-exist` returns 404
 - `test_fp_sec_4_tests_use_isolated_database` (FP-SEC-4, brief: "Any test that uses a database
-  **MUST** use an isolated test database"): the `app` fixture's `DATABASE` is under `tmp_path` and
-  differs between two tests (record the path from one test in a module-level variable, compare in
-  the next).
+  **MUST** use an isolated test database"): the `app` fixture's `DATABASE` is under `tmp_path`;
+  and, self-contained in one test, two apps built with `create_app` on `tmp_path / "a"` and
+  `tmp_path / "b"` have different `DATABASE` paths and a row inserted through one is absent from
+  the other (no module-level state, no dependence on test order).
 
 ## Done when
 - `python scripts/check.py` passes, `python scripts/check_scope.py T01` passes
diff --git a/docs/tasks/T04.md b/docs/tasks/T04.md
index 49d01bc..0fb537e 100644
--- a/docs/tasks/T04.md
+++ b/docs/tasks/T04.md
@@ -78,6 +78,11 @@ Jobs have no open/closed flag (D18) and slots belong to the employer, not to a j
    ```
    with the owner task in the reason. In `test_auth.py` and `test_matching.py` replace the template's
    `pass` bodies this way. Create the other files with a module docstring naming the owner task.
+   The "plus" FP-SEC names in that table (`test_fp_sec_2_sql_metacharacters_stay_bound` in
+   `test_auth.py`, `test_fp_sec_3_script_tag_is_escaped` in `test_emp_company.py`,
+   `test_fp_sec_1_object_access_boundaries` in `test_authz_sweep.py`) get placeholders the same way;
+   the exception is `test_fp_sec_4_tests_use_isolated_database`, which T01 writes directly in
+   `tests/unit/test_db.py` (not in this card's Owns).
 7. Delete `tests/unit/test_workflows.py` and `tests/unit/test_scheduling.py` after their names exist
    in the new files.
 8. `tests/unit/test_conftest.py`: each factory works twice in one test (`make_booking` twice needs
diff --git a/docs/tasks/T05.md b/docs/tasks/T05.md
index 3ecb56b..647d0b5 100644
--- a/docs/tasks/T05.md
+++ b/docs/tasks/T05.md
@@ -67,7 +67,7 @@ Routes: `auth.register` GET/POST `/auth/register`, `auth.login` GET/POST `/auth/
 6. Logout: `session.clear()`, flash "Signed out", redirect to `/auth/login`.
 7. Signed-in users opening register or login are redirected to `/`.
 
-## Tests (`tests/unit/test_auth.py`; remove the skip on these four, keep the FP-AUTH-3 placeholder)
+## Tests (`tests/unit/test_auth.py`; remove the skip on these five, keep the FP-AUTH-3 placeholder)
 - `test_fp_auth_1_registration_and_session_lifecycle`: register via the form, session has
   `user_id`; logout; session empty; login again; GET `/` redirects by role.
 - `test_fp_auth_1_invalid_registration`: parametrised: bad email, empty email, short password,
@@ -77,9 +77,9 @@ Routes: `auth.register` GET/POST `/auth/register`, `auth.login` GET/POST `/auth/
   starts with a known Werkzeug method prefix; two users with the same password have different
   hashes; `authenticate` true for right, None for wrong password and for unknown email.
 - `test_fp_sec_2_sql_metacharacters_stay_bound` (FP-SEC-2): register and then authenticate with
-  the email `x'); DROP TABLE users; --@example.com` and the display name
-  `Robert'); DELETE FROM users; --`; afterwards the `users` table still exists (query
-  `sqlite_master`) and holds the rows; the literal strings are stored unchanged (email lower-cased).
+  the email `x');drop--table@example.com` (no whitespace, so it passes the email rule above) and
+  the display name `Robert'); DELETE FROM users; --`; afterwards the `users` table still exists
+  (query `sqlite_master`) and holds the row; the literal strings are stored unchanged.
 - extra: login with `next=//evil.com` redirects to `/`; with `next=/candidate/profile` goes there.
 - extra: 6th bad login for the same email gives 429.
 - extra: logout via GET gives 405; logout POST without token gives 403.
diff --git a/docs/tasks/T06.md b/docs/tasks/T06.md
index 9f249db..8f9f2e9 100644
--- a/docs/tasks/T06.md
+++ b/docs/tasks/T06.md
@@ -54,10 +54,17 @@ codes, so a different code is a hole in that feature, not a disagreement about t
    page itself is `/employer/slots` with no id since D13; it belongs in step 3.)
 2. `test_authz_sweep.py`: one parametrised test over that list. For each route: user B (same role)
    with A's id: 403; right role, missing id (999999): 404; wrong role: 403; signed out: redirect
-   (GET) or 401 (other methods). Use factories and `login_as`. POSTs use `csrf_post`. For
-   `jobs.detail` and `candidates.resume_view` (any signed-in role) the "wrong role" case does not
-   apply; `candidates.resume_view` with another user's id is 403 for both a candidate and an
-   employer.
+   (GET) or 401 (other methods). Use factories and `login_as`. POSTs use `csrf_post`. Exceptions
+   the sweep must encode:
+   - `candidates.resume_view` gives 403 for any id that is not the caller's own, **including a
+     missing id** (Forbidden is checked before existence, D10; `07-CONTRACTS.md`
+     `get_resume_for_viewer`, T08). Its missing-id case is therefore 403, not 404, and it is 403 for
+     both a candidate and an employer.
+   - `jobs.detail`, `applications.confirm` and `applications.submit` have no owner (any signed-in
+     user may view any job; any candidate may apply to any job), so "user B with A's id" is 200,
+     200 and 302 (after a successful submit) respectively, not 403. Their missing-id case stays 404.
+   - For `jobs.detail` and `candidates.resume_view` (any signed-in role) the "wrong role" case does
+     not apply.
 3. A second parametrised test: every route without a path parameter, wrong role gives 403 and signed
    out redirects or 401.
 4. `test_fp_sec_1_object_access_boundaries` in `test_authz_sweep.py` (FP-SEC-1): the brief's three
diff --git a/docs/tasks/T09.md b/docs/tasks/T09.md
index bf8a85f..4887d0a 100644
--- a/docs/tasks/T09.md
+++ b/docs/tasks/T09.md
@@ -48,8 +48,9 @@ Routes: `employers.home` GET `/employer/`, `employers.company` GET/POST `/employ
    `company.update`, return the company id.
 3. Company page: the form, with the website shown as plain text (never as an unescaped link).
 4. Home page: if no company, a card "Create your company profile to post jobs" with a button to
-   `/employer/company`. Otherwise company name and links to `/employer/jobs` and "Post a job"
-   `/employer/jobs/new`. T10 owns those pages.
+   `/employer/company`. Otherwise company name and links to `/employer/jobs`, "Post a job"
+   `/employer/jobs/new`, and "Interview slots" `/employer/slots`. T10 and T12 own those pages; T12
+   only consumes the slots link (this card owns `employers/home.html`, so the link is added here).
 
 ## Tests (`tests/unit/test_emp_company.py`; remove the skip on the template test)
 - `test_fp_emp_1_company_profile`: create, read back, update (same id), every validation error,
@@ -58,9 +59,10 @@ Routes: `employers.home` GET `/employer/`, `employers.company` GET/POST `/employ
 - candidate GET `/employer/company` gives 403
 - POST through the form works and redirects with a flash
 - `test_fp_sec_3_script_tag_is_escaped` (FP-SEC-3): save a company whose name and description are
-  both `<script>alert(1)</script>`; GET `/employer/company` and GET `/employer/` render them as
-  `&lt;script&gt;alert(1)&lt;/script&gt;` and the raw string `<script>alert(1)</script>` never
-  appears in either response body
+  both `<script>alert(1)</script>`; GET `/employer/company` renders both (name and description) as
+  `&lt;script&gt;alert(1)&lt;/script&gt;`; GET `/employer/` renders the name that way (the home shows
+  the name only, Step 4); the raw string `<script>alert(1)</script>` never appears in either response
+  body
 
 ## Done when
 - check and scope pass
diff --git a/docs/tasks/T10.md b/docs/tasks/T10.md
index 6777f91..b7f64de 100644
--- a/docs/tasks/T10.md
+++ b/docs/tasks/T10.md
@@ -72,9 +72,11 @@ is `@role_required("employer")`. `jobs.detail` is `@login_required` and shows an
 
 ## Steps
 1. Tests first.
-2. A private `_validate(...)` returns cleaned values or raises `ValidationError` with all field
-   errors. Salary: empty string means None; otherwise `int()` inside `try`; reject non-numbers.
-   `parse_skill_list` may return an empty list; that is valid.
+2. A private `_validate(...)` strips `title`, `description` and `location` before validation (so a
+   whitespace-only title is empty and fails "non-empty"), then returns cleaned values or raises
+   `ValidationError` with all field errors. Salary: empty string means None; otherwise `int()`
+   inside `try`; reject non-numbers, negatives and values over 10_000_000. `parse_skill_list` may
+   return an empty list; that is valid.
 3. `create_job`: employer must have a company (`ValidationError({"company": "Create your company
    profile first."})`). Insert job and `job_skills` in one transaction. Audit `job.create`.
 4. `get_owned_job`: `SELECT ... FROM jobs JOIN companies ... WHERE jobs.id = ?`; no row: `NotFound`;
@@ -91,14 +93,17 @@ is `@role_required("employer")`. `jobs.detail` is `@login_required` and shows an
 9. Routes and templates: list (with empty state), form (new and edit share `jobs/form.html`), a
    confirm-delete page that says either "This job has no applications and can be deleted" with the
    delete button, or "This job has N applications and cannot be deleted" with no delete button;
+   `jobs.edit` GET and `jobs.confirm_delete` GET load the job with `get_owned_job` (so another
+   employer's job is 403 and a missing one 404 on the GET too, not only on the POST);
    `jobs.delete` POST on a job with applications returns 409 (let `Conflict` reach the error
    handler, or re-render the confirm page with status 409); detail page with skills as badges (or
    "No specific skills required") and a link "Apply to this job" to `/jobs/<id>/apply` (T14 builds
-   it).
+   it). Every POST form includes `csrf_field()` (04-AUTH-SECURITY.md).
 
 ## Tests (`tests/unit/test_emp_jobs.py`; remove the skip on the template test)
-- `test_fp_emp_2_job_validation_and_deletion`: parametrised invalid inputs (empty title, empty
-  description, over-long fields, bad salary, min > max, 31 skills) each give the right field error
+- `test_fp_emp_2_job_validation_and_deletion`: parametrised invalid inputs (empty title,
+  whitespace-only title, empty description, over-long fields, bad salary, negative salary, salary
+  over 10_000_000, min > max, 31 skills) each give the right field error
   and no row; a valid job saved with normalised skills; a job with an empty skills list is saved
   with no `job_skills` rows; delete removes a job with no applications (and its `job_skills`);
   delete of a job with an application raises `Conflict`, and afterwards the job row, its skills and
@@ -111,6 +116,9 @@ is `@role_required("employer")`. `jobs.detail` is `@login_required` and shows an
 - detail of any job: owner 200, another employer 200, a candidate 200; missing job 404
 - `jobs.delete` POST for a job with an application returns 409 and the job still exists; employer
   B POST gives 403
+- employer B GET of A's edit page and of A's confirm-delete page gives 403; a missing job id gives
+  404 on both
+- the new-job and edit forms and the confirm-delete form each contain the hidden `csrf_token` input
 - the confirm-delete page shows "cannot be deleted" and no delete button when applications exist
 - candidate POST to `/employer/jobs/new` gives 403
 
diff --git a/docs/tasks/T12.md b/docs/tasks/T12.md
index 51243dd..479ec84 100644
--- a/docs/tasks/T12.md
+++ b/docs/tasks/T12.md
@@ -68,8 +68,9 @@ def list_slots_for_employer(conn: Conn, employer_id: int) -> list[dict]   # adds
 ```
 Routes `scheduling.slots` GET/POST `/employer/slots`, `scheduling.delete_slot` POST
 `/employer/slots/<int:slot_id>/delete`, both `@role_required("employer")`. Template
-`scheduling/slots.html`. The page is linked from the employer home (`employers.home`, T09 owns that
-template; add the link there only if T09 has not, otherwise report it).
+`scheduling/slots.html`. The page is reached from the employer home: T09 adds the "Interview slots"
+link to `/employer/slots` in `employers/home.html` (T09 owns that template); this card only consumes
+it and never edits a T09 file.
 
 No job ownership query: slots are not attached to jobs. Do not import `app.jobs.service`.
 
@@ -90,8 +91,11 @@ No job ownership query: slots are not attached to jobs. Do not import `app.jobs.
 5. `list_slots_for_employer`: one query with `LEFT JOIN bookings`, `booked` as bool, ordered by
    `starts_at`.
 6. Page: add-slot form (date, start, end, time zone select defaulting to the employer's last used
-   zone or UTC), list in the chosen zone using `format_local` ("Mon 30 Nov, 10:00 to 10:30
-   (Asia/Hong_Kong)"), delete button only on unbooked slots, booked ones marked "Booked".
+   zone or UTC), list in the chosen zone with a range label such as "Mon 30 Nov, 10:00 to 10:30
+   (Asia/Hong_Kong)", composed in the template from two `utc_to_local` calls (start and end) plus
+   the zone name; `format_local` stays a single-time formatter and is not used for the range.
+   Delete button only on unbooked slots, booked ones marked "Booked". Every POST form (add slot,
+   delete slot) includes `csrf_field()` (04-AUTH-SECURITY.md).
 
 ## Tests
 `tests/unit/test_timeutil.py`:
@@ -113,6 +117,7 @@ No job ownership query: slots are not attached to jobs. Do not import `app.jobs.
 - an overlapping slot of a different employer is allowed
 - candidate POST to `/employer/slots` gives 403; employer B POST delete on A's slot gives 403;
   missing slot id gives 404
+- the slots page contains the hidden `csrf_token` input in the add-slot form
 
 ## Done when
 - check and scope pass
diff --git a/docs/tasks/T13.md b/docs/tasks/T13.md
index 634e6ec..8b313ba 100644
--- a/docs/tasks/T13.md
+++ b/docs/tasks/T13.md
@@ -51,7 +51,10 @@ Route `matching.recommendations` GET `/candidate/recommendations`, `@role_requir
 2. `recommend_for`: `set(get_profile(conn, candidate_id)["skills"])`, `list_jobs(conn)`, `rank`.
 3. `score_candidate_for_job`: `get_job` (NotFound if missing), then `engine.score`.
 4. Page: one card per job in the returned order, `score_bar`, "Matched:" and "Missing:" lists,
-   link to `/jobs/<id>`. Empty states from `05-UX-FLOWS.md` (no skills; no jobs).
+   link to `/jobs/<id>`. The only empty state is "no jobs" (`05-UX-FLOWS.md`). A candidate with no
+   skills still sees the full ranked list (brief FP-CAN-2 "all current (not deleted) jobs"); the
+   hint "Add your skills to see how jobs match you." with an Edit profile link is shown **above**
+   the list in addition to it, never instead of it.
 
 ## Tests (`tests/unit/test_can_recommend.py`; remove the skip)
 - `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs`: 6 jobs from two employers,
@@ -59,7 +62,8 @@ Route `matching.recommendations` GET `/candidate/recommendations`, `@role_requir
   with the same value; order equals `engine.rank` on the same input; a zero-overlap job is still
   present; the job with no required skills scores 100.
 - page shows jobs in the same order as the service (check the titles' positions in the HTML)
-- candidate with no skills sees the empty-state text
+- candidate with no skills sees the hint text **and** every job title (the list is not replaced by
+  the hint; the job with no required skills shows 100 and the others 0)
 - employer GET gives 403
 
 ## Done when
diff --git a/docs/tasks/T14.md b/docs/tasks/T14.md
index 8f08dad..3a10e6c 100644
--- a/docs/tasks/T14.md
+++ b/docs/tasks/T14.md
@@ -45,11 +45,12 @@ job.")`, HTTP 409; cover note max 2000 chars.
 
 ## May read
 - `CLAUDE.md`
-- `docs/plan/07-CONTRACTS.md` (sections: applications, jobs, scheduling)
+- `docs/plan/07-CONTRACTS.md` (sections: applications, jobs, scheduling, candidates: profile)
 - `docs/plan/05-UX-FLOWS.md` (sections: Confirm application, Empty states)
 - `docs/plan/03-DATA-MODEL.md` (tables: applications and its unique index, bookings, interview_slots)
-- `app/jobs/service.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
-  `app/applications/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
+- `app/jobs/service.py`, `app/timeutil.py`, `app/candidates/profile_service.py`, `app/audit.py`,
+  `app/db.py`, `app/errors.py`, `app/applications/__init__.py`, `app/templates/components/*`,
+  `tests/conftest.py`
 
 ## Contract
 ```python
@@ -60,8 +61,10 @@ LABELS: dict[str, str]                    # "pending" -> "Pending", and so on
 
 # app/applications/service.py
 def apply(conn: Conn, candidate_id: int, job_id: int, cover_note: str) -> int
-    # NotFound if the job is missing; Conflict("You have already applied to this job.") for any
-    # existing application by this candidate to this job, whatever its status; no row in that case
+    # NotFound if the job is missing; ValidationError({"cover_note": ...}) if the stripped note is
+    # over 2000 chars (DEFAULT (not in brief)); Conflict("You have already applied to this job.")
+    # for any existing application by this candidate to this job, whatever its status; no row in
+    # any of those cases
 def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
     # per row at least: id, job_id, job_title, company_name, status, created_at, booking
     # where booking is None or {"slot_id", "starts_at", "ends_at"}
@@ -84,7 +87,9 @@ Routes: `applications.confirm` GET and `applications.submit` POST `/jobs/<int:jo
    first.
 5. Confirm page uses `confirm_box`: the job and company, the cover note field, and "This will be
    sent to <company>: your name, your skills, your cover note. Not shared: your resume, your email
-   address, your other applications." Primary button "Submit application".
+   address, your other applications." Primary button "Submit application". Every POST form
+   includes `csrf_field()` (04-AUTH-SECURITY.md). A `ValidationError` on the cover note re-renders
+   the confirm page with the field error and status 400.
 6. Submit: success redirects to `/candidate/applications` with flash "Application sent to <company>";
    `Conflict` re-renders the confirm page with the message and status 409.
 7. Mine page: table with job, company, date, status badge (`LABELS`), booking time when there is
@@ -98,10 +103,15 @@ Routes: `applications.confirm` GET and `applications.submit` POST `/jobs/<int:jo
   candidate B calling `get_own_application` on A's raises `Forbidden`; a missing id raises
   `NotFound`.
 - applying to a missing job: `NotFound` from the service and 404 via the route
+- a 2001-character cover note: `ValidationError` with key `cover_note` from the service, 400 via the
+  route, and no application row; a 2000-character note is accepted
+- the confirm page contains the hidden `csrf_token` input
 - `STATUSES == ("pending", "interviewing", "rejected", "accepted")`; `LABELS` gives the brief's
   spellings; `TRANSITIONS[s]` is the other three for every `s`
 - `list_for_candidate` returns `booking None` without a booking and `{"slot_id", "starts_at",
   "ends_at"}` after `make_booking`; the mine page shows the booking time
+- non-UTC render: with the candidate's profile timezone set to `Asia/Hong_Kong` and a booking on
+  the default `make_slot` (`2030-01-07T02:00:00Z`), the mine page shows `10:00 (Asia/Hong_Kong)`
 - the confirm page shows the company name and the privacy lines, and no resume field
 - the route for a duplicate returns 409
 - employer POST to apply gives 403; candidate B GET `/candidate/applications/<A's id>` is 403 (T16's
diff --git a/docs/tasks/T15.md b/docs/tasks/T15.md
index c2ce9a7..6e9cb57 100644
--- a/docs/tasks/T15.md
+++ b/docs/tasks/T15.md
@@ -87,7 +87,10 @@ field), all `@role_required("employer")`.
 4. Applicants page: table (fields above; date with `format_local` in UTC; booking shown as its
    time or "No interview booked"), one link per other status to the confirm page. No resume link.
 5. Confirm-status page: `confirm_box` "Change <name>'s application from <Old> to <New>?" using
-   `LABELS`, POST form.
+   `LABELS`, POST form carrying `to` as a hidden field. Every POST form includes `csrf_field()`
+   (04-AUTH-SECURITY.md). On the GET, a `to` that is missing, not in `STATUSES`, or equal to the
+   current status renders `errors/400.html` with status 400 (there is no form to re-render on a GET;
+   DEFAULT (not in brief)). Ownership (`NotFound` / `Forbidden`) is checked on the GET too.
 
 ## Tests (`tests/unit/test_emp_applicants.py`; remove the skip)
 - `test_fp_emp_3_applicant_fields_order_status_and_role`: three applicants with different and equal
@@ -103,6 +106,9 @@ field), all `@role_required("employer")`.
 - after `make_booking` on an `interviewing` application, `set_status` to `rejected` leaves the
   booking row unchanged and the slot still booked (FP-SCHED-2)
 - query count stays fixed for 30 applicants (`set_trace_callback`)
+- `applications.confirm_status` GET with no `to`, with `to=bogus`, and with `to` equal to the
+  current status each return 400; with a valid `to` it returns 200 and the page contains the hidden
+  `csrf_token` input; employer B GET gives 403; a missing application id gives 404
 - the applicants page shows no resume link and shows the booking time for a booked applicant
 
 ## Done when
diff --git a/docs/tasks/T16.md b/docs/tasks/T16.md
index 30c258b..2d19506 100644
--- a/docs/tasks/T16.md
+++ b/docs/tasks/T16.md
@@ -58,14 +58,17 @@ Decided:
 ## Contract
 ```python
 def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
-    # the brief's five conditions except the slot ones: owns it, status interviewing, no booking yet
+    # loads the application with get_own_application (NotFound if missing, Forbidden if another
+    # candidate's), then returns True only if status is interviewing and it has no booking yet
 def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
     # future, unbooked slots of the employer who owns the application's job; start ascending
 def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
     # NotFound: application or slot missing. Forbidden: application is another candidate's, or
     # status is not interviewing, or the application already has a booking, or the slot belongs
-    # to another employer. Conflict("Slot already booked"): slot already booked (checked inside
-    # BEGIN IMMEDIATE, and again from sqlite3.IntegrityError). Nothing is written on any failure.
+    # to another employer, or the slot is in the past. Conflict("Slot already booked"): slot
+    # already booked (checked inside BEGIN IMMEDIATE, and again from sqlite3.IntegrityError).
+    # No booking row is written on any failure; on Conflict a booking.conflict audit row is
+    # written in a separate transaction after the rollback (D14).
 ```
 Routes: `scheduling.application_detail` GET `/candidate/applications/<int:application_id>`;
 `scheduling.confirm_booking` GET and `scheduling.book` POST
@@ -74,8 +77,9 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
 ## Steps
 1. Tests first, using the brief's rule.
 2. `is_eligible`: `get_own_application` (raises `NotFound` for a missing one, `Forbidden` for
-   another candidate's), then the application-side conditions: status is `interviewing` and no
-   `bookings` row for it.
+   another candidate's; these propagate, the function never returns False for them), then returns
+   a bool for the application-side conditions only: status is `interviewing` and no `bookings` row
+   for it.
 3. `list_bookable_slots`: the application's job's company owner is the employer; select that
    employer's slots with `starts_at > now_iso()` and no booking (`LEFT JOIN bookings ... WHERE
    bookings.id IS NULL`), start ascending. Returns `[]` when `is_eligible` is false.
@@ -91,7 +95,8 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
    `format_local(..., candidate timezone from get_profile)` and the zone name, or the booked slot, or
    a line explaining why booking is not open (not eligible).
 6. Confirm page: `confirm_box` with the time in the candidate's zone and in the employer's
-   `created_tz`, and the job. POST books, redirects to the detail page with a flash.
+   `created_tz`, and the job. POST books, redirects to the detail page with a flash. Every POST form
+   includes `csrf_field()` (04-AUTH-SECURITY.md).
 
 ## Tests (`tests/unit/test_sched_booking.py`; remove the two FP-SCHED-2 skips, keep FP-SCHED-3 skipped)
 - `test_fp_sched_2_eligible_booking`: candidate with an `interviewing` application books a future
@@ -109,6 +114,9 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
   employer's slot
 - employer GET of the detail page gives 403; candidate B GET of A's detail page gives 403;
   candidate B POST book with A's application gives 403 and no booking row (FP-SEC-1 boundary 3)
+- `is_eligible` raises `NotFound` for a missing application and `Forbidden` for another
+  candidate's (it does not return False for those)
+- the confirm-booking page contains the hidden `csrf_token` input
 
 ## Done when
 - check and scope pass; then merge review
diff --git a/docs/tasks/T17.md b/docs/tasks/T17.md
index f15b507..7bfcf21 100644
--- a/docs/tasks/T17.md
+++ b/docs/tasks/T17.md
@@ -49,8 +49,11 @@ Decided (D14):
 `book_slot` as in `07-CONTRACTS.md` (unchanged signature):
 ```python
 def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
+    # Forbidden list unchanged from T16 (another candidate's application, status not interviewing,
+    # existing booking, slot of another employer, slot in the past).
     # Conflict("Slot already booked"): slot already booked (checked inside BEGIN IMMEDIATE, and
-    # again from sqlite3.IntegrityError). Nothing is written on any failure.
+    # again from sqlite3.IntegrityError). No booking row is written on any failure; on Conflict a
+    # booking.conflict audit row is written in a separate transaction after the rollback (D14).
 ```
 Route `scheduling.book` POST: on `Conflict`, render `scheduling/book.html` with the message
 `Slot already booked`, status 409.
diff --git a/docs/tasks/T19.md b/docs/tasks/T19.md
index 2838e8b..9d169f4 100644
--- a/docs/tasks/T19.md
+++ b/docs/tasks/T19.md
@@ -42,9 +42,11 @@ data"):
    - candidates: `meilin@demo.keystone` (skills Python, SQL), `arjun@demo.keystone` (skills
      Python), `sofia@demo.keystone` (skills Rust); employers `daniel@demo.keystone` (Harbourline
      Logistics), `priya@demo.keystone` (Tidewater Freight).
-   - jobs: Harbourline "Data Analyst" requires Python, SQL; Tidewater "Graduate Trainee" requires no
-     skills. These give the four FP-MATCH-1 examples: Mei Lin 100, Arjun 50 and Sofia 0 on Data
-     Analyst; everyone 100 on Graduate Trainee. More jobs may be added after these.
+   - jobs (three mandatory): Harbourline "Data Analyst" requires Python, SQL; Tidewater "Logistics
+     Coordinator" requires SQL, Excel (so "two jobs with required skills" holds on any reading);
+     Tidewater "Graduate Trainee" requires no skills. These give the four FP-MATCH-1 examples: Mei
+     Lin 100, Arjun 50 and Sofia 0 on Data Analyst; everyone 100 on Graduate Trainee. More jobs may
+     be added after these.
    - applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates
      eligible to race for one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee
      `accepted`; Sofia on Graduate Trainee `rejected`.
@@ -55,8 +57,9 @@ data"):
 4. Also expose `seed(app)` so `wsgi.py` can seed a new database on first start.
 
 ## Tests (`tests/unit/test_seed.py`)
-- `seed(app)` on the test app creates exactly 5 users (3 candidates, 2 employers), at least 2 jobs
-  including "Data Analyst" (skills `python`, `sql`) and "Graduate Trainee" (no skills), 5
+- `seed(app)` on the test app creates exactly 5 users (3 candidates, 2 employers), at least 3 jobs
+  including "Data Analyst" (skills `python`, `sql`), "Logistics Coordinator" (skills `sql`,
+  `excel`) and "Graduate Trainee" (no skills), so at least two jobs have a non-empty skills list; 5
   applications with statuses covering all four values, exactly 2 `interviewing` applications on
   Data Analyst, 2 unbooked future slots (one per employer), and Mei Lin's resume text
 - the four FP-MATCH-1 examples come out of `engine.score` on the seeded rows: Mei Lin 100, Arjun 50,
```

## Check output (orchestrator ran it)

CHECK PASSED; SCOPE OK for CC01
