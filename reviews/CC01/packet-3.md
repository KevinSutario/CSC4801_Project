# Review packet CC01 (3 of 8)

Worktree: C:\Users\sutar\Documents\Y4Sem1\CSC4801 AI-Assisted SWE\ks-CC01

Files in this packet: docs/plan/07-CONTRACTS.md, docs/plan/11-TESTING.md, docs/plan/12-DEPLOY.md, docs/tasks/T01.md

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
diff --git a/docs/plan/07-CONTRACTS.md b/docs/plan/07-CONTRACTS.md
index 2b956eb..1e5363e 100644
--- a/docs/plan/07-CONTRACTS.md
+++ b/docs/plan/07-CONTRACTS.md
@@ -25,13 +25,13 @@ Creates `instance/` and `UPLOAD_DIR` if missing.
 class Config:
     SECRET_KEY: str           # env SECRET_KEY or secrets.token_hex(32)
     DATABASE: str             # env DATABASE or <instance>/keystone.sqlite3
-    UPLOAD_DIR: str           # env UPLOAD_DIR or <instance>/uploads
-    MAX_UPLOAD_MB: int        # env MAX_UPLOAD_MB or 2
+    UPLOAD_DIR: str           # env UPLOAD_DIR or <instance>/uploads (unused since CC01; kept so the Dockerfile and .env.example do not change)
+    MAX_UPLOAD_MB: int        # env MAX_UPLOAD_MB or 2 (unused since CC01, same reason)
     MAX_CONTENT_LENGTH: int   # MAX_UPLOAD_MB * 1024 * 1024
     SESSION_COOKIE_HTTPONLY = True
     SESSION_COOKIE_SAMESITE = "Lax"
     SESSION_COOKIE_SECURE: bool   # env SESSION_COOKIE_SECURE == "1"
-    PERMANENT_SESSION_LIFETIME: timedelta   # 8 hours unless the brief says otherwise
+    PERMANENT_SESSION_LIFETIME: timedelta   # 8 hours, DEFAULT (not in brief)
 ```
 
 ### `app/db.py` (T01)
@@ -89,9 +89,9 @@ def list_events(conn: Conn, actor_id: int, limit: int = 100) -> list[dict]   # n
 ACTIONS: frozenset[str]   # the fixed list in 03-DATA-MODEL.md; log_event raises ValueError otherwise
 ```
 
-### `app/skills.py` (T01 writes a PROVISIONAL version, T11 owns it afterwards)
+### `app/skills.py` (T01 writes it, T11 owns it afterwards and adds tests)
 ```python
-def normalise_skill(raw: str) -> str          # PROVISIONAL: strip, lower-case, collapse spaces
+def normalise_skill(raw: str) -> str          # brief FP-MATCH-1: strip surrounding whitespace, lower-case; nothing else (no inner-space collapsing)
 def parse_skill_list(text: str) -> list[str]  # split on commas, normalise, drop empties, dedupe keeping order
 def get_or_create_skill_ids(conn: Conn, names: list[str]) -> list[int]   # names already normalised
 ```
@@ -116,16 +116,17 @@ Macro signatures are in `06-DESIGN-SYSTEM.md`. Import with
 
 ### `tests/conftest.py` (T01 writes app, client, conn; T04 adds the rest)
 Fixtures: `app`, `client`, `conn`, `make_candidate`, `make_employer`, `make_company`, `make_job`,
