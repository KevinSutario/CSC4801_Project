# Review packet phase-0 (2 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: .env.example, .github/ISSUE_TEMPLATE/audit_bug_report.yml, .github/labels.yml, .gitignore, CLAUDE.md, Dockerfile, INSTALL.md, README.md, SPEC.md

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
diff --git a/.env.example b/.env.example
new file mode 100644
index 0000000..fbf7871
--- /dev/null
+++ b/.env.example
@@ -0,0 +1,5 @@
+# Optional settings. The app does not automatically load this file.
+# Omit SECRET_KEY for a generated key (sessions expire on server restart).
+# SECRET_KEY=replace-with-a-random-local-secret
+# DATABASE=/absolute/path/to/local-demo.sqlite3
+# PORT=8080
diff --git a/.github/ISSUE_TEMPLATE/audit_bug_report.yml b/.github/ISSUE_TEMPLATE/audit_bug_report.yml
new file mode 100644
index 0000000..42ff0e1
--- /dev/null
+++ b/.github/ISSUE_TEMPLATE/audit_bug_report.yml
@@ -0,0 +1,58 @@
+name: Cross-team audit bug report
+description: Report a reproducible bug found during the Week 12 peer review
+title: "[AUDIT] "
+labels:
+  - "audit:report"
+  - "status:needs-triage"
+body:
+  - type: markdown
+    attributes:
+      value: |
+        Read the `PEER_REVIEW.md` first and search existing issues before filing. Audit the latest commit on the target team's `main` branch, built from the repository's `Dockerfile`. Never post credentials or personal data. After submitting, add exactly one `type:*` label matching your selection below.
+  - type: input
+    id: reporting-team
+    attributes:
+      label: Reporting team
+      placeholder: Team number and name
+    validations:
+      required: true
+  - type: input
+    id: commit
+    attributes:
+      label: Commit SHA
+      description: Full 40-character SHA of the commit where you observed the bug.
+    validations:
+      required: true
+  - type: dropdown
+    id: bug-type
+    attributes:
+      label: Type
+      options:
+        - security
+        - functional
+        - performance
+    validations:
+      required: true
+  - type: textarea
+    id: reproduction
+    attributes:
+      label: Minimal test case
+      description: Numbered, exact commands or UI actions that reproduce the bug.
+      placeholder: |
+        1. Run ...
+        2. Sign in as ...
+        3. Observe ...
+    validations:
+      required: true
+  - type: textarea
+    id: expected
+    attributes:
+      label: Expected behavior
+    validations:
+      required: true
+  - type: textarea
+    id: actual
+    attributes:
+      label: Actual behavior
+    validations:
+      required: true
diff --git a/.github/labels.yml b/.github/labels.yml
new file mode 100644
index 0000000..25cf1b4
--- /dev/null
+++ b/.github/labels.yml
@@ -0,0 +1,38 @@
+# Cross-team audit labels for the CSC4801 final project.
+#
+# Import into a team repository with, e.g., github-label-sync:
+#   npx github-label-sync --labels labels.yml <owner>/<repo>
+# or any label importer that accepts a name/color/description list.
+
+- name: "audit:report"
+  color: "d73a4a"
+  description: "Cross-team audit bug report"
+- name: "audit:repair"
+  color: "0e8a16"
+  description: "Repair of a confirmed audit finding"
+
+- name: "type:security"
+  color: "b60205"
+  description: "Auth, authorization, privacy, injection, XSS, or secret handling fails"
+- name: "type:functional"
+  color: "1d76db"
+  description: "Required behavior is missing or incorrect"
+- name: "type:performance"
+  color: "5319e7"
+  description: "Reproducible performance problem on a small, safe fixture"
+
+- name: "status:needs-triage"
+  color: "fbca04"
+  description: "New report awaiting triage by the target team or instructor"
+- name: "status:confirmed"
+  color: "0e8a16"
+  description: "Reproducible, in scope, safe, and not a duplicate"
+- name: "status:rejected"
+  color: "e11d21"
+  description: "Fails a valid-finding condition"
+- name: "status:duplicate"
+  color: "cccccc"
+  description: "Same root cause as an earlier linked issue"
+- name: "status:fixed"
+  color: "c2e0c6"
+  description: "Fix and regression evidence pass at the linked fix commit"
diff --git a/.gitignore b/.gitignore
new file mode 100644
index 0000000..eb555ca
--- /dev/null
+++ b/.gitignore
@@ -0,0 +1,17 @@
+.venv/
+venv/
+__pycache__/
+*.py[cod]
+.pytest_cache/
+data/
+.env
+*.sqlite3
+
+# Claude Code personal settings (may contain tokens)
+.claude/settings.local.json
+
+# Keystone
+instance/
+tests/repro/
+reviews/*/repro/
+.ruff_cache/
diff --git a/CLAUDE.md b/CLAUDE.md
new file mode 100644
index 0000000..ce7115f
--- /dev/null
+++ b/CLAUDE.md
@@ -0,0 +1,83 @@
+# Keystone: rules for every agent
+
+You are working on Keystone, a job platform for the CSC4801 final project.
+Read this file fully at the start of every task. It is short on purpose.
+
+## Who you are
+
+- **Orchestrator**: the main session. You plan, dispatch, review and merge. You do not write app code.
+- **Subagent**: you were started with a task card or a review packet. Do only that. Nothing else.
+
+If you are a subagent, your prompt names your task card (for example `docs/tasks/T07.md`) and your
+worktree folder. Read the card. It tells you every file you may read and every file you may change.
+
+## Hard rules
+
+1. **Stay inside your worktree.** Every command starts with `cd <your worktree> &&`. Never edit files
+   in the main repo folder or in another task's worktree.
+2. **Only change files listed under "Owns" in your task card.** Need another file changed? Stop and
+   report. `python scripts/check_scope.py <task-id>` must pass before you finish.
+3. **Read before you write.** Never edit a file you have not opened in this session. Before calling a
+   function you did not write, quote its real signature from its file.
+4. **Never invent.** No made-up functions, routes, columns, config keys, Flask APIs, or library
+   methods. Check `docs/plan/07-CONTRACTS.md` or the code. If it is not there, stop and ask.
+5. **Rules come from the brief.** Business rules (matching, scheduling, validation limits) come from
+   `docs/BRIEF.md` only. If your card says BLOCKED, or the brief section is empty, stop and report.
+6. **No new dependencies.** Only what is in `requirements.lock` and `requirements-dev.txt`.
+7. **Prove it.** Run `python scripts/check.py` and paste the real output before you say done. The
+   words "done", "fixed" and "should work" are banned unless passing output is right above them.
+8. **Two strikes then stop.** If the same error survives two fix attempts, stop and report: the exact
+   error, what you tried, your two best guesses, what you need.
+9. **Never weaken a test** to get green. No skipping, deleting or loosening assertions.
+10. **Test first for logic.** Write the failing test, show it failing, then write the code.
+11. **No git history changes.** No rebase, reset, force push, or branch deletion. Commit only on your
+    own task branch. Never push. Never merge (the orchestrator merges).
+
+## Fixing a bug
+
+1. Write a test that fails because of the bug. Run it. Show it failing.
+2. State the cause in one sentence (the mechanism, not the symptom).
+3. Search for the same mistake elsewhere: `git grep -n "<pattern>"`. List the hits. Do not fix them
+   in this change; report them.
+4. Fix the cause with the smallest change. Show the test passing, then `python scripts/check.py`.
+5. Put a `BUG:` block in your final reply (symptom, cause, test name, other hits). The orchestrator
+   copies it into `docs/state/BUGS.md`.
+
+## Stack (do not change)
+
+- Python 3.12, Flask 3.1, Jinja2, SQLite via the standard `sqlite3` module, waitress, pytest.
+- Server-rendered HTML forms. No JavaScript framework. No ORM.
+- Times stored as UTC ISO-8601 strings. Converted with `zoneinfo` (needs the `tzdata` package).
+
+## Commands (use exactly these)
+
+```
+python scripts/check.py              # the gate: lint + all tests. Must pass.
+python -m pytest tests/unit/test_X.py::test_name -q    # one test
+python scripts/check_scope.py T07    # are my changes inside my Owns list?
+python -m flask --app app run --debug   # local run (never in Docker)
+python scripts/seed.py --reset       # demo data (after task T19 exists)
+```
+
+## Where things are
+
+- `docs/BRIEF.md`: the course brief, the source of truth for rules
+- `docs/plan/`: the plan. `07-CONTRACTS.md` is the frozen list of names and signatures
+- `docs/tasks/`: one card per task
+- `docs/state/STATUS.md`: what is done, running, next (orchestrator updates it)
+- `docs/state/JOURNAL.md`, `DECISIONS.md`, `BUGS.md`: logs
+- `reviews/`: review packets, findings and verdicts
+
+## Reply format when you finish a task
+
+```
+TASK: T07
+FILES CHANGED: <paths>
+TESTS ADDED: <test names>
+CHECK OUTPUT: <paste the last 15 lines of python scripts/check.py>
+SCOPE CHECK: <paste output of check_scope.py>
+STATUS: done | blocked | failing
+OPEN QUESTIONS: <or "none">
+```
+
+Write `unknown` instead of guessing anything.
diff --git a/Dockerfile b/Dockerfile
new file mode 100644
index 0000000..408fc9c
--- /dev/null
+++ b/Dockerfile
@@ -0,0 +1,20 @@
+# Python starter example: adapt the image and commands to your project's stack.
+FROM python:3.12.11-slim-bookworm
+ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
+WORKDIR /app
+
+# Install your locked dependencies.
+COPY requirements.lock requirements.txt ./
+RUN python -m pip install --no-cache-dir -r requirements.txt
+
+# Copy source and run as an unprivileged user.
+RUN useradd --create-home --uid 10001 student
+COPY --chown=student:student . .
+USER student
+
+# TODO: configure any writable data directories and required environment variables.
+# TODO: expose your application's port, for example:
+# EXPOSE 8080
+
+# TODO: replace this placeholder with your application's startup command.
+CMD ["python", "-c", "raise SystemExit('Template only: configure your application startup command in Dockerfile.')"]
diff --git a/INSTALL.md b/INSTALL.md
new file mode 100644
index 0000000..ecb5c20
--- /dev/null
+++ b/INSTALL.md
@@ -0,0 +1,21 @@
+# Installation Guide
+
+## Prerequisites and Versions
+
+## Dependency Installation
+
+## Environment Variables
+
+## Database Setup and Migrations
+
+## Demo Data and Reset Command
+
+## Docker Build
+
+## Docker Startup
+
+## Local Development
+
+## Running Unit Tests
+
+## Troubleshooting
diff --git a/README.md b/README.md
new file mode 100644
index 0000000..1415287
--- /dev/null
+++ b/README.md
@@ -0,0 +1,31 @@
+# Project Title
+
+## Project Overview
+
+## Team Members
+
+## Architecture Summary
+
+## Quick Start
+
+## Demo Accounts
+
+## Running Unit Tests
+
+## Requirement–Test Mapping
+
+Example rows only: replace the placeholder tests with your own assertions and
+extend this table to cover every requirement ID. Include implementation file(s)
+and named unit tests for each functional requirement. For non-functional
+requirements, describe the relevant verification evidence; mark unimplemented
+optional requirements as `N/A`. The `pass` examples do not verify behavior.
+
+| Requirement ID | Behavior to verify | Implementation file(s) | Unit test(s) / verification evidence |
+|---|---|---|---|
+| FP-AUTH-1 | Registration and session lifecycle | To be filled by the team | `tests/unit/test_auth.py::test_fp_auth_1_registration_and_session_lifecycle` (placeholder) |
+| FP-MATCH-1 | Skill-overlap examples and tie-breaking | To be filled by the team | `tests/unit/test_matching.py::test_fp_match_1_examples_normalization_and_floor`; `tests/unit/test_matching.py::test_fp_match_1_both_tie_breakers` (placeholders) |
+| FP-SCHED-3 | Booking conflict outcome | To be filled by the team | `tests/unit/test_scheduling.py::test_fp_sched_3_conflict_contract` (placeholder) |
+
+## Document Index
+
+## Known Limitations
diff --git a/SPEC.md b/SPEC.md
new file mode 100644
index 0000000..6acaaf6
--- /dev/null
+++ b/SPEC.md
@@ -0,0 +1,23 @@
+# Project Specification
+
+## Product Scope
+
+## Architecture
+
+## Data Model and Relationships
+
+## Authentication and Authorization
+
+## API Routes or Server Actions
+
+## User Interface and Workflows
+
+## Matching Algorithm and Skill Storage
+
+## Interview Scheduling and Booking Transaction
+
+## Security Controls
+
+## Optional AI Features and Data Flow
+
+## Design Decisions and Limitations

```
