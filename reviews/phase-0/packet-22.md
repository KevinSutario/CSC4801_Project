# Review packet phase-0 (22 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/phase-0/packet-10.md

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
diff --git a/reviews/phase-0/packet-10.md b/reviews/phase-0/packet-10.md
new file mode 100644
index 0000000..69f360e
--- /dev/null
+++ b/reviews/phase-0/packet-10.md
@@ -0,0 +1,653 @@
+# Review packet phase-0 (10 of 20)
+
+Worktree: /Users/mac/CSC4801_TeamA
+
+Files in this packet: docs/state/STATUS.md, docs/tasks/B1.md, docs/tasks/T-BRIEF.md, docs/tasks/T00.md, docs/tasks/T01.md, docs/tasks/T02.md
+
+## Review type: phase 0
+
+Compare: 4b825dc642cb6eb9a060e54bf8d69288fbee4904..dev
+
+## Requirements
+
+# 01 · Requirements
+
+Every graded requirement, where its rule text lives, which task builds it, and which tests prove it.
+
+## Status legend
+
+- **READY**: enough is known to build it. Exact limits still come from `docs/BRIEF.md` if the brief
+  states them.
+- **BLOCKED**: the rule is defined only in the brief, and the brief has not been pasted in yet.
+  No agent may write logic for a BLOCKED item. Tasks that need it stop at the test-writing step.
+
+## How to unblock
+
+1. Paste the full course brief into `docs/BRIEF.md`, keeping its headings and requirement IDs.
+2. For each row below, copy the exact rule sentence(s) into the "Rule text" column.
+3. Answer the open questions listed for that row, using only the brief.
+4. Change the status to READY and log it in `docs/state/DECISIONS.md`.
+
+## Requirement table
+
+The test names come from the course template. Keep them exactly. Tests live in per-task files
+(`07-CONTRACTS.md`, "Test files and owners") so parallel lanes never edit the same test file.
+
+### Accounts (FP-AUTH)
+
+| ID | What the template says | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-AUTH-1 | Registration and session lifecycle; invalid registration | READY (limits from brief) | T05 | `test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`, `::test_fp_auth_1_invalid_registration` |
+| FP-AUTH-2 | Salted hash and password verification | READY | T05 | `test_auth.py::test_fp_auth_2_salted_hash_and_password_verification` |
+| FP-AUTH-3 | Authorization and missing object | READY (status codes from brief) | T06 (phase 3 sweep); each feature task also tests its own routes | `test_auth.py::test_fp_auth_3_authorization_and_missing_object` |
+
+Open questions for the brief:
+- FP-AUTH-1: allowed roles at sign-up? Password length and rules? Email format rules? Session lifetime?
+- FP-AUTH-3: for another user's object, return 403 or 404? For a missing object, 404?
+
+### Candidate (FP-CAN)
+
+| ID | What the template says | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-CAN-1 | Profile and private resume rules | READY (limits from brief) | T07, T08 | `test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules` |
+| FP-CAN-2 | Recommendations preserve fields and rank all jobs | BLOCKED on FP-MATCH-1 | T13 | `test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
+| FP-CAN-3 | Pending duplicate and application owner | READY (statuses from brief) | T14 | `test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
+
+Open questions:
+- FP-CAN-1: required profile fields? Resume file types and size limit? Who may see a resume
+  (only the owner, or also employers the candidate applied to)?
+- FP-CAN-2: which fields must each recommendation show? Do zero-score jobs appear?
+- FP-CAN-3: application status list? Can a candidate re-apply after a rejection or withdrawal?
+
+### Employer (FP-EMP)
+
+| ID | What the template says | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-EMP-1 | Company profile | READY | T09 | `test_emp_company.py::test_fp_emp_1_company_profile` |
+| FP-EMP-2 | Job validation and deletion | READY (limits from brief) | T10 | `test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion` |
+| FP-EMP-3 | Applicant fields, order, status and role | READY (order from brief) | T15 | `test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
+
+Open questions:
+- FP-EMP-2: required job fields and limits? On delete, what happens to its applications and slots?
+- FP-EMP-3: which applicant fields are shown? Sort order? Which status changes are allowed?
+
+### Matching (FP-MATCH)
+
+| ID | What the template says | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-MATCH-1 | Skill-overlap examples, normalization and floor; both tie-breakers | **BLOCKED** | T11 | `test_matching.py::test_fp_match_1_examples_normalization_and_floor`, `::test_fp_match_1_both_tie_breakers` |
+
+Open questions (the brief must answer every one before T11 starts):
+- How is a skill normalised (case, whitespace, punctuation, synonyms)?
+- What is the score formula (overlap count, fraction of job skills, Jaccard)?
+- What is "the floor" (a minimum score, or rounding down)?
+- What are the two tie-breakers, in order?
+- Do the brief's worked examples exist? Copy every one, inputs and expected outputs, verbatim.
+
+### Scheduling (FP-SCHED)
+
+| ID | What the template says | Status | Task | Tests |
+|---|---|---|---|---|
+| FP-SCHED-1 | Slot creation, timezones and deletion; invalid slots | READY (rules from brief) | T12 | `test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_sched_slots.py::test_fp_sched_1_invalid_slots` |
+| FP-SCHED-2 | Eligible and ineligible booking | **BLOCKED** | T16 | `test_sched_booking.py::test_fp_sched_2_eligible_booking`, `test_sched_booking.py::test_fp_sched_2_ineligible_booking` |
+| FP-SCHED-3 | Booking conflict contract | **BLOCKED** | T17 | `test_sched_booking.py::test_fp_sched_3_conflict_contract` |
+
+Open questions:
+- FP-SCHED-1: slot length limits? Can slots overlap for one employer? Slots in the past? Which
+  timezone is shown to whom? Can a booked slot be deleted?
+- FP-SCHED-2: who is eligible to book (an application in which status, for which job)?
+- FP-SCHED-3: exactly what happens when two people book the same slot, or one person books twice?
+  What status code and message? This is a "contract", so the brief likely states it word for word.
+
+### Non-functional and delivery
+
+| Item | Source | Task |
+|---|---|---|
+| README requirement-test table | template README | T21 |
+| SPEC.md sections | template SPEC.md | T21 |
+| INSTALL.md sections, demo accounts, reset command | template INSTALL.md | T19, T21 |
+| Docker build and start | template Dockerfile | T20 |
+| Security (no auth bypass, no XSS, no injection, no secret leaks) | audit labels `type:security` | T02, T05, T06, phase 5 |
+| Performance on small fixtures | audit labels `type:performance` | `11-TESTING.md`, phase 5 |
+| Optional AI features | template SPEC.md | not planned (optional) |
+
+
+## Changed files (whole phase)
+
+```
+ .claude/agents/implementer.md               |  49 +++++
+ .claude/agents/review-judge.md              |  61 ++++++
+ .claude/agents/reviewer.md                  |  56 +++++
+ .claude/skills/bugfix/SKILL.md              |  18 ++
+ .claude/skills/dispatch/SKILL.md            |  35 +++
+ .claude/skills/merge/SKILL.md               |  28 +++
+ .claude/skills/orient/SKILL.md              |  24 +++
+ .claude/skills/phase-gate/SKILL.md          |  19 ++
+ .claude/skills/review-task/SKILL.md         |  36 ++++
+ .dockerignore                               |   9 +
+ .env.example                                |   5 +
+ .github/ISSUE_TEMPLATE/audit_bug_report.yml |  58 +++++
+ .github/labels.yml                          |  38 ++++
+ .gitignore                                  |  17 ++
+ CLAUDE.md                                   |  83 +++++++
+ Dockerfile                                  |  20 ++
+ INSTALL.md                                  |  21 ++
+ README.md                                   |  31 +++
+ SPEC.md                                     |  23 ++
+ claude-setup/agents/implementer.md          |  49 +++++
+ claude-setup/agents/review-judge.md         |  61 ++++++
+ claude-setup/agents/reviewer.md             |  56 +++++
+ claude-setup/skills/bugfix/SKILL.md         |  18 ++
+ claude-setup/skills/dispatch/SKILL.md       |  35 +++
+ claude-setup/skills/merge/SKILL.md          |  28 +++
+ claude-setup/skills/orient/SKILL.md         |  24 +++
+ claude-setup/skills/phase-gate/SKILL.md     |  19 ++
+ claude-setup/skills/review-task/SKILL.md    |  36 ++++
+ docs/BRIEF.md                               |  12 ++
+ docs/plan/00-OVERVIEW.md                    |  70 ++++++
+ docs/plan/01-REQUIREMENTS.md                | 100 +++++++++
+ docs/plan/02-ARCHITECTURE.md                | 147 +++++++++++++
+ docs/plan/03-DATA-MODEL.md                  | 170 +++++++++++++++
+ docs/plan/04-AUTH-SECURITY.md               |  85 ++++++++
+ docs/plan/05-UX-FLOWS.md                    | 115 ++++++++++
+ docs/plan/06-DESIGN-SYSTEM.md               | 113 ++++++++++
+ docs/plan/07-CONTRACTS.md                   | 324 ++++++++++++++++++++++++++++
+ docs/plan/08-TASKS.md                       | 118 ++++++++++
+ docs/plan/09-AGENT-WORKFLOW.md              | 154 +++++++++++++
+ docs/plan/10-REVIEW-PROTOCOL.md             | 147 +++++++++++++
+ docs/plan/11-TESTING.md                     |  78 +++++++
+ docs/plan/12-DEPLOY.md                      |  48 +++++
+ docs/state/BUGS.md                          |  21 ++
+ docs/state/DECISIONS.md                     |  35 +++
+ docs/state/JOURNAL.md                       |  31 +++
+ docs/state/STATUS.md                        |  41 ++++
+ docs/tasks/B1.md                            |  44 ++++
+ docs/tasks/T-BRIEF.md                       |  57 +++++
+ docs/tasks/T00.md                           |  29 +++
+ docs/tasks/T01.md                           | 114 ++++++++++
+ docs/tasks/T02.md                           |  74 +++++++
+ docs/tasks/T03.md                           |  69 ++++++
+ docs/tasks/T04.md                           |  75 +++++++
+ docs/tasks/T05.md                           |  81 +++++++
+ docs/tasks/T06.md                           |  44 ++++
+ docs/tasks/T07.md                           |  68 ++++++
+ docs/tasks/T08.md                           |  77 +++++++
+ docs/tasks/T09.md                           |  56 +++++
+ docs/tasks/T10.md                           |  63 ++++++
+ docs/tasks/T11.md                           |  72 +++++++
+ docs/tasks/T12.md                           |  71 ++++++
+ docs/tasks/T13.md                           |  53 +++++
+ docs/tasks/T14.md                           |  67 ++++++
+ docs/tasks/T15.md                           |  63 ++++++
+ docs/tasks/T16.md                           |  66 ++++++
+ docs/tasks/T17.md                           |  48 +++++
+ docs/tasks/T18.md                           |  44 ++++
+ docs/tasks/T19.md                           |  41 ++++
+ docs/tasks/T20.md                           |  41 ++++
+ docs/tasks/T21.md                           |  47 ++++
+ docs/tasks/T22.md                           |  34 +++
+ docs/tasks/TEMPLATE.md                      |  37 ++++
+ pytest.ini                                  |   3 +
+ requirements-dev.txt                        |   3 +
+ requirements.lock                           |  19 ++
+ requirements.txt                            |   3 +
+ reviews/B1/implementer.md                   |  54 +++++
+ reviews/B1/packet-1.md                      | 206 ++++++++++++++++++
+ reviews/B1/r1.md                            |   3 +
+ reviews/B1/r2.md                            |   3 +
+ reviews/B1/r3.md                            |   3 +
+ reviews/B1/verdict.md                       |  11 +
+ reviews/README.md                           |   7 +
+ reviews/T00/implementer.md                  |  30 +++
+ reviews/T00/orchestrator-check.md           |  22 ++
+ reviews/T00/packet-1.md                     |  91 ++++++++
+ reviews/T00/r1.md                           |   3 +
+ reviews/T00/r2.md                           |   3 +
+ reviews/T00/r3.md                           |   3 +
+ reviews/T00/verdict.md                      |  11 +
+ reviews/merge-B1/packet-1.md                | 206 ++++++++++++++++++
+ reviews/merge-B1/r1.md                      |   3 +
+ reviews/merge-B1/r2.md                      |   3 +
+ reviews/merge-B1/r3.md                      |   3 +
+ reviews/merge-B1/verdict.md                 |  12 ++
+ reviews/merge-T00/orchestrator-check.md     |  25 +++
+ reviews/merge-T00/packet-1.md               |  91 ++++++++
+ reviews/merge-T00/r1.md                     |   3 +
+ reviews/merge-T00/r2.md                     |   3 +
+ reviews/merge-T00/r3.md                     |   3 +
+ reviews/merge-T00/verdict.md                |  11 +
+ ruff.toml                                   |  11 +
+ scripts/check.py                            |  65 ++++++
+ scripts/check_contracts.py                  |  97 +++++++++
+ scripts/check_scope.py                      | 119 ++++++++++
+ scripts/contracts.json                      | 324 ++++++++++++++++++++++++++++
+ scripts/install_claude_setup.py             |  36 ++++
+ scripts/make_packet.py                      | 169 +++++++++++++++
+ tests/__init__.py                           |   0
+ tests/unit/__init__.py                      |   0
+ tests/unit/test_auth.py                     |  17 ++
+ tests/unit/test_make_packet.py              |  78 +++++++
+ tests/unit/test_matching.py                 |   9 +
+ tests/unit/test_scheduling.py               |  21 ++
+ tests/unit/test_workflows.py                |  25 +++
+ 115 files changed, 6113 insertions(+)
+
+```
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
+
+
+
+## Diff
+
+```diff
+diff --git a/docs/state/STATUS.md b/docs/state/STATUS.md
+new file mode 100644
+index 0000000..8c7b22f
+--- /dev/null
++++ b/docs/state/STATUS.md
+@@ -0,0 +1,41 @@
++# Status
++
++The orchestrator updates this file. It is the orchestrator's memory between sessions.
++States: READY, BLOCKED, RUNNING, CHECKED, REVIEWED, MERGED, DONE.
++`scripts/check_contracts.py` reads the State column, so keep the table format.
++
++Current phase: **0** · Brief: **missing** (docs/BRIEF.md is empty)
++
++| Task | Phase | State | Worktree | Notes |
++|---|---|---|---|---|
++| T00 | 0 | MERGED | - | merged into dev at 42113ab; task and merge reviews PASS; gate passed (17 tests); phase-0 gate pending |
++| B1 | 0 | MERGED | - | merged at 6507ca5; task and merge reviews PASS; 20 tests passed; Phase 0 packet generation repaired |
++| T-BRIEF | - | BLOCKED | - | waiting for Kevin to paste the brief |
++| T01 | 1 | READY | - | |
++| T02 | 1 | READY | - | after T01 |
++| T03 | 1 | READY | - | after T02 |
++| T04 | 1 | READY | - | after T03 |
++| T05 | 1 | READY | - | after T04 |
++| T07 | 2 | READY | - | |
++| T08 | 2 | READY | - | after T07 |
++| T09 | 2 | READY | - | |
++| T10 | 2 | READY | - | after T09 |
++| T11 | 2 | BLOCKED | - | needs T-BRIEF |
++| T12 | 2 | READY | - | |
++| T13 | 3 | BLOCKED | - | needs T11 |
++| T14 | 3 | READY | - | after T08, T10 |
++| T15 | 3 | READY | - | after T11, T14 |
++| T16 | 3 | BLOCKED | - | needs T-BRIEF |
++| T17 | 3 | BLOCKED | - | needs T-BRIEF, T16 |
++| T18 | 3 | READY | - | after T14 |
++| T06 | 3 | READY | - | after T10, T15, T16 |
++| T19 | 4 | READY | - | after phase 3 |
++| T20 | 4 | READY | - | after phase 3 |
++| T21 | 4 | READY | - | after T19, T20 |
++| T22 | 5 | READY | - | after phase 4 |
++
++## Running now
++none
++
++## Waiting on Kevin
++- Paste the course brief into `docs/BRIEF.md`.
+diff --git a/docs/tasks/B1.md b/docs/tasks/B1.md
+new file mode 100644
+index 0000000..f397b1a
+--- /dev/null
++++ b/docs/tasks/B1.md
+@@ -0,0 +1,44 @@
++# B1 · Phase 0 review packets must not require phase--1
++
++| Phase | Lane | Depends on | Joins lanes | Status |
++|---|---|---|---|---|
++| 0 | tooling | T00 | no | READY |
++
++## Goal
++`python scripts/make_packet.py phase 0` currently fails with an ambiguous `phase--1..dev` revision. Generate complete Phase 0 packets without inventing a predecessor tag. Keep phase 1 and later comparisons against their predecessor tags.
++
++## Requirement
++Tooling only; no business rule or course brief is needed. Phase 0 contains initial repository tooling and setup; review the whole repository at `dev` against Git's empty tree because there is no preceding phase. Later phases retain the existing tag baseline.
++
++## Owns
++- `scripts/make_packet.py`
++- `tests/unit/test_make_packet.py`
++
++## May read
++- `CLAUDE.md`
++- `docs/tasks/B1.md`
++- `scripts/make_packet.py`
++- `scripts/check.py`
++- `scripts/check_scope.py`
++- `pytest.ini`
++- `ruff.toml`
++- `requirements-dev.txt`
++- `docs/plan/10-REVIEW-PROTOCOL.md`
++
++## Contract
++Keep `python scripts/make_packet.py phase <n>` and its existing packet naming/output. No new dependencies. Use the existing Git empty-tree constant for phase 0; preserve missing-tag failures for later phases.
++
++## Steps
++1. Use the existing Python 3.12 environment at `/private/tmp/keystone-phase0-venv` via PATH. Set `PYTHONDONTWRITEBYTECODE=1` and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`.
++2. Read before editing. Write an offline regression test using a temporary Git repository that invokes the real packet command for phase 0 with no tags. Show it failing with the actual missing-revision error.
++3. State the root cause. Search for the same predecessor calculation elsewhere with `git grep`; report hits without changing unrelated code.
++4. Make the smallest fix for phase 0. Test phase 1 still compares against phase-0 and fails clearly when that required tag is absent.
++5. Run regression tests, `python scripts/check.py`, and `python scripts/check_scope.py B1`. Commit on `task/B1` only. Do not generate review packets in the main repo.
++
++## Tests
++- Real CLI generates phase-0 packets without a predecessor tag and includes the repository diff.
++- Phase 1 uses phase-0 and preserves failure when its predecessor tag is absent.
++
++## Done when
++- Regression tests pass, full gate prints CHECK PASSED, and B1 scope passes.
++- Reply includes actual failing/passing output, BUG and JOURNAL blocks.
+diff --git a/docs/tasks/T-BRIEF.md b/docs/tasks/T-BRIEF.md
+new file mode 100644
+index 0000000..96e38cc
+--- /dev/null
++++ b/docs/tasks/T-BRIEF.md
+@@ -0,0 +1,57 @@
++# T-BRIEF · Fill rules from the course brief
++
++| Phase | Lane | Depends on | Joins lanes | Status |
++|---|---|---|---|---|
++| any | docs | `docs/BRIEF.md` filled by Kevin | no | BLOCKED until docs/BRIEF.md has the brief |
++
++## Goal
++Copy every business rule the app needs from the brief into the plan, word for word, so no later
++agent has to guess. Docs only. No code.
++
++## Requirement
++All FP-* ids.
++
++## Owns
++- `docs/plan/01-REQUIREMENTS.md`
++- `docs/tasks/T05.md`
++- `docs/tasks/T06.md`
++- `docs/tasks/T07.md`
++- `docs/tasks/T08.md`
++- `docs/tasks/T09.md`
++- `docs/tasks/T10.md`
++- `docs/tasks/T11.md`
++- `docs/tasks/T12.md`
++- `docs/tasks/T13.md`
++- `docs/tasks/T14.md`
++- `docs/tasks/T15.md`
++- `docs/tasks/T16.md`
++- `docs/tasks/T17.md`
++
++## May read
++- `CLAUDE.md`
++- `docs/BRIEF.md`
++- every file listed under Owns
++
++## Steps
++1. Read `docs/BRIEF.md` fully. List every requirement id it defines.
++2. In `01-REQUIREMENTS.md`, for each FP-* row: add a "Rule text" block under the table section,
++   quoting the brief exactly, with the brief's section name. Answer each "Open questions" item with a
++   quote, or write `NOT IN BRIEF`.
++3. For FP-MATCH-1 and FP-SCHED-1 to 3: copy every worked example from the brief exactly (inputs and
++   expected outputs) into the matching task card under `## Requirement`.
++4. In each task card listed under Owns: replace every "(from the brief)" placeholder with the quoted
++   rule. If a rule is `NOT IN BRIEF`, write the default already in the card and mark it
++   `DEFAULT (not in brief)`.
++5. If the brief has a requirement that no card covers: do not invent a card. List it under
++   OPEN QUESTIONS in your reply.
++6. Set Status to READY on every card whose rules are now complete. Leave BLOCKED where a rule the
++   card needs is still missing, with the reason.
++
++## Done when
++- Every FP-* row has rule text or `NOT IN BRIEF`.
++- No card still says "(from the brief)" without a quote or a DEFAULT mark.
++- `python scripts/check_scope.py T-BRIEF` passes.
++
++## Pitfalls
++- Never paraphrase a rule. Quote it. A paraphrase is how a requirement gets silently changed.
++- Do not change any card's Owns, Contract or test names.
+diff --git a/docs/tasks/T00.md b/docs/tasks/T00.md
+new file mode 100644
+index 0000000..a54894c
+--- /dev/null
++++ b/docs/tasks/T00.md
+@@ -0,0 +1,29 @@
++# T00 · Tooling and gate
++
++| Phase | Lane | Depends on | Joins lanes | Status |
++|---|---|---|---|---|
++| 0 | tooling | none | no | DONE in setup: verify and commit |
++
++## Goal
++`python scripts/check.py` works on Windows and in Docker and passes on the template repo.
++
++## Owns
++- `scripts/*`
++- `pytest.ini`
++- `ruff.toml`
++- `requirements-dev.txt`
++- `requirements.lock`
++- `.gitignore`
++
++## May read
++- `CLAUDE.md`, `docs/plan/09-AGENT-WORKFLOW.md`, `docs/plan/10-REVIEW-PROTOCOL.md`
++
++## Steps (already done in setup; the agent only verifies)
++1. `requirements.lock` contains `tzdata==2026.5`.
++2. `.gitignore` contains `instance/`, `tests/repro/`, `reviews/*/repro/`.
++3. `python -m pip install -r requirements-dev.txt`
++4. `python scripts/check.py` prints CHECK PASSED.
++5. `python scripts/check_scope.py --overlap T07 T09 T12` prints OK.
++
++## Done when
++- Steps 3 to 5 pass. Kevin commits on `dev` and tags `phase-0`.
+diff --git a/docs/tasks/T01.md b/docs/tasks/T01.md
+new file mode 100644
+index 0000000..f003f95
+--- /dev/null
++++ b/docs/tasks/T01.md
+@@ -0,0 +1,114 @@
++# T01 · App skeleton, config, database, schema, errors, blueprint stubs
++
++| Phase | Lane | Depends on | Joins lanes | Status |
++|---|---|---|---|---|
++| 1 | foundation | T00 | no | READY |
++
++## Goal
++`create_app()` builds a Flask app with config, a SQLite database created from `schema.sql`, error
++classes and handlers, and every blueprint registered (with empty route stubs), so later tasks only
++fill in their own files.
++
++## Owns
++- `app/__init__.py`
++- `app/config.py`
++- `app/db.py`
++- `app/schema.sql`
++- `app/errors.py`
++- `app/skills.py`
++- `app/security.py`
++- `app/core/*`
++- `app/auth/*`
++- `app/candidates/*`
++- `app/employers/*`
++- `app/jobs/*`
++- `app/matching/*`
++- `app/applications/*`
++- `app/scheduling/*`
++- `app/activity/*`
++- `app/templates/errors/*`
++- `tests/conftest.py`
++- `tests/unit/test_db.py`
++
++## May read
++- `CLAUDE.md`
++- `docs/plan/02-ARCHITECTURE.md`
++- `docs/plan/03-DATA-MODEL.md`
++- `docs/plan/07-CONTRACTS.md` (sections: Shared modules, Blueprint objects)
++- `.env.example`
++
++## Contract
++Exactly the `app/__init__.py`, `app/config.py`, `app/db.py`, `app/errors.py` and `app/skills.py`
++sections of `07-CONTRACTS.md`. Blueprint `__init__.py` files exactly as "Blueprint objects".
++
++Blueprint packages and their stub route modules:
++
++| Package | Blueprint name | url_prefix | Stub route modules |
++|---|---|---|---|
++| `app/core` | `core` | none | `routes.py` |
++| `app/auth` | `auth` | `/auth` | `routes.py` |
++| `app/candidates` | `candidates` | none | `routes_profile.py`, `routes_resume.py` |
++| `app/employers` | `employers` | none | `routes.py` |
++| `app/jobs` | `jobs` | none | `routes.py` |
++| `app/matching` | `matching` | none | `routes.py` |
++| `app/applications` | `applications` | none | `routes_candidate.py`, `routes_employer.py` |
++| `app/scheduling` | `scheduling` | none | `routes_employer.py`, `routes_candidate.py` |
++| `app/activity` | `activity` | none | `routes.py` |
++
++Only `auth` has a url_prefix. All other paths are written in full in their routes (see contracts).
++
++Also create empty service modules, each holding only a module docstring naming its owner task:
++`app/auth/service.py`, `app/candidates/profile_service.py`, `app/candidates/resume_service.py`,
++`app/employers/service.py`, `app/jobs/service.py`, `app/matching/engine.py`,
++`app/matching/service.py`, `app/applications/statuses.py`, `app/applications/service.py`,
++`app/applications/review_service.py`, `app/scheduling/slots.py`, `app/scheduling/booking.py`.
++
++`app/security.py` here is a **stub** with one function `def init_app(app): return None`. T02 replaces it.
++
++## Steps
++1. `app/config.py`: the `Config` class. Read env vars with `os.environ.get`. `SECRET_KEY` falls back to
++   `secrets.token_hex(32)`. Paths default under `app.instance_path`, so set them in `create_app`
++   when the env var is missing.
++2. `app/schema.sql`: copy the SQL block from `03-DATA-MODEL.md` exactly.
++3. `app/db.py`: `get_db` opens `sqlite3.connect(DATABASE, isolation_level=None,
++   detect_types=0)`, sets `row_factory = sqlite3.Row`, runs `PRAGMA foreign_keys = ON`, stores it on
++   `g`. `transaction()` is a `contextlib.contextmanager` that runs `BEGIN` or `BEGIN IMMEDIATE`,
++   yields, then `COMMIT`, and on any exception `ROLLBACK` and re-raise. `init_db()` runs
++   `executescript` on `schema.sql`. `now_iso()` uses `datetime.now(timezone.utc)` and
++   `strftime("%Y-%m-%dT%H:%M:%SZ")`. Register `close_db` with `app.teardown_appcontext` and an
++   `init-db` CLI command with `app.cli.command`.
++4. `app/errors.py`: the classes and `init_app` from the contract. Handlers render
++   `errors/<code>.html` with the right status code. A `Conflict` handler renders `errors/409.html`
++   with `message`.
++5. `app/templates/errors/{400,403,404,405,409,413,500}.html`: minimal plain HTML pages (a heading
++   and one sentence, no styling). T03 restyles them later.
++6. `app/skills.py`: the PROVISIONAL versions. Put this comment at the top:
++   `# PROVISIONAL normalisation. T11 replaces normalise_skill with the brief's rule.`
++7. Blueprint packages, stub route modules, empty service modules, `app/security.py` stub.
++8. `app/__init__.py`: `create_app(test_config=None)`: `Flask(__name__, instance_relative_config=True)`,
++   load `Config`, then `test_config` on top, fill default paths, `os.makedirs` for the instance folder
++   and `UPLOAD_DIR`, init db teardown and CLI, `errors.init_app`, `security.init_app`, register the
++   blueprints in contract order. If the database file does not exist, call `init_db()` inside an app
++   context.
++9. `tests/conftest.py`: fixtures `app` (tmp_path database and upload dir, `TESTING=True`,
++   `SECRET_KEY="test"`), `client`, `conn` (yields `get_db()` inside `app.app_context()`).
++10. `tests/unit/test_db.py`: tests below.
++
++## Tests (`tests/unit/test_db.py`)
++- every table in `03-DATA-MODEL.md` exists after `create_app` (query `sqlite_master`)
++- `PRAGMA foreign_keys` returns 1 on a connection from `get_db()`
++- a write inside `transaction()` that raises is rolled back (row count unchanged)
++- inserting two pending applications for the same job and candidate raises `sqlite3.IntegrityError`
++- inserting two bookings for the same slot raises `sqlite3.IntegrityError`
++- `now_iso()` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`
++- `parse_skill_list(" Python, sql,PYTHON ,, ")` returns `["python", "sql"]`
++- GET `/does-not-exist` returns 404
++
++## Done when
++- `python scripts/check.py` passes, `python scripts/check_scope.py T01` passes
++- `python -m flask --app app init-db` runs without error
++
++## Pitfalls
++- `isolation_level=None` means autocommit. Every write must be inside `transaction()`.
++- `executescript` commits on its own; do not call it inside `transaction()`.
++- Do not register any routes except via the stubs. Do not add templates other than `errors/`.
+diff --git a/docs/tasks/T02.md b/docs/tasks/T02.md
+new file mode 100644
+index 0000000..f979921
+--- /dev/null
++++ b/docs/tasks/T02.md
+@@ -0,0 +1,74 @@
++# T02 · Security module and audit log
++
++| Phase | Lane | Depends on | Joins lanes | Status |
++|---|---|---|---|---|
++| 1 | foundation | T01 | no | READY |
++
++## Goal
++Every request has the user loaded, every POST is CSRF-checked, every response has security headers,
++routes can require login and a role, login attempts are rate limited, and services can write to the
++audit log.
++
++## Owns
++- `app/security.py`
++- `app/audit.py`
++- `tests/unit/test_security.py`
++- `tests/unit/test_audit.py`
++
++## May read
++- `CLAUDE.md`
++- `docs/plan/04-AUTH-SECURITY.md`
++- `docs/plan/07-CONTRACTS.md` (sections: `app/security.py`, `app/audit.py`)
++- `docs/plan/03-DATA-MODEL.md` (sections: users, audit_log, Audit actions)
++- `app/__init__.py`, `app/db.py`, `app/errors.py`, `tests/conftest.py`
++
++## Contract
++`app/security.py` and `app/audit.py` sections of `07-CONTRACTS.md`, exactly.
++
++## Steps
++1. `load_user` (before_request): if `session.get("user_id")`, select the user row (id, email, role,
++   display_name); set `g.user` to a dict or None. If the id is not in the database, `session.clear()`.
++2. `csrf_token()`: `session["csrf"]` = `secrets.token_urlsafe(32)` if missing; return it.
++   `rotate_csrf()` always sets a new one.
++3. `csrf_protect` (before_request): for POST, PUT, PATCH, DELETE: compare `request.form.get("csrf_token")`
++   with `session.get("csrf")` using `hmac.compare_digest`. Missing or wrong: `abort(403)`.
++4. Security headers (after_request): exactly the list in `04-AUTH-SECURITY.md` (CSP, X-Frame-Options,
++   X-Content-Type-Options, Referrer-Policy).
++5. `login_required`: no `g.user`: GET redirects to `url_for("auth.login", next=request.path)`, other
++   methods `abort(401)`. `role_required(role)`: login check first, then wrong role `abort(403)`.
++   Use `functools.wraps`.
++6. `is_safe_next(target)`: True only if target is a non-empty string starting with `/`, not `//`,
++   and with no `\` and no scheme.
++7. Rate limit: module-level dict `key -> list of failure timestamps` (use `time.monotonic()`).
++   5 failures within 600 seconds blocks for 600 seconds from the last failure. `login_key(email, ip)`
++   returns `f"{email.strip().lower()}|{ip}"`. Store the dict at
++   `app.extensions["login_limiter"]` so tests get a fresh one per app.
++8. `init_app(app)`: register the hooks, add Jinja globals `csrf_token` and `current_user` (a
++   context processor returning `g.user`), set the empty limiter dict.
++9. `app/audit.py`: `ACTIONS` is the frozenset of the action names in `03-DATA-MODEL.md`.
++   `log_event` raises `ValueError` for an unknown action, truncates `detail` to 500 characters, and
++   inserts with `now_iso()`. It does not open its own transaction. `list_events` returns dicts, newest
++   first, filtered by actor.
++
++## Tests
++`tests/unit/test_security.py` (register a throwaway blueprint inside the test app fixture is NOT
++allowed; test through the hooks with `app.test_request_context` and the client):
++- a POST to any path without a token returns 403; with the right token it does not return 403
++- `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` present on a 404 response
++- `is_safe_next`: `/candidate/` True; `//evil.com`, `http://evil.com`, `\\evil`, `""`, `None` False
++- rate limit: 5 `record_failed_login` calls block; `reset_login_failures` unblocks; another key is
++  not blocked
++- `load_user` clears the session when the user id no longer exists
++
++`tests/unit/test_audit.py`:
++- `log_event` with an unknown action raises `ValueError`
++- events are listed newest first and only for that actor
++- detail longer than 500 characters is truncated
++
++## Done when
++- check and scope pass
++
++## Pitfalls
++- `hmac.compare_digest` needs two strings; treat a missing value as `""`.
++- Do not exempt any route from CSRF.
++- Do not put secrets or tokens in the audit `detail`.
+
+```

```
