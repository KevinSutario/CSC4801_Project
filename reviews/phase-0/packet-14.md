# Review packet phase-0 (14 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/tasks/T15.md, docs/tasks/T16.md, docs/tasks/T17.md, docs/tasks/T18.md, docs/tasks/T19.md, docs/tasks/T20.md, docs/tasks/T21.md

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
diff --git a/docs/tasks/T15.md b/docs/tasks/T15.md
new file mode 100644
index 0000000..d1f5c3d
--- /dev/null
+++ b/docs/tasks/T15.md
@@ -0,0 +1,63 @@
+# T15 · Employer applicants list and status changes
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | EMP + CAN + MATCH | T11, T14 | yes | READY (fields and order from the brief, defaults below) |
+
+## Goal
+An employer sees the applicants for one of their jobs, with the fields and order the brief requires,
+and moves an application through allowed statuses via a confirm screen.
+
+## Requirement
+FP-EMP-3: applicant fields, order, status and role. Rule text: (from the brief)
+Defaults: fields `application_id, candidate_name, headline, score, matched, missing, status,
+applied_at, resume_id`; order by score high to low, then `applied_at` oldest first, then
+`application_id`; only an employer who owns the job may see or change; transitions from
+`statuses.TRANSITIONS`; an invalid transition gives `ValidationError({"status": ...})`.
+
+## Owns
+- `app/applications/review_service.py`
+- `app/applications/routes_employer.py`
+- `app/templates/applications/applicants.html`
+- `app/templates/applications/confirm_status.html`
+- `tests/unit/test_emp_applicants.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: applications, matching, jobs)
+- `docs/plan/05-UX-FLOWS.md` (section: Applicants table)
+- `app/applications/statuses.py`, `app/matching/engine.py`, `app/jobs/service.py`,
+  `app/timeutil.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
+  `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def list_applicants(conn, employer_id: int, job_id: int) -> list[dict]
+def set_status(conn, employer_id: int, application_id: int, new_status: str) -> None
+```
+Routes: `applications.applicants` GET `/employer/jobs/<int:job_id>/applicants`;
+`applications.confirm_status` GET and `applications.set_status` POST
+`/employer/applications/<int:application_id>/status` (the target status in a `to` query or form
+field), all `@role_required("employer")`.
+
+## Steps
+1. Tests first.
+2. `list_applicants`: `get_owned_job` first. One query for the applications with candidate name and
+   headline, one query for all those candidates' skills; score each with `engine.score` against the
+   job's skills; sort by the rule; return dicts with exactly the listed keys.
+3. `set_status`: load the application joined to its job's company; not the owner: `NotFound`.
+   `new_status` not in `TRANSITIONS[current]`: `ValidationError`. Update and audit
+   `application.status` with detail `"<old> -> <new>"`.
+4. Applicants page: table (fields above; date with `format_local` in UTC unless the brief says
+   otherwise), resume link to `/resumes/<id>`, one link per allowed next status to the confirm page.
+5. Confirm-status page: `confirm_box` "Change <name>'s application from <old> to <new>?", POST form.
+
+## Tests (`tests/unit/test_emp_applicants.py`; remove the skip)
+- `test_fp_emp_3_applicant_fields_order_status_and_role`: three applicants with different and equal
+  scores; keys are exactly the listed fields; order follows the rule including both ties; allowed
+  transition works and is audited; disallowed transition rejected; employer B gets `NotFound`;
+  candidate GET gives 403.
+- query count stays fixed for 30 applicants (`set_trace_callback`)
+
+## Done when
+- check and scope pass; then merge review
diff --git a/docs/tasks/T16.md b/docs/tasks/T16.md
new file mode 100644
index 0000000..bc13476
--- /dev/null
+++ b/docs/tasks/T16.md
@@ -0,0 +1,66 @@
+# T16 · Booking: eligibility, bookable slots, confirm, book
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | SCHED + CAN | T12, T14, T-BRIEF | yes | **BLOCKED**: eligibility rule only in the brief |
+
+## Goal
+An eligible candidate sees the open slots for their application, in their time zone, and books one
+through a confirm screen. Ineligible candidates cannot book.
+
+## Requirement
+FP-SCHED-2: eligible and ineligible booking. Rule text: (from the brief)
+- Who is eligible: (from the brief). Likely shape: own application, for this slot's job, in status
+  (from the brief).
+- Can one application hold more than one booking: (from the brief). If no, add the
+  `uq_booking_application` index through a contract change request first.
+
+## Owns
+- `app/scheduling/booking.py`
+- `app/scheduling/routes_candidate.py`
+- `app/templates/scheduling/book.html`
+- `app/templates/scheduling/confirm_booking.html`
+- `tests/unit/test_sched_booking.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/BRIEF.md` (scheduling section only)
+- `docs/plan/07-CONTRACTS.md` (sections: scheduling, applications)
+- `docs/plan/03-DATA-MODEL.md` (tables: interview_slots, bookings, applications)
+- `app/timeutil.py`, `app/scheduling/slots.py`, `app/applications/service.py`,
+  `app/applications/statuses.py`, `app/candidates/profile_service.py`, `app/audit.py`, `app/db.py`,
+  `app/errors.py`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def is_eligible(conn, candidate_id: int, application_id: int) -> bool
+def list_bookable_slots(conn, candidate_id: int, application_id: int) -> list[dict]
+def book_slot(conn, candidate_id: int, application_id: int, slot_id: int) -> int
+```
+Routes: `scheduling.application_detail` GET `/candidate/applications/<int:application_id>`;
+`scheduling.confirm_booking` GET and `scheduling.book` POST
+`/candidate/applications/<int:application_id>/book/<int:slot_id>`, all `@role_required("candidate")`.
+
+## Steps
+1. Tests first, using the brief's rule and examples.
+2. `is_eligible`: `get_own_application` (raises `NotFound` for others), then the brief's rule.
+3. `list_bookable_slots`: future, unbooked slots of the application's job, start ascending.
+4. `book_slot` (simple version; T17 hardens it): own application (`NotFound`), eligible
+   (`Forbidden`), slot exists and belongs to the same job (`NotFound`), inside
+   `transaction(conn, immediate=True)`: insert booking, audit `booking.create`.
+5. Detail page: application status, then either "Book an interview" with slots shown by
+   `format_local(..., candidate timezone from get_profile)` and the zone name, or the booked slot, or
+   a line explaining why booking is not open (not eligible).
+6. Confirm page: `confirm_box` with the time in the candidate's zone and in the employer's
+   `created_tz`, and the job. POST books, redirects to the detail page with a flash.
+
+## Tests (`tests/unit/test_sched_booking.py`; remove the two FP-SCHED-2 skips, keep FP-SCHED-3 skipped)
+- `test_fp_sched_2_eligible_booking`: eligible candidate books; booking row exists; slot no longer
+  listed as bookable; detail page shows the booked time in the candidate's zone.
+- `test_fp_sched_2_ineligible_booking`: parametrised: status not eligible, another candidate's
+  application, slot of a different job, missing slot, missing application. Each refused with the
+  right error and no booking row.
+- employer GET of the detail page gives 403
+
+## Done when
+- check and scope pass; then merge review
diff --git a/docs/tasks/T17.md b/docs/tasks/T17.md
new file mode 100644
index 0000000..3151835
--- /dev/null
+++ b/docs/tasks/T17.md
@@ -0,0 +1,48 @@
+# T17 · Booking conflict contract and concurrency
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | SCHED | T16, T-BRIEF | no | **BLOCKED**: conflict contract only in the brief |
+
+## Goal
+When two people try to book the same slot, or one person books twice, the result is exactly the
+brief's conflict contract, and the database never holds a double booking.
+
+## Requirement
+FP-SCHED-3: booking conflict contract. Rule text, verbatim: (from the brief)
+- Status code: (from the brief)
+- Message or body: (from the brief)
+- What the losing user sees next: (from the brief)
+
+## Owns
+- `app/scheduling/booking.py`
+- `app/scheduling/routes_candidate.py`
+- `app/templates/scheduling/*`
+- `tests/unit/test_sched_booking.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/BRIEF.md` (scheduling section only)
+- `docs/plan/07-CONTRACTS.md` (section: scheduling)
+- `app/scheduling/booking.py`, `app/scheduling/routes_candidate.py`, `app/db.py`, `app/errors.py`,
+  `app/audit.py`, `tests/conftest.py`, `tests/unit/test_sched_booking.py`
+
+## Steps
+1. Tests first, built from the brief's contract text.
+2. In `book_slot`, inside `transaction(conn, immediate=True)`: re-check the slot is free with a
+   SELECT; if booked: raise `Conflict(<brief message>)`. Also wrap the INSERT: on
+   `sqlite3.IntegrityError` raise the same `Conflict`. Log `booking.conflict` in a **separate** small
+   transaction after the rollback (the first one is rolled back).
+3. Route: catch `Conflict` and return exactly the brief's status code and message (render
+   `scheduling/book.html` with the message, or the format the brief says).
+
+## Tests (in `tests/unit/test_sched_booking.py`; remove the FP-SCHED-3 skip)
+- `test_fp_sched_3_conflict_contract`: candidate A books slot S; candidate B (also eligible for the
+  same job) books S: gets the brief's status and message; still exactly one booking row; A's booking
+  unchanged; a `booking.conflict` audit row exists.
+- two connections: open a second `sqlite3` connection to the same file, start `BEGIN IMMEDIATE` on
+  it, insert a booking for S, commit; then `book_slot` on the first connection gives `Conflict`.
+- the same candidate booking the same slot twice gets the contract result (or what the brief says).
+
+## Done when
+- check and scope pass
diff --git a/docs/tasks/T18.md b/docs/tasks/T18.md
new file mode 100644
index 0000000..37285c5
--- /dev/null
+++ b/docs/tasks/T18.md
@@ -0,0 +1,44 @@
+# T18 · Activity log page and Today page widgets
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | governance | T14 | yes | READY |
+
+## Goal
+Every signed-in user can see what they did (Keystone's audit idea). The candidate Today page shows
+application statuses and the next step.
+
+## Owns
+- `app/activity/routes.py`
+- `app/templates/activity/*`
+- `app/templates/candidates/today.html`
+- `app/candidates/routes_profile.py`
+- `tests/unit/test_activity.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: activity, `app/audit.py`, applications, candidates: profile)
+- `docs/plan/05-UX-FLOWS.md` (sections: Empty states)
+- `app/audit.py`, `app/applications/service.py`, `app/applications/statuses.py`,
+  `app/candidates/profile_service.py`, `app/candidates/routes_profile.py`,
+  `app/templates/candidates/today.html`, `app/timeutil.py`, `tests/conftest.py`
+
+## Steps
+1. Tests first.
+2. `activity.list` GET `/activity`, `@login_required`: `list_events(conn, g.user["id"], 100)`,
+   table of time (`format_local` in the user's zone, UTC for employers), action as plain words
+   (a dict in the route: `"application.submit": "Submitted an application"` and so on for every
+   action), object. Empty state text from `05-UX-FLOWS.md`.
+3. Today page: fill `today_widgets` with "Your applications" (latest 5 from `list_for_candidate`
+   with status badges, link to all) and "Next step" (first missing profile item, or "Check your
+   recommendations").
+4. `routes_profile.py`: only pass the extra data to `today.html`. Do not change `profile`.
+
+## Tests (`tests/unit/test_activity.py`)
+- after a profile save, `/activity` shows "Updated your profile" for that user only
+- another user's events never appear
+- signed out: redirect to sign-in
+- Today page lists the candidate's latest application status
+
+## Done when
+- check and scope pass; then merge review
diff --git a/docs/tasks/T19.md b/docs/tasks/T19.md
new file mode 100644
index 0000000..7bbbaa0
--- /dev/null
+++ b/docs/tasks/T19.md
@@ -0,0 +1,41 @@
+# T19 · Demo data and reset command
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 4 | delivery | phase 3 closed | no | READY |
+
+## Goal
+One command resets the app to a known demo state that shows every feature, with the demo accounts
+from `docs/plan/12-DEPLOY.md`.
+
+## Owns
+- `scripts/seed.py`
+- `scripts/demo_resume.pdf`
+- `tests/unit/test_seed.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/12-DEPLOY.md` (section: Demo data)
+- `docs/plan/07-CONTRACTS.md` (all service signatures)
+- `app/__init__.py`, `app/db.py`, `tests/conftest.py`
+
+## Steps
+1. `scripts/seed.py`: `--reset` deletes the database file and the upload folder (paths from the app
+   config, never hard-coded), then `init_db()`. Without `--reset` it refuses if the database already
+   has users. Then it creates the demo data **through the real services** (`register`,
+   `save_profile`, `save_company`, `create_job`, `create_slot`, `apply`, `set_status`), so demo data
+   always obeys the rules. Demo password: `Demo-Keystone-2026` for all four accounts.
+2. Data: the four accounts, 5 jobs with overlapping skills (so ranking and ties show), slots in two
+   time zones, Mei Lin with one application at `interview` status (so booking is possible) and one
+   pending.
+3. `scripts/demo_resume.pdf`: a tiny valid one-page PDF with the text "Demo resume. Fictional person."
+   Attach it to Mei Lin through `save_resume` (wrap the file in `werkzeug.datastructures.FileStorage`).
+4. Also expose `seed(app)` so `wsgi.py` can seed a new database on first start.
+
+## Tests (`tests/unit/test_seed.py`)
+- `seed(app)` on the test app creates exactly 4 users, 5 jobs, and Mei Lin's recommendations are
+  not empty
+- running it twice without reset refuses and changes nothing
+
+## Done when
+- check and scope pass; `python scripts/seed.py --reset` runs locally and every demo user can sign in
diff --git a/docs/tasks/T20.md b/docs/tasks/T20.md
new file mode 100644
index 0000000..e1b0fed
--- /dev/null
+++ b/docs/tasks/T20.md
@@ -0,0 +1,41 @@
+# T20 · Dockerfile, wsgi and start-up
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 4 | delivery | phase 3 closed | no | READY |
+
+## Goal
+`docker build` and `docker run` from a fresh clone give a working app on port 8080 with demo data.
+
+## Owns
+- `Dockerfile`
+- `.dockerignore`
+- `wsgi.py`
+- `.env.example`
+- `tests/unit/test_wsgi.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/12-DEPLOY.md`
+- `Dockerfile`, `.dockerignore`, `.env.example`, `app/__init__.py`, `app/config.py`
+
+## Steps
+1. `wsgi.py`: `app = create_app()`; if the database has no users, call `scripts.seed.seed(app)`
+   (import inside a function). Under `if __name__ == "__main__":` serve with
+   `waitress.serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))`.
+2. `Dockerfile`: keep the template's base image, user and install steps. Add
+   `ENV DATABASE=/app/data/keystone.sqlite3 UPLOAD_DIR=/app/data/uploads PORT=8080`, create
+   `/app/data` owned by `student` before `USER student`, `EXPOSE 8080`, `CMD ["python", "wsgi.py"]`.
+   Remove the template TODO lines.
+3. `.env.example`: list every env var from `02-ARCHITECTURE.md` "Configuration", commented, with
+   meanings. No real secrets.
+4. `.dockerignore`: keep the template list; add `instance`, `reviews`, `tests/repro`.
+
+## Tests (`tests/unit/test_wsgi.py`)
+- importing `wsgi` with `DATABASE` and `UPLOAD_DIR` env vars set to a temp folder creates a seeded
+  database (use `monkeypatch.setenv` and `importlib.reload`)
+
+## Done when
+- check and scope pass
+- Kevin runs: `docker build -t keystone .` and `docker run --rm -p 8080:8080 keystone`, opens
+  `http://localhost:8080`, signs in as `meilin@demo.keystone`
diff --git a/docs/tasks/T21.md b/docs/tasks/T21.md
new file mode 100644
index 0000000..2534bf1
--- /dev/null
+++ b/docs/tasks/T21.md
@@ -0,0 +1,47 @@
+# T21 · README, SPEC.md, INSTALL.md
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 4 | delivery | T19, T20 | no | READY |
+
+## Goal
+Every section of the three template documents is filled with true, checkable content, and the
+README maps every requirement to its code and its named tests.
+
+## Owns
+- `README.md`
+- `SPEC.md`
+- `INSTALL.md`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/*`
+- `docs/BRIEF.md`
+- `docs/state/DECISIONS.md`
+- `scripts/contracts.json`
+- `Dockerfile`, `requirements.lock`, `.env.example`, `scripts/seed.py`
+
+## Steps
+1. Keep every heading the templates have, in their order. Fill each one. No empty section.
+2. README:
+   - Project title "Keystone", a short overview, team member "Kevin Sutario", an architecture summary
+     taken from `02-ARCHITECTURE.md`, a quick start, demo accounts (from `12-DEPLOY.md`), how to run
+     tests.
+   - Requirement–test mapping: one row per FP-* id. Implementation files from `07-CONTRACTS.md`.
+     Tests: the exact `tests/unit/<file>::<test>` names. Run `python -m pytest --collect-only -q` and
+     check every name you write exists. Remove the template's "Example rows only" note.
+   - Document index (links to SPEC.md, INSTALL.md, `docs/plan/`). Known limitations: only true ones
+     (for example: rate limiting is per process; sessions end on restart when SECRET_KEY is not set).
+3. SPEC.md: each template section from the plan files: scope (`00`), architecture (`02`), data model
+   (`03`), auth (`04`), routes (`07`), UI and workflows (`05`), matching (brief rule + `T11`),
+   scheduling and the booking transaction (brief rule + `T16`, `T17`), security controls (`04`),
+   optional AI features: "Not implemented", design decisions (`docs/state/DECISIONS.md`).
+4. INSTALL.md: versions from `Dockerfile` and `requirements.lock`; `pip install -r requirements.txt`;
+   env vars; `flask --app app init-db`; `python scripts/seed.py --reset`; Docker build and run;
+   `python -m flask --app app run --debug`; `python scripts/check.py`; troubleshooting (port in use,
+   time zone errors on Windows mean `tzdata` is missing).
+
+## Done when
+- No template heading is empty
+- Every test name in the README exists in `--collect-only` output
+- scope passes

```
