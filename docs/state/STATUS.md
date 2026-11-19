# Status

P2 (integration lead) updates this file. It is the team's shared memory.
States (slimmed 2026-11-19): **TODO**, **DOING**, **MERGED**, **BLOCKED**. (Old rows may still read
READY/RUNNING — treat READY as TODO, RUNNING as DOING.)
`scripts/check_contracts.py` reads the State column and keys off the literal **MERGED**, so keep that
word exact and keep the table format.

Current phase: **1** · Brief: **present** (docs/BRIEF.md holds the full course brief)

Team split: **docs/state/DIVISION.md** — three lanes (P1 candidate+docs, P2 employer/auth+integration lead, P3 platform/matching/scheduling).

| Task | Phase | State | Worktree | Notes |
|---|---|---|---|---|
| T00 | 0 | MERGED | - | merged into dev at 42113ab; task and merge reviews PASS; gate passed (17 tests); phase-0 gate pending |
| B1 | 0 | MERGED | - | merged at 6507ca5; task and merge reviews PASS; 20 tests passed; Phase 0 packet generation repaired |
| B2 | 0 | MERGED | - | c3980e8; task and merge reviews PASS; 32 tests passed; empty-suite failure and lint/scope regressions |
| B3 | 0 | MERGED | - | 9f1f8db; task and merge reviews PASS; 41 tests; rename source/destination scope enforced |
| T-BRIEF | - | MERGED | - | 8f78b54; task review FIX then re-check, 4 minor leftovers carried into CC01 (D19); rules quoted on T05-T17 |
| CC01 | - | FIXING | ../ks-CC01 | 7e800bd; review FIX (26 confirmed); fix round 1; contract changes D9-D18 (403, raw-text resume, 4 statuses, 409 delete, employer slots, no closed state); runs alone |
| T01 | 1 | READY | - | |
| T02 | 1 | READY | - | after T01 |
| T03 | 1 | READY | - | after T02 |
| T04 | 1 | READY | - | after T03 |
| T05 | 1 | READY | - | after T04 |
| T07 | 2 | BLOCKED | - | needs CC01; |
| T08 | 2 | BLOCKED | - | needs CC01; after T07 |
| T09 | 2 | READY | - | |
| T10 | 2 | BLOCKED | - | needs CC01; after T09 |
| T11 | 2 | READY | - | after CC01 |
| T12 | 2 | BLOCKED | - | needs CC01; |
| T13 | 3 | BLOCKED | - | needs CC01; needs T11 |
| T14 | 3 | BLOCKED | - | needs CC01; after T08, T10 |
| T15 | 3 | BLOCKED | - | needs CC01; after T11, T14 |
| T16 | 3 | BLOCKED | - | needs CC01; needs T-BRIEF |
| T17 | 3 | BLOCKED | - | needs CC01; needs T-BRIEF, T16 |
| T18 | 3 | READY | - | after T14 |
| T06 | 3 | BLOCKED | - | needs CC01; after T10, T15, T16 |
| T19 | 4 | READY | - | after phase 3 |
| T20 | 4 | READY | - | after phase 3 |
| T21 | 4 | READY | - | after T19, T20 |
| T22 | 5 | READY | - | after phase 4 |

## Running now
CC01 (implementer, worktree ../ks-CC01). Nothing else may run until CC01 merges.

## Phase 0 gate
- CLOSED 2026-11-10: main fast-forwarded to 347725b (PR #2 on GitHub), `phase-0` tagged locally.
- T00, B1, B2 and B3 MERGED; lint and 41 tests pass; phase review PASS (`reviews/phase-0/verdict.md`).

## Waiting on Kevin
- nothing blocking; D16 (display name editable) and D18 (no closed job state) were orchestrator calls on brief MUSTs, confirm or revert
