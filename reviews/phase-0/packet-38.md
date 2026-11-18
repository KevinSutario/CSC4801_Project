# Review packet phase-0 (38 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/phase-0/packet-7.md

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
diff --git a/reviews/phase-0/packet-7.md b/reviews/phase-0/packet-7.md
new file mode 100644
index 0000000..f18a704
--- /dev/null
+++ b/reviews/phase-0/packet-7.md
@@ -0,0 +1,588 @@
+# Review packet phase-0 (7 of 20)
+
+Worktree: /Users/mac/CSC4801_TeamA
+
+Files in this packet: docs/plan/07-CONTRACTS.md
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
+diff --git a/docs/plan/07-CONTRACTS.md b/docs/plan/07-CONTRACTS.md
+new file mode 100644
+index 0000000..2b956eb
+--- /dev/null
++++ b/docs/plan/07-CONTRACTS.md
+@@ -0,0 +1,324 @@
++# 07 · Contracts (frozen)
++
++This file is the single source of truth for **names**. If a name is not here, it does not exist.
++Do not rename anything. Do not add a public function to a module you do not own.
++
++To change this file, the orchestrator follows "Contract change request" in `09-AGENT-WORKFLOW.md`.
++
++Type notes: `Conn` means `sqlite3.Connection` with `row_factory = sqlite3.Row`. Services return
++plain `dict` (convert rows with `dict(row)`) or `list[dict]`, never `sqlite3.Row`.
++
++---
++
++## Shared modules (written in Phase 1)
++
++### `app/__init__.py` (T01)
++```python
++def create_app(test_config: dict | None = None) -> Flask
++```
++Registers blueprints in this order: `core`, `auth`, `candidates`, `employers`, `jobs`, `matching`,
++`applications`, `scheduling`, `activity`. Calls `security.init_app(app)` and `errors.init_app(app)`.
++Creates `instance/` and `UPLOAD_DIR` if missing.
++
++### `app/config.py` (T01)
++```python
++class Config:
++    SECRET_KEY: str           # env SECRET_KEY or secrets.token_hex(32)
++    DATABASE: str             # env DATABASE or <instance>/keystone.sqlite3
++    UPLOAD_DIR: str           # env UPLOAD_DIR or <instance>/uploads
++    MAX_UPLOAD_MB: int        # env MAX_UPLOAD_MB or 2
++    MAX_CONTENT_LENGTH: int   # MAX_UPLOAD_MB * 1024 * 1024
++    SESSION_COOKIE_HTTPONLY = True
++    SESSION_COOKIE_SAMESITE = "Lax"
++    SESSION_COOKIE_SECURE: bool   # env SESSION_COOKIE_SECURE == "1"
++    PERMANENT_SESSION_LIFETIME: timedelta   # 8 hours unless the brief says otherwise
++```
++
++### `app/db.py` (T01)
++```python
++def get_db() -> Conn            # one per request on flask.g; isolation_level=None; foreign_keys ON
++def close_db(e: BaseException | None = None) -> None
++def init_db() -> None            # runs schema.sql on the configured database
++def transaction(conn: Conn, immediate: bool = False) -> ContextManager[Conn]
++    # BEGIN (or BEGIN IMMEDIATE); COMMIT on success; ROLLBACK and re-raise on error
++def now_iso() -> str             # UTC now as "YYYY-MM-DDTHH:MM:SSZ"
++```
++CLI: `flask --app app init-db` (registered in `create_app`).
++**Every write must happen inside `with transaction(conn):`.** Connections are in autocommit mode
++(`isolation_level=None`), so a write outside a transaction commits immediately.
++
++### `app/errors.py` (T01)
++```python
++class ServiceError(Exception): ...
++class ValidationError(ServiceError):
++    def __init__(self, errors: dict[str, str]) -> None   # field name -> message
++    errors: dict[str, str]
++class NotFound(ServiceError): ...
++class Forbidden(ServiceError): ...
++class Conflict(ServiceError):
++    def __init__(self, message: str) -> None
++    message: str
++def init_app(app: Flask) -> None
++    # NotFound -> 404 errors/404.html; Forbidden -> 403 errors/403.html
++    # Conflict -> 409 errors/409.html (unless the route handles it)
++    # also handles HTTP 400, 403, 404, 405, 413, 500 with errors/<code>.html
++```
++Routes catch `ValidationError` themselves and re-render the form with status 400.
++
++### `app/security.py` (T02)
++```python
++def init_app(app: Flask) -> None     # before_request: load_user, csrf_protect; after_request: headers
++def login_required(view)              # decorator
++def role_required(role: str)          # decorator factory: "candidate" | "employer"
++def csrf_token() -> str               # creates session["csrf"] if missing
++def rotate_csrf() -> None             # new token (call after login)
++def is_safe_next(target: str | None) -> bool
++def login_key(email: str, ip: str) -> str
++def is_login_blocked(key: str) -> bool
++def record_failed_login(key: str) -> None
++def reset_login_failures(key: str) -> None
++```
++`g.user` is `dict | None` with keys `id, email, role, display_name`.
++Jinja globals: `csrf_token()`, `current_user` (same as `g.user`).
++
++### `app/audit.py` (T02)
++```python
++def log_event(conn: Conn, actor_id: int | None, action: str, object_type: str,
++              object_id: int | None, detail: str = "") -> None   # call inside the caller's transaction
++def list_events(conn: Conn, actor_id: int, limit: int = 100) -> list[dict]   # newest first
++ACTIONS: frozenset[str]   # the fixed list in 03-DATA-MODEL.md; log_event raises ValueError otherwise
++```
++
++### `app/skills.py` (T01 writes a PROVISIONAL version, T11 owns it afterwards)
++```python
++def normalise_skill(raw: str) -> str          # PROVISIONAL: strip, lower-case, collapse spaces
++def parse_skill_list(text: str) -> list[str]  # split on commas, normalise, drop empties, dedupe keeping order
++def get_or_create_skill_ids(conn: Conn, names: list[str]) -> list[int]   # names already normalised
++```
++
++### Templates and static (T03)
++```
++templates/base.html               blocks: title, content. Shows nav for current_user.role.
++templates/index.html              landing page
++templates/components/ui.html      button, link_button, badge, card, empty_state, score_bar,
++                                  confirm_box, flash_messages
++templates/components/forms.html   field, textarea_field, select_field, csrf_field
++templates/errors/400.html 403.html 404.html 405.html 409.html 413.html 500.html
++static/css/tokens.css  static/css/app.css
++```
++Macro signatures are in `06-DESIGN-SYSTEM.md`. Import with
++`{% from "components/ui.html" import button, badge %}`.
++
++### `app/core/routes.py` (T03)
++| Endpoint | Method and path | Who |
++|---|---|---|
++| `core.index` | GET `/` | anyone. Signed in: redirect to `candidates.today` or `employers.home`. |
++
++### `tests/conftest.py` (T01 writes app, client, conn; T04 adds the rest)
++Fixtures: `app`, `client`, `conn`, `make_candidate`, `make_employer`, `make_company`, `make_job`,
++`make_application`, `make_slot`, `login`, `login_as`, `csrf_post`. Signatures:
++```python
++make_candidate(email="cand@example.com", password="Passw0rd!", name="Mei Lin Tan",
++               skills=("python", "sql")) -> int          # user id
++make_employer(email="emp@example.com", password="Passw0rd!", name="Daniel Wong") -> int
++make_company(employer_id: int, name="Harbourline Logistics") -> int
++make_job(employer_id: int, title="Data Analyst", skills=("python",), is_open=1, **cols) -> int
++make_application(candidate_id: int, job_id: int, status="pending") -> int
++make_slot(employer_id: int, job_id: int, starts_at="2030-01-07T02:00:00Z",
++          ends_at="2030-01-07T02:45:00Z", created_tz="UTC") -> int
++login(client, email, password) -> Response           # through /auth/login (works after T05)
++login_as(client, user_id: int, role: str) -> None     # sets the session directly, plus a csrf token
++csrf_post(client, url, data: dict, **kwargs) -> Response   # adds the session CSRF token
++```
++Factories insert with SQL directly (not through services), so lanes do not depend on each other.
++
++---
++
++## Feature modules
++
++Each row lists the owning task. Only that task (or a later bug task) edits the file.
++
++### auth (T05, T06)
++`app/auth/service.py`
++```python
++def register(conn: Conn, email: str, password: str, role: str, display_name: str) -> int
++def authenticate(conn: Conn, email: str, password: str) -> dict | None
++def get_user(conn: Conn, user_id: int) -> dict | None
++```
++`app/auth/routes.py`
++| Endpoint | Path | Methods |
++|---|---|---|
++| `auth.register` | `/auth/register` | GET, POST |
++| `auth.login` | `/auth/login` | GET, POST |
++| `auth.logout` | `/auth/logout` | POST |
++
++### candidates: profile (T07)
++`app/candidates/profile_service.py`
++```python
++def get_profile(conn: Conn, candidate_id: int) -> dict
++    # keys: headline, location, timezone, summary, skills (list[str]), updated_at (or None)
++def save_profile(conn: Conn, candidate_id: int, headline: str, location: str,
++                 timezone: str, summary: str, skills_text: str) -> None
++```
++`app/candidates/routes_profile.py`: `candidates.today` GET `/candidate/`;
++`candidates.profile` GET, POST `/candidate/profile`
++
++### candidates: resume (T08)
++`app/candidates/resume_service.py`
++```python
++def save_resume(conn: Conn, upload_dir: str, owner_id: int, file) -> int   # file: werkzeug FileStorage
++def list_resumes(conn: Conn, owner_id: int) -> list[dict]
++def delete_resume(conn: Conn, upload_dir: str, owner_id: int, resume_id: int) -> None
++def can_view_resume(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> bool
++def get_resume_for_download(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> dict
++    # raises NotFound if missing or not allowed
++```
++`app/candidates/routes_resume.py`: `candidates.resume` GET, POST `/candidate/resume`;
++`candidates.resume_delete` POST `/candidate/resume/<int:resume_id>/delete`;
++`candidates.resume_download` GET `/resumes/<int:resume_id>`
++
++### employers (T09)
++`app/employers/service.py`
++```python
++def get_company(conn: Conn, employer_id: int) -> dict | None
++def get_company_by_id(conn: Conn, company_id: int) -> dict | None
++def save_company(conn: Conn, employer_id: int, name: str, industry: str, location: str,
++                 website: str, description: str) -> int
++```
++`app/employers/routes.py`: `employers.home` GET `/employer/`;
++`employers.company` GET, POST `/employer/company`
++
++### jobs (T10)
++`app/jobs/service.py`
++```python
++def create_job(conn: Conn, employer_id: int, title: str, description: str, location: str,
++               employment_type: str, salary_min: str, salary_max: str, skills_text: str) -> int
++def update_job(conn: Conn, employer_id: int, job_id: int, title: str, description: str,
++               location: str, employment_type: str, salary_min: str, salary_max: str,
++               skills_text: str, is_open: bool) -> None
++def delete_job(conn: Conn, employer_id: int, job_id: int) -> None
++def get_owned_job(conn: Conn, employer_id: int, job_id: int) -> dict    # NotFound if not theirs
++def get_job(conn: Conn, job_id: int) -> dict    # with company_name, skills; NotFound if missing
++def list_jobs_for_employer(conn: Conn, employer_id: int) -> list[dict]
++def list_open_jobs(conn: Conn) -> list[dict]    # every open job with company_name and skills
++EMPLOYMENT_TYPES: tuple[str, ...]               # from the brief
++```
++Salary fields arrive as form strings; the service parses them (empty means None).
++`app/jobs/routes.py`: `jobs.my_jobs` GET `/employer/jobs`; `jobs.new` GET, POST `/employer/jobs/new`;
++`jobs.edit` GET, POST `/employer/jobs/<int:job_id>/edit`; `jobs.confirm_delete` GET and
++`jobs.delete` POST `/employer/jobs/<int:job_id>/delete`; `jobs.detail` GET `/jobs/<int:job_id>`
++
++### matching (T11 engine, T13 service and routes)
++`app/matching/engine.py` (pure: no imports from `app` except `app.skills`)
++```python
++def score(candidate_skills: set[str], job_skills: set[str]) -> dict
++    # {"score": <number per brief>, "matched": sorted list, "missing": sorted list}
++def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]
++    # returns NEW dicts: each job's fields unchanged plus score, matched, missing;
++    # sorted by the brief's rule and both tie-breakers; never mutates the input
++```
++`app/matching/service.py` (T13)
++```python
++def recommend_for(conn: Conn, candidate_id: int) -> list[dict]
++def score_candidate_for_job(conn: Conn, candidate_id: int, job_id: int) -> dict
++```
++`app/matching/routes.py` (T13): `matching.recommendations` GET `/candidate/recommendations`
++
++### applications (T14 candidate side, T15 employer side)
++`app/applications/statuses.py` (T14)
++```python
++STATUSES: tuple[str, ...]                      # from the brief, first is "pending"
++TRANSITIONS: dict[str, tuple[str, ...]]        # allowed next statuses, from the brief
++LABELS: dict[str, str]                         # status -> display text
++```
++`app/applications/service.py` (T14)
++```python
++def apply(conn: Conn, candidate_id: int, job_id: int, resume_id: int | None,
++          cover_note: str) -> int
++def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
++def get_own_application(conn: Conn, candidate_id: int, application_id: int) -> dict
++```
++`app/applications/review_service.py` (T15)
++```python
++def list_applicants(conn: Conn, employer_id: int, job_id: int) -> list[dict]
++def set_status(conn: Conn, employer_id: int, application_id: int, new_status: str) -> None
++```
++`app/applications/routes_candidate.py` (T14): `applications.confirm` GET and
++`applications.submit` POST `/jobs/<int:job_id>/apply`; `applications.mine` GET `/candidate/applications`
++`app/applications/routes_employer.py` (T15): `applications.applicants` GET
++`/employer/jobs/<int:job_id>/applicants`; `applications.confirm_status` GET and
++`applications.set_status` POST `/employer/applications/<int:application_id>/status`
++
++### scheduling (T12 slots, T16 and T17 booking)
++`app/timeutil.py` (T12, pure)
++```python
++def validate_tz(name: str) -> str                   # ValueError if not an IANA zone
++def local_to_utc(date_str: str, time_str: str, tz_name: str) -> str   # "YYYY-MM-DD","HH:MM" -> UTC iso
++def utc_to_local(utc_iso: str, tz_name: str) -> datetime
++def format_local(utc_iso: str, tz_name: str) -> str  # "Mon 30 Nov 2026, 10:00 (Asia/Hong_Kong)"
++def parse_iso(utc_iso: str) -> datetime              # aware UTC
++COMMON_TIMEZONES: tuple[str, ...]                    # for the select box
++```
++`local_to_utc` raises `ValueError` for a local time that does not exist (DST gap): it converts,
++converts back, and compares.
++
++`app/scheduling/slots.py` (T12)
++```python
++def create_slot(conn: Conn, employer_id: int, job_id: int, date_str: str, start_str: str,
++                end_str: str, tz_name: str) -> int
++def delete_slot(conn: Conn, employer_id: int, slot_id: int) -> None
++def list_slots_for_job(conn: Conn, employer_id: int, job_id: int) -> list[dict]   # adds "booked": bool
++```
++`app/scheduling/booking.py` (T16, then T17)
++```python
++def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
++def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
++def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
++    # Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief
++```
++`app/scheduling/routes_employer.py` (T12): `scheduling.slots` GET, POST
++`/employer/jobs/<int:job_id>/slots`; `scheduling.delete_slot` POST `/employer/slots/<int:slot_id>/delete`
++`app/scheduling/routes_candidate.py` (T16): `scheduling.application_detail` GET
++`/candidate/applications/<int:application_id>`; `scheduling.confirm_booking` GET and
++`scheduling.book` POST `/candidate/applications/<int:application_id>/book/<int:slot_id>`
++
++### activity (T18)
++`app/activity/routes.py`: `activity.list` GET `/activity` (signed-in users; own events only)
++
++---
++
++## Blueprint objects
++
++Each package `__init__.py` (written by T01, frozen) is exactly:
++```python
++from flask import Blueprint
++bp = Blueprint("<name>", __name__)
++from . import <route modules>  # noqa: E402,F401
++```
++Route modules start as stubs (T01): `from . import bp` and nothing else. The owning task fills them.
++
++## Test files and owners
++
++| File | Owner | Template test names it must contain |
++|---|---|---|
++| `tests/unit/test_db.py` | T01 | none (extra) |
++| `tests/unit/test_security.py` | T02 | none (extra) |
++| `tests/unit/test_audit.py` | T02 | none (extra) |
++| `tests/unit/test_auth.py` | T04 (placeholders), T05, then T06 | `test_fp_auth_1_registration_and_session_lifecycle`, `test_fp_auth_1_invalid_registration`, `test_fp_auth_2_salted_hash_and_password_verification`, `test_fp_auth_3_authorization_and_missing_object` |
++| `tests/unit/test_can_profile.py` | T07 | none (extra) |
++| `tests/unit/test_can_resume.py` | T08 | `test_fp_can_1_profile_and_private_resume_rules` |
++| `tests/unit/test_emp_company.py` | T09 | `test_fp_emp_1_company_profile` |
++| `tests/unit/test_emp_jobs.py` | T10 | `test_fp_emp_2_job_validation_and_deletion` |
++| `tests/unit/test_matching.py` | T11 | `test_fp_match_1_examples_normalization_and_floor`, `test_fp_match_1_both_tie_breakers` |
++| `tests/unit/test_timeutil.py` | T12 | none (extra) |
++| `tests/unit/test_sched_slots.py` | T12 | `test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_fp_sched_1_invalid_slots` |
++| `tests/unit/test_can_recommend.py` | T13 | `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
++| `tests/unit/test_can_apply.py` | T14 | `test_fp_can_3_pending_duplicate_and_application_owner` |
++| `tests/unit/test_emp_applicants.py` | T15 | `test_fp_emp_3_applicant_fields_order_status_and_role` |
++| `tests/unit/test_sched_booking.py` | T16, then T17 | `test_fp_sched_2_eligible_booking`, `test_fp_sched_2_ineligible_booking`, `test_fp_sched_3_conflict_contract` |
++| `tests/unit/test_activity.py` | T18 | none (extra) |
++| `tests/unit/test_authz_sweep.py` | T06 | none (extra) |
++
++T04 creates every file in this table that does not exist yet, holding the template test names as
++`@pytest.mark.skip(reason="TODO Txx")` placeholders, and deletes the template's
++`tests/unit/test_workflows.py` and `tests/unit/test_scheduling.py` (their tests move to the files above).
+
+```

```
