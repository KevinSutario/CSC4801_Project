# Review packet phase-0 (45 of 46)

Worktree: /Users/mac/CSC4801_TeamA

Files in this packet: scripts/make_packet.py, tests/__init__.py, tests/unit/__init__.py, tests/unit/test_auth.py, tests/unit/test_check.py, tests/unit/test_check_scope.py

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
diff --git a/scripts/make_packet.py b/scripts/make_packet.py
new file mode 100644
index 0000000..65244ea
--- /dev/null
+++ b/scripts/make_packet.py
@@ -0,0 +1,169 @@
+"""Build review packets for the three reviewers and the judge.
+
+Usage (run from the main repo folder, on branch dev):
+    python scripts/make_packet.py task T07
+        task branch task/T07 against dev, worktree ../ks-T07
+    python scripts/make_packet.py merge T07
+        integration branch int/T07 against dev, worktree ../ks-int
+    python scripts/make_packet.py phase 2
+        everything since tag phase-1 on dev, split by file
+    python scripts/make_packet.py audit security
+        whole app on main, one audit area (T22), worktree ../ks-audit.
+        Areas: security, functional, performance, delivery
+
+Writes reviews/<id>/packet-<k>.md and prints each path plus the worktree path.
+A packet holds at most about 400 changed lines; bigger diffs are split by file.
+"""
+
+from __future__ import annotations
+
+import os
+import re
+import subprocess
+import sys
+
+ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+MAX_LINES = 400
+EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
+AUDIT_AREAS = {
+    "security": ["app/security.py", "app/errors.py", "app/auth", "app/candidates/resume_service.py",
+                 "app/candidates/routes_resume.py", "app/*/routes*.py", "app/templates"],
+    "functional": ["app", "tests/unit", "docs/BRIEF.md"],
+    "performance": ["app/jobs", "app/matching", "app/applications", "app/scheduling",
+                    "app/schema.sql"],
+    "delivery": ["README.md", "SPEC.md", "INSTALL.md", "Dockerfile", ".dockerignore", "wsgi.py",
+                 ".env.example", "scripts/seed.py", "requirements.lock"],
+}
+
+
+def git(*args: str, cwd: str = ROOT) -> str:
+    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
+    if proc.returncode != 0:
+        sys.exit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
+    return proc.stdout
+
+
+def read(rel: str) -> str:
+    path = os.path.join(ROOT, rel)
+    if not os.path.exists(path):
+        return f"(missing: {rel})"
+    with open(path, encoding="utf-8") as fh:
+        return fh.read()
+
+
+def security_checklist() -> str:
+    text = read("docs/plan/04-AUTH-SECURITY.md")
+    marker = "## Security review checklist"
+    return text[text.find(marker):] if marker in text else "(checklist not found)"
+
+
+def run_in(cwd: str, cmd: list[str]) -> str:
+    if not os.path.isdir(cwd):
+        return f"(worktree {cwd} not found)"
+    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
+    out = (proc.stdout or "") + (proc.stderr or "")
+    return "\n".join(out.strip().splitlines()[-40:])
+
+
+def split_by_file(diff: str) -> list[tuple[str, str]]:
+    parts = re.split(r"(?m)^(?=diff --git )", diff)
+    files = []
+    for part in parts:
+        if not part.strip():
+            continue
+        m = re.match(r"diff --git a/(\S+) ", part)
+        files.append((m.group(1) if m else "?", part))
+    return files
+
+
+def chunk(files: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
+    chunks: list[list[tuple[str, str]]] = []
+    current: list[tuple[str, str]] = []
+    size = 0
+    for name, part in sorted(files, key=lambda f: f[0]):
+        n = part.count("\n")
+        if current and size + n > MAX_LINES:
+            chunks.append(current)
+            current, size = [], 0
+        current.append((name, part))
+        size += n
+    if current:
+        chunks.append(current)
+    return chunks or [[]]
+
+
+def write_packets(review_id: str, header: str, diff: str, worktree: str) -> None:
+    out_dir = os.path.join(ROOT, "reviews", review_id)
+    os.makedirs(out_dir, exist_ok=True)
+    chunks = chunk(split_by_file(diff))
+    for k, files in enumerate(chunks, start=1):
+        names = ", ".join(n for n, _ in files) or "(no changes)"
+        body = "".join(p for _, p in files)
+        path = os.path.join(out_dir, f"packet-{k}.md")
+        with open(path, "w", encoding="utf-8") as fh:
+            fh.write(f"# Review packet {review_id} ({k} of {len(chunks)})\n\n")
+            fh.write(f"Worktree: {worktree}\n\nFiles in this packet: {names}\n\n")
+            fh.write(header)
+            fh.write("\n\n## Diff\n\n```diff\n" + body + "\n```\n")
+        print(f"PACKET: {path}")
+    print(f"WORKTREE: {worktree}")
+
+
+def main() -> int:
+    if len(sys.argv) != 3 or sys.argv[1] not in ("task", "merge", "phase", "audit"):
+        print(__doc__)
+        return 2
+    mode, ident = sys.argv[1], sys.argv[2]
+    parent = os.path.dirname(ROOT)
+
+    if mode in ("task", "merge"):
+        branch = f"task/{ident}" if mode == "task" else f"int/{ident}"
+        worktree = os.path.join(parent, f"ks-{ident}" if mode == "task" else "ks-int")
+        review_id = ident if mode == "task" else f"merge-{ident}"
+        diff = git("diff", f"dev...{branch}")
+        stat = git("diff", "--stat", f"dev...{branch}")
+        header = (
+            f"## Review type: {mode}\n\n"
+            f"## Task card\n\n{read(f'docs/tasks/{ident}.md')}\n\n"
+            f"## Changed files\n\n```\n{stat}\n```\n\n"
+            f"## Check output (in the worktree)\n\n```\n"
+            f"{run_in(worktree, [sys.executable, 'scripts/check.py'])}\n```\n\n"
+            f"## Scope check\n\n```\n"
+            f"{run_in(worktree, [sys.executable, 'scripts/check_scope.py', ident])}\n```\n\n"
+            f"{security_checklist()}\n"
+        )
+        write_packets(review_id, header, diff, worktree)
+        return 0
+
+    if mode == "audit":
+        if ident not in AUDIT_AREAS:
+            sys.exit("area must be one of: " + ", ".join(AUDIT_AREAS))
+        worktree = os.path.join(parent, "ks-audit")
+        paths = AUDIT_AREAS[ident]
+        diff = git("diff", EMPTY_TREE, "main", "--", *paths)
+        header = (
+            f"## Review type: audit ({ident}), whole app on main\n\n"
+            f"Every line shows as added because this compares against an empty tree.\n\n"
+            f"## Requirements\n\n{read('docs/plan/01-REQUIREMENTS.md')}\n\n"
+            f"{security_checklist()}\n"
+        )
+        write_packets(f"T22-{ident}", header, diff, worktree)
+        return 0
+
+    phase = int(ident)
+    base = EMPTY_TREE if phase == 0 else f"phase-{phase - 1}"
+    diff = git("diff", f"{base}..dev")
+    stat = git("diff", "--stat", f"{base}..dev")
+    header = (
+        f"## Review type: phase {phase}\n\n"
+        f"Compare: {base}..dev\n\n"
+        f"## Requirements\n\n{read('docs/plan/01-REQUIREMENTS.md')}\n\n"
+        f"## Changed files (whole phase)\n\n```\n{stat}\n```\n\n"
+        f"{security_checklist()}\n"
+    )
+    write_packets(f"phase-{phase}", header, diff, ROOT)
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/__init__.py b/tests/__init__.py
new file mode 100644
index 0000000..e69de29
diff --git a/tests/unit/__init__.py b/tests/unit/__init__.py
new file mode 100644
index 0000000..e69de29
diff --git a/tests/unit/test_auth.py b/tests/unit/test_auth.py
new file mode 100644
index 0000000..4bd58db
--- /dev/null
+++ b/tests/unit/test_auth.py
@@ -0,0 +1,17 @@
+# Structure example only: replace each pass with your own unit-test assertions.
+
+
+def test_fp_auth_1_registration_and_session_lifecycle():
+    pass
+
+
+def test_fp_auth_1_invalid_registration():
+    pass
+
+
+def test_fp_auth_2_salted_hash_and_password_verification():
+    pass
+
+
+def test_fp_auth_3_authorization_and_missing_object():
+    pass
diff --git a/tests/unit/test_check.py b/tests/unit/test_check.py
new file mode 100644
index 0000000..5863bdf
--- /dev/null
+++ b/tests/unit/test_check.py
@@ -0,0 +1,76 @@
+"""CLI regression tests for the development gate."""
+
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+import pytest
+
+
+ROOT = Path(__file__).resolve().parents[2]
+
+
+@pytest.fixture
+def gate_repo(tmp_path: Path) -> Path:
+    scripts = tmp_path / "scripts"
+    scripts.mkdir()
+    shutil.copyfile(ROOT / "scripts" / "check.py", scripts / "check.py")
+    shutil.copyfile(ROOT / "ruff.toml", tmp_path / "ruff.toml")
+    (tmp_path / "tests" / "unit").mkdir(parents=True)
+    return tmp_path
+
+
+def run_gate(repo: Path) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [sys.executable, str(repo / "scripts" / "check.py")],
+        cwd=repo, capture_output=True, text=True, timeout=15,
+    )
+
+
+def write_test(repo: Path, assertion: str) -> None:
+    (repo / "tests" / "unit" / "test_example.py").write_text(
+        f"def test_example():\n    assert {assertion}\n", encoding="utf-8",
+    )
+
+
+def test_gate_fails_when_no_tests_are_collected(gate_repo: Path) -> None:
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert "no tests ran" in output, output
+    assert result.returncode != 0, output
+    assert "CHECK FAILED: tests" in output, output
+    assert "CHECK PASSED" not in output, output
+
+
+def test_gate_passes_with_clean_lint_and_passing_test(gate_repo: Path) -> None:
+    write_test(gate_repo, "True")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode == 0, output
+    assert "All checks passed!" in output, output
+    assert "1 passed" in output, output
+    assert "CHECK PASSED" in output, output
+
+
+def test_gate_fails_when_lint_fails(gate_repo: Path) -> None:
+    write_test(gate_repo, "True")
+    (gate_repo / "bad_lint.py").write_text("import os\n", encoding="utf-8")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode != 0, output
+    assert "F401" in output, output
+    assert "1 passed" in output, output
+    assert "CHECK FAILED: lint" in output, output
+    assert "CHECK PASSED" not in output, output
+
+
+def test_gate_fails_when_a_test_fails(gate_repo: Path) -> None:
+    write_test(gate_repo, "1 == 2")
+    result = run_gate(gate_repo)
+    output = result.stdout + result.stderr
+    assert result.returncode != 0, output
+    assert "All checks passed!" in output, output
+    assert "1 failed" in output, output
+    assert "CHECK FAILED: tests" in output, output
+    assert "CHECK PASSED" not in output, output
diff --git a/tests/unit/test_check_scope.py b/tests/unit/test_check_scope.py
new file mode 100644
index 0000000..39797f0
--- /dev/null
+++ b/tests/unit/test_check_scope.py
@@ -0,0 +1,72 @@
+"""CLI regression tests for task ownership enforcement."""
+
+import os
+from pathlib import Path
+import shutil
+import subprocess
+import sys
+
+import pytest
+
+
+SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_scope.py"
+
+
+def git(repo: Path, *args: str) -> None:
+    subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)
+
+
+@pytest.fixture
+def scope_repo(tmp_path: Path) -> Path:
+    (tmp_path / "scripts").mkdir()
+    (tmp_path / "docs" / "tasks").mkdir(parents=True)
+    shutil.copyfile(SCRIPT, tmp_path / "scripts" / "check_scope.py")
+    (tmp_path / "docs" / "tasks" / "B2.md").write_text(
+        "# Fixture task\n\n## Owns\n- `owned.txt`\n- `owned-new.txt`\n", encoding="utf-8",
+    )
+    for name in ("owned.txt", "unowned.txt"):
+        (tmp_path / name).write_text("original\n", encoding="utf-8")
+    git(tmp_path, "init", "--initial-branch=dev")
+    git(tmp_path, "config", "user.name", "Scope test")
+    git(tmp_path, "config", "user.email", "scope@example.invalid")
+    git(tmp_path, "add", ".")
+    git(tmp_path, "commit", "-m", "Fixture baseline")
+    git(tmp_path, "checkout", "-b", "task/B2")
+    return tmp_path
+
+
+def change_file(repo: Path, name: str, state: str) -> str:
+    if state == "untracked":
+        name = name.replace(".txt", "-new.txt")
+    (repo / name).write_text("changed\n", encoding="utf-8")
+    if state in ("staged", "committed"):
+        git(repo, "add", name)
+    if state == "committed":
+        git(repo, "commit", "-m", "Change fixture file")
+    return name
+
+
+def run_scope(repo: Path) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [sys.executable, "scripts/check_scope.py", "B2"],
+        cwd=repo, capture_output=True, text=True,
+        env={**os.environ, "SCOPE_BASE": "dev"}, timeout=15,
+    )
+
+
+@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
+def test_scope_accepts_owned_changes(scope_repo: Path, state: str) -> None:
+    change_file(scope_repo, "owned.txt", state)
+    result = run_scope(scope_repo)
+    assert result.returncode == 0, result.stdout + result.stderr
+    assert "SCOPE OK for B2" in result.stdout
+
+
+@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
+def test_scope_rejects_unowned_changes(scope_repo: Path, state: str) -> None:
+    name = change_file(scope_repo, "unowned.txt", state)
+    result = run_scope(scope_repo)
+    assert result.returncode != 0, result.stdout + result.stderr
+    assert "SCOPE FAILED for B2" in result.stdout
+    assert name in result.stdout
+    assert "SCOPE OK" not in result.stdout

```
