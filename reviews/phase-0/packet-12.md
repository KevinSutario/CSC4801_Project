# Review packet phase-0 (12 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/tasks/T05.md, docs/tasks/T06.md, docs/tasks/T07.md, docs/tasks/T08.md, docs/tasks/T09.md

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
diff --git a/docs/tasks/T05.md b/docs/tasks/T05.md
new file mode 100644
index 0000000..2be4c93
--- /dev/null
+++ b/docs/tasks/T05.md
@@ -0,0 +1,81 @@
+# T05 · Register, sign in, sign out, safe redirects
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 1 | foundation | T04 | no | READY (limits from the brief, defaults below) |
+
+## Goal
+People can create an account as a candidate or an employer, sign in, and sign out, safely.
+
+## Requirement
+- FP-AUTH-1: registration and session lifecycle; invalid registration. Rule text: (from the brief)
+- FP-AUTH-2: salted hash and password verification. Rule text: (from the brief)
+- Defaults until the brief says otherwise: email lower-cased, max 254 chars, must match
+  `^[^@\s]+@[^@\s]+\.[^@\s]+$`; password 8 to 128 chars; display name 1 to 80 chars after strip;
+  role `candidate` or `employer`.
+
+## Owns
+- `app/auth/service.py`
+- `app/auth/routes.py`
+- `app/templates/auth/*`
+- `tests/unit/test_auth.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/04-AUTH-SECURITY.md`
+- `docs/plan/07-CONTRACTS.md` (sections: auth, `app/security.py`, `app/errors.py`, `app/db.py`)
+- `docs/plan/05-UX-FLOWS.md` (section: Forms)
+- `app/security.py`, `app/audit.py`, `app/db.py`, `app/errors.py`, `app/auth/__init__.py`,
+  `app/templates/base.html`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def register(conn, email: str, password: str, role: str, display_name: str) -> int
+def authenticate(conn, email: str, password: str) -> dict | None
+def get_user(conn, user_id: int) -> dict | None
+```
+Routes: `auth.register` GET/POST `/auth/register`, `auth.login` GET/POST `/auth/login`,
+`auth.logout` POST `/auth/logout`. Templates `auth/register.html`, `auth/login.html`.
+
+## Steps
+1. Tests first (below). Run them, see them fail.
+2. `register`: strip and lower the email, validate every field, collect all errors in one dict,
+   raise `ValidationError`. Duplicate email: catch `sqlite3.IntegrityError` and raise
+   `ValidationError({"email": "That email cannot be used."})`. Hash with
+   `generate_password_hash(password)`. Insert user; for a candidate also insert a
+   `candidate_profiles` row. `audit.log_event(..., "user.register", "user", id)`. All in one
+   `transaction()`.
+3. `authenticate`: look up by lower-cased email, `check_password_hash`. Return the user dict
+   without `password_hash`, or None.
+4. Routes: register POST success: sign the user in (step 5), flash "Welcome to Keystone",
+   redirect to `/`. ValidationError: re-render with errors and values (never the password),
+   status 400.
+5. Login POST: `key = login_key(email, request.remote_addr or "")`. If `is_login_blocked(key)`:
+   render with "Too many attempts. Try again in 10 minutes." status 429. Bad credentials:
+   `record_failed_login`, audit `user.login_failed` with actor None, render "Email or password is
+   wrong." status 400. Good: `reset_login_failures`, `session.clear()`, set `user_id`, `role`,
+   `session.permanent = True`, `rotate_csrf()`, audit `user.login`, redirect to `next` if
+   `is_safe_next(next)` else `/`.
+6. Logout: `session.clear()`, flash "Signed out", redirect to `/auth/login`.
+7. Signed-in users opening register or login are redirected to `/`.
+
+## Tests (`tests/unit/test_auth.py`; remove the skip on these four, keep the FP-AUTH-3 placeholder)
+- `test_fp_auth_1_registration_and_session_lifecycle`: register via the form, session has
+  `user_id`; logout; session empty; login again; GET `/` redirects by role.
+- `test_fp_auth_1_invalid_registration`: parametrised: bad email, empty email, short password,
+  long password, empty name, role `admin`, duplicate email (any case). Each gives 400 and a field error,
+  and no user row is added.
+- `test_fp_auth_2_salted_hash_and_password_verification`: stored hash differs from the password and
+  starts with a known Werkzeug method prefix; two users with the same password have different
+  hashes; `authenticate` true for right, None for wrong password and for unknown email.
+- extra: login with `next=//evil.com` redirects to `/`; with `next=/candidate/profile` goes there.
+- extra: 6th bad login for the same email gives 429.
+- extra: logout via GET gives 405; logout POST without token gives 403.
+
+## Done when
+- check and scope pass
+
+## Pitfalls
+- Do not tell the user whether an email exists.
+- Never put the password into the template context, logs or audit.
+- `session.clear()` before setting the new session.
diff --git a/docs/tasks/T06.md b/docs/tasks/T06.md
new file mode 100644
index 0000000..742b7c3
--- /dev/null
+++ b/docs/tasks/T06.md
@@ -0,0 +1,44 @@
+# T06 · Authorization sweep (FP-AUTH-3)
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | security | T10, T15, T16 | yes | READY after its dependencies (status codes from the brief) |
+
+## Goal
+Prove, route by route, that nobody can read or change what is not theirs, and that missing objects
+give 404. This task only writes tests. Holes it finds are reported, not fixed here.
+
+## Requirement
+FP-AUTH-3: authorization and missing object. Rule text: (from the brief)
+Default until the brief says otherwise: wrong role 403; another user's object 404; missing object 404;
+signed out GET redirects to sign-in, signed out POST 401.
+
+## Owns
+- `tests/unit/test_auth.py`
+- `tests/unit/test_authz_sweep.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/04-AUTH-SECURITY.md`
+- `docs/plan/07-CONTRACTS.md` (every Routes line)
+- `scripts/contracts.json`
+- `tests/conftest.py`
+
+## Steps
+1. From `scripts/contracts.json`, list every endpoint with a path parameter. For each, write down:
+   the role that may use it, how to make an object owned by user A, and the URL.
+2. `test_authz_sweep.py`: one parametrised test over that list. For each route: user B (same role)
+   with A's id: expected code; right role, missing id (999999): 404; wrong role: 403; signed out:
+   redirect or 401. Use factories and `login_as`. POSTs use `csrf_post`.
+3. A second parametrised test: every route without a path parameter, wrong role gives 403 and signed
+   out redirects or 401.
+4. `test_auth.py`: remove the skip on `test_fp_auth_3_authorization_and_missing_object` and make it a
+   short, readable version of the sweep for the main cases (employer B edits A's job; candidate B reads
+   A's application; candidate opens an employer page; missing job).
+5. Run. Every failing case is a real hole: list each in your reply under `BUG:` with the route and
+   what happened. Mark those cases `@pytest.mark.xfail(strict=True, reason="B<n>: <route>")` so the
+   gate passes and the hole stays visible. The bug cards remove the xfail when fixed.
+
+## Done when
+- check and scope pass
+- every endpoint with an id appears in the sweep
diff --git a/docs/tasks/T07.md b/docs/tasks/T07.md
new file mode 100644
index 0000000..640b050
--- /dev/null
+++ b/docs/tasks/T07.md
@@ -0,0 +1,68 @@
+# T07 · Candidate profile and skills, Today page shell
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | CAN | T05 | no | READY (limits from the brief, defaults below) |
+
+## Goal
+A candidate can fill in and edit their profile and skills. The Today page welcomes them and shows
+what to do next.
+
+## Requirement
+FP-CAN-1 (profile part). Rule text: (from the brief)
+Defaults: headline max 120, location max 80, summary max 2000, timezone must be a valid IANA name
+(use `zoneinfo.available_timezones()`), skills: comma separated, at most 30, each 1 to 40 chars
+after normalising.
+
+## Owns
+- `app/candidates/profile_service.py`
+- `app/candidates/routes_profile.py`
+- `app/templates/candidates/today.html`
+- `app/templates/candidates/profile.html`
+- `tests/unit/test_can_profile.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: candidates: profile, `app/skills.py`, `app/security.py`)
+- `docs/plan/05-UX-FLOWS.md` (sections: Journey: candidate, Forms, Empty states)
+- `app/skills.py`, `app/audit.py`, `app/db.py`, `app/errors.py`, `app/candidates/__init__.py`,
+  `app/templates/base.html`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def get_profile(conn, candidate_id: int) -> dict
+    # headline, location, timezone, summary, skills: list[str] (sorted), updated_at (None if never saved)
+def save_profile(conn, candidate_id: int, headline: str, location: str, timezone: str,
+                 summary: str, skills_text: str) -> None
+```
+Routes: `candidates.today` GET `/candidate/`, `candidates.profile` GET/POST `/candidate/profile`.
+Both `@login_required` and `@role_required("candidate")`.
+
+## Steps
+1. Tests first.
+2. `get_profile`: read `candidate_profiles` (create nothing; if the row is missing return defaults),
+   join skills.
+3. `save_profile`: strip all text, validate (collect all errors), `parse_skill_list`, then in one
+   transaction: upsert profile (`INSERT ... ON CONFLICT(user_id) DO UPDATE`), delete old
+   `candidate_skills`, insert new ones via `get_or_create_skill_ids`, audit `profile.update`.
+4. Profile page: form with the five fields (timezone as a `select_field` of
+   `sorted(zoneinfo.available_timezones())`), current skills shown as badges, errors per field.
+5. Today page: "Good morning, <display name>" style heading, a card listing what is missing
+   (no skills, no resume, no summary) with links to `/candidate/profile` and `/candidate/resume`.
+   T18 adds widgets later; leave a `{% block today_widgets %}{% endblock %}`.
+
+## Tests (`tests/unit/test_can_profile.py`)
+- save then get returns the same values; skills normalised, deduped, sorted
+- each limit: one character over gives a field error; nothing saved
+- invalid timezone `Mars/Base` rejected
+- skills text with 31 skills rejected
+- saving again replaces skills (old ones gone)
+- employer session GET `/candidate/profile` gives 403; signed out gives redirect to login
+- POST profile form via `csrf_post` saves and redirects with a flash
+
+## Done when
+- check and scope pass
+
+## Pitfalls
+- `app/skills.py` is provisional and owned by T11. Do not edit it. Use simple test skills like
+  "Python" and "sql" whose normal form will not change.
diff --git a/docs/tasks/T08.md b/docs/tasks/T08.md
new file mode 100644
index 0000000..d2b32bb
--- /dev/null
+++ b/docs/tasks/T08.md
@@ -0,0 +1,77 @@
+# T08 · Resume upload, list, delete, private download
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | CAN | T07 | no | READY (rules from the brief, defaults below) |
+
+## Goal
+A candidate can upload a resume, see and delete their resumes, and download them. Nobody else can,
+except as the brief allows.
+
+## Requirement
+FP-CAN-1 (private resume rules). Rule text: (from the brief)
+Defaults: PDF only (extension `.pdf` and content starting with `%PDF-`), size limit
+`MAX_UPLOAD_MB`, at most 5 resumes per candidate. Who may view: the owner; and an employer who owns a
+job that has an application using this resume.
+
+## Owns
+- `app/candidates/resume_service.py`
+- `app/candidates/routes_resume.py`
+- `app/templates/candidates/resume.html`
+- `tests/unit/test_can_resume.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/04-AUTH-SECURITY.md` (section: File uploads)
+- `docs/plan/07-CONTRACTS.md` (sections: candidates: resume)
+- `docs/plan/03-DATA-MODEL.md` (tables: resumes, applications, jobs, companies)
+- `app/audit.py`, `app/db.py`, `app/errors.py`, `app/security.py`, `app/candidates/__init__.py`,
+  `app/candidates/profile_service.py`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def save_resume(conn, upload_dir: str, owner_id: int, file) -> int
+def list_resumes(conn, owner_id: int) -> list[dict]
+def delete_resume(conn, upload_dir: str, owner_id: int, resume_id: int) -> None
+def can_view_resume(conn, viewer_id: int, viewer_role: str, resume_id: int) -> bool
+def get_resume_for_download(conn, viewer_id: int, viewer_role: str, resume_id: int) -> dict
+```
+Routes: `candidates.resume` GET/POST `/candidate/resume` (candidate only),
+`candidates.resume_delete` POST `/candidate/resume/<int:resume_id>/delete` (candidate only),
+`candidates.resume_download` GET `/resumes/<int:resume_id>` (any signed-in user; access checked).
+
+## Steps
+1. Tests first.
+2. `save_resume`: no file or empty name: `ValidationError({"resume": "Choose a PDF file."})`.
+   Check extension lower-cased, read the first 5 bytes (`file.stream.read(5)` then `seek(0)`),
+   check count limit. Stored name `secrets.token_hex(16) + ".pdf"`, path
+   `os.path.join(upload_dir, stored_name)`. Save, then insert the row in a transaction with
+   `os.path.getsize`. If the insert fails, delete the file. Audit `resume.upload`.
+3. `delete_resume`: owner only (else `NotFound`); delete row in a transaction, then the file
+   (ignore a missing file). Audit `resume.delete`.
+4. `can_view_resume` and `get_resume_for_download`: rules above, in SQL with `?` placeholders.
+   Missing or not allowed: `NotFound` (404, so ids cannot be probed).
+5. Download route: `send_file(path, as_attachment=True, download_name=<secure_filename of original
+   name or "resume.pdf">, mimetype="application/pdf")`.
+6. Over-size uploads: Flask raises 413 before the route runs; the 413 error page handles it.
+7. Page: upload form (`enctype="multipart/form-data"`), list with name, size, date, download and
+   delete (delete is a POST form with `csrf_field()`). Privacy line: "Only you and employers you
+   apply to can open your resume."
+
+## Tests (`tests/unit/test_can_resume.py`; remove the skip on the template test)
+- `test_fp_can_1_profile_and_private_resume_rules`: profile saved (through `profile_service`);
+  PDF upload works; `.txt` rejected; a file named `.pdf` without `%PDF-` rejected; owner can
+  download (200, `Content-Disposition: attachment`); another candidate gets 404; an unrelated
+  employer gets 404; an employer whose job has an application with this resume gets 200 (create the
+  application with `make_application` and SQL to set `resume_id`).
+- upload over the size limit returns 413 (set `MAX_UPLOAD_MB` small in a test app)
+- delete removes the row and the file; deleting someone else's gives 404
+- stored file name is never the uploaded name; `../../evil.pdf` as a name is stored safely
+- sixth resume rejected
+
+## Done when
+- check and scope pass
+
+## Pitfalls
+- Never build a path from `original_name`.
+- Never put uploads under `static/`.
diff --git a/docs/tasks/T09.md b/docs/tasks/T09.md
new file mode 100644
index 0000000..0e7f5c3
--- /dev/null
+++ b/docs/tasks/T09.md
@@ -0,0 +1,56 @@
+# T09 · Company profile and employer home
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | EMP | T05 | no | READY (limits from the brief, defaults below) |
+
+## Goal
+An employer can create and edit one company profile, and has a home page.
+
+## Requirement
+FP-EMP-1: company profile. Rule text: (from the brief)
+Defaults: name required, 1 to 120 chars; industry max 80; location max 80; website optional, if given
+must start with `https://` or `http://` and be max 200 chars; description max 4000.
+
+## Owns
+- `app/employers/service.py`
+- `app/employers/routes.py`
+- `app/templates/employers/*`
+- `tests/unit/test_emp_company.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: employers, `app/security.py`)
+- `docs/plan/05-UX-FLOWS.md` (sections: Journey: employer, Forms, Empty states)
+- `app/audit.py`, `app/db.py`, `app/errors.py`, `app/employers/__init__.py`,
+  `app/templates/base.html`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def get_company(conn, employer_id: int) -> dict | None
+def get_company_by_id(conn, company_id: int) -> dict | None
+def save_company(conn, employer_id: int, name: str, industry: str, location: str,
+                 website: str, description: str) -> int
+```
+Routes: `employers.home` GET `/employer/`, `employers.company` GET/POST `/employer/company`. Both
+`@role_required("employer")`.
+
+## Steps
+1. Tests first.
+2. `save_company`: strip, validate, upsert on `owner_id` (`ON CONFLICT(owner_id) DO UPDATE`), audit
+   `company.update`, return the company id.
+3. Company page: the form, with the website shown as plain text (never as an unescaped link).
+4. Home page: if no company, a card "Create your company profile to post jobs" with a button to
+   `/employer/company`. Otherwise company name and links to `/employer/jobs` and "Post a job"
+   `/employer/jobs/new`. T10 owns those pages.
+
+## Tests (`tests/unit/test_emp_company.py`; remove the skip on the template test)
+- `test_fp_emp_1_company_profile`: create, read back, update (same id), every validation error,
+  one company per employer.
+- `javascript:alert(1)` as website rejected
+- candidate GET `/employer/company` gives 403
+- POST through the form works and redirects with a flash
+- a name with `<script>` is shown escaped on the page
+
+## Done when
+- check and scope pass

```
