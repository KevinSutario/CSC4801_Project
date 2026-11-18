# Review packet phase-0 (18 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: reviews/T00/orchestrator-check.md, reviews/T00/packet-1.md, reviews/T00/r1.md, reviews/T00/r2.md, reviews/T00/r3.md, reviews/T00/verdict.md, reviews/merge-B1/packet-1.md, reviews/merge-B1/r1.md, reviews/merge-B1/r2.md

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
diff --git a/reviews/T00/orchestrator-check.md b/reviews/T00/orchestrator-check.md
new file mode 100644
index 0000000..f98c173
--- /dev/null
+++ b/reviews/T00/orchestrator-check.md
@@ -0,0 +1,22 @@
+# T00 independent verification
+
+Verified on branch `task/T00`, commit `fe889b2`, in `/Users/mac/ks-T00`.
+Used its Python 3.12 virtual environment via PATH and disabled bytecode writes.
+
+```text
+=== lint: /Users/mac/ks-T00/.venv/bin/python -m ruff check .
+All checks passed!
+
+=== tests: /Users/mac/ks-T00/.venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
+.................                                                        [100%]
+17 passed in 0.01s
+
+=== contracts: skipped (no app/ folder yet)
+
+============================================================
+CHECK PASSED
+SCOPE OK for T00
+```
+
+Task worktree clean. No source changes; task commit records verification only.
+Ready for `/review-task T00`; no merge or phase tag performed.
diff --git a/reviews/T00/packet-1.md b/reviews/T00/packet-1.md
new file mode 100644
index 0000000..8ae4b68
--- /dev/null
+++ b/reviews/T00/packet-1.md
@@ -0,0 +1,91 @@
+# Review packet T00 (1 of 1)
+
+Worktree: /Users/mac/ks-T00
+
+Files in this packet: (no changes)
+
+## Review type: task
+
+## Task card
+
+# T00 · Tooling and gate
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 0 | tooling | none | no | DONE in setup: verify and commit |
+
+## Goal
+`python scripts/check.py` works on Windows and in Docker and passes on the template repo.
+
+## Owns
+- `scripts/*`
+- `pytest.ini`
+- `ruff.toml`
+- `requirements-dev.txt`
+- `requirements.lock`
+- `.gitignore`
+
+## May read
+- `CLAUDE.md`, `docs/plan/09-AGENT-WORKFLOW.md`, `docs/plan/10-REVIEW-PROTOCOL.md`
+
+## Steps (already done in setup; the agent only verifies)
+1. `requirements.lock` contains `tzdata==2026.5`.
+2. `.gitignore` contains `instance/`, `tests/repro/`, `reviews/*/repro/`.
+3. `python -m pip install -r requirements-dev.txt`
+4. `python scripts/check.py` prints CHECK PASSED.
+5. `python scripts/check_scope.py --overlap T07 T09 T12` prints OK.
+
+## Done when
+- Steps 3 to 5 pass. Kevin commits on `dev` and tags `phase-0`.
+
+
+## Changed files
+
+```
+
+```
+
+## Check output (in the worktree)
+
+```
+=== lint: /Users/mac/ks-T00/.venv/bin/python -m ruff check .
+All checks passed!
+
+=== tests: /Users/mac/ks-T00/.venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
+.................                                                        [100%]
+17 passed in 0.01s
+
+=== contracts: skipped (no app/ folder yet)
+
+============================================================
+CHECK PASSED
+```
+
+## Scope check
+
+```
+SCOPE OK for T00
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
+
+```
diff --git a/reviews/T00/r1.md b/reviews/T00/r1.md
new file mode 100644
index 0000000..11b5cec
--- /dev/null
+++ b/reviews/T00/r1.md
@@ -0,0 +1,3 @@
+REVIEWER: 1
+CHECKED: 1 (task requirements and tooling contracts; gate and overlap check pass), 2 (all 12 security items checked; no application changes), 3 (template tests preserved, dependencies consistent, empty commit diff, no scope violations)
+FINDINGS: 0
diff --git a/reviews/T00/r2.md b/reviews/T00/r2.md
new file mode 100644
index 0000000..65dfe24
--- /dev/null
+++ b/reviews/T00/r2.md
@@ -0,0 +1,3 @@
+REVIEWER: 2
+CHECKED: 2 (security checklist 1–12: no changed security surfaces), 3 (tests, edges, transactions, performance, scope), 1 (requirements and contracts). Confirmed empty verification commit, exact installed dependency pins, CHECK PASSED with 17 tests, and passing T07/T09/T12 overlap check.
+FINDINGS: 0
diff --git a/reviews/T00/r3.md b/reviews/T00/r3.md
new file mode 100644
index 0000000..a0f4e9e
--- /dev/null
+++ b/reviews/T00/r3.md
@@ -0,0 +1,3 @@
+REVIEWER: 3
+CHECKED: 3 (tests, edges, scope); 1 (T00 acceptance, dependency versions, gate and overlap checks); 2 (all 12 security items assessed; no application changes or routes)
+FINDINGS: 0
diff --git a/reviews/T00/verdict.md b/reviews/T00/verdict.md
new file mode 100644
index 0000000..9bfdc59
--- /dev/null
+++ b/reviews/T00/verdict.md
@@ -0,0 +1,11 @@
+JUDGE: T00
+RESULT: PASS
+
+| Group | Found by | Category | Severity | Verdict | Proof |
+|---|---|---|---|---|---|
+
+FIX LIST (CONFIRMED only, worst first):
+None.
+
+QUESTIONS FOR KEVIN (UNCLEAR only):
+None.
diff --git a/reviews/merge-B1/packet-1.md b/reviews/merge-B1/packet-1.md
new file mode 100644
index 0000000..21fbb15
--- /dev/null
+++ b/reviews/merge-B1/packet-1.md
@@ -0,0 +1,206 @@
+# Review packet merge-B1 (1 of 1)
+
+Worktree: /Users/mac/ks-int
+
+Files in this packet: scripts/make_packet.py, tests/unit/test_make_packet.py
+
+## Review type: merge
+
+## Task card
+
+# B1 · Phase 0 review packets must not require phase--1
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 0 | tooling | T00 | no | READY |
+
+## Goal
+`python scripts/make_packet.py phase 0` currently fails with an ambiguous `phase--1..dev` revision. Generate complete Phase 0 packets without inventing a predecessor tag. Keep phase 1 and later comparisons against their predecessor tags.
+
+## Requirement
+Tooling only; no business rule or course brief is needed. Phase 0 contains initial repository tooling and setup; review the whole repository at `dev` against Git's empty tree because there is no preceding phase. Later phases retain the existing tag baseline.
+
+## Owns
+- `scripts/make_packet.py`
+- `tests/unit/test_make_packet.py`
+
+## May read
+- `CLAUDE.md`
+- `docs/tasks/B1.md`
+- `scripts/make_packet.py`
+- `scripts/check.py`
+- `scripts/check_scope.py`
+- `pytest.ini`
+- `ruff.toml`
+- `requirements-dev.txt`
+- `docs/plan/10-REVIEW-PROTOCOL.md`
+
+## Contract
+Keep `python scripts/make_packet.py phase <n>` and its existing packet naming/output. No new dependencies. Use the existing Git empty-tree constant for phase 0; preserve missing-tag failures for later phases.
+
+## Steps
+1. Use the existing Python 3.12 environment at `/private/tmp/keystone-phase0-venv` via PATH. Set `PYTHONDONTWRITEBYTECODE=1` and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`.
+2. Read before editing. Write an offline regression test using a temporary Git repository that invokes the real packet command for phase 0 with no tags. Show it failing with the actual missing-revision error.
+3. State the root cause. Search for the same predecessor calculation elsewhere with `git grep`; report hits without changing unrelated code.
+4. Make the smallest fix for phase 0. Test phase 1 still compares against phase-0 and fails clearly when that required tag is absent.
+5. Run regression tests, `python scripts/check.py`, and `python scripts/check_scope.py B1`. Commit on `task/B1` only. Do not generate review packets in the main repo.
+
+## Tests
+- Real CLI generates phase-0 packets without a predecessor tag and includes the repository diff.
+- Phase 1 uses phase-0 and preserves failure when its predecessor tag is absent.
+
+## Done when
+- Regression tests pass, full gate prints CHECK PASSED, and B1 scope passes.
+- Reply includes actual failing/passing output, BUG and JOURNAL blocks.
+
+
+## Changed files
+
+```
+ scripts/make_packet.py         |  2 +-
+ tests/unit/test_make_packet.py | 78 ++++++++++++++++++++++++++++++++++++++++++
+ 2 files changed, 79 insertions(+), 1 deletion(-)
+
+```
+
+## Check output (in the worktree)
+
+```
+=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
+All checks passed!
+
+=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
+....................                                                     [100%]
+20 passed in 0.30s
+
+=== contracts: skipped (no app/ folder yet)
+
+============================================================
+CHECK PASSED
+```
+
+## Scope check
+
+```
+SCOPE OK for B1
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
+diff --git a/scripts/make_packet.py b/scripts/make_packet.py
+index 61291a1..65244ea 100644
+--- a/scripts/make_packet.py
++++ b/scripts/make_packet.py
+@@ -151,7 +151,7 @@ def main() -> int:
+         return 0
+ 
+     phase = int(ident)
+-    base = f"phase-{phase - 1}"
++    base = EMPTY_TREE if phase == 0 else f"phase-{phase - 1}"
+     diff = git("diff", f"{base}..dev")
+     stat = git("diff", "--stat", f"{base}..dev")
+     header = (
+diff --git a/tests/unit/test_make_packet.py b/tests/unit/test_make_packet.py
+new file mode 100644
+index 0000000..fe8f131
+--- /dev/null
++++ b/tests/unit/test_make_packet.py
+@@ -0,0 +1,78 @@
++"""Offline regression tests for phase review packet baselines."""
++
++from pathlib import Path
++import shutil
++import subprocess
++import sys
++
++import pytest
++
++
++SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "make_packet.py"
++EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
++
++
++def git(repo: Path, *args: str) -> str:
++    return subprocess.run(
++        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
++    ).stdout
++
++
++@pytest.fixture
++def packet_repo(tmp_path: Path) -> Path:
++    repo = tmp_path / "repo"
++    (repo / "scripts").mkdir(parents=True)
++    shutil.copyfile(SCRIPT, repo / "scripts" / "make_packet.py")
++    git(repo, "init", "--initial-branch=dev")
++    git(repo, "config", "user.name", "Packet test")
++    git(repo, "config", "user.email", "packet@example.invalid")
++    (repo / "README.md").write_text("Initial repository content\n", encoding="utf-8")
++    git(repo, "add", ".")
++    git(repo, "commit", "-m", "Initial repository")
++    return repo
++
++
++def run_phase(repo: Path, phase: int) -> subprocess.CompletedProcess[str]:
++    return subprocess.run(
++        [sys.executable, "scripts/make_packet.py", "phase", str(phase)],
++        cwd=repo, capture_output=True, text=True,
++    )
++
++
++def test_phase_zero_without_tags_includes_whole_repository(packet_repo: Path) -> None:
++    assert git(packet_repo, "tag") == ""
++    result = run_phase(packet_repo, 0)
++    assert result.returncode == 0, result.stderr
++    packets = sorted((packet_repo / "reviews" / "phase-0").glob("packet-*.md"))
++    assert packets
++    text = "\n".join(packet.read_text(encoding="utf-8") for packet in packets)
++    assert f"Compare: {EMPTY_TREE}..dev" in text
++    assert "diff --git a/README.md b/README.md" in text
++    assert "+Initial repository content" in text
++    assert "diff --git a/scripts/make_packet.py b/scripts/make_packet.py" in text
++    assert "new file mode" in text
++    assert f"PACKET: {packets[0]}" in result.stdout
++    assert f"WORKTREE: {packet_repo}" in result.stdout
++
++
++def test_phase_one_compares_against_phase_zero_tag(packet_repo: Path) -> None:
++    git(packet_repo, "tag", "phase-0")
++    (packet_repo / "phase-one.txt").write_text("Phase one content\n", encoding="utf-8")
++    git(packet_repo, "add", "phase-one.txt")
++    git(packet_repo, "commit", "-m", "Phase one")
++    result = run_phase(packet_repo, 1)
++    assert result.returncode == 0, result.stderr
++    packet = packet_repo / "reviews" / "phase-1" / "packet-1.md"
++    text = packet.read_text(encoding="utf-8")
++    assert "Compare: phase-0..dev" in text
++    assert "+Phase one content" in text
++    assert "diff --git a/README.md" not in text
++    assert "diff --git a/scripts/make_packet.py" not in text
++
++
++def test_phase_one_requires_phase_zero_tag(packet_repo: Path) -> None:
++    result = run_phase(packet_repo, 1)
++    assert result.returncode != 0
++    assert "git diff phase-0..dev failed:" in result.stderr
++    assert "unknown revision or path not in the working tree" in result.stderr
++    assert not (packet_repo / "reviews" / "phase-1").exists()
+
+```
diff --git a/reviews/merge-B1/r1.md b/reviews/merge-B1/r1.md
new file mode 100644
index 0000000..3680189
--- /dev/null
+++ b/reviews/merge-B1/r1.md
@@ -0,0 +1,3 @@
+REVIEWER: 1
+CHECKED: 1–9; security checklist 1–12 (not applicable to this tooling change); trigger B shared contracts, integration compatibility, and merge-only changes. All 20 unit tests passed.
+FINDINGS: 0
diff --git a/reviews/merge-B1/r2.md b/reviews/merge-B1/r2.md
new file mode 100644
index 0000000..5f67e70
--- /dev/null
+++ b/reviews/merge-B1/r2.md
@@ -0,0 +1,3 @@
+REVIEWER: 2
+CHECKED: 1–9; security checklist 1–12 (not applicable to this tooling-only change); trigger B shared-contract compatibility and merge integrity. Verified both changed files match the task branch without merge-only changes. Full gate passed; 20 tests passed, including real CLI coverage for phase 0 and phase 1.
+FINDINGS: 0

```
