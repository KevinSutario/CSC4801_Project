# Review packet phase-0 (11 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/tasks/T01.md, docs/tasks/T02.md, docs/tasks/T03.md, docs/tasks/T04.md

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
diff --git a/docs/tasks/T01.md b/docs/tasks/T01.md
new file mode 100644
index 0000000..f003f95
--- /dev/null
+++ b/docs/tasks/T01.md
@@ -0,0 +1,114 @@
+# T01 · App skeleton, config, database, schema, errors, blueprint stubs
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 1 | foundation | T00 | no | READY |
+
+## Goal
+`create_app()` builds a Flask app with config, a SQLite database created from `schema.sql`, error
+classes and handlers, and every blueprint registered (with empty route stubs), so later tasks only
+fill in their own files.
+
+## Owns
+- `app/__init__.py`
+- `app/config.py`
+- `app/db.py`
+- `app/schema.sql`
+- `app/errors.py`
+- `app/skills.py`
+- `app/security.py`
+- `app/core/*`
+- `app/auth/*`
+- `app/candidates/*`
+- `app/employers/*`
+- `app/jobs/*`
+- `app/matching/*`
+- `app/applications/*`
+- `app/scheduling/*`
+- `app/activity/*`
+- `app/templates/errors/*`
+- `tests/conftest.py`
+- `tests/unit/test_db.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/02-ARCHITECTURE.md`
+- `docs/plan/03-DATA-MODEL.md`
+- `docs/plan/07-CONTRACTS.md` (sections: Shared modules, Blueprint objects)
+- `.env.example`
+
+## Contract
+Exactly the `app/__init__.py`, `app/config.py`, `app/db.py`, `app/errors.py` and `app/skills.py`
+sections of `07-CONTRACTS.md`. Blueprint `__init__.py` files exactly as "Blueprint objects".
+
+Blueprint packages and their stub route modules:
+
+| Package | Blueprint name | url_prefix | Stub route modules |
+|---|---|---|---|
+| `app/core` | `core` | none | `routes.py` |
+| `app/auth` | `auth` | `/auth` | `routes.py` |
+| `app/candidates` | `candidates` | none | `routes_profile.py`, `routes_resume.py` |
+| `app/employers` | `employers` | none | `routes.py` |
+| `app/jobs` | `jobs` | none | `routes.py` |
+| `app/matching` | `matching` | none | `routes.py` |
+| `app/applications` | `applications` | none | `routes_candidate.py`, `routes_employer.py` |
+| `app/scheduling` | `scheduling` | none | `routes_employer.py`, `routes_candidate.py` |
+| `app/activity` | `activity` | none | `routes.py` |
+
+Only `auth` has a url_prefix. All other paths are written in full in their routes (see contracts).
+
+Also create empty service modules, each holding only a module docstring naming its owner task:
+`app/auth/service.py`, `app/candidates/profile_service.py`, `app/candidates/resume_service.py`,
+`app/employers/service.py`, `app/jobs/service.py`, `app/matching/engine.py`,
+`app/matching/service.py`, `app/applications/statuses.py`, `app/applications/service.py`,
+`app/applications/review_service.py`, `app/scheduling/slots.py`, `app/scheduling/booking.py`.
+
+`app/security.py` here is a **stub** with one function `def init_app(app): return None`. T02 replaces it.
+
+## Steps
+1. `app/config.py`: the `Config` class. Read env vars with `os.environ.get`. `SECRET_KEY` falls back to
+   `secrets.token_hex(32)`. Paths default under `app.instance_path`, so set them in `create_app`
+   when the env var is missing.
+2. `app/schema.sql`: copy the SQL block from `03-DATA-MODEL.md` exactly.
+3. `app/db.py`: `get_db` opens `sqlite3.connect(DATABASE, isolation_level=None,
+   detect_types=0)`, sets `row_factory = sqlite3.Row`, runs `PRAGMA foreign_keys = ON`, stores it on
+   `g`. `transaction()` is a `contextlib.contextmanager` that runs `BEGIN` or `BEGIN IMMEDIATE`,
+   yields, then `COMMIT`, and on any exception `ROLLBACK` and re-raise. `init_db()` runs
+   `executescript` on `schema.sql`. `now_iso()` uses `datetime.now(timezone.utc)` and
+   `strftime("%Y-%m-%dT%H:%M:%SZ")`. Register `close_db` with `app.teardown_appcontext` and an
+   `init-db` CLI command with `app.cli.command`.
+4. `app/errors.py`: the classes and `init_app` from the contract. Handlers render
+   `errors/<code>.html` with the right status code. A `Conflict` handler renders `errors/409.html`
+   with `message`.
+5. `app/templates/errors/{400,403,404,405,409,413,500}.html`: minimal plain HTML pages (a heading
+   and one sentence, no styling). T03 restyles them later.
+6. `app/skills.py`: the PROVISIONAL versions. Put this comment at the top:
+   `# PROVISIONAL normalisation. T11 replaces normalise_skill with the brief's rule.`
+7. Blueprint packages, stub route modules, empty service modules, `app/security.py` stub.
+8. `app/__init__.py`: `create_app(test_config=None)`: `Flask(__name__, instance_relative_config=True)`,
+   load `Config`, then `test_config` on top, fill default paths, `os.makedirs` for the instance folder
+   and `UPLOAD_DIR`, init db teardown and CLI, `errors.init_app`, `security.init_app`, register the
+   blueprints in contract order. If the database file does not exist, call `init_db()` inside an app
+   context.
+9. `tests/conftest.py`: fixtures `app` (tmp_path database and upload dir, `TESTING=True`,
+   `SECRET_KEY="test"`), `client`, `conn` (yields `get_db()` inside `app.app_context()`).
+10. `tests/unit/test_db.py`: tests below.
+
+## Tests (`tests/unit/test_db.py`)
+- every table in `03-DATA-MODEL.md` exists after `create_app` (query `sqlite_master`)
+- `PRAGMA foreign_keys` returns 1 on a connection from `get_db()`
+- a write inside `transaction()` that raises is rolled back (row count unchanged)
+- inserting two pending applications for the same job and candidate raises `sqlite3.IntegrityError`
+- inserting two bookings for the same slot raises `sqlite3.IntegrityError`
+- `now_iso()` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
+- `parse_skill_list(" Python, sql,PYTHON ,, ")` returns `["python", "sql"]`
+- GET `/does-not-exist` returns 404
+
+## Done when
+- `python scripts/check.py` passes, `python scripts/check_scope.py T01` passes
+- `python -m flask --app app init-db` runs without error
+
+## Pitfalls
+- `isolation_level=None` means autocommit. Every write must be inside `transaction()`.
+- `executescript` commits on its own; do not call it inside `transaction()`.
+- Do not register any routes except via the stubs. Do not add templates other than `errors/`.
diff --git a/docs/tasks/T02.md b/docs/tasks/T02.md
new file mode 100644
index 0000000..f979921
--- /dev/null
+++ b/docs/tasks/T02.md
@@ -0,0 +1,74 @@
+# T02 · Security module and audit log
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 1 | foundation | T01 | no | READY |
+
+## Goal
+Every request has the user loaded, every POST is CSRF-checked, every response has security headers,
+routes can require login and a role, login attempts are rate limited, and services can write to the
+audit log.
+
+## Owns
+- `app/security.py`
+- `app/audit.py`
+- `tests/unit/test_security.py`
+- `tests/unit/test_audit.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/04-AUTH-SECURITY.md`
+- `docs/plan/07-CONTRACTS.md` (sections: `app/security.py`, `app/audit.py`)
+- `docs/plan/03-DATA-MODEL.md` (sections: users, audit_log, Audit actions)
+- `app/__init__.py`, `app/db.py`, `app/errors.py`, `tests/conftest.py`
+
+## Contract
+`app/security.py` and `app/audit.py` sections of `07-CONTRACTS.md`, exactly.
+
+## Steps
+1. `load_user` (before_request): if `session.get("user_id")`, select the user row (id, email, role,
+   display_name); set `g.user` to a dict or None. If the id is not in the database, `session.clear()`.
+2. `csrf_token()`: `session["csrf"]` = `secrets.token_urlsafe(32)` if missing; return it.
+   `rotate_csrf()` always sets a new one.
+3. `csrf_protect` (before_request): for POST, PUT, PATCH, DELETE: compare `request.form.get("csrf_token")`
+   with `session.get("csrf")` using `hmac.compare_digest`. Missing or wrong: `abort(403)`.
+4. Security headers (after_request): exactly the list in `04-AUTH-SECURITY.md` (CSP, X-Frame-Options,
+   X-Content-Type-Options, Referrer-Policy).
+5. `login_required`: no `g.user`: GET redirects to `url_for("auth.login", next=request.path)`, other
+   methods `abort(401)`. `role_required(role)`: login check first, then wrong role `abort(403)`.
+   Use `functools.wraps`.
+6. `is_safe_next(target)`: True only if target is a non-empty string starting with `/`, not `//`,
+   and with no `\` and no scheme.
+7. Rate limit: module-level dict `key -> list of failure timestamps` (use `time.monotonic()`).
+   5 failures within 600 seconds blocks for 600 seconds from the last failure. `login_key(email, ip)`
+   returns `f"{email.strip().lower()}|{ip}"`. Store the dict at
+   `app.extensions["login_limiter"]` so tests get a fresh one per app.
+8. `init_app(app)`: register the hooks, add Jinja globals `csrf_token` and `current_user` (a
+   context processor returning `g.user`), set the empty limiter dict.
+9. `app/audit.py`: `ACTIONS` is the frozenset of the action names in `03-DATA-MODEL.md`.
+   `log_event` raises `ValueError` for an unknown action, truncates `detail` to 500 characters, and
+   inserts with `now_iso()`. It does not open its own transaction. `list_events` returns dicts, newest
+   first, filtered by actor.
+
+## Tests
+`tests/unit/test_security.py` (register a throwaway blueprint inside the test app fixture is NOT
+allowed; test through the hooks with `app.test_request_context` and the client):
+- a POST to any path without a token returns 403; with the right token it does not return 403
+- `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` present on a 404 response
+- `is_safe_next`: `/candidate/` True; `//evil.com`, `http://evil.com`, `\\evil`, `""`, `None` False
+- rate limit: 5 `record_failed_login` calls block; `reset_login_failures` unblocks; another key is
+  not blocked
+- `load_user` clears the session when the user id no longer exists
+
+`tests/unit/test_audit.py`:
+- `log_event` with an unknown action raises `ValueError`
+- events are listed newest first and only for that actor
+- detail longer than 500 characters is truncated
+
+## Done when
+- check and scope pass
+
+## Pitfalls
+- `hmac.compare_digest` needs two strings; treat a missing value as `""`.
+- Do not exempt any route from CSRF.
+- Do not put secrets or tokens in the audit `detail`.
diff --git a/docs/tasks/T03.md b/docs/tasks/T03.md
new file mode 100644
index 0000000..6b293ee
--- /dev/null
+++ b/docs/tasks/T03.md
@@ -0,0 +1,69 @@
+# T03 · Design tokens, layout, components, landing page
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 1 | foundation | T02 | no | READY |
+
+## Goal
+Every later page can extend one layout and use ready-made macros for buttons, badges, fields,
+cards, empty states, score bars and confirm boxes, all in the Keystone look.
+
+## Owns
+- `app/static/css/tokens.css`
+- `app/static/css/app.css`
+- `app/templates/base.html`
+- `app/templates/index.html`
+- `app/templates/components/*`
+- `app/templates/errors/*`
+- `app/core/routes.py`
+- `tests/unit/test_layout.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/06-DESIGN-SYSTEM.md`
+- `docs/plan/05-UX-FLOWS.md` (sections: Principles, Roles and their home, Forms)
+- `docs/plan/07-CONTRACTS.md` (sections: Templates and static, `app/core/routes.py`)
+- `app/security.py`, `app/core/__init__.py`, `app/templates/errors/*`, `tests/conftest.py`
+
+## Contract
+- Templates and macros exactly as in `06-DESIGN-SYSTEM.md` "Components".
+- `core.index` GET `/`: signed in as candidate, redirect to `/candidate/`; as employer, redirect to
+  `/employer/`; else render `index.html`. Use the literal paths (those endpoints do not exist yet; use
+  `redirect("/candidate/")`).
+
+## Steps
+1. `tokens.css`: the `:root` block from `06-DESIGN-SYSTEM.md`, plus spacing `--s-1`..`--s-8`
+   (4, 8, 12, 16, 20, 24, 32, 48 px), radii `--r-control: 6px`, `--r-card: 8px`, the two font stacks.
+2. `app.css`: classes for layout (`.layout`, `.sidebar`, `.main`, `.page-header`), `.card`,
+   `.btn .btn-primary .btn-secondary .btn-danger`, `.badge .badge-<tone>`, `.field .field-error`,
+   `.table`, `.empty`, `.score-bar`, `.confirm-box`, `.flash-success .flash-error`. Use only token
+   variables, no raw hex values. Below 800 px the sidebar stacks on top.
+3. `base.html`: `<!doctype html>`, `lang="en"`, viewport meta, title block, the Google Fonts link
+   (IBM Plex Sans 400/500/600 and Mono 400), both CSS files via `url_for('static', ...)`. Sidebar nav
+   per `current_user.role` (labels and order from `05-UX-FLOWS.md`; for links whose endpoints do not
+   exist yet, use literal paths). A sign-out button: a POST form to `/auth/logout` with
+   `csrf_field()`. Then `flash_messages()`, then `{% block content %}`.
+4. `components/ui.html` and `components/forms.html`: every macro in the table. `csrf_field()` renders
+   `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. `field()` shows the error
+   under the input with `aria-describedby`. `score_bar(score, max_score)` handles `max_score` 0
+   (shows an empty bar).
+5. Restyle `errors/*.html` to extend `base.html`. Keep one heading and one sentence; 409 shows `message`.
+6. `index.html`: the landing page from canvas P01 (navy hero, product sentence, "Create account" and
+   "Sign in" links to `/auth/register` and `/auth/login`). No invented stats or quotes.
+7. `core/routes.py`: `core.index`.
+
+## Tests (`tests/unit/test_layout.py`)
+- GET `/` returns 200 and contains "Create account"
+- the page has no `style="` attribute and no `<script` tag
+- a candidate session (`with client.session_transaction() as s: s["user_id"]=...`, after inserting a
+  user row with SQL) GET `/` redirects to `/candidate/`
+- 404 page extends the layout (contains the nav wrapper class) and returns status 404
+- render `csrf_field()` in a test request context: the value equals `session["csrf"]`
+
+## Done when
+- check and scope pass
+- open `python -m flask --app app run --debug`, look at `/` and a 404 page: they look like the canvas
+
+## Pitfalls
+- The CSP blocks inline styles and scripts. Not one `style=` attribute anywhere.
+- Never `|safe`.
diff --git a/docs/tasks/T04.md b/docs/tasks/T04.md
new file mode 100644
index 0000000..b48e0ad
--- /dev/null
+++ b/docs/tasks/T04.md
@@ -0,0 +1,75 @@
+# T04 · Test harness: factories, helpers, placeholder tests
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 1 | foundation | T03 | no | READY |
+
+## Goal
+Every later task can create test users, companies, jobs, applications and slots in one line, sign
+in, and post forms with a CSRF token. Every template test name exists as a skipped placeholder, so
+progress is visible and nothing passes by accident.
+
+## Owns
+- `tests/conftest.py`
+- `tests/unit/test_conftest.py`
+- `tests/unit/test_auth.py`
+- `tests/unit/test_matching.py`
+- `tests/unit/test_workflows.py`
+- `tests/unit/test_scheduling.py`
+- `tests/unit/test_can_profile.py`
+- `tests/unit/test_can_resume.py`
+- `tests/unit/test_can_recommend.py`
+- `tests/unit/test_can_apply.py`
+- `tests/unit/test_emp_company.py`
+- `tests/unit/test_emp_jobs.py`
+- `tests/unit/test_emp_applicants.py`
+- `tests/unit/test_timeutil.py`
+- `tests/unit/test_sched_slots.py`
+- `tests/unit/test_sched_booking.py`
+- `tests/unit/test_activity.py`
+- `tests/unit/test_authz_sweep.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: `tests/conftest.py`, Test files and owners)
+- `docs/plan/11-TESTING.md`
+- `docs/plan/03-DATA-MODEL.md`
+- `tests/conftest.py`, `tests/unit/test_auth.py`, `tests/unit/test_matching.py`,
+  `tests/unit/test_workflows.py`, `tests/unit/test_scheduling.py`, `app/db.py`, `app/security.py`,
+  `app/skills.py`
+
+## Contract
+The fixtures and signatures in `07-CONTRACTS.md`, section `tests/conftest.py`.
+
+## Steps
+1. Factories insert with plain SQL inside `transaction(conn)`. Passwords hashed with
+   `werkzeug.security.generate_password_hash`. `make_candidate` also inserts a `candidate_profiles`
+   row (timezone `UTC`) and its skills via `app.skills.get_or_create_skill_ids`. `make_job` creates a
+   company for the employer if none exists. All times use `now_iso()` except slot times.
+2. Each factory fixture returns a function, so a test can call it many times. Emails default to
+   unique values when called again (append a counter) so two calls never clash.
+3. `login_as(client, user_id, role)`: sets `user_id`, `role` and a fresh `csrf` in the session.
+4. `csrf_post(client, url, data, **kw)`: reads `session["csrf"]` (creating one with a GET to `/` if
+   missing), adds it as `csrf_token`, posts.
+5. `login(client, email, password)`: `csrf_post(client, "/auth/login", {...})`.
+6. Placeholders: for every file in the "Test files and owners" table that has template test names,
+   write each name as
+   ```python
+   @pytest.mark.skip(reason="TODO T05")
+   def test_fp_auth_1_registration_and_session_lifecycle():
+       raise NotImplementedError
+   ```
+   with the owner task in the reason. In `test_auth.py` and `test_matching.py` replace the template's
+   `pass` bodies this way. Create the other files with a module docstring naming the owner task.
+7. Delete `tests/unit/test_workflows.py` and `tests/unit/test_scheduling.py` after their names exist
+   in the new files.
+8. `tests/unit/test_conftest.py`: each factory works twice in one test; `login_as` then GET `/`
+   redirects by role; `csrf_post` to `/nowhere` gives 404, not 403.
+
+## Done when
+- check passes, showing the placeholder tests as skipped
+- `python -m pytest --collect-only -q` lists every template test name
+- scope passes
+
+## Pitfalls
+- Factories must not call any service module (they are empty now, and lanes must stay independent).

```
