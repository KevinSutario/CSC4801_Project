# Review packet phase-0 (5 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/plan/03-DATA-MODEL.md, docs/plan/04-AUTH-SECURITY.md, docs/plan/05-UX-FLOWS.md

## Review type: phase 0

Compare: 4b825dc642cb6eb9a060e54bf8d69288fbee4904..dev

## Requirements

# 01 · Requirements

Every graded requirement, where its rule text lives, which task builds it, and which tests prove it.

## Status legend

- **READY**: enough is known to build it. Exact limits still come from `docs/BRIEF.md` if the brief
  states them.
- **BLOCKED**: the rule is defined only in the brief, and the brief has not been pasted in yet.
  No agent may write logic for a BLOCKED item. Tasks that need it stop at the test-writing step.

## How to unblock

1. Paste the full course brief into `docs/BRIEF.md`, keeping its headings and requirement IDs.
2. For each row below, copy the exact rule sentence(s) into the "Rule text" column.
3. Answer the open questions listed for that row, using only the brief.
4. Change the status to READY and log it in `docs/state/DECISIONS.md`.

## Requirement table

The test names come from the course template. Keep them exactly. Tests live in per-task files
(`07-CONTRACTS.md`, "Test files and owners") so parallel lanes never edit the same test file.

### Accounts (FP-AUTH)

| ID | What the template says | Status | Task | Tests |
|---|---|---|---|---|
| FP-AUTH-1 | Registration and session lifecycle; invalid registration | READY (limits from brief) | T05 | `test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`, `::test_fp_auth_1_invalid_registration` |
| FP-AUTH-2 | Salted hash and password verification | READY | T05 | `test_auth.py::test_fp_auth_2_salted_hash_and_password_verification` |
| FP-AUTH-3 | Authorization and missing object | READY (status codes from brief) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |

Open questions for the brief:
- FP-AUTH-1: allowed roles at sign-up? Password length and rules? Email format rules? Session lifetime?
- FP-AUTH-3: for another user's object, return 403 or 404? For a missing object, 404?

### Candidate (FP-CAN)

| ID | What the template says | Status | Task | Tests |
|---|---|---|---|---|
| FP-CAN-1 | Profile and private resume rules | READY (limits from brief) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
| FP-CAN-2 | Recommendations preserve fields and rank all jobs | BLOCKED on FP-MATCH-1 | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
| FP-CAN-3 | Pending duplicate and application owner | READY (statuses from brief) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |

Open questions:
- FP-CAN-1: required profile fields? Resume file types and size limit? Who may see a resume
  (only the owner, or also employers the candidate applied to)?
- FP-CAN-2: which fields must each recommendation show? Do zero-score jobs appear?
- FP-CAN-3: application status list? Can a candidate re-apply after a rejection or withdrawal?

### Employer (FP-EMP)

| ID | What the template says | Status | Task | Tests |
|---|---|---|---|---|
| FP-EMP-1 | Company profile | READY | T09 | `test_emp_company.py::test_fp_emp_1_company_profile` |
| FP-EMP-2 | Job validation and deletion | READY (limits from brief) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
| FP-EMP-3 | Applicant fields, order, status and role | READY (order from brief) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |

Open questions:
- FP-EMP-2: required job fields and limits? On delete, what happens to its applications and slots?
- FP-EMP-3: which applicant fields are shown? Sort order? Which status changes are allowed?

### Matching (FP-MATCH)

| ID | What the template says | Status | Task | Tests |
|---|---|---|---|---|
| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | **BLOCKED** | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |

Open questions (the brief must answer every one before T11 starts):
- How is a skill normalised (case, whitespace, punctuation, synonyms)?
- What is the score formula (overlap count, fraction of job skills, Jaccard)?
- What is "the floor" (a minimum score, or rounding down)?
- What are the two tie-breakers, in order?
- Do the brief's worked examples exist? Copy every one, inputs and expected outputs, verbatim.

### Scheduling (FP-SCHED)

| ID | What the template says | Status | Task | Tests |
|---|---|---|---|---|
| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rules from brief) | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
| FP-SCHED-2 | Eligible and ineligible booking | **BLOCKED** | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
| FP-SCHED-3 | Booking conflict contract | **BLOCKED** | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |

Open questions:
- FP-SCHED-1: slot length limits? Can slots overlap for one employer? Slots in the past? Which
  timezone is shown to whom? Can a booked slot be deleted?
