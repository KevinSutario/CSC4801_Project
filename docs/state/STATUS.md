# Status

P2 (integration lead) updates this file. It is the team's shared memory.
States (slimmed 2026-11-19): **TODO**, **DOING**, **MERGED**, **BLOCKED**. (Old rows may still read
READY/RUNNING — treat READY as TODO, RUNNING as DOING.)
`scripts/check_contracts.py` reads the State column and keys off the literal **MERGED**, so keep that
word exact and keep the table format.

Current phase: **6 (integrated on dev)** · Brief: **present** (docs/BRIEF.md holds the full course brief)

> **Repo migrated 2026-11-19:** git history did not come over, so the commit SHAs, the `phase-0` tag
> and the `../ks-CC01` worktree below are stale and will not resolve. The file outputs of the MERGED
> tasks are present; trust the files, not the SHAs. History restarts from the migration commit.

Team split: **docs/state/DIVISION.md** — three lanes (P1 candidate+docs, P2 employer/auth+integration lead, P3 platform/matching/scheduling).

| Task | Phase | State | Worktree | Notes |
|---|---|---|---|---|
| T00 | 0 | MERGED | - | merged into dev at 42113ab; task and merge reviews PASS; gate passed (17 tests); phase-0 gate pending |
| B1 | 0 | MERGED | - | merged at 6507ca5; task and merge reviews PASS; 20 tests passed; Phase 0 packet generation repaired |
| B2 | 0 | MERGED | - | c3980e8; task and merge reviews PASS; 32 tests passed; empty-suite failure and lint/scope regressions |
| B3 | 0 | MERGED | - | 9f1f8db; task and merge reviews PASS; 41 tests; rename source/destination scope enforced |
| T-BRIEF | - | MERGED | - | 8f78b54; task review FIX then re-check, 4 minor leftovers carried into CC01 (D19); rules quoted on T05-T17 |
| CC01 | - | MERGED | - | 2026-11-19: D9-D18 applied to contracts, schema, plan docs and cards T01-T21; Step-7 grep clean; lint + 41 tests pass. Decided 26 review findings skipped per Kevin ("only the decisions"); minor wording nitpicks remain for later. |
| T01 | 1 | MERGED | - | merged into dev at 644ea70 (--no-ff); review PASS (reviews/T01.md, careful); gate passed (56 tests); schema byte-identical to 03-DATA-MODEL.md |
| T02 | 1 | MERGED | - | merged into dev at 52325b0 (--no-ff); review PASS (reviews/T02.md, careful); gate passed (81 tests); security.py + audit.py |
| T03 | 1 | MERGED | - | merged into dev via PR #2 (e4914cf); owner P1; design tokens, layout, components, landing |
| T04 | 1 | MERGED | - | merged into dev at 5cd217b (--no-ff); review PASS (reviews/T04.md); gate 77 passed + 20 placeholder skips; conftest factories + per-task placeholder tests. P3's out-of-scope STATUS.md edit dropped at merge (P2 owns this file) |
| T05 | 1 | MERGED | - | committed directly on dev at dc56c6d (no merge commit — branch step was skipped; code reviewed PASS, reviews/T05.md, careful); gate 93 passed; auth service + routes + templates |
| T07 | 2 | MERGED | - | merged into dev via PR #6 (6f013c2); owner P1; candidate profile + skills + candidate home; gate passes on dev. State recorded by P2 (PR did not update this table) |
| T08 | 2 | MERGED | - | merged into dev at 51cae58 (--no-ff, PR #7); owner P1; review PASS (reviews/T08.md, careful); gate 139 passed; private resume, D10 (403 non-own incl missing, 404 own-missing), FP-SEC-3. P1's out-of-scope STATUS.md edit dropped at merge |
| T09 | 2 | MERGED | - | committed directly on dev at 7175141 (no merge commit; review PASS reviews/T09.md light+); gate 104 passed; company profile + employer home; FP-EMP-1 + FP-SEC-3 |
| T10 | 2 | MERGED | - | merged into dev at 0ea9bbb (--no-ff); review PASS (reviews/T10.md, careful); gate 124 passed; jobs CRUD + detail; FP-EMP-2 (409 delete, 403/404 ownership); list_jobs fixed 2 queries |
| T11 | 2 | MERGED | - | merged into dev at 372ab19 (--no-ff); owner P3; review PASS (reviews/T11.md, careful); pure matching engine (score/rank) + skill normalisation; FP-MATCH-1 |
| T12 | 2 | MERGED | - | merged into dev at e38b360 (--no-ff); owner P3; review PASS (reviews/T12.md, careful); timeutil (UTC/DST) + interview slots (30min, overlap, 409-on-booked); FP-SCHED-1 |
| T13 | 3 | MERGED | - | merged into dev at 7ba049a (--no-ff); owner P1; review PASS (reviews/T13.md, careful); recommendations page ranks all jobs; FP-CAN-2 |
| T14 | 3 | MERGED | - | merged into dev at 58b02d7 (--no-ff); owner P1; review PASS (reviews/T14.md, careful); apply + confirm + my applications; FP-CAN-3 (apply-once, 409 duplicate, 403/404 ownership) |
| T15 | 3 | MERGED | - | merged into dev at ab63577 (--no-ff); owner P2; review PASS (reviews/T15.md, careful); applicants list + status changes; FP-EMP-3 (order D15, 4 statuses, 403/404, booking kept on status change) |
| T16 | 3 | MERGED | - | merged into dev at a924ea2 (--no-ff); owner P3; review PASS (reviews/T16.md, careful); booking eligibility + bookable slots + confirm; FP-SCHED-2 (5 conditions, no partial write). T17 hardens concurrency next |
| T17 | 3 | MERGED | - | merged into dev at f0ee89c (--no-ff); owner P3; review PASS (reviews/T17.md, careful); booking conflict contract + concurrency; FP-SCHED-3 (BEGIN IMMEDIATE + unique index, 409 "Slot already booked", booking.conflict audit) |
| T18 | - | DESCOPED | - | D22: activity log + Today widgets cut (outside brief, 1-week timeline); blocks nothing |
| T06 | 3 | MERGED | - | merged into dev at 96408a1 (--no-ff); owner P2; review PASS (reviews/T06.md, careful); authorization sweep FP-AUTH-3/FP-SEC-1 over all 14 id-routes; NO holes found, no Bxx needed |
| T19 | 4 | MERGED | - | merged into dev at e47e5e0 (--no-ff); owner P3; review PASS (reviews/T19.md, careful); seed demo data (5 users, 3 jobs, 4 statuses) via real services + --reset; seed(app) exposed. Unblocks T20 |
| T20 | 4 | MERGED | - | merged into dev at fcc7450 (--no-ff); owner P2; review PASS (reviews/T20.md); Dockerfile + wsgi + first-start seed; --release gate 225 passed 0 skips. NOTE: docker build/run not run in review sandbox — run once before Phase-4 gate |
| T21 | 4 | MERGED | - | merged into dev at 0cd0e5c (--no-ff); owner P1; review PASS (reviews/T21.md, careful); README+SPEC+INSTALL, no empty sections, all 30 cited test names verified to exist; --release gate green |
| T22 | 5 | TODO | - | after phase 4; all three |
| CC02 | 6 | MERGED | - | merged into dev at b9a8439; resume_files table and CV-file contracts (D23) |
| T23 | 6 | MERGED | - | merged into dev at 0a3bc86 (--no-ff); owner P1; review PASS (reviews/T23.md, careful); gate 228 passed; CV file upload alongside text, owner-only download (403 before existence), traversal guard, 6 invalid-upload cases; reuses resume.update. Unblocks T24, T25 |
| T24 | 6 | MERGED | - | merged into dev at bad79da; review PASS (reviews/T24.md); employer views an applicant's CV for an owned job |
| T25 | 6 | MERGED | - | merged into dev at f4fd6c4; review PASS (reviews/T25.md); seeds a demo CV through save_resume_file |
| T26 | 6 | MERGED | - | merged into dev at 6b70d54 (PR #17); links each employer job to its applicant list |
| CC03 | 6 | MERGED | - | merged into dev at 5677165 (PR #19); additive SQLite upgrade for slot notes (D24) |
| T27 | 6 | MERGED | - | merged into dev at 74cc473 (PR #18); booking notes and validated HTTPS meeting links (D24) |

## T22 self-audit (Phase 5) — result
Four independent audits against main/dev (security, functional, performance, delivery):
- Performance: no N+1; all list/scoring paths <2ms at 200 rows (target 1s); indexes used.
- Functional: no MUST violations; all FP-* match the brief (floor formula, tie-breaks, apply-once,
  4 statuses, booking 5 conditions, exact "Slot already booked", every job listed).
- Delivery: INSTALL/README/SPEC/Dockerfile accurate; all 30 cited test names exist.
- Security: ONE confirmed hole — login rate limit bypassable by rotating IP. Fixed as **B5**
  (per-email + per-IP keys, merged e0919f1). No xfail left; no open Bxx.
Accepted non-bugs (documented, not MUST violations): interview slots don't block job deletion
(D13 — a booked slot implies a counted interviewing application); unauthenticated POST returns 403
(CSRF before auth; brief allows 401-or-redirect and GET redirects).
T22 gate: check.py --release passes, no open Bxx, no xfail. Phase 5 complete pending main tag.

## Running now
Phase 3 COMPLETE: T13, T14, T15, T16, T17, T06 all MERGED on dev. 219 passed, 0 skips. The authz
sweep (T06) found no holes. Next: the **Phase-3 gate** (P2) — check.py + check_contracts.py pass,
Phase-3 FP-* (FP-CAN-2, FP-CAN-3, FP-EMP-3, FP-SCHED-2, FP-SCHED-3, FP-AUTH-3, FP-SEC-1) each have a
test, then merge dev->main and tag phase-3. (phase-1, phase-2 tags already on main.)
Phase 4 cards all MERGED: T19 (P3), T20 (P2), T21 (P1). Phase-4 gate (P2) in progress:
Earlier check.py --release passed (225, 0 skips), and docs have no empty sections. Docker testing
found B4 (PermissionError on /app/instance: container runs as student, /app root-owned, create_app
always makes instance_path). Fixed in the Dockerfile and MERGED into dev at fb4bb18 (reviews/B4.md);
release gate still green (225, 0 skips). The user rebuilt and confirmed the container serves and a
demo login works. Before tagging phase-4, still recommended: a FRESH-CLONE build/run and sign-in as
all five demo accounts (release checklist item 2). Then: merge dev->main, tag phase-4.
Phase 5: T22 self-audit (all three).
Phase 5: T22 self-audit (all three).

## Phase 6 — CV file + employer resume view (added 2026-11-24, D23)
New post-submission requirements: a real CV **file** input for candidates, and a place for employers
to see submissions. Four cards, strictly ordered by the schema freeze + a service dependency:
**CC02 (P2)** → **T23 (P1)** → { **T24 (P2)**, **T25 (P3)** }. CC02 adds the `resume_files` table +
contracts (it is a CC card because `schema.sql`/contracts froze after Phase 1). T23 builds the
candidate upload + owner-only download (graded FP-CAN-1: direct URL is owner-only, 403 otherwise).
T24 adds the employer "View CV" link for its own applicants (encouraged, UNGRADED — not a valid
audit finding); it must not regress the graded T15 fields or the T23 owner-only URL. T25 seeds a demo
CV through the real service. Audit uses the existing `resume.update` action (frozen `audit.py`
untouched). Cards: docs/tasks/CC02.md, T23.md, T24.md, T25.md.
Close-out (2026-11-26): CC02, T23–T27, and CC03 are merged into `dev`. T26 adds employer applicant
navigation. CC03 and T27 add interview notes and meeting links for bookings (D24). The integrated
release gate passed with 233 tests and no skips.

Note: the Phase-1 gate (merge dev->main, tag phase-1) should be confirmed — verify main + tag exist.
Skeleton freeze applies from Phase 1 onward: app/__init__.py, db.py, schema.sql, security.py,
audit.py, base.html, components/*, conftest.py — only a CCxx (P2) may touch these.

## Phase 0 gate
- Closed earlier (pre-migration). T00, B1, B2, B3 MERGED; their file outputs (scripts, packet
  tooling) are in the tree. The `phase-0` tag was lost in the migration; re-tag if needed.

## Waiting on Kevin
- Nothing. 2026-11-19: D16 (display name editable) confirmed; D17 third seed job confirmed; D18
  "stop/resume accepting applications" deferred (outside brief; descoped for the 1-week timeline) —
  jobs are plain, no status flag. Scope otherwise unchanged from the brief.