-`make_application`, `make_slot`, `login`, `login_as`, `csrf_post`. Signatures:
+`make_application`, `make_slot`, `make_booking`, `login`, `login_as`, `csrf_post`. Signatures:
 ```python
 make_candidate(email="cand@example.com", password="Passw0rd!", name="Mei Lin Tan",
                skills=("python", "sql")) -> int          # user id
 make_employer(email="emp@example.com", password="Passw0rd!", name="Daniel Wong") -> int
 make_company(employer_id: int, name="Harbourline Logistics") -> int
-make_job(employer_id: int, title="Data Analyst", skills=("python",), is_open=1, **cols) -> int
+make_job(employer_id: int, title="Data Analyst", skills=("python",), **cols) -> int
 make_application(candidate_id: int, job_id: int, status="pending") -> int
-make_slot(employer_id: int, job_id: int, starts_at="2030-01-07T02:00:00Z",
-          ends_at="2030-01-07T02:45:00Z", created_tz="UTC") -> int
+make_slot(employer_id: int, starts_at="2030-01-07T02:00:00Z",
+          ends_at="2030-01-07T02:30:00Z", created_tz="UTC") -> int
+make_booking(application_id: int, slot_id: int) -> int
 login(client, email, password) -> Response           # through /auth/login (works after T05)
 login_as(client, user_id: int, role: str) -> None     # sets the session directly, plus a csrf token
 csrf_post(client, url, data: dict, **kwargs) -> Response   # adds the session CSRF token
@@ -156,9 +157,11 @@ def get_user(conn: Conn, user_id: int) -> dict | None
 `app/candidates/profile_service.py`
 ```python
 def get_profile(conn: Conn, candidate_id: int) -> dict
