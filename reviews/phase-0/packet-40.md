# Review packet phase-0 (40 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/phase-0/packet-9.md

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
diff --git a/reviews/phase-0/packet-9.md b/reviews/phase-0/packet-9.md
new file mode 100644
index 0000000..a04e7e1
--- /dev/null
+++ b/reviews/phase-0/packet-9.md
@@ -0,0 +1,654 @@
+# Review packet phase-0 (9 of 20)
+
+Worktree: /Users/mac/CSC4801_TeamA
+
+Files in this packet: docs/plan/10-REVIEW-PROTOCOL.md, docs/plan/11-TESTING.md, docs/plan/12-DEPLOY.md, docs/state/BUGS.md, docs/state/DECISIONS.md, docs/state/JOURNAL.md
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
+diff --git a/docs/plan/10-REVIEW-PROTOCOL.md b/docs/plan/10-REVIEW-PROTOCOL.md
+new file mode 100644
+index 0000000..21574de
+--- /dev/null
++++ b/docs/plan/10-REVIEW-PROTOCOL.md
+@@ -0,0 +1,147 @@
++# 10 · Review protocol: three reviewers and a judge
++
++Every review uses the same shape: **three reviewers do the same review independently, then one
++judge checks every finding against the code and keeps only the bugs that are really there.**
++
++A single flash-model reviewer misses a lot and invents some. Three independent reviews catch more
++real bugs. The judge throws away the invented ones, so fixes are only spent on real problems.
++
++## When a review runs (triggers)
++
++| Trigger | When | What is reviewed | Packet command |
++|---|---|---|---|
++| **A. Task review** | an implementer finished a task and its check passed | the task branch against `dev` | `python scripts/make_packet.py task T07` |
++| **B. Merge review** | merging a task into `dev` after `dev` has changed since the task started (another agent's work went in), or any Phase 3 task that joins two lanes | the integration branch `int/T07` against `dev`, plus the files of the lanes it joins | `python scripts/make_packet.py merge T07` |
++| **C. Phase review** | all tasks in a phase are merged | everything changed in the phase, split into chunks by package | `python scripts/make_packet.py phase 2` |
++
++## Step by step (the orchestrator runs this, via `/review-task`)
++
++1. **Make the packet.** The command writes `reviews/<id>/packet-1.md` (and `packet-2.md`... if the
++   diff is over 400 changed lines; it splits by file). A packet holds: the task card, the
++   requirement rows, the security checklist, the diff, the check output and the scope output.
++2. **Spawn three `reviewer` subagents at the same time**, one per packet. All three get the same prompt:
++   ```
++   You are reviewer <n> of 3 for <id>. Review packet: <absolute path to packet-1.md>.
++   The code is in worktree <absolute path>. You may open any file in that worktree to check a claim.
++   Do not edit anything. Follow your agent instructions and return findings in the exact format.
++   ```
++   The `<n>` only changes which checklist section the reviewer starts from (1: correctness first,
++   2: security first, 3: tests first). The review itself is the same.
++3. **Save the three replies** as `reviews/<id>/r1.md`, `r2.md`, `r3.md`. Do not edit them.
++4. **Spawn the `review-judge`** with:
++   ```
++   You are the judge for <id>. Packet: <path>. Worktree: <path>.
++   Findings: <path>/r1.md, r2.md, r3.md. Repro folder: <worktree>/tests/repro/
++   Follow your agent instructions. Return the verdict in the exact format.
++   ```
++5. **Save the verdict** as `reviews/<id>/verdict.md`, and copy the judge's repro tests from
++   `<worktree>/tests/repro/` to `reviews/<id>/repro/` so they are kept. (`tests/repro/` is
++   gitignored and not run by the gate.)
++6. **Act on it:**
++   - `PASS` (no confirmed findings): go to merge.
++   - `FIX`: spawn an `implementer` on the same worktree with the card plus this line:
++     `Fix the CONFIRMED findings in <path>/verdict.md, in order. For each, first move its repro test
++     into the right test file as a regression test, see it fail, then fix.` Then run trigger A again
++     with **only the judge** checking each fixed finding plus `python scripts/check.py`. If the fix
++     diff is over 80 lines, run all three reviewers again.
++   - `UNCLEAR` items: ask Kevin. Do not fix guesses.
++   - After 3 rounds, stop and ask Kevin.
++
++## What reviewers check (same list for all three)
++
++1. **Requirement**: does the code do what the card and the brief rule say? Every acceptance item?
++2. **Contract**: names, signatures, routes and templates exactly as in `07-CONTRACTS.md`?
++3. **Invented things**: every function, method, column, config key and Flask API used actually
++   exists. Name the file or documentation for each one you are unsure of.
++4. **Security**: the 12-line checklist in `04-AUTH-SECURITY.md`.
++5. **Edge cases**: empty, whitespace only, too long, zero, negative, None, wrong type, duplicate,
++   someone else's id, missing id, already deleted, timezone and DST.
++6. **Transactions**: every write inside `transaction()`? Booking uses `immediate=True`?
++7. **Tests**: are the template test names present? Do tests check failure paths? Would the test
++   fail if the code were wrong (try it in your head: remove a line, does a test catch it)?
++   Any test weakened, skipped or deleted?
++8. **Scope**: any change outside the Owns list, any reformatting or refactoring not asked for?
++9. **Performance**: queries inside loops over many rows (N+1)? Loading every row where one is needed?
++
++## Reviewer output format (exact)
++
++```
++REVIEWER: <n>
++CHECKED: <list of checklist numbers you covered>
++FINDINGS: <count>
++
++F1
++severity: critical | major | minor
++category: security | functional | performance | test-gap | contract | scope
++where: app/jobs/service.py:42
++claim: <one sentence: what is wrong>
++trigger: <exact input or steps that make it go wrong>
++expected: <what should happen>
++actual: <what the code does instead>
++evidence: <the code lines, quoted>
++
++F2 ...
++```
++Rules: at most 10 findings, worst first. Only problems you can trigger or point to in a quoted line.
++No style opinions. If you found nothing, write `FINDINGS: 0` and still list what you checked.
++
++## What the judge does
++
++The judge is the higher-level agent. It trusts nothing it has not checked itself.
++
++1. **Group** findings from r1, r2 and r3 that have the same root cause. Note how many reviewers
++   found each group (1, 2 or 3).
++2. **Verify each group, one at a time:**
++   - Open the quoted lines. If the code does not say what the reviewer quoted: REJECTED.
++   - If it can be tested: write a small test in `<worktree>/tests/repro/test_<group>.py` that
++     should fail if the bug is real. It can use the normal fixtures from `tests/conftest.py`. Run it:
++     `cd <worktree> && python -m pytest tests/repro/test_<group>.py -q -p no:cacheprovider`
++     Fails as predicted: CONFIRMED. Passes: REJECTED.
++   - If it cannot be tested (docs, missing test, contract name): check by reading, quote the proof,
++     then CONFIRMED or REJECTED.
++   - If it still cannot decide: UNCLEAR, with the exact question for Kevin.
++3. **Severity**: the judge sets the final severity. Being found by 3 reviewers does not make a
++   bug real, and being found by 1 does not make it fake. Only the proof counts.
++4. **Mutation spot-check** (trigger C only): in a scratch copy of the worktree (`../ks-mut`), make 3
++   small breaking changes in the phase's most important logic (flip a comparison, remove an
++   ownership check, drop a tie-breaker). Run the tests. Any change no test catches becomes a
++   CONFIRMED `test-gap` finding.
++5. **Never edit app code or real tests.** Only files in `tests/repro/`.
++
++## Judge output format (exact)
++
++```
++JUDGE: <id>
++RESULT: PASS | FIX | UNCLEAR
++
++| Group | Found by | Category | Severity | Verdict | Proof |
++|---|---|---|---|---|---|
++| G1 (r1.F2, r3.F1) | 2 | security | critical | CONFIRMED | tests/repro/test_g1.py fails: AssertionError ... |
++| G2 (r2.F4) | 1 | functional | minor | REJECTED | line 42 already strips input: "title = title.strip()" |
++
++FIX LIST (CONFIRMED only, in this order):
++1. G1: <what to fix, where, which repro test proves it>
++2. ...
++
++QUESTIONS FOR KEVIN (UNCLEAR only):
++1. ...
++```
++
++## Merge review (trigger B) extra checks
++
++- Do both sides still use the shared contracts the same way (same function names, same status values)?
++- Do the joined features work together? The judge writes at least one repro test that goes through
++  both features (for example: employer posts a job, candidate applies, employer sees the applicant).
++- Did the merge itself change any line that neither branch changed? (It should not.)
++
++## Phase review (trigger C) extra checks
++
++- Read `01-REQUIREMENTS.md`: is every requirement in this phase built and tested?
++- `python scripts/check_contracts.py` passes.
++- The security checklist across the whole phase, not only one task.
++- The mutation spot-check above.
++
++## Bugs found later (Week 12 audit and phase 5)
++
++Each confirmed audit issue becomes a card `docs/tasks/B<issue number>.md` from `TEMPLATE.md`, using
++the bug steps in `CLAUDE.md`: failing test first, fix, log in `docs/state/BUGS.md`, then trigger A.
+diff --git a/docs/plan/11-TESTING.md b/docs/plan/11-TESTING.md
+new file mode 100644
+index 0000000..96d6f24
+--- /dev/null
++++ b/docs/plan/11-TESTING.md
+@@ -0,0 +1,78 @@
++# 11 · Testing
++
++## Rules
++
++1. **Test first for logic.** Write the test, run it, show it failing, then write the code.
++2. **Services are tested directly** with the `conn` fixture. Routes are tested with `client` only
++   for: status codes, redirects, CSRF, login and role checks, and that the page shows the right text.
++3. **Every requirement test name from the template is kept exactly** (`07-CONTRACTS.md`). A task may
++   add more tests. It never renames a template test.
++4. **Test the failure paths**, not only the happy path: missing fields, too long, wrong type, someone
++   else's object, missing object, duplicate, conflict.
++5. **No sleeping, no network, no real clock in assertions.** Use fixed UTC strings far in the future
++   (2030 and later), so tests never break as time passes.
++6. **No skipped tests at release.** Placeholders are `@pytest.mark.skip(reason="TODO Txx")` until
++   their task replaces them. `python scripts/check.py --release` fails if any test is skipped.
++7. **Brief examples are copied verbatim.** If the brief gives worked examples (matching, booking),
++   each one becomes a parametrised test case with the brief's exact inputs and outputs, and a
++   comment `# brief: <section>`.
++
++## Fixtures (`tests/conftest.py`: T01 writes app, client, conn; T04 adds the rest; then frozen)
++
++```python
++@pytest.fixture
++def app(tmp_path):         # create_app with TESTING, temp DATABASE and UPLOAD_DIR, SECRET_KEY="test"
++                           # runs init_db(); resets the login rate limiter
++@pytest.fixture
++def client(app): ...       # app.test_client()
++@pytest.fixture
++def conn(app): ...         # yields get_db() inside app.app_context()
++```
++Factory fixtures return functions (see `07-CONTRACTS.md` for signatures).
++`csrf_post(client, url, data)` reads the token from the session and adds `csrf_token` to `data`.
++
++Example:
++```python
++def test_fp_emp_2_job_validation_and_deletion(conn, make_employer, make_company):
++    emp = make_employer()
++    make_company(emp)
++    with pytest.raises(ValidationError) as e:
++        jobs_service.create_job(conn, emp, title="", description="x", location="",
++                                employment_type="", salary_min="", salary_max="", skills_text="")
++    assert "title" in e.value.errors
++```
++
++## What a good requirement test checks
++
++| Requirement | Must check at least |
++|---|---|
++| FP-AUTH-1 | register, then login works, session has user; logout clears it; protected page redirects after logout; invalid email, short password, duplicate email, bad role all rejected with field errors |
++| FP-AUTH-2 | stored hash is not the password; two users with the same password get different hashes; correct password verifies; wrong password does not |
++| FP-AUTH-3 | candidate cannot open employer pages (403); employer A cannot see or edit employer B's job (agreed code); missing id gives 404 |
++| FP-CAN-1 | profile saves and reloads; skills normalised and deduped; resume: wrong type and too-large rejected; owner can download; another candidate cannot; rules from brief for employers |
++| FP-CAN-2 | every open job is returned (count equals open jobs); each keeps all its original fields; order follows the brief; closed jobs excluded if the brief says so |
++| FP-CAN-3 | second pending application to the same job is refused with the brief's result; a candidate cannot read another's application |
++| FP-EMP-1 | create, read back, update company; validation errors; one company per employer |
++| FP-EMP-2 | every invalid field rejected; valid job saved with skills; delete removes it and follows the brief for linked rows; cannot delete another employer's job |
++| FP-EMP-3 | applicant rows have exactly the brief's fields, in the brief's order; status change follows allowed transitions; only the job's owner (employer role) can see or change |
++| FP-MATCH-1 | every brief example exactly; normalisation cases; the floor; each tie-breaker on its own, and both together |
++| FP-SCHED-1 | slot entered in Asia/Hong_Kong stored as correct UTC; shown back correctly in another zone; end before start rejected; nonexistent DST time rejected; delete works; deleting a booked slot follows the brief |
++| FP-SCHED-2 | eligible applicant books; ineligible (wrong status, another job, someone else's application) refused |
++| FP-SCHED-3 | second booking of the same slot gets exactly the brief's conflict result; the database still holds one booking |
++
++## Extra test layers (cheap, find the bugs reviewers miss)
++
++- **Property tests without new dependencies**: loop over 200 generated inputs with
++  `random.Random(1234)` (fixed seed). Use for: `rank` never drops or duplicates jobs, never mutates
++  input, is deterministic; `local_to_utc` then `utc_to_local` gives back the same local time.
++- **Mutation check** (phase gates): the judge agent breaks the code on purpose in a scratch copy
++  (flip a comparison, remove a tie-breaker, drop an ownership check) and confirms a test fails.
++  Survivors become new tests. See `10-REVIEW-PROTOCOL.md`.
++- **Performance smoke test** (T22): seed 200 jobs and 200 candidates; recommendations and
++  applicants pages each answer in under 1 second with the test client.
++
++## Requirement-test mapping (for the README, written by T21)
++
++T21 builds the README table from this file plus `07-CONTRACTS.md`: one row per FP-* ID, with the
++implementation files and the exact `file::test_name`. Run
++`python -m pytest --collect-only -q` and check every named test exists.
+diff --git a/docs/plan/12-DEPLOY.md b/docs/plan/12-DEPLOY.md
+new file mode 100644
+index 0000000..33276f2
+--- /dev/null
++++ b/docs/plan/12-DEPLOY.md
+@@ -0,0 +1,48 @@
++# 12 · Deploy and run
++
++The audit builds `main` from the `Dockerfile` (see the issue template). That build must work from a
++fresh clone with no extra steps.
++
++## Runtime
++
++- `wsgi.py` creates the app and serves it with waitress on `0.0.0.0:$PORT` (default 8080).
++- On start: create `instance/` and `UPLOAD_DIR`, run `init_db()` if the database file does not
++  exist, then seed demo data if the database is new (so auditors can sign in at once).
++- `debug` is never on in Docker.
++
++## Dockerfile (T20 fills in the template's TODOs)
++
++- Keep the base image and the unprivileged `student` user from the template.
++- Data folder: `/app/data` owned by `student`; `DATABASE=/app/data/keystone.sqlite3`,
++  `UPLOAD_DIR=/app/data/uploads`.
++- `EXPOSE 8080`
++- `CMD ["python", "wsgi.py"]`
++- `tzdata` is pinned in `requirements.lock`, so time zones work in the slim image and on Windows.
++
++Commands (also in INSTALL.md):
++```
++docker build -t keystone .
++docker run --rm -p 8080:8080 keystone
++# then open http://localhost:8080
++```
++
++## Demo data (T19)
++
++`python scripts/seed.py --reset` deletes the database and uploads, recreates the schema, and adds:
++
++| Account | Password | Role | Notes |
++|---|---|---|---|
++| `meilin@demo.keystone` | from INSTALL.md | candidate | full profile, Python, SQL, dbt, Tableau, one resume |
++| `arjun@demo.keystone` | from INSTALL.md | candidate | few skills, no resume |
++| `daniel@demo.keystone` | from INSTALL.md | employer | Harbourline Logistics, 3 jobs, slots |
++| `priya@demo.keystone` | from INSTALL.md | employer | Tidewater Freight, 2 jobs |
++
++Demo passwords are documented in INSTALL.md and README "Demo Accounts" because the template asks for
++them. They are demo-only and must not be reused anywhere. All people and companies are fictional.
++
++## Release checklist (phase 4 gate)
++
++1. `python scripts/check.py --release` passes (no skipped tests).
++2. Fresh clone in a new folder, then `docker build` and `docker run`, then sign in as each demo account.
++3. README, SPEC.md and INSTALL.md have no empty sections.
++4. `git status` clean on `main`; tag `release-1`.
+diff --git a/docs/state/BUGS.md b/docs/state/BUGS.md
+new file mode 100644
+index 0000000..849226c
+--- /dev/null
++++ b/docs/state/BUGS.md
+@@ -0,0 +1,21 @@
++# Bug log
++
++One entry per bug, including small ones. Newest at the bottom.
++
++Template:
++
++## B<n>: <one line symptom>
++- Found by: test | review (reviews/<id>/verdict.md) | Kevin | audit issue #<n>
++- Class: auth | ownership | validation | csrf | xss | injection | upload | timezone | transaction | ordering | performance | other
++- Cause: <one sentence, the mechanism>
++- Fix: <file and what changed>
++- Guarded by: <tests/unit/file.py::test_name>
++- Same cause elsewhere: <list, or "checked, none">
++
++## B1: Phase 0 review packet requests nonexistent phase--1 tag
++- Found by: `python scripts/make_packet.py phase 0` during the Phase 0 gate.
++- Class: other
++- Cause: The packet baseline unconditionally subtracted one from the phase number.
++- Fix: `scripts/make_packet.py` uses the existing empty-tree constant for Phase 0; later phases retain predecessor tags.
++- Guarded by: `tests/unit/test_make_packet.py::test_phase_zero_without_tags_includes_whole_repository`, `test_phase_one_compares_against_phase_zero_tag`, `test_phase_one_requires_phase_zero_tag`.
++- Same cause elsewhere: checked, none; other search hits were status/card text and packet naming.
+diff --git a/docs/state/DECISIONS.md b/docs/state/DECISIONS.md
+new file mode 100644
+index 0000000..979271c
+--- /dev/null
++++ b/docs/state/DECISIONS.md
+@@ -0,0 +1,35 @@
++# Locked decisions
++
++An agent may not change these. If one looks wrong, stop and report.
++
++## D1: Stack is Flask + SQLite + Jinja + pytest
++- Chosen: the course template stack, server-rendered forms, no ORM, no JavaScript framework.
++- Rejected: Next.js + Postgres (Kevin's usual stack). Would replace the template, Dockerfile and test
++  layout, and gives a flash model more APIs to invent.
++- Consequence: no new dependencies beyond `requirements.lock` and `requirements-dev.txt`.
++
++## D2: Business rules come only from docs/BRIEF.md
++- Chosen: rules are quoted from the brief. Tasks needing a missing rule are BLOCKED.
++- Consequence: matching (T11), booking (T16, T17) cannot start until the brief is pasted.
++
++## D3: Missing and not-yours objects both return 404
++- Chosen: 404 for both, so ids cannot be probed, unless the brief says 403.
++
++## D4: Shared files frozen after Phase 1
++- Files: `app/__init__.py`, `app/db.py`, `app/schema.sql`, `app/errors.py`, `app/security.py`,
++  `app/audit.py`, `app/templates/base.html`, `app/templates/components/*`, `tests/conftest.py`.
++- Changed only through a contract change request card (CCxx).
++
++## D5: Tests split per task file, template test names kept
++- Template files `tests/unit/test_workflows.py` and `test_scheduling.py` are replaced by per-task
++  files (T04), so parallel lanes never edit the same file. Every template test name is kept exactly.
++
++## D6: Web-only scope
++- Phone screens, extension, email, team chat, Keystone console, Handshake, mock interviews, offers and
++  negotiation are out of scope.
++
++## D7: FP-AUTH-3 tested as a Phase 3 sweep (T06)
++- It needs real objects from every feature, so it is tested after they exist, across every route.
++
++## D8: Matching engine (T11) is pure; its database service is T13's
++- So T11 can run in Phase 2 in parallel with jobs (T10) without depending on it.
+diff --git a/docs/state/JOURNAL.md b/docs/state/JOURNAL.md
+new file mode 100644
+index 0000000..e604476
+--- /dev/null
++++ b/docs/state/JOURNAL.md
+@@ -0,0 +1,31 @@
++# Journal
++
++Append only. Newest at the bottom. The orchestrator copies each task's `JOURNAL:` block here at
++merge, and one line per review result.
++
++## 2026-11-01 setup
++- Plan, agent definitions, skills, scripts and task cards written into the repo.
++- Tooling (T00) written and tested in setup; needs Kevin's commit on `dev`.
++
++2026-11-02 T00 review: PASS, 0 confirmed, 0 rejected.
++
++2026-11-02 merge-T00 review: PASS, 0 confirmed, 0 rejected.
++
++## 2026-11-02 T00 merged
++- Merged `task/T00` through `int/T00` into `dev` at `42113ab`; task and merge reviews both PASS.
++- Verified T00 using an isolated Python 3.12.14 virtual environment because the shell lacked `python`.
++- Installed pinned dependencies, including `tzdata==2026.5`; confirmed all required ignore patterns.
++- Gate passed with Ruff clean and 17 tests passing; T00 scope and T07/T09/T12 overlap checks passed.
++- Sandbox initially blocked Ruff’s cache; approved rerun passed. Recorded verification commit `fe889b2` with no tracked file changes.
++- Final gate on `dev` passed. Removed task and integration worktrees; retained branches under CLAUDE.md's no-branch-deletion rule.
++- T01's dependency is satisfied. Phase 0 remains current pending its phase gate; the brief is still missing.
++
++2026-11-02 B1 review: PASS, 0 confirmed, 0 rejected.
++
++2026-11-02 merge-B1 review: PASS, 0 confirmed, 0 rejected.
++
++## 2026-11-02 B1 merged
++- Phase 0 now uses the existing Git empty-tree constant.
++- Phase 1 retains its `phase-0` baseline and missing-tag failure.
++- CLI regression tests use temporary repositories; no main-repository packets generated by the implementer.
++- Merged at `6507ca5`; final gate passed with 20 tests. Task and merge reviews both PASS.
+
+```

```
