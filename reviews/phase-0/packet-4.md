# Review packet phase-0 (4 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/plan/00-OVERVIEW.md, docs/plan/01-REQUIREMENTS.md, docs/plan/02-ARCHITECTURE.md

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
diff --git a/docs/plan/00-OVERVIEW.md b/docs/plan/00-OVERVIEW.md
new file mode 100644
index 0000000..a40c622
--- /dev/null
+++ b/docs/plan/00-OVERVIEW.md
@@ -0,0 +1,70 @@
+# 00 · Overview: read this first
+
+## What we are building
+
+**Keystone** is a job platform with two kinds of users:
+
+- **Candidates** build a profile with skills and a private resume, see jobs ranked by how well they
+  match, apply, and book an interview slot.
+- **Employers** build a company profile, post jobs, see applicants, and offer interview slots.
+
+It is the web-only cut of the Keystone design canvas. Its look (navy and blue, IBM Plex, clean
+cards) comes from that canvas. Its required behaviour comes from the course brief.
+
+**Keystone's core idea, kept in this build:** the system proposes, a person decides. Nothing
+consequential happens without a clear confirm screen, and important actions are written to an
+audit log.
+
+## What is graded (from the repo template)
+
+| Area | Requirement IDs | Plan file |
+|---|---|---|
+| Accounts and sessions | FP-AUTH-1, FP-AUTH-2, FP-AUTH-3 | `04-AUTH-SECURITY.md` |
+| Candidate workflows | FP-CAN-1, FP-CAN-2, FP-CAN-3 | `05-UX-FLOWS.md` |
+| Employer workflows | FP-EMP-1, FP-EMP-2, FP-EMP-3 | `05-UX-FLOWS.md` |
+| Matching | FP-MATCH-1 | `02-ARCHITECTURE.md`, task T11 |
+| Scheduling | FP-SCHED-1, FP-SCHED-2, FP-SCHED-3 | `03-DATA-MODEL.md`, tasks T12, T16, T17 |
+| Docs and delivery | README mapping, SPEC.md, INSTALL.md, Dockerfile | tasks T19 to T21 |
+| Cross-team audit (Week 12) | security, functional, performance bugs found by other teams | `10-REVIEW-PROTOCOL.md`, phase 5 |
+
+`01-REQUIREMENTS.md` has the full list and which ones are still **BLOCKED** on the brief.
+
+## Not in this build
+
+Phone screens, browser extension, email, team chat, Keystone staff console, agent-to-agent
+Handshake, mock interviews, offers and negotiation. These were cut from the canvas. Do not build
+them, even partly.
+
+## How to read the plan
+
+| File | What it holds | Who reads it |
+|---|---|---|
+| `00-OVERVIEW.md` | this page | everyone, once |
+| `01-REQUIREMENTS.md` | every FP-* requirement, its rule source, its tests | orchestrator, test writers |
+| `02-ARCHITECTURE.md` | folders, modules, request and data flow | everyone, once |
+| `03-DATA-MODEL.md` | the exact SQL schema | tasks that touch data |
+| `04-AUTH-SECURITY.md` | auth design and the security checklist | auth tasks, every reviewer |
+| `05-UX-FLOWS.md` | screens, routes and user journeys per role | UI tasks |
+| `06-DESIGN-SYSTEM.md` | colors, type, spacing, components | UI tasks |
+| `07-CONTRACTS.md` | **frozen** names: routes, functions, templates, tables | everyone, every task |
+| `08-TASKS.md` | phases, task order, parallel lanes, dependencies | orchestrator |
+| `09-AGENT-WORKFLOW.md` | how agents are dispatched, isolated and merged | orchestrator |
+| `10-REVIEW-PROTOCOL.md` | 3 reviewers + 1 judge | orchestrator, reviewers |
+| `11-TESTING.md` | test rules, fixtures, requirement-test mapping | everyone |
+| `12-DEPLOY.md` | Docker, waitress, demo data | delivery tasks |
+
+## Phases
+
+| Phase | Goal | Runs | Gate |
+|---|---|---|---|
+| 0 | Tooling: the gate command works | 1 agent | `python scripts/check.py` passes on an empty app |
+| 1 | Foundation: app, database, security, layout, auth | 1 agent at a time | Phase review clean, FP-AUTH-1 and 2 tests pass |
+| 2 | Core features in 4 parallel lanes | up to 3 agents at once | Each task reviewed, phase review clean |
+| 3 | Features that join lanes together | up to 2 at once | Merge reviews clean, all FP tests pass |
+| 4 | Delivery: seed data, Docker, docs | 1 to 2 at once | Fresh clone builds and runs from README |
+| 5 | Hardening: self-audit like Week 12 | review agents only | No confirmed bugs left open |
+
+## The one rule that matters most
+
+**One task, one agent, one worktree, one fresh context.** A flash model loses track in long
+sessions. Small task cards and fresh sessions keep every agent working at its best.
diff --git a/docs/plan/01-REQUIREMENTS.md b/docs/plan/01-REQUIREMENTS.md
new file mode 100644
index 0000000..308e183
--- /dev/null
+++ b/docs/plan/01-REQUIREMENTS.md
@@ -0,0 +1,100 @@
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
diff --git a/docs/plan/02-ARCHITECTURE.md b/docs/plan/02-ARCHITECTURE.md
new file mode 100644
index 0000000..18a7137
--- /dev/null
+++ b/docs/plan/02-ARCHITECTURE.md
@@ -0,0 +1,147 @@
+# 02 · Architecture
+
+## Shape of the app
+
+A single Flask app, server-rendered with Jinja templates, backed by one SQLite file.
+Every feature is a **blueprint package** with two layers:
+
+- `routes.py`: thin. Reads the form, checks login and role, calls a service, renders a template.
+- `service.py`: all logic. Plain Python functions that take a `sqlite3.Connection` and plain
+  values, and return plain dicts or raise a defined error. No Flask imports. **Unit tests call
+  services directly.**
+
+Pure logic with no database (matching, time conversion) lives in its own module with no I/O at all.
+
+## Folder layout (created in Phase 1, then frozen)
+
+```
+app/
+  __init__.py            create_app(config=None): config, db, security, blueprints, error pages
+  config.py              Config class: reads env vars (SECRET_KEY, DATABASE, MAX_UPLOAD_MB)
+  db.py                  get_db(), close_db(), init_db(), transaction() context manager
+  schema.sql             all tables (03-DATA-MODEL.md), created once
+  errors.py              ServiceError classes + HTTP error handlers
+  security.py            csrf, security headers, login_required, role_required, rate limit
+  audit.py               log_event(conn, actor_id, action, object_type, object_id, detail)
+  timeutil.py            pure: to_utc(), from_utc(), validate_tz()
+  auth/        routes.py service.py
+  candidates/  routes.py service.py        profile, skills, resume
+  employers/   routes.py service.py        company profile
+  jobs/        routes.py service.py        job CRUD, job skills
+  matching/    engine.py                   pure scoring + ranking (no db)
+               service.py                  loads data, calls engine
+  applications/ routes.py service.py       apply, list, status changes
+  scheduling/  routes.py service.py        slots, bookings
+  templates/
+    base.html                layout, nav per role, flash messages, csrf meta
+    components/              macros: button, card, badge, field, table, empty_state, confirm
+    auth/ candidates/ employers/ jobs/ applications/ scheduling/ errors/
+  static/
+    css/tokens.css           design tokens (06-DESIGN-SYSTEM.md)
+    css/app.css              components built on tokens
+scripts/
+  check.py                   the gate
+  check_scope.py             changed files inside the task's Owns list?
+  seed.py                    demo data and --reset
+tests/
+  conftest.py                app, client, db, login helpers, factories
+  unit/test_*.py             one file per area
+wsgi.py                      waitress entry point for Docker
+```
+
+## Why this shape suits a flash model
+
+- Every task owns one package folder plus its own templates folder plus its own test file. Two
+  agents never need the same file.
+- Every shared file (`__init__.py`, `schema.sql`, `base.html`, `conftest.py`) is written in Phase 1
+  and frozen. All blueprints are registered up front with stub routes, so later tasks only fill in
+  their own package.
+- Services are plain functions with fixed signatures (`07-CONTRACTS.md`), so an agent can test its
+  work without the browser.
+
+## Request flow
+
+```
+Browser form POST
+  -> security.before_request: load user from session, check CSRF token, rate-limit login
+  -> blueprint route: @login_required, @role_required("employer")
+       -> read and strip form fields
+       -> service.function(conn, actor_id, **fields)
+            -> validate (raise ValidationError with field messages)
+            -> check ownership (raise NotFound / Forbidden)
+            -> SQL with ? placeholders only, inside db.transaction()
+            -> audit.log_event(...) for consequential actions
+            -> return dict
+       -> on ValidationError: re-render the form with messages, HTTP 400
+       -> on success: flash message, redirect (POST-redirect-GET)
+  -> security.after_request: add security headers
+```
+
+## Data flow per feature
+
+### Sign up and sign in (FP-AUTH)
+```
+form(email, password, role) -> auth.service.register -> validate -> hash password
+  -> INSERT users -> audit "user.register"
+login form -> rate limit check -> auth.service.authenticate -> verify hash
+  -> session.clear(); session["user_id"], session["role"]; rotate CSRF token -> redirect home
+logout POST -> session.clear() -> redirect to sign in
+```
+
+### Candidate profile and resume (FP-CAN-1)
+```
+profile form -> candidates.service.save_profile -> upsert candidate_profiles
+skills field "Python, SQL"  -> normalise_skill() each -> replace candidate_skills rows
+resume upload -> size and type check -> random file name -> save under instance/uploads/
+  -> INSERT resumes (owner_id, stored_name, original_name, size, mime)
+resume download GET /resumes/<id> -> can_view_resume(viewer, resume) -> send_file as attachment
+```
+Resume files are **never** under `static/`. They are only served through the checked route.
+
+### Jobs and company (FP-EMP-1, FP-EMP-2)
+```
+company form -> employers.service.save_company -> upsert companies (one per employer)
+job form -> jobs.service.create_job / update_job -> validate -> INSERT jobs + job_skills
+delete POST -> jobs.service.delete_job -> ownership -> rules from brief for linked rows
+```
+
+### Recommendations (FP-CAN-2, FP-MATCH-1)
+```
+GET /candidate/recommendations
+  -> matching.service.recommend_for(conn, candidate_id)
+       -> load candidate skills (normalised) and ALL open jobs with their skills
+       -> matching.engine.rank(candidate_skills, jobs)   pure function, rules from BRIEF
+       -> return every job with its score and its fields unchanged
+  -> template lists them in ranked order
+```
+
+### Applying and applicants (FP-CAN-3, FP-EMP-3)
+```
+confirm page (shows exactly what will be sent) -> POST apply
+  -> applications.service.apply -> duplicate pending check -> INSERT applications
+employer applicants page -> applications.service.list_applicants(conn, employer_id, job_id)
+  -> ownership -> ordered per brief -> fields per brief
+status change POST -> applications.service.set_status -> allowed transitions -> audit
+```
+
+### Slots and booking (FP-SCHED)
+```
+employer slot form (local date, time, timezone) -> timeutil.to_utc -> scheduling.service.create_slot
+candidate booking POST -> scheduling.service.book_slot
+  -> BEGIN IMMEDIATE (one writer at a time)
+  -> eligibility check (brief) -> slot still free? -> INSERT bookings (UNIQUE slot_id)
+  -> COMMIT, or on IntegrityError: conflict result defined by the brief
+display -> timeutil.from_utc(utc, viewer_tz)
+```
+
+## Configuration
+
+| Env var | Default | Meaning |
+|---|---|---|
+| `SECRET_KEY` | random per start (sessions end on restart) | session signing key |
+| `DATABASE` | `instance/keystone.sqlite3` | SQLite file path |
+| `UPLOAD_DIR` | `instance/uploads` | resume storage, outside static |
+| `MAX_UPLOAD_MB` | value from brief, else 2 | upload size cap |
+| `PORT` | 8080 | waitress port in Docker |
+
+Tests use `create_app({"TESTING": True, "DATABASE": tmp_path, "UPLOAD_DIR": tmp_path, "SECRET_KEY": "test"})`.

```
