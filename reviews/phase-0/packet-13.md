# Review packet phase-0 (13 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/tasks/T10.md, docs/tasks/T11.md, docs/tasks/T12.md, docs/tasks/T13.md, docs/tasks/T14.md

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
diff --git a/docs/tasks/T10.md b/docs/tasks/T10.md
new file mode 100644
index 0000000..0c268a3
--- /dev/null
+++ b/docs/tasks/T10.md
@@ -0,0 +1,63 @@
+# T10 · Jobs: create, edit, close, delete, detail
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | EMP | T09 | no | READY (rules from the brief, defaults below) |
+
+## Goal
+An employer can post, edit, close and delete jobs with required skills. Anyone signed in can view
+an open job's detail page.
+
+## Requirement
+FP-EMP-2: job validation and deletion. Rule text: (from the brief)
+Defaults: title 1 to 120 chars; description 1 to 5000; location max 80; employment type one of
+`EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "internship")`; salary min and max
+optional whole numbers from 0 to 10_000_000, min <= max; skills 1 to 30. Delete: also deletes its
+applications, slots and bookings (database cascade) unless the brief says otherwise.
+
+## Owns
+- `app/jobs/service.py`
+- `app/jobs/routes.py`
+- `app/templates/jobs/*`
+- `tests/unit/test_emp_jobs.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: jobs, employers, `app/skills.py`)
+- `docs/plan/03-DATA-MODEL.md` (tables: jobs, job_skills, companies, applications, interview_slots)
+- `docs/plan/05-UX-FLOWS.md` (screen list rows for jobs)
+- `app/employers/service.py`, `app/skills.py`, `app/audit.py`, `app/db.py`, `app/errors.py`,
+  `app/jobs/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+The `jobs` section of `07-CONTRACTS.md`, exactly. Every employer route is
+`@role_required("employer")`. `jobs.detail` is `@login_required`; a closed job is 404 unless the
+viewer owns it.
+
+## Steps
+1. Tests first.
+2. A private `_validate(...)` returns cleaned values or raises `ValidationError` with all field
+   errors. Salary: empty string means None; otherwise `int()` inside `try`; reject non-numbers.
+3. `create_job`: employer must have a company (`ValidationError({"company": "Create your company
+   profile first."})`). Insert job and `job_skills` in one transaction. Audit `job.create`.
+4. `get_owned_job`: select where `jobs.id = ? AND companies.owner_id = ?`; none: `NotFound`.
+5. `update_job`, `delete_job`: use `get_owned_job` first. Audit `job.update`, `job.delete`.
+6. `list_open_jobs`: one query for jobs with company name, one query for all their skills, then group
+   in Python (no query per job).
+7. Routes and templates: list (with empty state), form (new and edit share `jobs/form.html`), a
+   confirm-delete page that states what else is deleted (counts of applications and slots), detail
+   page with skills as badges and a link "Apply to this job" to `/jobs/<id>/apply` (T14 builds it).
+
+## Tests (`tests/unit/test_emp_jobs.py`; remove the skip on the template test)
+- `test_fp_emp_2_job_validation_and_deletion`: parametrised invalid inputs each give the right field
+  error and no row; a valid job saved with normalised skills; delete removes it plus its
+  applications and slots; employer B deleting employer A's job gets `NotFound` and nothing is deleted.
+- no company yet: create gives the company error
+- `list_open_jobs` excludes closed jobs and includes skills for each
+- `list_open_jobs` runs a fixed number of queries no matter how many jobs (use
+  `conn.set_trace_callback` to count; 50 jobs, at most 3 queries)
+- detail of a closed job: owner 200, other users 404; missing job 404
+- candidate POST to `/employer/jobs/new` gives 403
+
+## Done when
+- check and scope pass
diff --git a/docs/tasks/T11.md b/docs/tasks/T11.md
new file mode 100644
index 0000000..a260e8a
--- /dev/null
+++ b/docs/tasks/T11.md
@@ -0,0 +1,72 @@
+# T11 · Matching engine and skill normalisation
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | MATCH | T05, T-BRIEF | no | **BLOCKED**: rules only in the brief |
+
+## Goal
+A pure, deterministic engine that scores a candidate against a job and ranks every job exactly as
+the brief says, and the brief's skill normalisation.
+
+## Requirement
+FP-MATCH-1: skill-overlap examples, normalization and floor; both tie-breakers.
+
+Rule text (T-BRIEF fills these; until then this card is BLOCKED):
+- Normalisation rule: (from the brief)
+- Score formula: (from the brief)
+- The floor: (from the brief)
+- Tie-breaker 1: (from the brief)
+- Tie-breaker 2: (from the brief)
+- Worked examples, verbatim: (from the brief)
+
+## Owns
+- `app/skills.py`
+- `app/matching/engine.py`
+- `tests/unit/test_matching.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/BRIEF.md` (matching section only)
+- `docs/plan/07-CONTRACTS.md` (sections: matching, `app/skills.py`, jobs)
+- `app/skills.py`, `tests/conftest.py`
+
+## Contract
+```python
+# app/matching/engine.py  (pure: import only app.skills and the standard library)
+def score(candidate_skills: set[str], job_skills: set[str]) -> dict
+    # {"score": <number>, "matched": sorted list, "missing": sorted list}
+def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]
+```
+`app/matching/service.py` (database side) is T13's job, not this task's.
+`rank` input jobs are dicts shaped like `jobs.service.list_open_jobs` output (each has `id`,
+`title`, `skills` as a list of normalised names, `created_at`, and more). Build such dicts by hand
+in tests; this task uses no database. Output: new dicts with every original key unchanged, plus `score`, `matched`, `missing`.
+
+## Steps
+1. Tests first: one parametrised test case per brief example, inputs and outputs exactly as written,
+   with a `# brief: <section>` comment. Run them. See them fail.
+2. `normalise_skill`: replace the provisional body with the brief's rule. Keep the signature.
+3. `score`: the brief's formula and floor. Use `fractions` or integers if the brief's numbers need
+   exact arithmetic; never compare floats with `==`.
+4. `rank`: `sorted()` with a key tuple built from the score and the two tie-breakers in the brief's
+   order. Add a final key `job["id"]` so equal items are always in the same order (unless the brief
+   defines the last tie-breaker as something else). Copy each dict (`dict(job)`), never mutate.
+5. Property tests (fixed seed `random.Random(1234)`, 200 rounds): `rank` returns every job exactly
+   once; the input list and dicts are unchanged afterwards; running twice gives the same order.
+
+## Tests (`tests/unit/test_matching.py`; remove both skips)
+- `test_fp_match_1_examples_normalization_and_floor`: every brief example, each normalisation case,
+  the floor at, just under and just over the boundary.
+- `test_fp_match_1_both_tie_breakers`: a pair that ties on score and is split by tie-breaker 1; a
+  pair that ties on score and tie-breaker 1 and is split by tie-breaker 2; reverse the input order and
+  get the same result.
+- extra: job with no skills; candidate with no skills; empty job list; property tests above.
+
+## Done when
+- check and scope pass
+- every brief example is a test case
+
+## Pitfalls
+- T07 and T10 already store skills with the provisional rule. If the brief's rule differs (for
+  example synonyms), say so in your reply under OPEN QUESTIONS: existing rows may need re-normalising,
+  which is a contract change, not part of this task.
diff --git a/docs/tasks/T12.md b/docs/tasks/T12.md
new file mode 100644
index 0000000..a48466d
--- /dev/null
+++ b/docs/tasks/T12.md
@@ -0,0 +1,71 @@
+# T12 · Time zone helpers and interview slots
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 2 | SCHED | T05 | no | READY (rules from the brief, defaults below) |
+
+## Goal
+Employers add interview slots for their jobs in their own time zone. Slots are stored in UTC and
+shown correctly in any time zone. Invalid slots are rejected.
+
+## Requirement
+FP-SCHED-1: slot creation, timezones and deletion; invalid slots. Rule text: (from the brief)
+Defaults: date `YYYY-MM-DD`, times `HH:MM` 24-hour; end after start; length 15 to 240 minutes;
+start must be in the future; no overlap with another slot of the same job; a booked slot cannot be
+deleted (`Conflict("This slot is booked and cannot be deleted.")`).
+
+## Owns
+- `app/timeutil.py`
+- `app/scheduling/slots.py`
+- `app/scheduling/routes_employer.py`
+- `app/templates/scheduling/slots.html`
+- `tests/unit/test_timeutil.py`
+- `tests/unit/test_sched_slots.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: scheduling, jobs)
+- `docs/plan/03-DATA-MODEL.md` (tables: interview_slots, bookings, jobs, companies)
+- `app/audit.py`, `app/db.py`, `app/errors.py`, `app/scheduling/__init__.py`,
+  `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+`app/timeutil.py` and `app/scheduling/slots.py` exactly as in `07-CONTRACTS.md`. Routes
+`scheduling.slots` GET/POST `/employer/jobs/<int:job_id>/slots`, `scheduling.delete_slot` POST
+`/employer/slots/<int:slot_id>/delete`, both `@role_required("employer")`.
+
+Ownership of the job: query `jobs JOIN companies` where `companies.owner_id = ?` directly in
+`slots.py`. Do not import `app.jobs.service` (another lane).
+
+## Steps
+1. Tests first.
+2. `timeutil`: use `zoneinfo.ZoneInfo`. `validate_tz` raises `ValueError` for unknown names (catch
+   `ZoneInfoNotFoundError` and `ValueError`). `local_to_utc`: parse with `datetime.strptime`, attach
+   the zone, convert to UTC, then convert back and compare with the input; if different, the time does
+   not exist (DST gap): `ValueError`. Output format `%Y-%m-%dT%H:%M:%SZ`. `COMMON_TIMEZONES`: UTC,
+   Asia/Hong_Kong, Asia/Shanghai, Asia/Jakarta, Asia/Singapore, Europe/London, America/New_York.
+3. `create_slot`: validate every field (collect errors), check job ownership (`NotFound`), future
+   start (compare with `now_iso()` as strings is fine: same format), overlap query
+   (`starts_at < ? AND ends_at > ?`), insert, audit `slot.create`.
+4. `delete_slot`: ownership via slot's job; booked: `Conflict`; else delete, audit `slot.delete`.
+5. `list_slots_for_job`: one query with `LEFT JOIN bookings`, `booked` as bool, ordered by start.
+6. Page: add-slot form (date, start, end, time zone select defaulting to the employer's last used
+   zone or UTC), list in the chosen zone using `format_local`, delete button only on open slots.
+
+## Tests
+`tests/unit/test_timeutil.py`:
+- `2030-01-07 10:00 Asia/Hong_Kong` gives `2030-01-07T02:00:00Z`; shown in `Europe/London` as 02:00
+- a nonexistent New York DST time (`2030-03-10 02:30 America/New_York`) raises `ValueError`
+- round trip for 200 random local times in 3 zones (fixed seed) gives the same local time back
+- `validate_tz("Mars/Base")` raises
+
+`tests/unit/test_sched_slots.py` (remove both skips):
+- `test_fp_sched_1_slot_creation_timezones_and_deletion`: create in Hong Kong time, stored UTC is
+  right, listed with `booked False`; delete works; booked slot delete gives `Conflict` (insert a
+  booking with SQL).
+- `test_fp_sched_1_invalid_slots`: parametrised: bad date, bad time, end before start, too short,
+  too long, in the past, overlapping, unknown zone, someone else's job (`NotFound`).
+- candidate POST to the slots page gives 403
+
+## Done when
+- check and scope pass
diff --git a/docs/tasks/T13.md b/docs/tasks/T13.md
new file mode 100644
index 0000000..87d927b
--- /dev/null
+++ b/docs/tasks/T13.md
@@ -0,0 +1,53 @@
+# T13 · Recommendations page
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | CAN + MATCH + EMP | T07, T10, T11 | yes | BLOCKED until T11 is merged |
+
+## Goal
+A candidate sees every open job ranked for them, each with its score and which skills matched and
+which are missing.
+
+## Requirement
+FP-CAN-2: recommendations preserve fields and rank all jobs. Rule text: (from the brief)
+Which fields each card shows: (from the brief). Default: title, company name, location, employment
+type, salary range or "Not stated", score, matched, missing.
+
+## Owns
+- `app/matching/service.py`
+- `app/matching/routes.py`
+- `app/templates/matching/*`
+- `tests/unit/test_can_recommend.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: matching, jobs, candidates: profile)
+- `docs/plan/05-UX-FLOWS.md` (sections: Recommendations card, Empty states)
+- `app/matching/engine.py`, `app/jobs/service.py`, `app/candidates/profile_service.py`,
+  `app/matching/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+```python
+def recommend_for(conn, candidate_id: int) -> list[dict]          # rank(skills, list_open_jobs(conn))
+def score_candidate_for_job(conn, candidate_id: int, job_id: int) -> dict   # engine.score for one job
+```
+Route `matching.recommendations` GET `/candidate/recommendations`, `@role_required("candidate")`.
+
+## Steps
+1. Tests first.
+2. `recommend_for`: `set(get_profile(conn, candidate_id)["skills"])`, `list_open_jobs(conn)`, `rank`.
+3. `score_candidate_for_job`: `get_job` (NotFound if missing or closed), then `engine.score`.
+4. Page: one card per job in the returned order, `score_bar`, "Matched:" and "Missing:" lists,
+   link to `/jobs/<id>`. Empty states from `05-UX-FLOWS.md` (no skills; no open jobs).
+
+## Tests (`tests/unit/test_can_recommend.py`; remove the skip)
+- `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs`: 5 open jobs and 1 closed;
+  result has exactly the 5 (or what the brief says about closed ones); every key from
+  `list_open_jobs` is present with the same value; order equals `engine.rank` on the same input; a
+  zero-overlap job is still present (unless the brief says otherwise).
+- page shows jobs in the same order as the service (check the titles' positions in the HTML)
+- candidate with no skills sees the empty-state text
+- employer GET gives 403
+
+## Done when
+- check and scope pass; then this goes through the merge review (it joins lanes)
diff --git a/docs/tasks/T14.md b/docs/tasks/T14.md
new file mode 100644
index 0000000..16be56d
--- /dev/null
+++ b/docs/tasks/T14.md
@@ -0,0 +1,67 @@
+# T14 · Apply with a confirm screen, my applications, statuses
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 3 | CAN + EMP | T08, T10 | yes | READY (statuses from the brief, defaults below) |
+
+## Goal
+A candidate applies to an open job through a confirm screen that shows exactly what will be shared,
+and can see all their applications. A second pending application to the same job is refused.
+
+## Requirement
+FP-CAN-3: pending duplicate and application owner. Rule text: (from the brief)
+Defaults: `STATUSES = ("pending", "interview", "rejected", "hired", "withdrawn")`;
+`TRANSITIONS = {"pending": ("interview", "rejected"), "interview": ("hired", "rejected"),
+"rejected": (), "hired": (), "withdrawn": ()}`; re-applying is allowed only when no application to
+that job is `pending`; duplicate pending gives `Conflict("You already have a pending application
+for this job.")` and HTTP 409. Cover note max 2000 chars.
+
+## Owns
+- `app/applications/statuses.py`
+- `app/applications/service.py`
+- `app/applications/routes_candidate.py`
+- `app/templates/applications/confirm.html`
+- `app/templates/applications/mine.html`
+- `tests/unit/test_can_apply.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/plan/07-CONTRACTS.md` (sections: applications, jobs, candidates: resume)
+- `docs/plan/05-UX-FLOWS.md` (sections: Confirm application, Empty states)
+- `docs/plan/03-DATA-MODEL.md` (table: applications and its unique index)
+- `app/jobs/service.py`, `app/candidates/resume_service.py`, `app/audit.py`, `app/db.py`,
+  `app/errors.py`, `app/applications/__init__.py`, `app/templates/components/*`, `tests/conftest.py`
+
+## Contract
+The `applications` T14 parts of `07-CONTRACTS.md`. Routes: `applications.confirm` GET and
+`applications.submit` POST `/jobs/<int:job_id>/apply`, `applications.mine` GET
+`/candidate/applications`, all `@role_required("candidate")`.
+
+## Steps
+1. Tests first.
+2. `apply`: job must exist and be open (`get_job`; closed: `NotFound`). `resume_id`, if given, must
+   belong to the candidate (`list_resumes`; else `ValidationError({"resume": ...})`). Check for an
+   existing pending application first (friendly `Conflict`), then insert inside
+   `transaction(conn, immediate=True)` and also catch `sqlite3.IntegrityError` from the unique index
+   as the same `Conflict` (two clicks at once). Audit `application.submit`.
+3. `get_own_application`: by id and candidate id; else `NotFound`.
+4. `list_for_candidate`: one query joining jobs and companies, newest first.
+5. Confirm page uses `confirm_box`: the job and company, a resume select (or "No resume, apply without
+   one"), cover note, and "Shared with <company>: the selected resume, your name, your cover note.
+   Not shared: your email, your other applications." Primary button "Submit application".
+6. Submit: success redirects to `/candidate/applications` with flash "Application sent to <company>";
+   `Conflict` re-renders the confirm page with the message and status 409.
+7. Mine page: table with job, company, date, status badge (`LABELS`), link to
+   `/candidate/applications/<id>` (T16 builds it).
+
+## Tests (`tests/unit/test_can_apply.py`; remove the skip)
+- `test_fp_can_3_pending_duplicate_and_application_owner`: apply once works; second apply to the
+  same job gives `Conflict` and still one row; after setting the first to `rejected` with SQL, apply
+  again works (or what the brief says); candidate B cannot `get_own_application` A's (`NotFound`).
+- applying to a closed job: `NotFound`; to a missing job: 404 via the route
+- someone else's resume id rejected
+- the confirm page shows the company name and the privacy lines
+- employer POST to apply gives 403
+
+## Done when
+- check and scope pass; then merge review

```
