# Status

P2 (integration lead) updates this file. It is the team's shared memory.
States (slimmed 2026-11-19): **TODO**, **DOING**, **MERGED**, **BLOCKED**. (Old rows may still read
READY/RUNNING — treat READY as TODO, RUNNING as DOING.)
`scripts/check_contracts.py` reads the State column and keys off the literal **MERGED**, so keep that
word exact and keep the table format.

Current phase: **1** · Brief: **present** (docs/BRIEF.md holds the full course brief)

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
| T13 | 3 | TODO | - | after T07, T10, T11; owner P1 |
| T14 | 3 | TODO | - | after T08, T10; owner P1 |
| T15 | 3 | TODO | - | after T11, T14; owner P2 |
| T16 | 3 | TODO | - | after T12, T14; owner P3 |
| T17 | 3 | TODO | - | after T16; owner P3 |
| T18 | - | DESCOPED | - | D22: activity log + Today widgets cut (outside brief, 1-week timeline); blocks nothing |
| T06 | 3 | TODO | - | after T10, T15, T16; owner P2 |
| T19 | 4 | TODO | - | after phase 3; owner P3 |
| T20 | 4 | TODO | - | after phase 3; owner P2 |
| T21 | 4 | TODO | - | after T19, T20; owner P1 |
| T22 | 5 | TODO | - | after phase 4; all three |

## Running now
Phase 2 complete: all six cards (T07-T12) MERGED on dev. Gate 168 passed, 8 placeholder skips
(Phase 3+ cards). Next: the **Phase-2 gate** (P2) — check.py + check_contracts.py pass, every
Phase-2 FP-* (FP-CAN-1, FP-EMP-1, FP-EMP-2, FP-MATCH-1, FP-SCHED-1) has a test, then merge dev into
main and tag phase-2. After that, Phase 3 (T13 P1, T14 P1, T15 P2, T16 P3, T17 P3, T06 P2) begins.
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