-    # keys: headline, location, timezone, summary, skills (list[str]), updated_at (or None)
-def save_profile(conn: Conn, candidate_id: int, headline: str, location: str,
+    # keys: display_name, headline, location, timezone, summary, skills (list[str]), updated_at (or None)
+def save_profile(conn: Conn, candidate_id: int, display_name: str, headline: str, location: str,
                  timezone: str, summary: str, skills_text: str) -> None
+    # also updates users.display_name in the same transaction (brief FP-CAN-1, D16);
+    # display_name 1 to 80 chars after strip is DEFAULT (not in brief)
 ```
 `app/candidates/routes_profile.py`: `candidates.today` GET `/candidate/`;
 `candidates.profile` GET, POST `/candidate/profile`
@@ -166,16 +169,18 @@ def save_profile(conn: Conn, candidate_id: int, headline: str, location: str,
 ### candidates: resume (T08)
 `app/candidates/resume_service.py`
 ```python
-def save_resume(conn: Conn, upload_dir: str, owner_id: int, file) -> int   # file: werkzeug FileStorage
-def list_resumes(conn: Conn, owner_id: int) -> list[dict]
-def delete_resume(conn: Conn, upload_dir: str, owner_id: int, resume_id: int) -> None
-def can_view_resume(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> bool
-def get_resume_for_download(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> dict
-    # raises NotFound if missing or not allowed
+def get_resume(conn: Conn, owner_id: int) -> dict | None      # keys: owner_id, body, updated_at
+def save_resume(conn: Conn, owner_id: int, body: str) -> None
+    # strip; ValidationError({"body": ...}) if empty or over RESUME_MAX_CHARS; upsert; audit resume.update
+def get_resume_for_viewer(conn: Conn, viewer_id: int, candidate_id: int) -> dict
+    # Forbidden unless viewer_id == candidate_id; then NotFound if that candidate has no resume
+RESUME_MAX_CHARS: int = 20000     # DEFAULT (not in brief)
 ```
-`app/candidates/routes_resume.py`: `candidates.resume` GET, POST `/candidate/resume`;
-`candidates.resume_delete` POST `/candidate/resume/<int:resume_id>/delete`;
-`candidates.resume_download` GET `/resumes/<int:resume_id>`
+`app/candidates/routes_resume.py`: `candidates.resume` GET, POST `/candidate/resume` (candidate
+only: shows the current text in a textarea, POST replaces it); `candidates.resume_view` GET
+`/candidates/<int:candidate_id>/resume` (`@login_required`, any role: the owner sees their text,
+anyone else gets 403 through `get_resume_for_viewer`). Template `candidates/resume.html` only.
+The resume is raw text (brief FP-CAN-1, D10): no files, no download, no delete.
 
 ### employers (T09)
 `app/employers/service.py`
@@ -195,14 +200,22 @@ def create_job(conn: Conn, employer_id: int, title: str, description: str, locat
                employment_type: str, salary_min: str, salary_max: str, skills_text: str) -> int
 def update_job(conn: Conn, employer_id: int, job_id: int, title: str, description: str,
                location: str, employment_type: str, salary_min: str, salary_max: str,
-               skills_text: str, is_open: bool) -> None
+               skills_text: str) -> None
+    # NotFound if missing; Forbidden if another employer's
 def delete_job(conn: Conn, employer_id: int, job_id: int) -> None
-def get_owned_job(conn: Conn, employer_id: int, job_id: int) -> dict    # NotFound if not theirs
+    # NotFound if missing; Forbidden if another employer's; Conflict if the job has any application
+    # (interview slots are employer-owned since CC01, so applications and their bookings are the
+    # only dependants); deletes nothing in that case (brief FP-EMP-2, D12)
+def count_dependants(conn: Conn, job_id: int) -> int    # number of applications on the job
+def get_owned_job(conn: Conn, employer_id: int, job_id: int) -> dict
+    # NotFound if missing; Forbidden if another user's
 def get_job(conn: Conn, job_id: int) -> dict    # with company_name, skills; NotFound if missing
 def list_jobs_for_employer(conn: Conn, employer_id: int) -> list[dict]
-def list_open_jobs(conn: Conn) -> list[dict]    # every open job with company_name and skills
-EMPLOYMENT_TYPES: tuple[str, ...]               # from the brief
+def list_jobs(conn: Conn) -> list[dict]         # every job with company_name and skills (no closed state, D18)
+EMPLOYMENT_TYPES: tuple[str, ...]               # DEFAULT (not in brief)
 ```
+Skills list may be empty: 0 to 30 skills (brief FP-EMP-2 "the list may be empty"; 30 is DEFAULT
+(not in brief)).
 Salary fields arrive as form strings; the service parses them (empty means None).
 `app/jobs/routes.py`: `jobs.my_jobs` GET `/employer/jobs`; `jobs.new` GET, POST `/employer/jobs/new`;
 `jobs.edit` GET, POST `/employer/jobs/<int:job_id>/edit`; `jobs.confirm_delete` GET and
@@ -212,10 +225,12 @@ Salary fields arrive as form strings; the service parses them (empty means None)
 `app/matching/engine.py` (pure: no imports from `app` except `app.skills`)
 ```python
 def score(candidate_skills: set[str], job_skills: set[str]) -> dict
-    # {"score": <number per brief>, "matched": sorted list, "missing": sorted list}
+    # {"score": int, "matched": sorted list, "missing": sorted list}
+    # brief FP-MATCH-1: score = 100 when the job has no skills, else floor(100 * |C âˆ© R| / |R|)
+    # as integer arithmetic: 100 * len(common) // len(required)
 def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]
     # returns NEW dicts: each job's fields unchanged plus score, matched, missing;
-    # sorted by the brief's rule and both tie-breakers; never mutates the input
+    # sorted by score descending, then title.lower(), then id (brief FP-MATCH-1); never mutates the input
 ```
 `app/matching/service.py` (T13)
 ```python
@@ -227,21 +242,35 @@ def score_candidate_for_job(conn: Conn, candidate_id: int, job_id: int) -> dict
 ### applications (T14 candidate side, T15 employer side)
 `app/applications/statuses.py` (T14)
 ```python
-STATUSES: tuple[str, ...]                      # from the brief, first is "pending"
-TRANSITIONS: dict[str, tuple[str, ...]]        # allowed next statuses, from the brief
-LABELS: dict[str, str]                         # status -> display text
+STATUSES: tuple[str, ...] = ("pending", "interviewing", "rejected", "accepted")   # brief FP-EMP-3, stored lower-case
+TRANSITIONS: dict[str, tuple[str, ...]]   # every status -> the other three (brief has no transition rules)
+LABELS: dict[str, str]                    # "pending" -> "Pending", and so on
 ```
 `app/applications/service.py` (T14)
 ```python
-def apply(conn: Conn, candidate_id: int, job_id: int, resume_id: int | None,
-          cover_note: str) -> int
+def apply(conn: Conn, candidate_id: int, job_id: int, cover_note: str) -> int
+    # NotFound if the job is missing; Conflict("You have already applied to this job.") for any
+    # existing application by this candidate to this job, whatever its status (brief FP-CAN-3, D11;
+    # the message is DEFAULT (not in brief)); no row is created in that case
 def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
+    # per row at least: id, job_id, job_title, company_name, status, created_at, booking
+    # where booking is None or {"slot_id", "starts_at", "ends_at"}
 def get_own_application(conn: Conn, candidate_id: int, application_id: int) -> dict
+    # NotFound if missing; Forbidden if another user's
 ```
 `app/applications/review_service.py` (T15)
 ```python
 def list_applicants(conn: Conn, employer_id: int, job_id: int) -> list[dict]
+    # NotFound if the job is missing; Forbidden if another employer's. Each dict has exactly:
+    # application_id, candidate_id, candidate_name, headline, skills (list[str], sorted), score,
+    # matched, missing, status, applied_at, booking (None or {"slot_id", "starts_at", "ends_at"})
+    # sorted by score descending, then display_name.lower(), then candidate_id (brief FP-MATCH-1)
 def set_status(conn: Conn, employer_id: int, application_id: int, new_status: str) -> None
+    # NotFound if missing; Forbidden if the application's job is another employer's;
+    # ValidationError({"status": ...}) unless new_status is in STATUSES and differs from the current
+    # one; never touches bookings (brief FP-SCHED-2: "If a booked application later leaves
+    # `Interviewing`, its booking MUST remain associated with the application and the slot MUST
+    # remain unavailable.")
 ```
 `app/applications/routes_candidate.py` (T14): `applications.confirm` GET and
 `applications.submit` POST `/jobs/<int:job_id>/apply`; `applications.mine` GET `/candidate/applications`
@@ -262,25 +291,38 @@ COMMON_TIMEZONES: tuple[str, ...]                    # for the select box
 `local_to_utc` raises `ValueError` for a local time that does not exist (DST gap): it converts,
 converts back, and compares.
 
-`app/scheduling/slots.py` (T12)
+`app/scheduling/slots.py` (T12). Slots belong to the employer, not to a job (brief FP-SCHED-1
+"one owner", D13).
 ```python
-def create_slot(conn: Conn, employer_id: int, job_id: int, date_str: str, start_str: str,
-                end_str: str, tz_name: str) -> int
+def create_slot(conn: Conn, employer_id: int, date_str: str, start_str: str, end_str: str,
+                tz_name: str) -> int
+    # ValidationError: bad date or time, unknown zone, DST gap, end not after start,
+    # duration not exactly 30 minutes, start not in the future, overlap with the employer's own slot
+    # (overlap rule is DEFAULT (not in brief))
 def delete_slot(conn: Conn, employer_id: int, slot_id: int) -> None
-def list_slots_for_job(conn: Conn, employer_id: int, job_id: int) -> list[dict]   # adds "booked": bool
+    # NotFound if missing; Forbidden if another employer's; Conflict if booked (409 is DEFAULT (not in brief))
+def list_slots_for_employer(conn: Conn, employer_id: int) -> list[dict]   # adds "booked": bool; start ascending
 ```
 `app/scheduling/booking.py` (T16, then T17)
 ```python
 def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
+    # the brief's five conditions except the slot ones: owns it, status interviewing, no booking yet
 def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
+    # future, unbooked slots of the employer who owns the application's job; start ascending
 def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
-    # Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief
+    # NotFound: application or slot missing. Forbidden: application is another candidate's, or
+    # status is not interviewing, or the application already has a booking, or the slot belongs
+    # to another employer. Conflict("Slot already booked"): slot already booked (checked inside
+    # BEGIN IMMEDIATE, and again from sqlite3.IntegrityError). Nothing is written on any failure.
+    # (brief FP-SCHED-2, FP-SCHED-3; D13, D14)
 ```
-`app/scheduling/routes_employer.py` (T12): `scheduling.slots` GET, POST
-`/employer/jobs/<int:job_id>/slots`; `scheduling.delete_slot` POST `/employer/slots/<int:slot_id>/delete`
+`app/scheduling/routes_employer.py` (T12): `scheduling.slots` GET, POST `/employer/slots`;
+`scheduling.delete_slot` POST `/employer/slots/<int:slot_id>/delete`. Template `scheduling/slots.html`.
 `app/scheduling/routes_candidate.py` (T16): `scheduling.application_detail` GET
 `/candidate/applications/<int:application_id>`; `scheduling.confirm_booking` GET and
-`scheduling.book` POST `/candidate/applications/<int:application_id>/book/<int:slot_id>`
+`scheduling.book` POST `/candidate/applications/<int:application_id>/book/<int:slot_id>`.
+On `Conflict` the `scheduling.book` route re-renders `scheduling/book.html` with the message
+`Slot already booked` and status 409 (T17; the re-render is DEFAULT (not in brief)).
 
 ### activity (T18)
 `app/activity/routes.py`: `activity.list` GET `/activity` (signed-in users; own events only)
@@ -301,13 +343,13 @@ Route modules start as stubs (T01): `from . import bp` and nothing else. The own
 
 | File | Owner | Template test names it must contain |
 |---|---|---|
-| `tests/unit/test_db.py` | T01 | none (extra) |
+| `tests/unit/test_db.py` | T01 | none (extra); plus `test_fp_sec_4_tests_use_isolated_database` (FP-SEC-4) |
 | `tests/unit/test_security.py` | T02 | none (extra) |
 | `tests/unit/test_audit.py` | T02 | none (extra) |
-| `tests/unit/test_auth.py` | T04 (placeholders), T05, then T06 | `test_fp_auth_1_registration_and_session_lifecycle`, `test_fp_auth_1_invalid_registration`, `test_fp_auth_2_salted_hash_and_password_verification`, `test_fp_auth_3_authorization_and_missing_object` |
+| `tests/unit/test_auth.py` | T04 (placeholders), T05, then T06 | `test_fp_auth_1_registration_and_session_lifecycle`, `test_fp_auth_1_invalid_registration`, `test_fp_auth_2_salted_hash_and_password_verification`, `test_fp_auth_3_authorization_and_missing_object`; plus `test_fp_sec_2_sql_metacharacters_stay_bound` (T05, FP-SEC-2) |
 | `tests/unit/test_can_profile.py` | T07 | none (extra) |
 | `tests/unit/test_can_resume.py` | T08 | `test_fp_can_1_profile_and_private_resume_rules` |
-| `tests/unit/test_emp_company.py` | T09 | `test_fp_emp_1_company_profile` |
+| `tests/unit/test_emp_company.py` | T09 | `test_fp_emp_1_company_profile`; plus `test_fp_sec_3_script_tag_is_escaped` (FP-SEC-3) |
 | `tests/unit/test_emp_jobs.py` | T10 | `test_fp_emp_2_job_validation_and_deletion` |
 | `tests/unit/test_matching.py` | T11 | `test_fp_match_1_examples_normalization_and_floor`, `test_fp_match_1_both_tie_breakers` |
 | `tests/unit/test_timeutil.py` | T12 | none (extra) |
@@ -317,7 +359,7 @@ Route modules start as stubs (T01): `from . import bp` and nothing else. The own
 | `tests/unit/test_emp_applicants.py` | T15 | `test_fp_emp_3_applicant_fields_order_status_and_role` |
 | `tests/unit/test_sched_booking.py` | T16, then T17 | `test_fp_sched_2_eligible_booking`, `test_fp_sched_2_ineligible_booking`, `test_fp_sched_3_conflict_contract` |
 | `tests/unit/test_activity.py` | T18 | none (extra) |
-| `tests/unit/test_authz_sweep.py` | T06 | none (extra) |
+| `tests/unit/test_authz_sweep.py` | T06 | none (extra); plus `test_fp_sec_1_object_access_boundaries` (FP-SEC-1) |
 
 T04 creates every file in this table that does not exist yet, holding the template test names as
 `@pytest.mark.skip(reason="TODO Txx")` placeholders, and deletes the template's
diff --git a/docs/plan/11-TESTING.md b/docs/plan/11-TESTING.md
index 96d6f24..c9b8662 100644
--- a/docs/plan/11-TESTING.md
+++ b/docs/plan/11-TESTING.md
@@ -48,17 +48,21 @@ def test_fp_emp_2_job_validation_and_deletion(conn, make_employer, make_company)
 |---|---|
 | FP-AUTH-1 | register, then login works, session has user; logout clears it; protected page redirects after logout; invalid email, short password, duplicate email, bad role all rejected with field errors |
 | FP-AUTH-2 | stored hash is not the password; two users with the same password get different hashes; correct password verifies; wrong password does not |
-| FP-AUTH-3 | candidate cannot open employer pages (403); employer A cannot see or edit employer B's job (agreed code); missing id gives 404 |
-| FP-CAN-1 | profile saves and reloads; skills normalised and deduped; resume: wrong type and too-large rejected; owner can download; another candidate cannot; rules from brief for employers |
-| FP-CAN-2 | every open job is returned (count equals open jobs); each keeps all its original fields; order follows the brief; closed jobs excluded if the brief says so |
-| FP-CAN-3 | second pending application to the same job is refused with the brief's result; a candidate cannot read another's application |
+| FP-AUTH-3 | candidate cannot open employer pages (403); employer A cannot see or edit employer B's job (403); missing id gives 404; signed out gives redirect (GET) or 401 |
+| FP-CAN-1 | profile saves and reloads; skills normalised and deduped; resume text saved and replaced; owner can read it; another candidate and an employer get 403 by direct URL |
+| FP-CAN-2 | every job is returned (count equals all jobs); each keeps all its original fields; order equals `engine.rank`; a job with no required skills scores 100 |
+| FP-CAN-3 | second application to the same job is refused with `Conflict` and no new row, even after the first is set to `rejected`; a candidate cannot read another's application (403) |
 | FP-EMP-1 | create, read back, update company; validation errors; one company per employer |
-| FP-EMP-2 | every invalid field rejected; valid job saved with skills; delete removes it and follows the brief for linked rows; cannot delete another employer's job |
-| FP-EMP-3 | applicant rows have exactly the brief's fields, in the brief's order; status change follows allowed transitions; only the job's owner (employer role) can see or change |
+| FP-EMP-2 | every invalid field rejected; empty skills list accepted; valid job saved with skills; delete removes a job with no applications; delete of a job with applications is `Conflict` and leaves the job and its applications unchanged; another employer's job gives 403 |
+| FP-EMP-3 | applicant rows have exactly the contract's keys, sorted by score, name, candidate id; any of the four statuses can be set except the current one; changing status never touches a booking; only the job's owner (employer role) can see or change |
 | FP-MATCH-1 | every brief example exactly; normalisation cases; the floor; each tie-breaker on its own, and both together |
-| FP-SCHED-1 | slot entered in Asia/Hong_Kong stored as correct UTC; shown back correctly in another zone; end before start rejected; nonexistent DST time rejected; delete works; deleting a booked slot follows the brief |
-| FP-SCHED-2 | eligible applicant books; ineligible (wrong status, another job, someone else's application) refused |
-| FP-SCHED-3 | second booking of the same slot gets exactly the brief's conflict result; the database still holds one booking |
+| FP-SCHED-1 | slot entered in Asia/Hong_Kong stored as correct UTC; shown back correctly in another zone; end before start, 29 and 31 minutes, past start, overlap, unknown zone and nonexistent DST time rejected; delete works; deleting a booked slot is `Conflict`; booked slots not listed as available |
+| FP-SCHED-2 | eligible applicant books; ineligible (wrong status, another employer's slot, someone else's application, existing booking, past slot) refused with nothing written |
+| FP-SCHED-3 | second booking of the same slot gets `Conflict("Slot already booked")`, 409; the database still holds exactly one booking; a `booking.conflict` audit row exists |
+| FP-SEC-1 | `test_fp_sec_1_object_access_boundaries` (T06): a candidate cannot read or modify another's resume or application; an employer cannot modify another's job or read its applicants; a candidate cannot book with another's application |
+| FP-SEC-2 | `test_fp_sec_2_sql_metacharacters_stay_bound` (T05): SQL metacharacters in email and display name are stored literally; the users table survives |
+| FP-SEC-3 | `test_fp_sec_3_script_tag_is_escaped` (T09): `<script>alert(1)</script>` in company fields renders as `&lt;script&gt;`; the raw tag never appears |
+| FP-SEC-4 | `test_fp_sec_4_tests_use_isolated_database` (T01): the `app` fixture's `DATABASE` is under `tmp_path` and differs between two tests |
 
 ## Extra test layers (cheap, find the bugs reviewers miss)
 
diff --git a/docs/plan/12-DEPLOY.md b/docs/plan/12-DEPLOY.md
index 33276f2..dd55895 100644
--- a/docs/plan/12-DEPLOY.md
+++ b/docs/plan/12-DEPLOY.md
@@ -6,8 +6,9 @@ fresh clone with no extra steps.
 ## Runtime
 
 - `wsgi.py` creates the app and serves it with waitress on `0.0.0.0:$PORT` (default 8080).
-- On start: create `instance/` and `UPLOAD_DIR`, run `init_db()` if the database file does not
-  exist, then seed demo data if the database is new (so auditors can sign in at once).
+- On start: create `instance/` and `UPLOAD_DIR` (unused since CC01, kept so the Dockerfile does not
+  change), run `init_db()` if the database file does not exist, then seed demo data if the database
+  is new (so auditors can sign in at once).
 - `debug` is never on in Docker.
 
 ## Dockerfile (T20 fills in the template's TODOs)
@@ -28,17 +29,27 @@ docker run --rm -p 8080:8080 keystone
 
 ## Demo data (T19)
 
-`python scripts/seed.py --reset` deletes the database and uploads, recreates the schema, and adds:
+`python scripts/seed.py --reset` deletes the database, recreates the schema, and adds at least the
+minimum the brief requires (FP-DOC-3: "two candidates and two employers; two jobs with required
+skills; the four matching examples required by FP-MATCH-1; applications covering all four statuses;
+and two `Interviewing` candidates eligible to race for the same available slot"). D17:
 
 | Account | Password | Role | Notes |
 |---|---|---|---|
-| `meilin@demo.keystone` | from INSTALL.md | candidate | full profile, Python, SQL, dbt, Tableau, one resume |
-| `arjun@demo.keystone` | from INSTALL.md | candidate | few skills, no resume |
-| `daniel@demo.keystone` | from INSTALL.md | employer | Harbourline Logistics, 3 jobs, slots |
-| `priya@demo.keystone` | from INSTALL.md | employer | Tidewater Freight, 2 jobs |
-
-Demo passwords are documented in INSTALL.md and README "Demo Accounts" because the template asks for
-them. They are demo-only and must not be reused anywhere. All people and companies are fictional.
+| `meilin@demo.keystone` | one demo password, from INSTALL.md | candidate | skills Python, SQL; resume text "Demo resume. Fictional person." |
+| `arjun@demo.keystone` | same | candidate | skills Python |
+| `sofia@demo.keystone` | same | candidate | skills Rust |
+| `daniel@demo.keystone` | same | employer | Harbourline Logistics; job "Data Analyst" requiring Python, SQL; one future 30-minute slot, unbooked, created in `Asia/Hong_Kong` |
+| `priya@demo.keystone` | same | employer | Tidewater Freight; job "Graduate Trainee" requiring no skills; one future 30-minute slot, unbooked, created in `Europe/London` |
+
+Applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates eligible to
+race for Daniel's one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee `accepted`;
+Sofia on Graduate Trainee `rejected`. These give the four FP-MATCH-1 examples: Mei Lin 100, Arjun 50
+and Sofia 0 on Data Analyst; everyone 100 on Graduate Trainee. T19 may add more jobs after these.
+
+One demo password is shared by all five accounts. It is documented in INSTALL.md and README "Demo
+Accounts" because the template asks for them, marked as local/demo-only (FP-DOC-3), and must not be
+reused anywhere. All people and companies are fictional.
 
 ## Release checklist (phase 4 gate)
 
diff --git a/docs/tasks/T01.md b/docs/tasks/T01.md
index f003f95..9f313dc 100644
--- a/docs/tasks/T01.md
+++ b/docs/tasks/T01.md
@@ -82,8 +82,10 @@ Also create empty service modules, each holding only a module docstring naming i
    with `message`.
 5. `app/templates/errors/{400,403,404,405,409,413,500}.html`: minimal plain HTML pages (a heading
    and one sentence, no styling). T03 restyles them later.
-6. `app/skills.py`: the PROVISIONAL versions. Put this comment at the top:
-   `# PROVISIONAL normalisation. T11 replaces normalise_skill with the brief's rule.`
+6. `app/skills.py`: the brief's rule from the start (D18), so no row ever needs re-normalising.
+   `normalise_skill` is "brief FP-MATCH-1: strip surrounding whitespace, lower-case; nothing else
+   (no inner-space collapsing)". `parse_skill_list`: split on commas, normalise, drop empties,
+   dedupe keeping order. T11 owns the file afterwards and adds tests; it does not change the rule.
 7. Blueprint packages, stub route modules, empty service modules, `app/security.py` stub.
 8. `app/__init__.py`: `create_app(test_config=None)`: `Flask(__name__, instance_relative_config=True)`,
    load `Config`, then `test_config` on top, fill default paths, `os.makedirs` for the instance folder
@@ -98,11 +100,20 @@ Also create empty service modules, each holding only a module docstring naming i
 - every table in `03-DATA-MODEL.md` exists after `create_app` (query `sqlite_master`)
 - `PRAGMA foreign_keys` returns 1 on a connection from `get_db()`
 - a write inside `transaction()` that raises is rolled back (row count unchanged)
-- inserting two pending applications for the same job and candidate raises `sqlite3.IntegrityError`
+- inserting two applications for the same job and candidate raises `sqlite3.IntegrityError`
+  (whatever their statuses: `uq_application` has no WHERE clause, D11)
 - inserting two bookings for the same slot raises `sqlite3.IntegrityError`
+- inserting two bookings for the same application raises `sqlite3.IntegrityError`
+  (`uq_booking_application`, D13)
+- deleting a job that has an application raises `sqlite3.IntegrityError` (`ON DELETE RESTRICT`, D12)
 - `now_iso()` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
-- `parse_skill_list(" Python, sql,PYTHON ,, ")` returns `["python", "sql"]`
+- `parse_skill_list(" Python, sql,PYTHON ,, ")` returns `["python", "sql"]`;
+  `normalise_skill("  Data  Science ")` returns `"data  science"` (inner spaces kept, brief FP-MATCH-1)
 - GET `/does-not-exist` returns 404
+- `test_fp_sec_4_tests_use_isolated_database` (FP-SEC-4, brief: "Any test that uses a database
+  **MUST** use an isolated test database"): the `app` fixture's `DATABASE` is under `tmp_path` and
+  differs between two tests (record the path from one test in a module-level variable, compare in
+  the next).
 
 ## Done when
 - `python scripts/check.py` passes, `python scripts/check_scope.py T01` passes

```
