# Review packet phase-0 (8 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: docs/plan/08-TASKS.md, docs/plan/09-AGENT-WORKFLOW.md

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
diff --git a/docs/plan/08-TASKS.md b/docs/plan/08-TASKS.md
new file mode 100644
index 0000000..88e9e3e
--- /dev/null
+++ b/docs/plan/08-TASKS.md
@@ -0,0 +1,118 @@
+# 08 · Tasks, phases and parallel lanes
+
+Each task has a card in `docs/tasks/`. A card is complete on its own: an agent needs nothing else.
+
+## Dependency map
+
+```
+Phase 0   T00 tooling
+             │
+Phase 1   T01 skeleton ─> T02 security+audit ─> T03 layout+UI ─> T04 test harness ─> T05 auth
+             │
+             ├────────── T-BRIEF (any time the brief arrives; runs alone, docs only)
+             │
+Phase 2   lane CAN:   T07 profile ─> T08 resume                                                      │
+          lane EMP:   T09 company ─> T10 jobs                                                         │
+          lane MATCH: T11 matching engine  (BLOCKED until T-BRIEF)                                   │
+          lane SCHED: T12 time + slots                                                               │
+             │
+Phase 3   T13 recommendations  (needs T07, T10, T11)        joins lanes
+          T14 apply            (needs T08, T10)             joins lanes
+          T15 applicants       (needs T11, T14)             joins lanes
+          T16 booking          (needs T12, T14; BLOCKED until T-BRIEF)   joins lanes
+          T17 booking conflict (needs T16; BLOCKED until T-BRIEF)
+          T18 activity + Today (needs T14)
+          T06 authorization sweep (needs T10, T15, T16)   FP-AUTH-3 across every route
+             │
+Phase 4   T19 seed data ─┬─> T21 docs
+          T20 Docker ────┘
+             │
+Phase 5   T22 self-audit (review agents only) ─> bug cards Bxx
+```
+
+## Phase 0: tooling
+
+| Task | Title | Depends on | Owns (short) | Status |
+|---|---|---|---|---|
+| T00 | Tooling and gate | none | scripts, configs | DONE in setup, needs commit and verify |
+
+Gate: `python scripts/check.py` prints CHECK PASSED. Tag `phase-0`.
+
+## Phase 1: foundation (strictly one task at a time)
+
+Everything here is shared by all later work, so it is built in order, by one agent at a time, and
+then frozen.
+
+| Task | Title | Depends on | Requirement |
+|---|---|---|---|
+| T01 | App skeleton, config, db, schema, errors, blueprint stubs, provisional skills | T00 | none |
+| T02 | Security module (CSRF, headers, login/role decorators, rate limit) and audit log | T01 | security |
+| T03 | Design tokens, CSS, base layout, component macros, landing page | T02 | UX |
+| T04 | Test harness: conftest fixtures and factories, placeholder tests | T03 | testing |
+| T05 | Register, sign in, sign out, safe redirects | T04 | FP-AUTH-1, FP-AUTH-2 |
+
+FP-AUTH-3 (authorization and missing objects) needs real objects, so it is tested in Phase 3 by
+T06, across every route that takes an id.
+
+Gate: phase review clean, FP-AUTH-1 and FP-AUTH-2 tests pass. Tag `phase-1`.
+
+## Phase 2: four lanes in parallel (max 3 agents at once)
+
+| Lane | Task | Title | Depends on | Requirement | Can run with |
+|---|---|---|---|---|---|
+| CAN | T07 | Candidate profile and skills, Today page shell | T05 | FP-CAN-1 (profile) | T09, T11, T12 |
+| CAN | T08 | Resume upload, list, delete, private download | T07 | FP-CAN-1 (resume) | T09, T10, T11, T12 |
+| EMP | T09 | Company profile, employer home | T05 | FP-EMP-1 | T07, T08, T11, T12 |
+| EMP | T10 | Jobs: create, edit, close, delete, detail | T09 | FP-EMP-2 | T07, T08, T11, T12 |
+| MATCH | T11 | Matching engine (pure) and normalisation | T05, T-BRIEF | FP-MATCH-1 | any |
+| SCHED | T12 | Time zone helpers, interview slots | T05 | FP-SCHED-1 | any |
+
+Suggested batches: {T07, T09, T12} then {T08, T10, T11}. Always confirm with
+`python scripts/check_scope.py --overlap ...`.
+
+Gate: each task reviewed (trigger A), each merge reviewed if dev moved (trigger B), phase review
+(trigger C). Tag `phase-2`.
+
+## Phase 3: joining the lanes (max 2 at once; every task has "Joins lanes: yes")
+
+| Task | Title | Depends on | Requirement | Can run with |
+|---|---|---|---|---|
+| T13 | Recommendations page | T07, T10, T11 | FP-CAN-2 | T14 |
+| T14 | Apply with confirm screen, my applications, statuses | T08, T10 | FP-CAN-3 | T13 |
+| T15 | Employer applicants list and status changes | T11, T14 | FP-EMP-3 | T16 |
+| T16 | Booking: eligibility, bookable slots, confirm, book | T12, T14, T-BRIEF | FP-SCHED-2 | T15 |
+| T17 | Booking conflict contract and concurrency | T16 | FP-SCHED-3 | T18 |
+| T18 | Activity log page and Today page widgets | T14 | Keystone governance | T17 |
+| T06 | Authorization sweep: other user's id and missing id on every route | T10, T15, T16 | FP-AUTH-3 | T17, T18 |
+
+T06 only writes tests. Any hole it finds becomes a bug card `Bxx`, fixed by the owner of that file.
+
+Gate: every FP test passes and none is skipped; phase review clean. Tag `phase-3`.
+
+## Phase 4: delivery
+
+| Task | Title | Depends on | Can run with |
+|---|---|---|---|
+| T19 | Seed demo data and reset command | phase 3 | T20 |
+| T20 | Dockerfile, wsgi, start-up | phase 3 | T19 |
+| T21 | README, SPEC.md, INSTALL.md | T19, T20 | none |
+
+Gate: `python scripts/check.py --release`, fresh-clone Docker run, Kevin signs in as each demo
+user. Merge to `main`. Tag `phase-4` and `release-1`.
+
+## Phase 5: hardening
+
+| Task | Title | Depends on |
+|---|---|---|
+| T22 | Self-audit: three reviewers per area, judge confirms, bug cards for each confirmed bug | phase 4 |
+
+Then every confirmed bug becomes `Bxx` via `/bugfix`. Gate: no open confirmed bugs. Tag `phase-5`.
+
+## Special cards
+
+| Card | When | Runs |
+|---|---|---|
+| T-BRIEF | as soon as `docs/BRIEF.md` is filled | alone, docs only |
+| CCxx | contract change request | alone |
+| Bxx | bug fix | normal, by ownership |
+| TEMPLATE | copy to make a new card | never |
diff --git a/docs/plan/09-AGENT-WORKFLOW.md b/docs/plan/09-AGENT-WORKFLOW.md
new file mode 100644
index 0000000..25a6966
--- /dev/null
+++ b/docs/plan/09-AGENT-WORKFLOW.md
@@ -0,0 +1,154 @@
+# 09 · Agent workflow: dispatch, isolation, context, merging
+
+This file is for the **orchestrator** (your main Claude Code session). Subagents do not need it.
+
+## Who does what
+
+| Agent | Defined in | Tools | Job | Writes to |
+|---|---|---|---|---|
+| Orchestrator | main session + `.claude/skills/` | all | picks tasks, makes worktrees, spawns agents, saves their reports, merges, updates state | `docs/state/*`, `reviews/*`, git branches |
+| `implementer` | `.claude/agents/implementer.md` | Read, Edit, Write, Bash, Grep, Glob | builds one task card in one worktree | only its card's Owns files, on its task branch |
+| `reviewer` | `.claude/agents/reviewer.md` | Read, Grep, Glob, Bash | reviews one packet, returns findings | nothing (returns text) |
+| `review-judge` | `.claude/agents/review-judge.md` | Read, Grep, Glob, Bash, Write | checks every finding is real, with proof | `<worktree>/tests/repro/` (gitignored) and its verdict text |
+
+Claude Code subagents cannot start other subagents. So **only the orchestrator spawns agents**,
+including the three reviewers and the judge.
+
+## The golden rules
+
+1. **One task, one agent, one worktree, one branch.** Nobody shares a working folder.
+2. **Owns lists never overlap** between tasks that run at the same time.
+   `python scripts/check_scope.py --overlap T07 T09 T12` must print `OK` before you dispatch them together.
+3. **Shared files are frozen after Phase 1** (`app/__init__.py`, `app/db.py`, `app/schema.sql`,
+   `app/errors.py`, `app/security.py`, `app/audit.py`, `base.html`, `components/*`, `tests/conftest.py`).
+   Only a contract change task may touch them.
+4. **Only the orchestrator writes shared state** (`docs/state/*`, `reviews/*`). Agents return text;
+   the orchestrator saves it. No two agents ever write the same file. The orchestrator commits these
+   on `dev` right away (`git add docs/state reviews && git commit -m "state: ..."`), so the main
+   folder stays clean for merges.
+5. **The orchestrator never reads app code.** It reads cards, agent reports, check output and
+   verdicts. This keeps its own context small and clear. Reading code is the reviewers' job.
+6. **At most 3 agents run at once.** More than that and the model endpoint slows down, and you lose
+   track.
+
+## Folder layout on your computer
+
+```
+CSC4801_TeamA/           main worktree, always on branch dev, the orchestrator works here
+ks-T07/                  worktree for task T07, branch task/T07  (sibling folder, created by /dispatch)
+ks-T09/                  worktree for task T09, branch task/T09
+ks-int/                  integration worktree for merge reviews, branch int/<id>
+```
+Worktrees live **next to** the repo folder (`../ks-T07`), never inside it.
+
+## Branches
+
+| Branch | Meaning | Who commits |
+|---|---|---|
+| `main` | what the auditors build. Updated only at phase gates. | orchestrator (merge) |
+| `dev` | integrated, reviewed work | orchestrator (merge) |
+| `task/Txx` | one task's work, from `dev` | the implementer |
+| `int/Txx` | dev + one task, for a merge review | orchestrator |
+
+Never rebase, reset or force-push. Merges only, with `--no-ff`.
+
+## The task lifecycle
+
+```
+READY ──/dispatch──> RUNNING ──report──> CHECKED ──/review-task──> REVIEWED ──/merge──> MERGED
+   ^                    │                    │                         │
+   │                    └── blocked ──> BLOCKED (needs Kevin or the brief)
+   │                                         └── fails ──> fix round (max 2) ──> REVIEWED
+   └──────────── confirmed findings ──> FIXING ──> back to CHECKED
+```
+
+### 1. Pick tasks (`/orient`)
+- Read `docs/state/STATUS.md` and the current phase in `08-TASKS.md`. Nothing else.
+- A task is READY when: all its `Depends on` tasks are MERGED, it is not BLOCKED, and its Owns list
+  does not overlap any RUNNING task.
+
+### 2. Dispatch (`/dispatch T07`)
+```
+git worktree add ../ks-T07 -b task/T07 dev
+python scripts/check_scope.py --overlap T07 <every RUNNING task>
+```
+Mark T07 RUNNING in STATUS.md. Then spawn the `implementer` subagent with exactly this prompt:
+
+```
+You are the implementer for task T07.
+Worktree: <absolute path to ks-T07>. Start every shell command with: cd "<that path>" &&
+Read, in order: <worktree>/CLAUDE.md, then <worktree>/docs/tasks/T07.md.
+Then read only the files listed under "May read" in that card.
+Follow the card's steps. Commit on branch task/T07 when python scripts/check.py passes.
+Finish with the reply format in CLAUDE.md.
+```
+Do not add anything else to the prompt. Everything the agent needs is in the card. That is the
+point: a fresh agent with a small, exact context.
+
+### 3. Check the report
+In the task's worktree run, yourself:
+```
+cd ../ks-T07 && python scripts/check.py && python scripts/check_scope.py T07
+```
+- Both pass: CHECKED.
+- Either fails: spawn a new `implementer` with the same prompt plus one line:
+  `Previous attempt failed. Output: <paste the failing output>. Fix only that.`
+  Two failed rounds: mark BLOCKED, log it, and ask Kevin.
+
+### 4. Review (`/review-task T07`)
+See `10-REVIEW-PROTOCOL.md`. Three reviewers in parallel, then the judge.
+
+### 5. Merge (`/merge T07`)
+```
+git worktree add ../ks-int -b int/T07 dev        (reuse ks-int if free)
+cd ../ks-int && git merge --no-ff task/T07
+python scripts/check.py
+```
+- If `dev` changed since T07 started (another task merged), this is a **merge of two agents' work**:
+  run the merge review (`10-REVIEW-PROTOCOL.md`, trigger B) on `int/T07` before going on.
+- Then, in the main folder: `git merge --no-ff int/T07` into `dev`, run `python scripts/check.py`
+  again, mark MERGED, append the task's journal lines to `docs/state/JOURNAL.md`.
+- Remove worktrees: `git worktree remove ../ks-T07` and `git worktree remove ../ks-int`.
+
+### 6. Phase gate (`/phase-gate 2`)
+All tasks in the phase MERGED, then the phase review (trigger C), then
+`python scripts/check.py --release` if it is phase 4 or 5, then merge `dev` into `main` and tag
+`phase-2`.
+
+## Keeping every agent in its best state (context management)
+
+| Risk | What we do |
+|---|---|
+| Long sessions make the model forget rules | Every implementer and reviewer is a **fresh subagent**. The orchestrator `/clear`s after every phase gate, and whenever its context is about half full, after updating STATUS.md. Then it runs `/orient`. |
+| Agent wanders around the repo | The card's **May read** list. Reviewers get one packet file. |
+| Agent changes other people's files | **Owns** list + `check_scope.py` + separate worktrees |
+| Agent invents functions | `07-CONTRACTS.md` + `python scripts/check_contracts.py` in the gate |
+| Two agents disturb each other | Separate folders, separate branches, non-overlapping Owns, temp databases in tests, only the orchestrator writes shared files |
+| Rules drift | Business rules only from `docs/BRIEF.md`; BLOCKED items stop work |
+| Orchestrator overloaded | It never reads code; it reads short reports. STATUS.md is its memory. |
+| Agent stuck in a loop | Two-strikes rule in CLAUDE.md; orchestrator caps fix rounds at 2 |
+
+## Contract change requests
+
+When an implementer reports `CONTRACT CHANGE NEEDED`:
+1. Do not let it edit the shared file. Mark its task BLOCKED.
+2. Write a small card `docs/tasks/CCnn.md` (copy `TEMPLATE.md`) that owns only the shared file and
+   `07-CONTRACTS.md`.
+3. Wait until no other task is RUNNING. Run CCnn alone, review it (trigger A), merge it.
+4. In every open task worktree: `git merge dev` (a merge, never a rebase). Then unblock.
+5. Log it in `docs/state/DECISIONS.md`.
+
+## When the brief arrives
+
+1. Paste it into `docs/BRIEF.md`.
+2. Run one `implementer` on card `T-BRIEF` (in `08-TASKS.md`). It fills the rule text and open
+   questions in `01-REQUIREMENTS.md` and the BLOCKED sections of task cards, citing brief sections.
+3. Review it with trigger A. Merge. Now BLOCKED tasks can run.
+
+## Daily routine for Kevin
+
+1. Open Claude Code in `CSC4801_TeamA` (on `dev`). Run `/orient`.
+2. Approve the tasks it proposes. It runs `/dispatch` for each.
+3. When agents report, it runs `/review-task`, then `/merge`.
+4. At the end of a phase it runs `/phase-gate`.
+5. Before stopping: it updates STATUS.md. Then `/clear`.

```
