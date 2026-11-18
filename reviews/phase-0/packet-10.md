# Review packet phase-0 (10 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/state/JOURNAL.md, docs/state/STATUS.md, docs/tasks/B1.md, docs/tasks/B2.md, docs/tasks/T-BRIEF.md, docs/tasks/T00.md

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
diff --git a/docs/state/JOURNAL.md b/docs/state/JOURNAL.md
new file mode 100644
index 0000000..fd55f0b
--- /dev/null
+++ b/docs/state/JOURNAL.md
@@ -0,0 +1,45 @@
+# Journal
+
+Append only. Newest at the bottom. The orchestrator copies each task's `JOURNAL:` block here at
+merge, and one line per review result.
+
+## 2026-11-01 setup
+- Plan, agent definitions, skills, scripts and task cards written into the repo.
+- Tooling (T00) written and tested in setup; needs Kevin's commit on `dev`.
+
+2026-11-02 T00 review: PASS, 0 confirmed, 0 rejected.
+
+2026-11-02 merge-T00 review: PASS, 0 confirmed, 0 rejected.
+
+## 2026-11-02 T00 merged
+- Merged `task/T00` through `int/T00` into `dev` at `42113ab`; task and merge reviews both PASS.
+- Verified T00 using an isolated Python 3.12.14 virtual environment because the shell lacked `python`.
+- Installed pinned dependencies, including `tzdata==2026.5`; confirmed all required ignore patterns.
+- Gate passed with Ruff clean and 17 tests passing; T00 scope and T07/T09/T12 overlap checks passed.
+- Sandbox initially blocked Ruff’s cache; approved rerun passed. Recorded verification commit `fe889b2` with no tracked file changes.
+- Final gate on `dev` passed. Removed task and integration worktrees; retained branches under CLAUDE.md's no-branch-deletion rule.
+- T01's dependency is satisfied. Phase 0 remains current pending its phase gate; the brief is still missing.
+
+2026-11-02 B1 review: PASS, 0 confirmed, 0 rejected.
+
+2026-11-02 merge-B1 review: PASS, 0 confirmed, 0 rejected.
+
+## 2026-11-02 B1 merged
+- Phase 0 now uses the existing Git empty-tree constant.
+- Phase 1 retains its `phase-0` baseline and missing-tag failure.
+- CLI regression tests use temporary repositories; no main-repository packets generated by the implementer.
+- Merged at `6507ca5`; final gate passed with 20 tests. Task and merge reviews both PASS.
+
+2026-11-03 phase-0 review: FIX, 3 confirmed, 0 rejected. Empty-suite false success plus surviving lint and scope mutations routed to B2.
+
+2026-11-03 B2 review: PASS, 0 confirmed, 0 rejected.
+
+2026-11-03 merge-B2 review: PASS, 0 confirmed, 0 rejected.
+
+## 2026-11-03 B2 merged
+- Gate now rejects pytest’s “no tests collected” exit status.
+- Added isolated real gate tests for empty, passing, lint-failing, and test-failing suites.
+- Added scope CLI tests covering owned/unowned unstaged, staged, committed, and untracked files.
+- Both surviving Phase 0 mutations are caught; gate passes with 32 tests and task scope passes.
+- Merged at `c3980e8`; task and merge reviews PASS. Integration repro passed 4 cases; final dev gate and contracts passed.
+- Worktrees used writable temporary directories with adjacent aliases for the packet tool; aliases and worktrees removed after merge. Branches retained under CLAUDE.md.
diff --git a/docs/state/STATUS.md b/docs/state/STATUS.md
new file mode 100644
index 0000000..7355afb
--- /dev/null
+++ b/docs/state/STATUS.md
@@ -0,0 +1,47 @@
+# Status
+
+The orchestrator updates this file. It is the orchestrator's memory between sessions.
+States: READY, BLOCKED, RUNNING, CHECKED, REVIEWED, MERGED, DONE.
+`scripts/check_contracts.py` reads the State column, so keep the table format.
+
+Current phase: **0** · Brief: **missing** (docs/BRIEF.md is empty)
+
+| Task | Phase | State | Worktree | Notes |
+|---|---|---|---|---|
+| T00 | 0 | MERGED | - | merged into dev at 42113ab; task and merge reviews PASS; gate passed (17 tests); phase-0 gate pending |
+| B1 | 0 | MERGED | - | merged at 6507ca5; task and merge reviews PASS; 20 tests passed; Phase 0 packet generation repaired |
+| B2 | 0 | MERGED | - | c3980e8; task and merge reviews PASS; 32 tests passed; empty-suite failure and lint/scope regressions |
+| T-BRIEF | - | BLOCKED | - | waiting for Kevin to paste the brief |
+| T01 | 1 | READY | - | |
+| T02 | 1 | READY | - | after T01 |
+| T03 | 1 | READY | - | after T02 |
+| T04 | 1 | READY | - | after T03 |
+| T05 | 1 | READY | - | after T04 |
+| T07 | 2 | READY | - | |
+| T08 | 2 | READY | - | after T07 |
+| T09 | 2 | READY | - | |
+| T10 | 2 | READY | - | after T09 |
+| T11 | 2 | BLOCKED | - | needs T-BRIEF |
+| T12 | 2 | READY | - | |
+| T13 | 3 | BLOCKED | - | needs T11 |
+| T14 | 3 | READY | - | after T08, T10 |
+| T15 | 3 | READY | - | after T11, T14 |
+| T16 | 3 | BLOCKED | - | needs T-BRIEF |
+| T17 | 3 | BLOCKED | - | needs T-BRIEF, T16 |
+| T18 | 3 | READY | - | after T14 |
+| T06 | 3 | READY | - | after T10, T15, T16 |
+| T19 | 4 | READY | - | after phase 3 |
+| T20 | 4 | READY | - | after phase 3 |
+| T21 | 4 | READY | - | after T19, T20 |
+| T22 | 5 | READY | - | after phase 4 |
+
+## Running now
+none
+
+## Phase 0 gate
+- T00, B1 and B2 MERGED; lint and 32 tests pass; contracts report nothing to check before app tasks.
+- Phase review round 1 FIX: 3 confirmed groups repaired by B2; full round 2 required because the fix and regression diff exceeds 80 lines.
+- Merge to `main` and `phase-0` tag await the final review and Kevin's approval.
+
+## Waiting on Kevin
+- Paste the course brief into `docs/BRIEF.md`.
diff --git a/docs/tasks/B1.md b/docs/tasks/B1.md
new file mode 100644
index 0000000..f397b1a
--- /dev/null
+++ b/docs/tasks/B1.md
@@ -0,0 +1,44 @@
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
diff --git a/docs/tasks/B2.md b/docs/tasks/B2.md
new file mode 100644
index 0000000..c3dd38b
--- /dev/null
+++ b/docs/tasks/B2.md
@@ -0,0 +1,58 @@
+# B2 · Fail empty test gates and guard lint/scope rejection
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| 0 | tooling | T00, B1 | no | READY |
+
+## Goal
+Resolve the three confirmed Phase 0 findings in `reviews/phase-0/verdict.md`. A gate with an existing but empty `tests/unit` currently prints CHECK PASSED because it accepts pytest exit code 5; it must fail. Regression tests must also catch broken lint failure propagation and a scope checker that accepts unowned files.
+
+## Requirement
+Tooling only; no course brief or business rule is needed. The Phase 0 gate and Owns enforcement must reject failures, and tests must detect the judge's lint and scope mutations.
+
+## Owns
+- `scripts/check.py`
+- `tests/unit/test_check.py`
+- `tests/unit/test_check_scope.py`
+
+## May read
+- `CLAUDE.md`
+- `.claude/agents/implementer.md`
+- `docs/tasks/B2.md`
+- `docs/plan/07-CONTRACTS.md`
+- `docs/plan/10-REVIEW-PROTOCOL.md`
+- `scripts/check.py`
+- `scripts/check_scope.py`
+- `pytest.ini`
+- `ruff.toml`
+- `requirements-dev.txt`
+- `tests/unit/test_make_packet.py`
+- `reviews/phase-0/verdict.md`
+- `reviews/phase-0/repro/test_g1.py`
+- `reviews/phase-0/repro/mutation-results.md`
+
+## Contract
+Preserve the documented `python scripts/check.py` and `python scripts/check_scope.py <task-id>` CLIs. Do not add dependencies or change application contracts. Preserve the scope checker behavior; the confirmed scope issue is missing regression coverage.
+
+## Steps
+1. Use `/private/tmp/keystone-phase0-venv/bin` on PATH, `PYTHONDONTWRITEBYTECODE=1`, and `RUFF_CACHE_DIR=/private/tmp/keystone-phase0-ruff`. Read the implementer instructions and every file before editing; quote real signatures before calling existing functions.
+2. Read the confirmed verdict and repro evidence. Port the empty-suite repro into `tests/unit/test_check.py` and show it failing for the predicted reason. Exercise the real gate in an isolated temporary fixture so that the test cannot recursively launch itself.
+3. State the root cause and search for the same mistake using `git grep`; report other hits without changing unrelated files.
+4. Make the smallest change so pytest exit code 5 fails the gate. Add meaningful tests for a clean gate, a failing lint run, and a failing test run. Exercise actual gate behavior; avoid assertions that merely mirror implementation text.
+5. Add a scope regression using an isolated temporary Git repository and task card: an owned change passes, an unowned change fails. Do not alter `scripts/check_scope.py`.
+6. Demonstrate the lint and scope tests fail for the judge's corresponding mutations in an isolated temporary copy. Keep all temporary mutations outside tracked source; restore any scratch copy afterward. Do not weaken or skip existing tests.
+7. Run the focused regressions, full `python scripts/check.py`, and `python scripts/check_scope.py B2`. Commit only Owns files on `task/B2`.
+
+## Tests
+- An empty unit-test suite fails the real gate and never prints CHECK PASSED.
+- Clean lint plus passing tests succeeds; lint failure and test failure each fail the gate.
+- An owned change passes the real scope CLI; an unowned change fails.
+- The Phase 0 lint and scope mutations are detected by the new regressions.
+
+## Done when
+- All three confirmed groups have regression coverage, the full gate passes, and scope prints OK.
+- Reply includes actual failing/passing evidence plus BUG and JOURNAL blocks.
+
+## Pitfalls
+- Gate subprocess tests must use isolated fixtures instead of launching the full repository gate recursively.
+- Repro archives are evidence; do not edit them. Only the orchestrator updates state and review files.
diff --git a/docs/tasks/T-BRIEF.md b/docs/tasks/T-BRIEF.md
new file mode 100644
index 0000000..96e38cc
--- /dev/null
+++ b/docs/tasks/T-BRIEF.md
@@ -0,0 +1,57 @@
+# T-BRIEF · Fill rules from the course brief
+
+| Phase | Lane | Depends on | Joins lanes | Status |
+|---|---|---|---|---|
+| any | docs | `docs/BRIEF.md` filled by Kevin | no | BLOCKED until docs/BRIEF.md has the brief |
+
+## Goal
+Copy every business rule the app needs from the brief into the plan, word for word, so no later
+agent has to guess. Docs only. No code.
+
+## Requirement
+All FP-* ids.
+
+## Owns
+- `docs/plan/01-REQUIREMENTS.md`
+- `docs/tasks/T05.md`
+- `docs/tasks/T06.md`
+- `docs/tasks/T07.md`
+- `docs/tasks/T08.md`
+- `docs/tasks/T09.md`
+- `docs/tasks/T10.md`
+- `docs/tasks/T11.md`
+- `docs/tasks/T12.md`
+- `docs/tasks/T13.md`
+- `docs/tasks/T14.md`
+- `docs/tasks/T15.md`
+- `docs/tasks/T16.md`
+- `docs/tasks/T17.md`
+
+## May read
+- `CLAUDE.md`
+- `docs/BRIEF.md`
+- every file listed under Owns
+
+## Steps
+1. Read `docs/BRIEF.md` fully. List every requirement id it defines.
+2. In `01-REQUIREMENTS.md`, for each FP-* row: add a "Rule text" block under the table section,
+   quoting the brief exactly, with the brief's section name. Answer each "Open questions" item with a
+   quote, or write `NOT IN BRIEF`.
+3. For FP-MATCH-1 and FP-SCHED-1 to 3: copy every worked example from the brief exactly (inputs and
+   expected outputs) into the matching task card under `## Requirement`.
+4. In each task card listed under Owns: replace every "(from the brief)" placeholder with the quoted
+   rule. If a rule is `NOT IN BRIEF`, write the default already in the card and mark it
+   `DEFAULT (not in brief)`.
+5. If the brief has a requirement that no card covers: do not invent a card. List it under
+   OPEN QUESTIONS in your reply.
+6. Set Status to READY on every card whose rules are now complete. Leave BLOCKED where a rule the
+   card needs is still missing, with the reason.
+
+## Done when
+- Every FP-* row has rule text or `NOT IN BRIEF`.
+- No card still says "(from the brief)" without a quote or a DEFAULT mark.
+- `python scripts/check_scope.py T-BRIEF` passes.
+
+## Pitfalls
+- Never paraphrase a rule. Quote it. A paraphrase is how a requirement gets silently changed.
+- Do not change any card's Owns, Contract or test names.
diff --git a/docs/tasks/T00.md b/docs/tasks/T00.md
new file mode 100644
index 0000000..a54894c
--- /dev/null
+++ b/docs/tasks/T00.md
@@ -0,0 +1,29 @@
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

```
