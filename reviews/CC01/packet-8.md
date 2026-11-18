# Review packet CC01 (8 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/tasks/T16.md, docs/tasks/T17.md, docs/tasks/T19.md, docs/tasks/T21.md, scripts/contracts.json

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
diff --git a/docs/tasks/T16.md b/docs/tasks/T16.md
index c85ba85..30c258b 100644
--- a/docs/tasks/T16.md
+++ b/docs/tasks/T16.md
@@ -2,11 +2,12 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | **BLOCKED** (NEEDS DECISION, same as the FP-SCHED-2 row in `01-REQUIREMENTS.md`) for three reasons: (1) the brief's eligibility is employer-level, "the slot belongs to the employer for the candidate's application", while Steps 3-4 and the ineligible test scope slots to the application's job (CONFLICT, see Requirement); (2) the T14 status-name decision (the rule needs the literal `Interviewing`); (3) the `uq_booking_application` index is an unmade contract change |
+| 3 | SCHED + CAN | T12, T14 | yes | READY (after T12, T14; employer-owned slots and one booking per application by D13, statuses by D11, codes by D9) |
 
 ## Goal
-An eligible candidate sees the open slots for their application, in their time zone, and books one
-through a confirm screen. Ineligible candidates cannot book.
+An eligible candidate sees the open slots of the employer behind their application, in their time
+zone, and books one through a confirm screen. Ineligible candidates cannot book, and a refused
+booking writes nothing.
 
 ## Requirement
 FP-SCHED-2: eligible and ineligible booking. Rule text (brief section "6. Applications and
@@ -23,21 +24,20 @@ interview scheduling", FP-SCHED-2 "Booking eligibility"):
 
 Worked examples: none in the brief for FP-SCHED-2.
 
-- Who is eligible: the five bullets above, all true. Status is the literal `Interviewing` (see the
-  T14 CONFLICT on status names).
-- CONFLICT (flagged, not changed; orchestrator decision needed): the brief's rule is "if and only
-  if", and its second bullet is "the slot belongs to the employer for the candidate's application".
-  Step 3 ("slots of the application's job"), Step 4 ("belongs to the same job (`NotFound`)") and the
-  "slot of a different job" case in `test_fp_sched_2_ineligible_booking` all scope the slot to the
-  job, which refuses a booking the brief says **MUST** be allowed (a slot of the same employer on a
-  different job). T12 attaches slots to jobs; whether booking checks the job or the employer is a
-  contract decision, not a card default.
-- Can one application hold more than one booking: no, "the application has no existing booking".
-  Request the `uq_booking_application` index through a contract change before building.
-- Leaving `Interviewing` later: the booking stays and the slot stays unavailable.
-- Refusal code for another candidate's application: `403` (FP-AUTH-3, FP-SEC-1 boundary 3 "a
-  candidate cannot book a slot using another candidate's application"). Step 2 says `NotFound`;
-  flagged, not changed. See T06.
+Decided:
+- Who is eligible: the five bullets above, all true. Status is the stored `interviewing` (shown as
+  `Interviewing`, D11).
+- Slots belong to the employer (D13): a slot is bookable for an application when
+  `interview_slots.employer_id` equals the owner of the application's job's company, whatever job
+  the slot was meant for. Slots carry no job reference.
+- One booking per application: "the application has no existing booking"; enforced by
+  `uq_booking_application` (D13).
+- Leaving `interviewing` later: the booking stays and the slot stays unavailable (T15 never touches
+  bookings).
+- Codes (D9, D14): another candidate's application: `Forbidden` (FP-SEC-1 boundary 3 "a candidate
+  cannot book a slot using another candidate's application"); not `interviewing`, already has a
+  booking, slot of another employer, or slot in the past: `Forbidden`; missing application or
+  slot: `NotFound`; slot already booked by another application: `Conflict("Slot already booked")`.
 
 ## Owns
 - `app/scheduling/booking.py`
@@ -57,23 +57,36 @@ Worked examples: none in the brief for FP-SCHED-2.
 
 ## Contract
 ```python
-def is_eligible(conn, candidate_id: int, application_id: int) -> bool
-def list_bookable_slots(conn, candidate_id: int, application_id: int) -> list[dict]
-def book_slot(conn, candidate_id: int, application_id: int, slot_id: int) -> int
+def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
+    # the brief's five conditions except the slot ones: owns it, status interviewing, no booking yet
+def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
+    # future, unbooked slots of the employer who owns the application's job; start ascending
+def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
+    # NotFound: application or slot missing. Forbidden: application is another candidate's, or
+    # status is not interviewing, or the application already has a booking, or the slot belongs
+    # to another employer. Conflict("Slot already booked"): slot already booked (checked inside
+    # BEGIN IMMEDIATE, and again from sqlite3.IntegrityError). Nothing is written on any failure.
 ```
 Routes: `scheduling.application_detail` GET `/candidate/applications/<int:application_id>`;
 `scheduling.confirm_booking` GET and `scheduling.book` POST
 `/candidate/applications/<int:application_id>/book/<int:slot_id>`, all `@role_required("candidate")`.
 
 ## Steps
-1. Tests first, using the brief's rule and examples.
-2. `is_eligible`: `get_own_application` (raises `NotFound` for others), then the brief's rule.
-3. `list_bookable_slots`: future, unbooked slots of the application's job, start ascending.
-   (CONFLICT: the brief scopes slots to the employer, not the job; see Requirement.)
-4. `book_slot` (simple version; T17 hardens it): own application (`NotFound`), eligible
-   (`Forbidden`), slot exists and belongs to the same job (`NotFound`) (CONFLICT: brief says "belongs
-   to the employer for the candidate's application"; see Requirement), inside
-   `transaction(conn, immediate=True)`: insert booking, audit `booking.create`.
+1. Tests first, using the brief's rule.
+2. `is_eligible`: `get_own_application` (raises `NotFound` for a missing one, `Forbidden` for
+   another candidate's), then the application-side conditions: status is `interviewing` and no
+   `bookings` row for it.
+3. `list_bookable_slots`: the application's job's company owner is the employer; select that
+   employer's slots with `starts_at > now_iso()` and no booking (`LEFT JOIN bookings ... WHERE
+   bookings.id IS NULL`), start ascending. Returns `[]` when `is_eligible` is false.
+4. `book_slot` (simple version; T17 hardens it): `get_own_application` (`NotFound` / `Forbidden`);
+   not `interviewing` or already has a booking: `Forbidden`; slot `SELECT`: no row: `NotFound`;
+   slot's `employer_id` is not the application's employer, or `starts_at <= now_iso()`:
+   `Forbidden`; inside `transaction(conn, immediate=True)`: slot already booked:
+   `Conflict("Slot already booked")`; else insert the booking, audit `booking.create`. On
+   `sqlite3.IntegrityError` from `slot_id UNIQUE` raise the same `Conflict`; from
+   `uq_booking_application` raise `Forbidden`. Every check happens before the insert, so a refused
+   booking writes nothing.
 5. Detail page: application status, then either "Book an interview" with slots shown by
    `format_local(..., candidate timezone from get_profile)` and the zone name, or the booked slot, or
    a line explaining why booking is not open (not eligible).
@@ -81,13 +94,21 @@ Routes: `scheduling.application_detail` GET `/candidate/applications/<int:applic
    `created_tz`, and the job. POST books, redirects to the detail page with a flash.
 
 ## Tests (`tests/unit/test_sched_booking.py`; remove the two FP-SCHED-2 skips, keep FP-SCHED-3 skipped)
-- `test_fp_sched_2_eligible_booking`: eligible candidate books; booking row exists; slot no longer
-  listed as bookable; detail page shows the booked time in the candidate's zone.
-- `test_fp_sched_2_ineligible_booking`: parametrised: status not eligible, another candidate's
-  application, slot of a different job (CONFLICT: under the brief a slot of the same employer's
-  other job is bookable; see Requirement), missing slot, missing application. Each refused with the
-  right error and no booking row.
-- employer GET of the detail page gives 403
+- `test_fp_sched_2_eligible_booking`: candidate with an `interviewing` application books a future
+  unbooked slot of the job's employer (made with `make_slot(employer_id)`); booking row exists; slot
+  no longer listed as bookable; detail page shows the booked time in the candidate's zone; the
+  employer's `list_slots_for_employer` shows it `booked True`.
+- `test_fp_sched_2_ineligible_booking`: parametrised over: status not `interviewing` (`pending`,
+  `rejected`, `accepted`: `Forbidden`), another candidate's application (`Forbidden`), slot of
+  another employer (`Forbidden`), application that already has a booking on a different slot
+  (`Forbidden`), slot in the past (`Forbidden`, make it with `starts_at="2020-01-07T02:00:00Z"`),
+  slot already booked by another application (`Conflict` with message `Slot already booked`),
+  missing slot (`NotFound`), missing application (`NotFound`). Each case asserts the booking count
+  is unchanged afterwards.
+- `list_bookable_slots` never lists a past slot or a booked slot, and does not list another
+  employer's slot
+- employer GET of the detail page gives 403; candidate B GET of A's detail page gives 403;
+  candidate B POST book with A's application gives 403 and no booking row (FP-SEC-1 boundary 3)
 
 ## Done when
 - check and scope pass; then merge review
diff --git a/docs/tasks/T17.md b/docs/tasks/T17.md
index 78a4fc6..f15b507 100644
--- a/docs/tasks/T17.md
+++ b/docs/tasks/T17.md
@@ -2,11 +2,12 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 3 | SCHED | T16, T-BRIEF | no | **BLOCKED** (conflict contract quoted from the brief): (1) the Goal and the last test bullet cover "one person books twice", which the brief does not define as a conflict case; by FP-SCHED-2 the second attempt is ineligible ("the application has no existing booking"), and the result the test must assert (`Forbidden` from the eligibility check, or the `Slot already booked` `Conflict`) is a decision the orchestrator makes against `07-CONTRACTS.md`, not a card default (see Requirement); (2) T16, which this card hardens, is BLOCKED |
+| 3 | SCHED | T16 | no | READY (after T16; conflict contract quoted from the brief; D14) |
 
 ## Goal
-When two people try to book the same slot, or one person books twice, the result is exactly the
-brief's conflict contract, and the database never holds a double booking.
+When two eligible candidates try to book the same slot, exactly one succeeds, the other gets the
+brief's conflict contract (`Slot already booked`, 409), and the database never holds a double
+booking. The same candidate booking twice is refused as ineligible, not as a conflict.
 
 ## Requirement
 FP-SCHED-3: booking conflict contract. Rule text, verbatim (brief section "6. Applications and
@@ -17,18 +18,16 @@ interview scheduling", FP-SCHED-3 "Atomic concurrency"):
 
 Worked examples: none in the brief beyond the scenario in the second paragraph.
 
-- Status code: "HTTP `409` or a clearly documented equivalent".
-- Message or body: the message `Slot already booked` (exact text).
-- What the losing user sees next: NOT IN BRIEF. DEFAULT: re-render `scheduling/book.html` with the
-  message, status 409.
-- Same candidate booking the same slot twice: NOT IN BRIEF as a conflict case. By FP-SCHED-2 the
-  second attempt is ineligible ("the application has no existing booking"), so the brief's own
-  classification is "ineligible booking" (FP-SCHED-2: "Ineligible bookings **MUST** fail without
-  partially changing either record"), not the FP-SCHED-3 conflict. NEEDS DECISION (this is why the
-  card is BLOCKED): the test bullet "gets the contract result (or what the brief says)" needs one
-  decided outcome. The T-BRIEF reviewer proposed `Forbidden` (the error T16 Step 4 raises for an
-  ineligible booking) and cited `07-CONTRACTS.md`; that file is outside this task's May read, so it
-  is recorded here as a proposal, not a DEFAULT. The orchestrator decides and logs it.
+Decided (D14):
+- Status code: HTTP 409.
+- Message: exactly `Slot already booked`, raised as `Conflict("Slot already booked")`.
+- Afterwards: exactly one booking row; a `booking.conflict` audit row written in a separate
+  transaction after the rollback.
+- What the losing user sees next: `scheduling/book.html` re-rendered with the message
+  `Slot already booked` and status 409 (DEFAULT (not in brief)).
+- The same candidate booking the same slot twice is not a conflict case: by FP-SCHED-2 the second
+  attempt is ineligible ("the application has no existing booking") and is refused as `Forbidden`
+  by T16's no-existing-booking condition, with nothing written.
 - Mechanism: "a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an
   equivalent database mechanism"; Step 2's `BEGIN IMMEDIATE` plus the unique index on `slot_id`
   satisfies this. "An in-process check alone is insufficient."
@@ -46,22 +45,36 @@ Worked examples: none in the brief beyond the scenario in the second paragraph.
 - `app/scheduling/booking.py`, `app/scheduling/routes_candidate.py`, `app/db.py`, `app/errors.py`,
   `app/audit.py`, `tests/conftest.py`, `tests/unit/test_sched_booking.py`
 
+## Contract
+`book_slot` as in `07-CONTRACTS.md` (unchanged signature):
+```python
+def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
+    # Conflict("Slot already booked"): slot already booked (checked inside BEGIN IMMEDIATE, and
+    # again from sqlite3.IntegrityError). Nothing is written on any failure.
+```
+Route `scheduling.book` POST: on `Conflict`, render `scheduling/book.html` with the message
+`Slot already booked`, status 409.
+
 ## Steps
 1. Tests first, built from the brief's contract text.
 2. In `book_slot`, inside `transaction(conn, immediate=True)`: re-check the slot is free with a
-   SELECT; if booked: raise `Conflict(<brief message>)`. Also wrap the INSERT: on
-   `sqlite3.IntegrityError` raise the same `Conflict`. Log `booking.conflict` in a **separate** small
-   transaction after the rollback (the first one is rolled back).
-3. Route: catch `Conflict` and return exactly the brief's status code and message (render
-   `scheduling/book.html` with the message, or the format the brief says).
+   SELECT; if booked: raise `Conflict("Slot already booked")`. Also wrap the INSERT: on
+   `sqlite3.IntegrityError` for `bookings.slot_id` raise the same `Conflict`. Log `booking.conflict`
+   in a **separate** small transaction after the rollback (the first one is rolled back).
+3. Route: catch `Conflict` and return status 409 with `scheduling/book.html` re-rendered, the
+   message `Slot already booked` visible in the page.
 
 ## Tests (in `tests/unit/test_sched_booking.py`; remove the FP-SCHED-3 skip)
-- `test_fp_sched_3_conflict_contract`: candidate A books slot S; candidate B (also eligible for the
-  same job) books S: gets the brief's status and message; still exactly one booking row; A's booking
-  unchanged; a `booking.conflict` audit row exists.
+- `test_fp_sched_3_conflict_contract`: candidates A and B both have `interviewing` applications to
+  the same employer's job; A books slot S; B books S: `Conflict` whose message is exactly
+  `Slot already booked`; via the route B gets status 409 and the page contains
+  `Slot already booked`; still exactly one booking row; A's booking unchanged; a
+  `booking.conflict` audit row exists.
 - two connections: open a second `sqlite3` connection to the same file, start `BEGIN IMMEDIATE` on
-  it, insert a booking for S, commit; then `book_slot` on the first connection gives `Conflict`.
-- the same candidate booking the same slot twice gets the contract result (or what the brief says).
+  it, insert a booking for S, commit; then `book_slot` on the first connection gives `Conflict`
+  with message `Slot already booked` and the count stays one.
+- the same candidate booking the same slot twice (or any slot after their first booking) gets
+  `Forbidden`, not `Conflict`, and the booking count stays one.
 
 ## Done when
 - check and scope pass
diff --git a/docs/tasks/T19.md b/docs/tasks/T19.md
index 7bbbaa0..2838e8b 100644
--- a/docs/tasks/T19.md
+++ b/docs/tasks/T19.md
@@ -2,15 +2,27 @@
 
 | Phase | Lane | Depends on | Joins lanes | Status |
 |---|---|---|---|---|
-| 4 | delivery | phase 3 closed | no | READY |
+| 4 | delivery | phase 3 closed | no | READY (after phase 3; seed content by D17) |
 
 ## Goal
 One command resets the app to a known demo state that shows every feature, with the demo accounts
-from `docs/plan/12-DEPLOY.md`.
+from `docs/plan/12-DEPLOY.md`, and satisfies the brief's seed minimum.
+
+## Requirement
+FP-DOC-3 (brief section "9. Documentation, data, tests, and CI", FP-DOC-3 "Deterministic demo
+data"):
+> One documented command **MUST** reset and seed a local database. Seed data **MUST** include at least:
+>
+> - two candidates and two employers;
+> - two jobs with required skills;
+> - the four matching examples required by FP-MATCH-1;
+> - applications covering all four statuses; and
+> - two `Interviewing` candidates eligible to race for the same available slot.
+>
+> Seed credentials **MUST** be clearly marked as local/demo credentials.
 
 ## Owns
 - `scripts/seed.py`
-- `scripts/demo_resume.pdf`
 - `tests/unit/test_seed.py`
 
 ## May read
@@ -20,21 +32,38 @@ from `docs/plan/12-DEPLOY.md`.
 - `app/__init__.py`, `app/db.py`, `tests/conftest.py`
 
 ## Steps
-1. `scripts/seed.py`: `--reset` deletes the database file and the upload folder (paths from the app
-   config, never hard-coded), then `init_db()`. Without `--reset` it refuses if the database already
-   has users. Then it creates the demo data **through the real services** (`register`,
-   `save_profile`, `save_company`, `create_job`, `create_slot`, `apply`, `set_status`), so demo data
-   always obeys the rules. Demo password: `Demo-Keystone-2026` for all four accounts.
-2. Data: the four accounts, 5 jobs with overlapping skills (so ranking and ties show), slots in two
-   time zones, Mei Lin with one application at `interview` status (so booking is possible) and one
-   pending.
-3. `scripts/demo_resume.pdf`: a tiny valid one-page PDF with the text "Demo resume. Fictional person."
-   Attach it to Mei Lin through `save_resume` (wrap the file in `werkzeug.datastructures.FileStorage`).
+1. `scripts/seed.py`: `--reset` deletes the database file (path from the app config, never
+   hard-coded), then `init_db()`. Without `--reset` it refuses if the database already has users.
+   Then it creates the demo data **through the real services** (`register`, `save_profile`,
+   `save_resume`, `save_company`, `create_job`, `create_slot`, `apply`, `set_status`), so demo data
+   always obeys the rules. One demo password, `Demo-Keystone-2026`, for all five accounts, documented
+   as demo-only.
+2. Data, the mandatory minimum (D17, quoting FP-DOC-3 above):
+   - candidates: `meilin@demo.keystone` (skills Python, SQL), `arjun@demo.keystone` (skills
+     Python), `sofia@demo.keystone` (skills Rust); employers `daniel@demo.keystone` (Harbourline
+     Logistics), `priya@demo.keystone` (Tidewater Freight).
+   - jobs: Harbourline "Data Analyst" requires Python, SQL; Tidewater "Graduate Trainee" requires no
+     skills. These give the four FP-MATCH-1 examples: Mei Lin 100, Arjun 50 and Sofia 0 on Data
+     Analyst; everyone 100 on Graduate Trainee. More jobs may be added after these.
+   - applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates
+     eligible to race for one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee
+     `accepted`; Sofia on Graduate Trainee `rejected`.
+   - slots: Daniel has one future 30-minute slot, unbooked, created in `Asia/Hong_Kong`; Priya has
+     one in `Europe/London`. Slot dates must stay in the future: compute them from today (for
+     example 14 days ahead at 10:00 local) rather than hard-coding a date.
+3. Mei Lin's resume: `save_resume(conn, user_id, "Demo resume. Fictional person.")`.
 4. Also expose `seed(app)` so `wsgi.py` can seed a new database on first start.
 
 ## Tests (`tests/unit/test_seed.py`)
-- `seed(app)` on the test app creates exactly 4 users, 5 jobs, and Mei Lin's recommendations are
-  not empty
+- `seed(app)` on the test app creates exactly 5 users (3 candidates, 2 employers), at least 2 jobs
+  including "Data Analyst" (skills `python`, `sql`) and "Graduate Trainee" (no skills), 5
+  applications with statuses covering all four values, exactly 2 `interviewing` applications on
+  Data Analyst, 2 unbooked future slots (one per employer), and Mei Lin's resume text
+- the four FP-MATCH-1 examples come out of `engine.score` on the seeded rows: Mei Lin 100, Arjun 50,
+  Sofia 0 against Data Analyst's skills; each of the three 100 against Graduate Trainee's
+- both `interviewing` candidates are eligible (`booking.is_eligible`) and Daniel's slot is in
+  `list_bookable_slots` for both
+- Mei Lin's recommendations are not empty
 - running it twice without reset refuses and changes nothing
 
 ## Done when
diff --git a/docs/tasks/T21.md b/docs/tasks/T21.md
index 2534bf1..03c5b36 100644
--- a/docs/tasks/T21.md
+++ b/docs/tasks/T21.md
@@ -34,8 +34,12 @@ README maps every requirement to its code and its named tests.
      (for example: rate limiting is per process; sessions end on restart when SECRET_KEY is not set).
 3. SPEC.md: each template section from the plan files: scope (`00`), architecture (`02`), data model
    (`03`), auth (`04`), routes (`07`), UI and workflows (`05`), matching (brief rule + `T11`),
-   scheduling and the booking transaction (brief rule + `T16`, `T17`), security controls (`04`),
-   optional AI features: "Not implemented", design decisions (`docs/state/DECISIONS.md`).
+   scheduling and the booking transaction (brief rule + `T16`, `T17`; cite D10 to D14 from
+   `docs/state/DECISIONS.md`: raw-text owner-only resume, four statuses and apply-once, 409 on
+   deleting a job with applications, employer-owned 30-minute slots with one booking per
+   application, and the `Slot already booked` conflict contract), the resume design (D10), security
+   controls (`04`), optional AI features: "Not implemented", design decisions
+   (`docs/state/DECISIONS.md`).
 4. INSTALL.md: versions from `Dockerfile` and `requirements.lock`; `pip install -r requirements.txt`;
    env vars; `flask --app app init-db`; `python scripts/seed.py --reset`; Docker build and run;
    `python -m flask --app app run --debug`; `python scripts/check.py`; troubleshooting (port in use,
diff --git a/scripts/contracts.json b/scripts/contracts.json
index 91c8b06..68afa62 100644
--- a/scripts/contracts.json
+++ b/scripts/contracts.json
@@ -101,11 +101,10 @@
   },
   "T08": {
     "names": [
+      "app.candidates.resume_service:get_resume",
       "app.candidates.resume_service:save_resume",
-      "app.candidates.resume_service:list_resumes",
-      "app.candidates.resume_service:delete_resume",
-      "app.candidates.resume_service:can_view_resume",
-      "app.candidates.resume_service:get_resume_for_download"
+      "app.candidates.resume_service:get_resume_for_viewer",
+      "app.candidates.resume_service:RESUME_MAX_CHARS"
     ],
     "endpoints": [
       [
@@ -114,14 +113,9 @@
         "/candidate/resume"
       ],
       [
-        "candidates.resume_delete",
-        "POST",
-        "/candidate/resume/<int:resume_id>/delete"
-      ],
-      [
-        "candidates.resume_download",
+        "candidates.resume_view",
         "GET",
-        "/resumes/<int:resume_id>"
+        "/candidates/<int:candidate_id>/resume"
       ]
     ]
   },
@@ -149,10 +143,11 @@
       "app.jobs.service:create_job",
       "app.jobs.service:update_job",
       "app.jobs.service:delete_job",
+      "app.jobs.service:count_dependants",
       "app.jobs.service:get_owned_job",
       "app.jobs.service:get_job",
       "app.jobs.service:list_jobs_for_employer",
-      "app.jobs.service:list_open_jobs",
+      "app.jobs.service:list_jobs",
       "app.jobs.service:EMPLOYMENT_TYPES"
     ],
     "endpoints": [
@@ -205,13 +200,13 @@
       "app.timeutil:COMMON_TIMEZONES",
       "app.scheduling.slots:create_slot",
       "app.scheduling.slots:delete_slot",
-      "app.scheduling.slots:list_slots_for_job"
+      "app.scheduling.slots:list_slots_for_employer"
     ],
     "endpoints": [
       [
         "scheduling.slots",
         "GET POST",
-        "/employer/jobs/<int:job_id>/slots"
+        "/employer/slots"
       ],
       [
         "scheduling.delete_slot",

```
