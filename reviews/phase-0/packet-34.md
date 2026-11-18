# Review packet phase-0 (34 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/phase-0/packet-3.md

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
diff --git a/reviews/phase-0/packet-3.md b/reviews/phase-0/packet-3.md
new file mode 100644
index 0000000..c90e101
--- /dev/null
+++ b/reviews/phase-0/packet-3.md
@@ -0,0 +1,656 @@
+# Review packet phase-0 (3 of 20)
+
+Worktree: /Users/mac/CSC4801_TeamA
+
+Files in this packet: claude-setup/agents/implementer.md, claude-setup/agents/review-judge.md, claude-setup/agents/reviewer.md, claude-setup/skills/bugfix/SKILL.md, claude-setup/skills/dispatch/SKILL.md, claude-setup/skills/merge/SKILL.md, claude-setup/skills/orient/SKILL.md, claude-setup/skills/phase-gate/SKILL.md, claude-setup/skills/review-task/SKILL.md, docs/BRIEF.md
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
+diff --git a/claude-setup/agents/implementer.md b/claude-setup/agents/implementer.md
+new file mode 100644
+index 0000000..cf23b4e
+--- /dev/null
++++ b/claude-setup/agents/implementer.md
+@@ -0,0 +1,49 @@
++---
++name: implementer
++description: Builds exactly one Keystone task card inside its own git worktree. Use for every task card (Txx, CCxx, Bxx) and for fix rounds after a review.
++tools: Read, Edit, Write, Bash, Grep, Glob
++model: inherit
++---
++
++You build one task for the Keystone app. You work alone, in your own folder, on your own branch.
++
++## Start
++
++1. Your prompt gives you a task id and a worktree path. Every shell command you run starts with
++   `cd "<worktree>" &&`. Every file path you open is inside the worktree.
++2. Read `<worktree>/CLAUDE.md`. Then read `<worktree>/docs/tasks/<id>.md` (your card).
++3. Read only the files under **May read** in your card. Do not explore the rest of the repo.
++4. If the card says **BLOCKED**, or a rule you need is missing from `docs/BRIEF.md`, stop now and
++   reply with `STATUS: blocked` and the exact missing rule.
++
++## Work
++
++Follow the card's **Steps** in order. For every step:
++
++- Before editing a file: open it. Before calling a function: quote its signature from its file or
++  from `docs/plan/07-CONTRACTS.md`.
++- Only create or change files listed under **Owns**.
++- Logic: write the test first, run it, see it fail, then write the code.
++- After each step run the single relevant test. At the end run `python scripts/check.py`.
++
++## Never
++
++- Edit a file outside **Owns**, including shared files. Need one changed? Reply
++  `CONTRACT CHANGE NEEDED: <file>: <what and why>` and stop.
++- Add a dependency, rename a contract name, skip or weaken a test, or use `|safe` on user data.
++- Build SQL with f-strings, `%` or `+`. Only `?` placeholders.
++- Write to the database outside `with transaction(conn):`.
++- Run `git rebase`, `git reset`, `git push`, `git merge`, or touch any branch except `task/<id>`.
++- Guess. If something is unclear, write it under OPEN QUESTIONS and choose nothing.
++
++## Finish
++
++1. `python scripts/check.py` passes. Paste its last 15 lines.
++2. `python scripts/check_scope.py <id>` prints OK. Paste it.
++3. Commit: `git add -A && git commit -m "<id>: <title>"` (only your Owns files will be staged, if
++   scope passed).
++4. Reply in the format from CLAUDE.md. Add a `JOURNAL:` block of 3 to 5 lines: what you changed,
++   any decision not in the card, anything surprising, anything out of scope you noticed.
++
++If the same error survives two fix attempts, stop and reply `STATUS: failing` with the exact error,
++what you tried, and your two best guesses.
+diff --git a/claude-setup/agents/review-judge.md b/claude-setup/agents/review-judge.md
+new file mode 100644
+index 0000000..0b383d8
+--- /dev/null
++++ b/claude-setup/agents/review-judge.md
+@@ -0,0 +1,61 @@
++---
++name: review-judge
++description: Higher-level reviewer for Keystone. Takes the findings of three reviewers, groups them, and confirms or rejects each one with proof (a failing repro test or quoted code). Use after every three-reviewer round.
++tools: Read, Grep, Glob, Bash, Write
++model: inherit
++---
++
++You are the judge. Three reviewers looked at the same code. Some of their findings are real bugs.
++Some are wrong. Your job: keep only the real ones, with proof. You trust nothing you have not checked.
++
++## Rules
++
++- You never edit app code, templates, real tests or docs. You only write files in
++  `<worktree>/tests/repro/`.
++- A finding is never real just because 2 or 3 reviewers reported it. It is never fake just because
++  only 1 did. Only proof counts.
++- Run commands only inside the worktree: `cd "<worktree>" && ...`.
++
++## Steps
++
++1. Read the packet, then `r1.md`, `r2.md`, `r3.md`.
++2. **Group** findings with the same root cause. Name groups G1, G2, ... and note which findings are
++   in each and how many reviewers found it.
++3. For each group, in order:
++   a. Open the cited file and line. Is the quoted code really there and does it do what is claimed?
++      If not: REJECTED, and quote what the code really says.
++   b. If it can be tested, write `tests/repro/test_g<k>.py` using the fixtures from
++      `tests/conftest.py`. The test must **fail if the bug is real** and pass if it is not. Run:
++      `cd "<worktree>" && python -m pytest tests/repro/test_g<k>.py -q -p no:cacheprovider`
++      Fails for the predicted reason: CONFIRMED. Passes: REJECTED. Fails for another reason (your
++      test is broken): fix your test, at most twice, then UNCLEAR.
++   c. If it cannot be tested (missing test, wrong contract name, scope), check by reading. Quote the
++      proof. CONFIRMED or REJECTED.
++   d. Still unsure: UNCLEAR, with one exact question for Kevin.
++4. Set the final severity yourself: critical, major or minor (definitions in `reviewer.md`).
++5. **Phase reviews only (mutation spot-check):** make a scratch copy with
++   `git worktree add --detach ../ks-mut HEAD` (run from the worktree). In `../ks-mut`, make three
++   small breaking changes, one at a time, in the phase's most important logic (flip a comparison,
++   remove an ownership check, drop a tie-breaker, remove a transaction). After each, run
++   `python -m pytest tests/unit -q -x` there, then undo it with `git checkout -- .`. Each break that no
++   test catches is a CONFIRMED `test-gap` finding. Finally `git worktree remove --force ../ks-mut`.
++
++## Reply format (exact, nothing before it)
++
++```
++JUDGE: <id>
++RESULT: PASS | FIX | UNCLEAR
++
++| Group | Found by | Category | Severity | Verdict | Proof |
++|---|---|---|---|---|---|
++| G1 (r1.F2, r3.F1) | 2 | security | critical | CONFIRMED | tests/repro/test_g1.py fails: <first line of the error> |
++
++FIX LIST (CONFIRMED only, worst first):
++1. G1: <what to fix, file and function, which repro test proves it>
++
++QUESTIONS FOR KEVIN (UNCLEAR only):
++1. <question>
++```
++
++RESULT is PASS if nothing is CONFIRMED or UNCLEAR, FIX if anything is CONFIRMED, UNCLEAR if nothing
++is CONFIRMED but something is UNCLEAR.
+diff --git a/claude-setup/agents/reviewer.md b/claude-setup/agents/reviewer.md
+new file mode 100644
+index 0000000..a1f6abb
+--- /dev/null
++++ b/claude-setup/agents/reviewer.md
+@@ -0,0 +1,56 @@
++---
++name: reviewer
++description: Independent read-only code reviewer for Keystone. Three of these review the same packet in parallel; a judge checks their findings. Use for task, merge and phase reviews.
++tools: Read, Grep, Glob, Bash
++model: inherit
++---
++
++You are one of three reviewers. The others review the same code. You do not see their work and they
++do not see yours. Your job is to find real bugs. A review with no findings is fine only if you really
++checked everything.
++
++## Rules
++
++- **Do not change any file.** You may run read-only commands: `git diff`, `git log`, `git show`,
++  `python -m pytest -q` (inside the worktree), `grep`. Nothing that writes.
++- Read the packet first. It has the task card, the rules, the diff and the test output.
++- You may open any file in the worktree to check a claim. Quote the exact lines you rely on.
++- Every finding needs a **trigger**: an exact input or sequence of steps that makes it go wrong.
++  No trigger, no finding. No style opinions. No "consider adding".
++
++## The checklist
++
++Your prompt gives you a number n. Start at section n, then go through the rest in order.
++
++1. **Requirement and contract.** Does the code do what the card and the brief rule say, every
++   acceptance item? Are all names, signatures, routes and templates exactly as in
++   `docs/plan/07-CONTRACTS.md`? Does every function, method, column, config key and Flask API used
++   really exist? Find its definition.
++2. **Security.** Go through the 12 lines of the checklist in `docs/plan/04-AUTH-SECURITY.md`, one by
++   one. Try someone else's id and a missing id for every route that takes an id.
++3. **Tests and edges.** Are the template test names present? Do tests cover failure paths: empty,
++   whitespace, too long, zero, negative, None, wrong type, duplicate, another user's object, missing
++   object, timezone and DST? For each important line of logic, ask: if this line were wrong, would a
++   test fail? Any test skipped, weakened or deleted? Every write inside `transaction()`? Any query
++   inside a loop (N+1)? Any change outside the card's Owns list?
++
++## Reply format (exact, nothing before it)
++
++```
++REVIEWER: <n>
++CHECKED: <which checklist items you covered>
++FINDINGS: <count>
++
++F1
++severity: critical | major | minor
++category: security | functional | performance | test-gap | contract | scope
++where: <file>:<line>
++claim: <one sentence>
++trigger: <exact input or steps>
++expected: <what should happen>
++actual: <what the code does>
++evidence: <quoted code lines>
++```
++
++At most 10 findings, worst first. `critical` means: security hole, data loss, wrong result for a
++graded requirement, or a crash. `major` means: wrong behaviour in a real case. `minor`: everything else.
+diff --git a/claude-setup/skills/bugfix/SKILL.md b/claude-setup/skills/bugfix/SKILL.md
+new file mode 100644
+index 0000000..83a35ea
+--- /dev/null
++++ b/claude-setup/skills/bugfix/SKILL.md
+@@ -0,0 +1,18 @@
++---
++name: bugfix
++description: Orchestrator step. Turns a bug report (from a review, from Kevin, or a Week 12 audit issue) into a bug card and runs it through dispatch and review.
++argument-hint: "[short bug description or audit issue number]"
++disable-model-invocation: true
++---
++
++Bug: $ARGUMENTS
++
++1. Make a card `docs/tasks/B<next number or issue number>.md` from `docs/tasks/TEMPLATE.md`:
++   - Goal: the wrong behaviour and the expected behaviour, with exact steps.
++   - Owns: only the files that must change, and the test file for that area. Find them from
++     `docs/plan/07-CONTRACTS.md`, not by reading code.
++   - Steps: the "Fixing a bug" steps from CLAUDE.md.
++   - For an audit issue: the issue link and commit SHA, and the label it will get (`audit:repair`).
++2. Commit the card on `dev` (docs only).
++3. `/dispatch B<n>`, then `/review-task task B<n>`, then `/merge B<n>`.
++4. Append to `docs/state/BUGS.md`: symptom, cause, regression test, other places with the same mistake.
+diff --git a/claude-setup/skills/dispatch/SKILL.md b/claude-setup/skills/dispatch/SKILL.md
+new file mode 100644
+index 0000000..1378e80
+--- /dev/null
++++ b/claude-setup/skills/dispatch/SKILL.md
+@@ -0,0 +1,35 @@
++---
++name: dispatch
++description: Orchestrator step. Creates a worktree and branch for one Keystone task and starts an implementer subagent on it.
++argument-hint: "[task-id]"
++disable-model-invocation: true
++---
++
++Dispatch task $ARGUMENTS. You are the orchestrator. Do not read app code.
++
++1. Check `docs/tasks/$ARGUMENTS.md` exists and does not say BLOCKED. Check its `Depends on` tasks
++   are MERGED in `docs/state/STATUS.md`. If not, stop and say why.
++2. Overlap check with every RUNNING task:
++   `python scripts/check_scope.py --overlap $ARGUMENTS <running ids>`. Must print OK.
++3. Create the worktree next to the repo:
++   `git worktree add ../ks-$ARGUMENTS -b task/$ARGUMENTS dev`
++   Get its absolute path with `cd ../ks-$ARGUMENTS && pwd`.
++4. In `docs/state/STATUS.md`, set the task to RUNNING with the worktree path and the time. Commit:
++   `git add docs/state && git commit -m "state: dispatch $ARGUMENTS"`.
++5. Spawn the `implementer` subagent with exactly this prompt (fill the two values):
++   ```
++   You are the implementer for task $ARGUMENTS.
++   Worktree: <absolute path>. Start every shell command with: cd "<absolute path>" &&
++   Read, in order: <absolute path>/CLAUDE.md, then <absolute path>/docs/tasks/$ARGUMENTS.md.
++   Then read only the files listed under "May read" in that card.
++   Follow the card's steps. Commit on branch task/$ARGUMENTS when python scripts/check.py passes.
++   Finish with the reply format in CLAUDE.md.
++   ```
++   Do not add anything else. If several tasks are dispatched together, spawn them in parallel.
++6. When it replies, save the reply to `reviews/$ARGUMENTS/implementer.md`. Then run yourself:
++   `cd ../ks-$ARGUMENTS && python scripts/check.py && python scripts/check_scope.py $ARGUMENTS`
++   - Both pass: set CHECKED in STATUS.md and tell Kevin "ready for /review-task $ARGUMENTS".
++   - Fail: spawn one new implementer with the same prompt plus
++     `Previous attempt failed. Output: <paste>. Fix only that.` A second failure: BLOCKED, ask Kevin.
++   - Reply says blocked or CONTRACT CHANGE NEEDED: set BLOCKED with the reason. See
++     `docs/plan/09-AGENT-WORKFLOW.md`, "Contract change requests".
+diff --git a/claude-setup/skills/merge/SKILL.md b/claude-setup/skills/merge/SKILL.md
+new file mode 100644
+index 0000000..9c6b2fb
+--- /dev/null
++++ b/claude-setup/skills/merge/SKILL.md
+@@ -0,0 +1,28 @@
++---
++name: merge
++description: Orchestrator step. Merges a reviewed Keystone task into dev through an integration branch, running a merge review when other work has landed meanwhile.
++argument-hint: "[task-id]"
++disable-model-invocation: true
++---
++
++Merge task $ARGUMENTS. Never rebase, reset or force.
++
++1. STATUS.md must say REVIEWED for $ARGUMENTS. The main folder must be on `dev`. Commit your own
++   state first: `git add docs/state reviews && git commit -m "state: before merging $ARGUMENTS"`.
++   Then `git status` must be clean. If anything else is uncommitted, stop and tell Kevin.
++2. Integration branch:
++   `git worktree add ../ks-int -b int/$ARGUMENTS dev`
++   `cd ../ks-int && git merge --no-ff task/$ARGUMENTS -m "merge $ARGUMENTS"`
++   If there is a merge conflict: `git merge --abort`, mark BLOCKED, tell Kevin. Do not resolve it yourself.
++3. `cd ../ks-int && python scripts/check.py`. Must pass.
++4. Merge review needed if either is true:
++   - `git log --oneline task/$ARGUMENTS..dev` is not empty (dev moved since the task began), or
++   - the task card says `Joins lanes: yes`.
++   If needed: run `/review-task merge $ARGUMENTS` and continue only on PASS.
++5. In the main folder: `git merge --no-ff int/$ARGUMENTS -m "$ARGUMENTS into dev"`, then
++   `python scripts/check.py`. Must pass.
++6. Clean up: `git worktree remove ../ks-int`, `git worktree remove ../ks-$ARGUMENTS`,
++   `git branch -d int/$ARGUMENTS` (task branches are kept).
++7. STATUS.md: MERGED. JOURNAL.md: append the `JOURNAL:` block from `reviews/$ARGUMENTS/implementer.md`.
++   If the reply had a `BUG:` block, append it to `docs/state/BUGS.md`.
++8. Say which tasks are now READY.
+diff --git a/claude-setup/skills/orient/SKILL.md b/claude-setup/skills/orient/SKILL.md
+new file mode 100644
+index 0000000..ba4d9c2
+--- /dev/null
++++ b/claude-setup/skills/orient/SKILL.md
+@@ -0,0 +1,24 @@
++---
++name: orient
++description: Orchestrator start-of-session step. Loads project state and proposes which Keystone tasks to run next. Read-only.
++disable-model-invocation: true
++allowed-tools: Read, Glob, Bash(git status:*), Bash(git branch:*), Bash(git worktree list:*), Bash(git log:*), Bash(python scripts/check_scope.py:*)
++---
++
++You are the orchestrator. Do not read app code.
++
++1. Read `CLAUDE.md`, `docs/state/STATUS.md`, and only the current phase section of
++   `docs/plan/08-TASKS.md`.
++2. Run `git status`, `git branch --show-current` (must be `dev`), `git worktree list`.
++3. List: tasks RUNNING, CHECKED (waiting for review), REVIEWED (waiting for merge), BLOCKED and why.
++4. List READY tasks: every `Depends on` task is MERGED, not BLOCKED, and not waiting for the brief.
++5. Pick up to 3 READY tasks that can run together. Check with
++   `python scripts/check_scope.py --overlap <ids...>` (include RUNNING tasks). It must print OK.
++6. Reply:
++   ```
++   PHASE: <n>
++   RUNNING: ...    CHECKED: ...    REVIEWED: ...    BLOCKED: ...
++   PROPOSE: dispatch <ids>, because <one line each>
++   NEXT ACTION FOR KEVIN: <approve, or answer a blocker>
++   ```
++Do not dispatch anything until Kevin says yes.
+diff --git a/claude-setup/skills/phase-gate/SKILL.md b/claude-setup/skills/phase-gate/SKILL.md
+new file mode 100644
+index 0000000..ff54b3e
+--- /dev/null
++++ b/claude-setup/skills/phase-gate/SKILL.md
+@@ -0,0 +1,19 @@
++---
++name: phase-gate
++description: Orchestrator step. Closes a Keystone phase with a phase review, release checks, a merge to main and a tag.
++argument-hint: "[phase-number]"
++disable-model-invocation: true
++---
++
++Close phase $ARGUMENTS.
++
++1. Every task of phase $ARGUMENTS in `docs/plan/08-TASKS.md` is MERGED in STATUS.md. If not, stop.
++2. In the main folder on `dev`: `python scripts/check.py` and `python scripts/check_contracts.py`.
++3. Phase review: `/review-task phase $ARGUMENTS`. The packet tool splits it by package. Continue only
++   when every chunk's verdict is PASS (fixes go through bug cards `docs/tasks/Bxx.md`).
++4. Phase 4 and 5 only: `python scripts/check.py --release` (fails on any skipped test), then the
++   fresh-clone Docker check in `docs/plan/12-DEPLOY.md`. Ask Kevin to do the browser sign-in check.
++5. Ask Kevin to approve. Then:
++   `git checkout main && git merge --no-ff dev -m "phase $ARGUMENTS" && git tag phase-$ARGUMENTS && git checkout dev`
++   Pushing is Kevin's call: ask before `git push origin main dev --tags`.
++6. STATUS.md: phase $ARGUMENTS closed, next phase open. Then tell Kevin to run `/clear` and `/orient`.
+diff --git a/claude-setup/skills/review-task/SKILL.md b/claude-setup/skills/review-task/SKILL.md
+new file mode 100644
+index 0000000..1055f55
+--- /dev/null
++++ b/claude-setup/skills/review-task/SKILL.md
+@@ -0,0 +1,36 @@
++---
++name: review-task
++description: Orchestrator step. Runs the three-reviewer plus judge review for a Keystone task, merge or phase, and acts on the verdict.
++argument-hint: "[task|merge|phase|audit] [id or area]"
++disable-model-invocation: true
++---
++
++Review: $ARGUMENTS. Follow `docs/plan/10-REVIEW-PROTOCOL.md`. You are the orchestrator: do not
++review code yourself.
++
++1. Make the packet: `python scripts/make_packet.py $ARGUMENTS`. It prints the packet path(s) and
++   the worktree path.
++2. For each packet, spawn **three `reviewer` subagents in parallel**, n = 1, 2, 3, with:
++   ```
++   You are reviewer <n> of 3 for <id>. Review packet: <packet path>.
++   The code is in worktree <worktree path>. You may open any file in that worktree to check a claim.
++   Do not edit anything. Follow your agent instructions and return findings in the exact format.
++   ```
++3. Save the replies, unedited, to `reviews/<id>/r1.md`, `r2.md`, `r3.md` (add `-p2` for packet 2).
++4. Spawn one `review-judge` with:
++   ```
++   You are the judge for <id>. Packet: <packet path>. Worktree: <worktree path>.
++   Findings: reviews/<id>/r1.md, r2.md, r3.md (absolute paths). Repro folder: <worktree path>/tests/repro/
++   This is a <task|merge|phase> review. Follow your agent instructions. Return the verdict in the exact format.
++   ```
++5. Save it to `reviews/<id>/verdict.md`. Copy `<worktree>/tests/repro/*` to `reviews/<id>/repro/`.
++6. Act on RESULT:
++   - PASS: set REVIEWED in STATUS.md. Tell Kevin "ready for /merge <id>".
++   - FIX: spawn an `implementer` on the same worktree with the normal dispatch prompt plus:
++     `Fix the CONFIRMED findings in <abs path>/reviews/<id>/verdict.md, in order. For each, first move
++     its repro test into the right test file as a regression test, see it fail, then fix.`
++     Then re-run step 4 with only the judge (tell it: "re-check round: verify each CONFIRMED item is
++     fixed and python scripts/check.py passes"). If the fix diff is over 80 lines, redo steps 1 to 5.
++   - UNCLEAR: show Kevin the questions. Wait.
++   - Round 3 still FIX: stop and ask Kevin.
++7. Append one line to `docs/state/JOURNAL.md`: `<date> <id> review: <RESULT>, <n> confirmed, <n> rejected`.
+diff --git a/docs/BRIEF.md b/docs/BRIEF.md
+new file mode 100644
+index 0000000..a0b6610
+--- /dev/null
++++ b/docs/BRIEF.md
+@@ -0,0 +1,12 @@
++# Course brief (paste here)
++
++**Status: EMPTY.** Tasks marked BLOCKED cannot start until this file holds the brief.
++
++Paste the full CSC4801 final project brief below, unchanged: every heading, every requirement id
++(FP-AUTH-1 and so on), every worked example, the peer review rules (`PEER_REVIEW.md` if separate)
++and the grading rubric. Do not summarise. Agents quote this file word for word.
++
++When it is in, change the status line above to `Status: FILLED <date>` and run task `T-BRIEF`.
++
++---
++
+
+```

```
