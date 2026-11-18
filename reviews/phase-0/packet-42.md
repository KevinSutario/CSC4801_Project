# Review packet phase-0 (42 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/phase-0/r2.md, reviews/phase-0/r3-round1.md, reviews/phase-0/r3.md, reviews/phase-0/repro/mutation-results.md, reviews/phase-0/repro/test_g1.py

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
diff --git a/reviews/phase-0/r2.md b/reviews/phase-0/r2.md
new file mode 100644
index 0000000..96e7cea
--- /dev/null
+++ b/reviews/phase-0/r2.md
@@ -0,0 +1,109 @@
+PACKET: 1
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; no application changes), 3 (tooling tests, edge cases, scope, performance)
+FINDINGS: 0
+
+PACKET: 2
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; documentation/configuration only), 3 (scope and delivery requirements)
+FINDINGS: 0
+
+PACKET: 3
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; agent definitions only), 3 (scope and workflow consistency)
+FINDINGS: 0
+
+PACKET: 4
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; planning documentation only), 3 (requirements and scope)
+FINDINGS: 0
+
+PACKET: 5
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; planning documentation only), 3 (requirements and scope)
+FINDINGS: 0
+
+PACKET: 6
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; design documentation only), 3 (requirements and scope)
+FINDINGS: 0
+
+PACKET: 7
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; contracts documentation only), 3 (contract names and scope)
+FINDINGS: 0
+
+PACKET: 8
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; task/workflow documentation only), 3 (dependencies, scope and consistency)
+FINDINGS: 0
+
+PACKET: 9
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; review/testing/deployment documentation only), 3 (protocol and scope)
+FINDINGS: 0
+
+PACKET: 10
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; task/state documentation only), 3 (phase status and scope)
+FINDINGS: 0
+
+PACKET: 11
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; task cards only), 3 (requirements, dependencies, scope)
+FINDINGS: 0
+
+PACKET: 12
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; task cards only), 3 (requirements, dependencies, scope)
+FINDINGS: 0
+
+PACKET: 13
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; task cards only), 3 (requirements, dependencies, scope)
+FINDINGS: 0
+
+PACKET: 14
+REVIEWER: 2
+CHECKED: 1, 2, 3 (task cards, dependency metadata, package configuration and review evidence; all 12 security items)
+FINDINGS: 0
+
+PACKET: 15
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; review artifacts/tooling only), 3 (B1 review evidence, tests and scope)
+FINDINGS: 0
+
+PACKET: 16
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; review artifacts/tooling only), 3 (merge-B1 evidence, tests and scope)
+FINDINGS: 0
+
+PACKET: 17
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; no application routes/forms/SQL/uploads), 3 (gate behavior, tests, scope, performance and merge artifacts)
+FINDINGS: 1
+
+F1
+severity: minor
+category: test-gap
+where: scripts/check.py:38
+claim: The gate treats pytest's “no tests collected” exit code as success.
+trigger: Remove or rename every file under `tests/unit` while leaving the directory present, then run the gate.
+expected: The gate should fail when no tests are collected.
+actual: Pytest exits 5 with “no tests ran”, but the gate accepts code 5 and prints `CHECK PASSED`.
+evidence: `if code not in (0, 5):` in `scripts/check.py:38`.
+
+PACKET: 18
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; scope checker only), 3 (scope matching, overlap behavior, edge cases and performance)
+FINDINGS: 0
+
+PACKET: 19
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; contract/install scripts only), 3 (contract coverage, scope and edge cases)
+FINDINGS: 0
+
+PACKET: 20
+REVIEWER: 2
+CHECKED: 1, 2 (all 12 security items; unit-test templates and packet tooling), 3 (test names, placeholder scope, regression coverage and performance)
+FINDINGS: 0
diff --git a/reviews/phase-0/r3-round1.md b/reviews/phase-0/r3-round1.md
new file mode 100644
index 0000000..823a423
--- /dev/null
+++ b/reviews/phase-0/r3-round1.md
@@ -0,0 +1,99 @@
+PACKET: 1
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 2
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 3
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 4
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 5
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 6
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 7
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 8
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 9
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 10
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 11
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 12
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 13
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 14
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 15
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 16
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 17
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 18
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 19
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 20
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
diff --git a/reviews/phase-0/r3.md b/reviews/phase-0/r3.md
new file mode 100644
index 0000000..823a423
--- /dev/null
+++ b/reviews/phase-0/r3.md
@@ -0,0 +1,99 @@
+PACKET: 1
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 2
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 3
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 4
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 5
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 6
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 7
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 8
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 9
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 10
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 11
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 12
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 13
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 14
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 15
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 16
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 17
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 18
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 19
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
+
+PACKET: 20
+REVIEWER: 3
+CHECKED: Requirements, contracts, security checklist, tests/edges, transactions, performance, scope; inspected packet diff and relevant sources.
+FINDINGS: 0
diff --git a/reviews/phase-0/repro/mutation-results.md b/reviews/phase-0/repro/mutation-results.md
new file mode 100644
index 0000000..c852a73
--- /dev/null
+++ b/reviews/phase-0/repro/mutation-results.md
@@ -0,0 +1,21 @@
+# Phase 0 mutation spot-check
+
+Detached scratch worktree: `/private/tmp/keystone-phase0-ks-mut`, created from HEAD `6c899eb`.
+All mutations were made one at a time, undone using `git checkout -- .`, and the scratch worktree was removed afterward. No app code or real tests in the main worktree were edited.
+
+Environment for all tests:
+`PATH=/private/tmp/keystone-phase0-venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`
+
+Baseline: `python -m pytest tests/unit -q -x -p no:cacheprovider`: **20 passed**.
+Mutation command: `python -m pytest tests/unit -q -x`.
+
+| ID | Mutation | Observed result | Interpretation |
+|---|---|---|---|
+| M1 | `scripts/make_packet.py`: changed `base = EMPTY_TREE if phase == 0 else ...` to `phase == 1` | `1 failed, 4 passed`; `test_phase_zero_without_tags_includes_whole_repository` failed with `AssertionError: git diff phase--1..dev failed` | CAUGHT |
+| M2 / G2 | `scripts/check.py:33`: changed lint `if code != 0:` to `if code == 0:` | `20 passed` | SURVIVED: no unit test catches a reversed lint-failure gate |
+| M3 / G3 | `scripts/check_scope.py:73`: changed `if outside:` to `if False:` | `20 passed` | SURVIVED: no unit test catches acceptance of out-of-scope files |
+
+Extra phase check: `python scripts/check_contracts.py` exited 0 with `CONTRACTS: nothing to check yet`.
+
+G1: `python -m pytest tests/repro/test_g1.py -q -p no:cacheprovider` failed as predicted:
+`AssertionError` at `assert result.returncode != 0, output`; subprocess returned 0 and printed `CHECK PASSED` after real pytest printed `no tests ran in 0.00s`. This repro copies only the gate and Ruff config to a temporary directory, leaving `tests/unit` present but empty.
diff --git a/reviews/phase-0/repro/test_g1.py b/reviews/phase-0/repro/test_g1.py
new file mode 100644
index 0000000..efcebef
--- /dev/null
+++ b/reviews/phase-0/repro/test_g1.py
@@ -0,0 +1,26 @@
+"""Reproduction for the phase-0 gate accepting an empty test suite."""
+
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+
+def test_gate_fails_when_no_tests_are_collected(tmp_path: Path) -> None:
+    """A present tests/unit directory with no tests must fail the gate."""
+    source_root = Path(__file__).resolve().parents[2]
+    scripts = tmp_path / "scripts"
+    scripts.mkdir()
+    shutil.copyfile(source_root / "scripts" / "check.py", scripts / "check.py")
+    shutil.copyfile(source_root / "ruff.toml", tmp_path / "ruff.toml")
+    (tmp_path / "tests" / "unit").mkdir(parents=True)
+    (tmp_path / "tests" / "unit" / "__init__.py").write_text("", encoding="utf-8")
+    result = subprocess.run(
+        [sys.executable, str(scripts / "check.py")],
+        cwd=tmp_path,
+        capture_output=True,
+        text=True,
+    )
+    output = result.stdout + result.stderr
+    assert "no tests ran" in output, output
+    assert result.returncode != 0, output

```