- FP-SCHED-2: who is eligible to book (an application in which status, for which job)?
- FP-SCHED-3: exactly what happens when two people book the same slot, or one person books twice?
  What status code and message? This is a "contract", so the brief likely states it word for word.

### Non-functional and delivery

| Item | Source | Task |
|---|---|---|
| README requirement-test table | template README | T21 |
| SPEC.md sections | template SPEC.md | T21 |
| INSTALL.md sections, demo accounts, reset command | template INSTALL.md | T19, T21 |
| Docker build and start | template Dockerfile | T20 |
| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | T02, T05, T06, phase 5 |
| Performance on small fixtures | audit labels `type:performance` | `11-TESTING.md`, phase 5 |
| Optional AI features | template SPEC.md | not planned (optional) |


## Changed files (whole phase)

```
 .claude/agents/implementer.md                    |  49 ++
 .claude/agents/review-judge.md                   |  61 +++
 .claude/agents/reviewer.md                       |  56 ++
 .claude/skills/bugfix/SKILL.md                   |  18 +
 .claude/skills/dispatch/SKILL.md                 |  35 ++
 .claude/skills/merge/SKILL.md                    |  28 +
 .claude/skills/orient/SKILL.md                   |  24 +
 .claude/skills/phase-gate/SKILL.md               |  19 +
 .claude/skills/review-task/SKILL.md              |  36 ++
 .dockerignore                                    |   9 +
 .env.example                                     |   5 +
 .github/ISSUE_TEMPLATE/audit_bug_report.yml      |  58 ++
 .github/labels.yml                               |  38 ++
 .gitignore                                       |  17 +
 CLAUDE.md                                        |  83 +++
 Dockerfile                                       |  20 +
 INSTALL.md                                       |  21 +
 README.md                                        |  31 ++
 SPEC.md                                          |  23 +
 claude-setup/agents/implementer.md               |  49 ++
 claude-setup/agents/review-judge.md              |  61 +++
 claude-setup/agents/reviewer.md                  |  56 ++
 claude-setup/skills/bugfix/SKILL.md              |  18 +
 claude-setup/skills/dispatch/SKILL.md            |  35 ++
 claude-setup/skills/merge/SKILL.md               |  28 +
 claude-setup/skills/orient/SKILL.md              |  24 +
 claude-setup/skills/phase-gate/SKILL.md          |  19 +
 claude-setup/skills/review-task/SKILL.md         |  36 ++
 docs/BRIEF.md                                    |  12 +
 docs/plan/00-OVERVIEW.md                         |  70 +++
 docs/plan/01-REQUIREMENTS.md                     | 100 ++++
 docs/plan/02-ARCHITECTURE.md                     | 147 +++++
 docs/plan/03-DATA-MODEL.md                       | 170 ++++++
 docs/plan/04-AUTH-SECURITY.md                    |  85 +++
 docs/plan/05-UX-FLOWS.md                         | 115 ++++
 docs/plan/06-DESIGN-SYSTEM.md                    | 113 ++++
 docs/plan/07-CONTRACTS.md                        | 324 +++++++++++
 docs/plan/08-TASKS.md                            | 118 ++++
 docs/plan/09-AGENT-WORKFLOW.md                   | 154 ++++++
 docs/plan/10-REVIEW-PROTOCOL.md                  | 147 +++++
 docs/plan/11-TESTING.md                          |  78 +++
 docs/plan/12-DEPLOY.md                           |  48 ++
 docs/state/BUGS.md                               |  29 +
 docs/state/DECISIONS.md                          |  35 ++
 docs/state/JOURNAL.md                            |  45 ++
 docs/state/STATUS.md                             |  47 ++
 docs/tasks/B1.md                                 |  44 ++
 docs/tasks/B2.md                                 |  58 ++
 docs/tasks/T-BRIEF.md                            |  57 ++
 docs/tasks/T00.md                                |  29 +
 docs/tasks/T01.md                                | 114 ++++
 docs/tasks/T02.md                                |  74 +++
 docs/tasks/T03.md                                |  69 +++
 docs/tasks/T04.md                                |  75 +++
 docs/tasks/T05.md                                |  81 +++
 docs/tasks/T06.md                                |  44 ++
 docs/tasks/T07.md                                |  68 +++
 docs/tasks/T08.md                                |  77 +++
 docs/tasks/T09.md                                |  56 ++
 docs/tasks/T10.md                                |  63 +++
 docs/tasks/T11.md                                |  72 +++
 docs/tasks/T12.md                                |  71 +++
 docs/tasks/T13.md                                |  53 ++
 docs/tasks/T14.md                                |  67 +++
 docs/tasks/T15.md                                |  63 +++
 docs/tasks/T16.md                                |  66 +++
 docs/tasks/T17.md                                |  48 ++
 docs/tasks/T18.md                                |  44 ++
 docs/tasks/T19.md                                |  41 ++
 docs/tasks/T20.md                                |  41 ++
 docs/tasks/T21.md                                |  47 ++
 docs/tasks/T22.md                                |  34 ++
 docs/tasks/TEMPLATE.md                           |  37 ++
 pytest.ini                                       |   3 +
 requirements-dev.txt                             |   3 +
 requirements.lock                                |  19 +
 requirements.txt                                 |   3 +
 reviews/B1/implementer.md                        |  54 ++
 reviews/B1/packet-1.md                           | 206 +++++++
 reviews/B1/r1.md                                 |   3 +
 reviews/B1/r2.md                                 |   3 +
 reviews/B1/r3.md                                 |   3 +
 reviews/B1/verdict.md                            |  11 +
 reviews/B2/implementer.md                        |  54 ++
 reviews/B2/packet-1.md                           | 297 ++++++++++
 reviews/B2/r1.md                                 |   3 +
 reviews/B2/r2.md                                 |   3 +
 reviews/B2/r3.md                                 |   3 +
 reviews/B2/verdict.md                            |  11 +
 reviews/README.md                                |   7 +
 reviews/T00/implementer.md                       |  30 ++
 reviews/T00/orchestrator-check.md                |  22 +
 reviews/T00/packet-1.md                          |  91 ++++
 reviews/T00/r1.md                                |   3 +
 reviews/T00/r2.md                                |   3 +
 reviews/T00/r3.md                                |   3 +
 reviews/T00/verdict.md                           |  11 +
 reviews/merge-B1/packet-1.md                     | 206 +++++++
 reviews/merge-B1/r1.md                           |   3 +
 reviews/merge-B1/r2.md                           |   3 +
 reviews/merge-B1/r3.md                           |   3 +
 reviews/merge-B1/verdict.md                      |  12 +
 reviews/merge-B2/packet-1.md                     | 297 ++++++++++
 reviews/merge-B2/r1.md                           |   3 +
 reviews/merge-B2/r2.md                           |   3 +
 reviews/merge-B2/r3.md                           |   3 +
 reviews/merge-B2/repro/test_b1_b2_integration.py |  98 ++++
 reviews/merge-B2/verdict.md                      |  14 +
 reviews/merge-T00/orchestrator-check.md          |  25 +
 reviews/merge-T00/packet-1.md                    |  91 ++++
 reviews/merge-T00/r1.md                          |   3 +
 reviews/merge-T00/r2.md                          |   3 +
 reviews/merge-T00/r3.md                          |   3 +
 reviews/merge-T00/verdict.md                     |  11 +
 reviews/phase-0/check-round2.md                  |  20 +
 reviews/phase-0/check.md                         |  25 +
 reviews/phase-0/packet-1.md                      | 653 ++++++++++++++++++++++
 reviews/phase-0/packet-10.md                     | 653 ++++++++++++++++++++++
 reviews/phase-0/packet-11.md                     | 625 +++++++++++++++++++++
 reviews/phase-0/packet-12.md                     | 627 ++++++++++++++++++++++
 reviews/phase-0/packet-13.md                     | 635 ++++++++++++++++++++++
 reviews/phase-0/packet-14.md                     | 600 +++++++++++++++++++++
 reviews/phase-0/packet-15.md                     | 591 ++++++++++++++++++++
 reviews/phase-0/packet-16.md                     | 656 +++++++++++++++++++++++
 reviews/phase-0/packet-17.md                     | 621 +++++++++++++++++++++
 reviews/phase-0/packet-18.md                     | 383 +++++++++++++
 reviews/phase-0/packet-19.md                     | 630 ++++++++++++++++++++++
 reviews/phase-0/packet-2.md                      | 608 +++++++++++++++++++++
 reviews/phase-0/packet-20.md                     | 619 +++++++++++++++++++++
 reviews/phase-0/packet-3.md                      | 656 +++++++++++++++++++++++
 reviews/phase-0/packet-4.md                      | 593 ++++++++++++++++++++
 reviews/phase-0/packet-5.md                      | 646 ++++++++++++++++++++++
 reviews/phase-0/packet-6.md                      | 377 +++++++++++++
 reviews/phase-0/packet-7.md                      | 588 ++++++++++++++++++++
 reviews/phase-0/packet-8.md                      | 542 +++++++++++++++++++
 reviews/phase-0/packet-9.md                      | 654 ++++++++++++++++++++++
 reviews/phase-0/r1-round1.md                     |  99 ++++
 reviews/phase-0/r1.md                            |  99 ++++
 reviews/phase-0/r2-round1.md                     | 109 ++++
 reviews/phase-0/r2.md                            | 109 ++++
 reviews/phase-0/r3-round1.md                     |  99 ++++
 reviews/phase-0/r3.md                            |  99 ++++
 reviews/phase-0/repro/mutation-results.md        |  21 +
 reviews/phase-0/repro/test_g1.py                 |  26 +
 reviews/phase-0/verdict-round1.md                |  24 +
 reviews/phase-0/verdict.md                       |  24 +
 ruff.toml                                        |  11 +
 scripts/check.py                                 |  65 +++
 scripts/check_contracts.py                       |  97 ++++
 scripts/check_scope.py                           | 119 ++++
 scripts/contracts.json                           | 324 +++++++++++
 scripts/install_claude_setup.py                  |  36 ++
 scripts/make_packet.py                           | 169 ++++++
 tests/__init__.py                                |   0
 tests/unit/__init__.py                           |   0
 tests/unit/test_auth.py                          |  17 +
 tests/unit/test_check.py                         |  76 +++
 tests/unit/test_check_scope.py                   |  72 +++
 tests/unit/test_make_packet.py                   |  78 +++
 tests/unit/test_matching.py                      |   9 +
 tests/unit/test_scheduling.py                    |  21 +
 tests/unit/test_workflows.py                     |  25 +
 162 files changed, 19847 insertions(+)

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
diff --git a/docs/plan/03-DATA-MODEL.md b/docs/plan/03-DATA-MODEL.md
new file mode 100644
index 0000000..b54351d
--- /dev/null
+++ b/docs/plan/03-DATA-MODEL.md
@@ -0,0 +1,170 @@
+# 03 · Data model
+
+This is the full schema. Task T01 writes it to `app/schema.sql` exactly. After Phase 1 it is
+**frozen**: a change needs a contract change request (see `09-AGENT-WORKFLOW.md`).
+
+Columns marked **(brief)** have limits or allowed values that come from `docs/BRIEF.md`. T01 uses
+the safe default shown; the task that owns the feature tightens validation in its service, not in
+the schema.
+
+## Conventions
+
+- `id INTEGER PRIMARY KEY` on every table.
+- Times: `TEXT` holding UTC ISO-8601 with a `Z`, for example `2026-11-30T02:00:00Z`.
+- Booleans: `INTEGER` 0 or 1 with a CHECK.
+- Every foreign key states `ON DELETE` explicitly. `PRAGMA foreign_keys = ON` is set on every
+  connection in `db.get_db()`.
+- Skills are stored **normalised** (the normalise rule is FP-MATCH-1, from the brief).
+
+## Tables
+
+```sql
+PRAGMA foreign_keys = ON;
+
+CREATE TABLE users (
+  id            INTEGER PRIMARY KEY,
+  email         TEXT NOT NULL UNIQUE COLLATE NOCASE,
+  password_hash TEXT NOT NULL,
+  role          TEXT NOT NULL CHECK (role IN ('candidate', 'employer')),
+  display_name  TEXT NOT NULL,
+  created_at    TEXT NOT NULL
+);
+
+CREATE TABLE candidate_profiles (
+  user_id     INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
+  headline    TEXT NOT NULL DEFAULT '',
+  location    TEXT NOT NULL DEFAULT '',
+  timezone    TEXT NOT NULL DEFAULT 'UTC',
+  summary     TEXT NOT NULL DEFAULT '',
+  updated_at  TEXT NOT NULL
+);
+
+CREATE TABLE skills (
+  id    INTEGER PRIMARY KEY,
+  name  TEXT NOT NULL UNIQUE          -- normalised form
+);
+
+CREATE TABLE candidate_skills (
+  candidate_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+  skill_id     INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
+  PRIMARY KEY (candidate_id, skill_id)
+);
+
+CREATE TABLE resumes (
+  id             INTEGER PRIMARY KEY,
+  owner_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+  stored_name    TEXT NOT NULL UNIQUE,   -- random hex, never user supplied
+  original_name  TEXT NOT NULL,          -- shown only, never used as a path
+  mime_type      TEXT NOT NULL,
+  size_bytes     INTEGER NOT NULL CHECK (size_bytes > 0),
+  uploaded_at    TEXT NOT NULL
+);
+
+CREATE TABLE companies (
+  id           INTEGER PRIMARY KEY,
+  owner_id     INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
+  name         TEXT NOT NULL,
+  industry     TEXT NOT NULL DEFAULT '',
+  location     TEXT NOT NULL DEFAULT '',
+  website      TEXT NOT NULL DEFAULT '',
+  description  TEXT NOT NULL DEFAULT '',
+  updated_at   TEXT NOT NULL
+);
+
+CREATE TABLE jobs (
+  id           INTEGER PRIMARY KEY,
+  company_id   INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
+  title        TEXT NOT NULL,                       -- (brief) length limits
+  description  TEXT NOT NULL,
+  location     TEXT NOT NULL DEFAULT '',
+  employment_type TEXT NOT NULL DEFAULT '',          -- (brief) allowed values
+  salary_min   INTEGER,                              -- (brief) required or optional
+  salary_max   INTEGER,
+  is_open      INTEGER NOT NULL DEFAULT 1 CHECK (is_open IN (0, 1)),
+  created_at   TEXT NOT NULL,
+  updated_at   TEXT NOT NULL,
+  CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max)
+);
+
+CREATE TABLE job_skills (
+  job_id    INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
+  skill_id  INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
+  PRIMARY KEY (job_id, skill_id)
+);
+
+CREATE TABLE applications (
+  id            INTEGER PRIMARY KEY,
+  job_id        INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,   -- (brief) delete rule
+  candidate_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+  resume_id     INTEGER REFERENCES resumes(id) ON DELETE SET NULL,
+  status        TEXT NOT NULL DEFAULT 'pending',     -- (brief) allowed values
+  cover_note    TEXT NOT NULL DEFAULT '',
+  created_at    TEXT NOT NULL,
+  updated_at    TEXT NOT NULL
+);
+-- one pending application per candidate per job (FP-CAN-3)
+CREATE UNIQUE INDEX uq_pending_application
+  ON applications (job_id, candidate_id) WHERE status = 'pending';
+
+CREATE TABLE interview_slots (
+  id           INTEGER PRIMARY KEY,
+  job_id       INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
+  employer_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+  starts_at    TEXT NOT NULL,      -- UTC
+  ends_at      TEXT NOT NULL,      -- UTC
+  created_tz   TEXT NOT NULL,      -- the IANA zone the employer entered it in
+  created_at   TEXT NOT NULL,
+  CHECK (ends_at > starts_at)
+);
+
+CREATE TABLE bookings (
+  id              INTEGER PRIMARY KEY,
+  slot_id         INTEGER NOT NULL UNIQUE REFERENCES interview_slots(id) ON DELETE CASCADE,
+  application_id  INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
+  booked_at       TEXT NOT NULL
+);
+-- (brief) if one application may hold only one booking, add:
+-- CREATE UNIQUE INDEX uq_booking_application ON bookings (application_id);
+
+CREATE TABLE audit_log (
+  id           INTEGER PRIMARY KEY,
+  actor_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
+  action       TEXT NOT NULL,      -- for example 'application.submit'
+  object_type  TEXT NOT NULL,
+  object_id    INTEGER,
+  detail       TEXT NOT NULL DEFAULT '',   -- short, never contains passwords or file contents
+  created_at   TEXT NOT NULL
+);
+
+CREATE INDEX ix_jobs_company ON jobs (company_id);
+CREATE INDEX ix_applications_job ON applications (job_id);
+CREATE INDEX ix_applications_candidate ON applications (candidate_id);
+CREATE INDEX ix_slots_job ON interview_slots (job_id, starts_at);
+CREATE INDEX ix_audit_actor ON audit_log (actor_id, created_at);
+```
+
+## Relationships
+
+```
+users (candidate) 1 ─ 1 candidate_profiles
+users (candidate) 1 ─ * candidate_skills * ─ 1 skills
+users (candidate) 1 ─ * resumes
+users (employer)  1 ─ 1 companies 1 ─ * jobs 1 ─ * job_skills * ─ 1 skills
+jobs 1 ─ * applications * ─ 1 users (candidate)
+jobs 1 ─ * interview_slots 1 ─ 0..1 bookings * ─ 1 applications
+users 1 ─ * audit_log
+```
+
+## Why these constraints
+
+- `uq_pending_application` makes the duplicate-pending rule (FP-CAN-3) hold even if two requests
+  race. The service still checks first, to give a friendly message.
+- `bookings.slot_id UNIQUE` makes double booking impossible at the database level (FP-SCHED-3).
+  The service uses `BEGIN IMMEDIATE` and turns the `IntegrityError` into the brief's conflict result.
+- `stored_name` is random, so a user can never choose a file path (path traversal).
+
+## Audit actions (fixed list)
+
+`user.register`, `user.login`, `user.login_failed`, `profile.update`, `resume.upload`,
+`resume.delete`, `company.update`, `job.create`, `job.update`, `job.delete`, `application.submit`,
+`application.status`, `slot.create`, `slot.delete`, `booking.create`, `booking.conflict`.
diff --git a/docs/plan/04-AUTH-SECURITY.md b/docs/plan/04-AUTH-SECURITY.md
new file mode 100644
index 0000000..6ce5edc
--- /dev/null
+++ b/docs/plan/04-AUTH-SECURITY.md
@@ -0,0 +1,85 @@
+# 04 · Authentication and security
+
+Other teams will attack this app in the Week 12 audit, and every confirmed security bug costs
+marks. This file is the spec, and it doubles as the checklist every reviewer uses.
+
+## Authentication
+
+| Item | Design |
+|---|---|
+| Accounts | email + password + role (`candidate` or `employer`), chosen at sign-up |
+| Password hashing | `werkzeug.security.generate_password_hash(password)` (salted, scrypt by default). Verify with `check_password_hash`. Never store or log the password. |
+| Password rules | from the brief; default minimum 8 characters, maximum 128 |
+| Email | stripped and lower-cased; basic format check; unique (case-insensitive) |
+| Sign-up errors | field messages, HTTP 400, form refilled except password |
+| Duplicate email | same generic message as other errors where the brief allows, to limit account probing |
+| Session | Flask signed cookie. Holds only `user_id`, `role`, `csrf`. |
+| Sign in | `session.clear()` first (stops session fixation), then set values and a new CSRF token |
+| Sign out | POST only, with CSRF. `session.clear()`. |
+| Cookie flags | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, `SESSION_COOKIE_SECURE` on when served over HTTPS |
+| Session lifetime | from the brief; default `PERMANENT_SESSION_LIFETIME` 8 hours |
+| Brute force | per email and per IP: 5 failed logins in 10 minutes blocks the next try for 10 minutes (in-memory dict, fine for one process). Message does not say whether the email exists. |
+| Current user | `security.load_user` runs before every request: reads `session["user_id"]`, loads the row, puts it on `g.user`. A deleted user means the session is cleared. |
+
+## Authorization
+
+- `@login_required`: no user, redirect to sign-in (GET) or 401 (POST).
+- `@role_required("employer")` or `("candidate")`: wrong role gives 403.
+- **Object ownership is checked in the service, every time**, with the actor id passed in.
+  Never trust an id from the form or URL on its own.
+- Missing object gives 404. Another user's object gives 403 or 404, as the brief says
+  (FP-AUTH-3). Until the brief says otherwise, use **404** for both, so ids cannot be probed.
+- Ownership helpers (in services): `get_owned_job(conn, employer_id, job_id)`,
+  `get_owned_slot(...)`, `get_own_application(...)`, `can_view_resume(conn, viewer, resume_id)`.
+
+## Request security
+
+| Threat | Control |
+|---|---|
+| CSRF | Every POST form has `<input type="hidden" name="csrf_token">` from the `csrf_field()` macro. `before_request` rejects a POST with a missing or wrong token (403), compared with `hmac.compare_digest`. No exceptions, logout included. |
+| SQL injection | Only `?` placeholders. No f-strings or `%` or `+` in SQL. Column and sort names, if dynamic, come from a fixed allowlist dict. |
+| XSS | Jinja autoescape stays on. Never use `|safe` or `Markup()` on user data. No inline event handlers. |
+| Open redirect | `next` parameter is accepted only if it starts with `/` and not `//`. |
+| Clickjacking | `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` |
+| Content sniffing | `X-Content-Type-Options: nosniff` on every response |
+| CSP | `default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'` |
+| Referrer | `Referrer-Policy: same-origin` |
+| Debug leaks | `debug` off in Docker. Error handlers render plain pages for 400, 403, 404, 413, 500 without tracebacks. |
+| Secrets | `SECRET_KEY` from env only. Never committed. `.env` stays gitignored. |
+| Mass assignment | Services take named fields only. Never `**request.form`. `role` is never editable after sign-up. |
+| Integer ids | Route converters `<int:job_id>`, so non-numbers give 404. |
+
+## File uploads (resumes)
+
+- `MAX_CONTENT_LENGTH` set from `MAX_UPLOAD_MB`; larger uploads give 413 with a friendly page.
+- Allowed types from the brief; default PDF only. Check the extension **and** the first bytes
+  (`%PDF-`).
+- Stored as `secrets.token_hex(16) + ".pdf"` under `UPLOAD_DIR`, outside `static/`.
+- `original_name` is for display only. It passes through `werkzeug.utils.secure_filename` and is
+  never used as a path.
+- Download route checks `can_view_resume`, then `send_file(path, as_attachment=True,
+  download_name=original_name, mimetype="application/pdf")`.
+- Deleting a resume removes the row and the file.
+
+## Data privacy
+
+- A resume is private to its owner, plus anyone the brief allows (likely the employer of a job
+  the candidate applied to).
+- Employers see applicants only for their own jobs.
+- The audit log never stores passwords, tokens or file contents.
+- Demo data uses fake people and companies only.
+
+## Security review checklist (reviewers tick every line)
+
+1. Every new route has `@login_required` and the right `@role_required`, or a written reason why not.
+2. Every POST form includes `csrf_field()`. No route skips the CSRF check.
+3. Every service that loads an object by id also checks the actor owns it or may see it.
+4. Missing and not-yours both give the agreed status code. Try an id that belongs to another user.
+5. All SQL uses `?` placeholders. Search the diff for `f"`, `.format(`, `%` and `+` near `execute`.
+6. No `|safe`, `Markup(` or `autoescape false` on anything a user typed.
+7. Uploads: size cap, type check by content, random stored name, served only via the checked route.
+8. Redirects use `url_for`, or a `next` value that passes the safe-redirect check.
+9. No secret, password, token or traceback appears in logs, flash messages, audit detail or HTML.
+10. Error responses use the error templates, with the right status code.
+11. Sign-in clears the session first. Sign-out is POST with CSRF.
+12. Role cannot be changed through any form field.
diff --git a/docs/plan/05-UX-FLOWS.md b/docs/plan/05-UX-FLOWS.md
new file mode 100644
index 0000000..aab0f17
--- /dev/null
+++ b/docs/plan/05-UX-FLOWS.md
@@ -0,0 +1,115 @@
+# 05 · UX flows and screens
+
+Screens follow the Keystone design canvas (web-only cut). The canvas ID in brackets, such as
+[C11], is the screen to look at for layout ideas. Routes and template names are frozen in
+`07-CONTRACTS.md`.
+
+## Principles (from the canvas)
+
+1. **The system proposes, a person decides.** Any action that sends data to someone else (apply,
+   change an applicant's status, delete a job, book a slot) goes through a **confirm screen**
+   showing exactly what will happen, to whom, and what will be shared.
+2. **Explain every score.** A match score always shows which skills matched and which did not.
+3. **Private by default.** Say plainly who can see what ("Only you and employers you apply to can
+   open this resume").
+4. **Plain, short words.** Sentence case. Verb-first buttons: "Save profile", "Apply to this job".
+5. **Every list has an empty state** that tells the user what to do next.
+
+## Roles and their home
+
+| Role | Home after sign-in | Nav items |
+|---|---|---|
+| Visitor | `/` landing [P01] | Sign in, Create account |
+| Candidate | `/candidate/` Today [C06] | Today, Recommendations, Applications, Profile, Activity |
+| Employer | `/employer/` Home [R01] | Home, Company, Jobs, Activity |
+
+## Journey: candidate
+
+```
+Landing [P01] -> Create account [P02] (role = candidate)
+  -> Profile [C22/C03]: headline, location, timezone, summary, skills (comma separated)
+  -> Upload resume [C01] (PDF, private)
+  -> Today [C06]: profile completeness, top 3 recommendations, application statuses
+  -> Recommendations [C07]: every open job, ranked, each with score + matched / missing skills
+  -> Job detail [C08]: full job, company card, "Apply to this job"
+  -> Confirm application [C11]: shows job, resume to be shared, cover note -> Submit
+  -> Applications [C12]: list with status badges
+  -> Application detail: status; if eligible, list of open slots in her timezone
+  -> Confirm booking -> Booked (or conflict message per brief)
+```
+
+## Journey: employer
+
+```
+Landing -> Create account (role = employer)
+  -> Company [R03 area]: name, industry, location, website, description
+  -> Jobs [R03]: list, "Post a job"
+  -> New job [R05]: title, description, location, type, salary range, skills
+  -> Job applicants [R06/R10]: applicants in the brief's order, each with match score, skills,
+     resume link, status; actions per allowed status change
+  -> Confirm status change -> Updated
+  -> Interview slots [R13]: add slot (date, start, end, timezone), list, delete unbooked slot
+```
+
+## Screen list
+
+| Screen | Route | Template | Task | Canvas |
+|---|---|---|---|---|
+| Landing | `GET /` | `index.html` | T03 | P01 |
+| Create account | `GET/POST /auth/register` | `auth/register.html` | T05 | P02 |
+| Sign in | `GET/POST /auth/login` | `auth/login.html` | T05 | P02 |
+| Candidate Today | `GET /candidate/` | `candidates/today.html` | T07 | C06 |
+| Candidate profile | `GET/POST /candidate/profile` | `candidates/profile.html` | T07 | C22 |
+| Resume upload and list | `GET/POST /candidate/resume` | `candidates/resume.html` | T08 | C01 |
+| Recommendations | `GET /candidate/recommendations` | `matching/recommendations.html` | T13 | C07 |
+| Job detail | `GET /jobs/<id>` | `jobs/detail.html` | T10 | C08 |
+| Confirm application | `GET /jobs/<id>/apply` | `applications/confirm.html` | T14 | C11 |
+| My applications | `GET /candidate/applications` | `applications/mine.html` | T14 | C12 |
+| Application detail and booking | `GET /candidate/applications/<id>` | `scheduling/book.html` | T16 | C12 |
+| Employer home | `GET /employer/` | `employers/home.html` | T09 | R01 |
+| Company profile | `GET/POST /employer/company` | `employers/company.html` | T09 | R03 |
+| My jobs | `GET /employer/jobs` | `jobs/list.html` | T10 | R03 |
+| New or edit job | `GET/POST /employer/jobs/new`, `/employer/jobs/<id>/edit` | `jobs/form.html` | T10 | R05 |
+| Confirm job delete | `GET /employer/jobs/<id>/delete` | `jobs/confirm_delete.html` | T10 | none |
+| Applicants | `GET /employer/jobs/<id>/applicants` | `applications/applicants.html` | T15 | R06, R10 |
+| Interview slots | `GET/POST /employer/jobs/<id>/slots` | `scheduling/slots.html` | T12 | R13 |
+| Activity log | `GET /activity` | `activity/list.html` | T18 | A02 |
+| Errors | 400, 403, 404, 405, 409, 413, 500 | `errors/<code>.html` | T03 | none |
+
+## Screen content rules
+
+**Recommendations card** (FP-CAN-2): job title, company name, location, employment type, salary
+range (or "Not stated"), score shown as a number plus a 5-segment bar, "Matched: Python, SQL",
+"Missing: dbt". Every open job appears, including weak matches, unless the brief says otherwise.
+Ranking and tie-breaks come from the brief only.
+
+**Applicants table** (FP-EMP-3): candidate name, headline, match score, matched skills, applied
+date (shown in the employer's timezone), status badge, resume link, actions. Columns and order
+from the brief.
+
+**Confirm application** (Keystone approval pattern): a box titled "This will be sent to
+<company>", listing the resume file name, the cover note, and "Not shared: your other
+applications, your email address" (adjust to the brief's privacy rules). Buttons: primary
+"Submit application", secondary "Back to job".
+
+**Slot times**: always show the timezone label, for example "Mon 30 Nov, 10:00 to 10:45 (Asia/Hong_Kong)".
+
+## Forms
+
+- Labels above fields, field errors directly under the field in danger color, a summary at the top
+  when there are errors ("2 fields need fixing").
+- Required fields marked "Required" in muted text, not with an asterisk only.
+- After a successful POST: redirect, then a success flash ("Profile saved").
+- Every POST form includes `{{ csrf_field() }}`.
+
+## Empty states (text is fixed, so tests can find it)
+
+| Where | Text | Action |
+|---|---|---|
+| Recommendations, no skills | "Add your skills to see how jobs match you." | Edit profile |
+| Recommendations, no open jobs | "No open jobs right now. Check back soon." | none |
+| My applications | "You have not applied to any jobs yet." | See recommendations |
+| My jobs | "You have not posted a job yet." | Post a job |
+| Applicants | "No one has applied to this job yet." | none |
+| Slots | "No interview slots yet. Add one so applicants can book." | Add slot |
+| Activity | "Nothing here yet. Actions you take will show up here." | none |

```
