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
| T01 | 1 | TODO | - | next up; owner P3 |
| T02 | 1 | TODO | - | after T01; owner P2 |
| T03 | 1 | TODO | - | after T02; owner P1 |
| T04 | 1 | TODO | - | after T03; owner P3 |
| T05 | 1 | TODO | - | after T04; owner P2 |
| T07 | 2 | TODO | - | after phase 1; owner P1 |
| T08 | 2 | TODO | - | after T07; owner P1 |
| T09 | 2 | TODO | - | after phase 1; owner P2 |
| T10 | 2 | TODO | - | after T09; owner P2 |
| T11 | 2 | TODO | - | after phase 1; owner P3 |
| T12 | 2 | TODO | - | after phase 1; owner P3 |
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
Nothing. CC01 is merged, so Phase 1 can start: P3 takes T01 first (the rest of Phase 1 is serial).

## Phase 0 gate
- Closed earlier (pre-migration). T00, B1, B2, B3 MERGED; their file outputs (scripts, packet
  tooling) are in the tree. The `phase-0` tag was lost in the migration; re-tag if needed.

## Waiting on Kevin
- Nothing. 2026-11-19: D16 (display name editable) confirmed; D17 third seed job confirmed; D18
  "stop/resume accepting applications" deferred (outside brief; descoped for the 1-week timeline) —
  jobs are plain, no status flag. Scope otherwise unchanged from the brief.
