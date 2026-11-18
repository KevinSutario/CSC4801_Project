# 08 · Tasks, phases and parallel lanes

Each task has a card in `docs/tasks/`. A card is complete on its own: an agent needs nothing else.

## Dependency map

```
Phase 0   T00 tooling
             │
Phase 1   T01 skeleton ─> T02 security+audit ─> T03 layout+UI ─> T04 test harness ─> T05 auth
             │
             ├────────── T-BRIEF (any time the brief arrives; runs alone, docs only)
             │
Phase 2   lane CAN:   T07 profile ─> T08 resume                                                      │
          lane EMP:   T09 company ─> T10 jobs                                                         │
          lane MATCH: T11 matching engine  (BLOCKED until T-BRIEF)                                   │
          lane SCHED: T12 time + slots                                                               │
             │
Phase 3   T13 recommendations  (needs T07, T10, T11)        joins lanes
          T14 apply            (needs T08, T10)             joins lanes
          T15 applicants       (needs T11, T14)             joins lanes
          T16 booking          (needs T12, T14; BLOCKED until T-BRIEF)   joins lanes
          T17 booking conflict (needs T16; BLOCKED until T-BRIEF)
          T18 activity + Today (needs T14)
          T06 authorization sweep (needs T10, T15, T16)   FP-AUTH-3 across every route
             │
Phase 4   T19 seed data ─┬─> T21 docs
          T20 Docker ────┘
             │
Phase 5   T22 self-audit (review agents only) ─> bug cards Bxx
```

## Phase 0: tooling

| Task | Title | Depends on | Owns (short) | Status |
|---|---|---|---|---|
| T00 | Tooling and gate | none | scripts, configs | DONE in setup, needs commit and verify |

Gate: `python scripts/check.py` prints CHECK PASSED. Tag `phase-0`.

## Phase 1: foundation (strictly one task at a time)

Everything here is shared by all later work, so it is built in order, by one agent at a time, and
then frozen.

| Task | Title | Depends on | Requirement |
|---|---|---|---|
| T01 | App skeleton, config, db, schema, errors, blueprint stubs, provisional skills | T00 | none |
| T02 | Security module (CSRF, headers, login/role decorators, rate limit) and audit log | T01 | security |
| T03 | Design tokens, CSS, base layout, component macros, landing page | T02 | UX |
| T04 | Test harness: conftest fixtures and factories, placeholder tests | T03 | testing |
| T05 | Register, sign in, sign out, safe redirects | T04 | FP-AUTH-1, FP-AUTH-2 |

FP-AUTH-3 (authorization and missing objects) needs real objects, so it is tested in Phase 3 by
T06, across every route that takes an id.

Gate: phase review clean, FP-AUTH-1 and FP-AUTH-2 tests pass. Tag `phase-1`.

## Phase 2: four lanes in parallel (max 3 agents at once)

| Lane | Task | Title | Depends on | Requirement | Can run with |
|---|---|---|---|---|---|
| CAN | T07 | Candidate profile and skills, Today page shell | T05 | FP-CAN-1 (profile) | T09, T11, T12 |
| CAN | T08 | Resume upload, list, delete, private download | T07 | FP-CAN-1 (resume) | T09, T10, T11, T12 |
| EMP | T09 | Company profile, employer home | T05 | FP-EMP-1 | T07, T08, T11, T12 |
| EMP | T10 | Jobs: create, edit, close, delete, detail | T09 | FP-EMP-2 | T07, T08, T11, T12 |
| MATCH | T11 | Matching engine (pure) and normalisation | T05, T-BRIEF | FP-MATCH-1 | any |
| SCHED | T12 | Time zone helpers, interview slots | T05 | FP-SCHED-1 | any |

Suggested batches: {T07, T09, T12} then {T08, T10, T11}. Always confirm with
`python scripts/check_scope.py --overlap ...`.

Gate: each task reviewed (trigger A), each merge reviewed if dev moved (trigger B), phase review
(trigger C). Tag `phase-2`.

## Phase 3: joining the lanes (max 2 at once; every task has "Joins lanes: yes")

| Task | Title | Depends on | Requirement | Can run with |
|---|---|---|---|---|
| T13 | Recommendations page | T07, T10, T11 | FP-CAN-2 | T14 |
| T14 | Apply with confirm screen, my applications, statuses | T08, T10 | FP-CAN-3 | T13 |
| T15 | Employer applicants list and status changes | T11, T14 | FP-EMP-3 | T16 |
| T16 | Booking: eligibility, bookable slots, confirm, book | T12, T14, T-BRIEF | FP-SCHED-2 | T15 |
| T17 | Booking conflict contract and concurrency | T16 | FP-SCHED-3 | T18 |
| T18 | Activity log page and Today page widgets | T14 | Keystone governance | T17 |
| T06 | Authorization sweep: other user's id and missing id on every route | T10, T15, T16 | FP-AUTH-3 | T17, T18 |

T06 only writes tests. Any hole it finds becomes a bug card `Bxx`, fixed by the owner of that file.

Gate: every FP test passes and none is skipped; phase review clean. Tag `phase-3`.

## Phase 4: delivery

| Task | Title | Depends on | Can run with |
|---|---|---|---|
| T19 | Seed demo data and reset command | phase 3 | T20 |
| T20 | Dockerfile, wsgi, start-up | phase 3 | T19 |
| T21 | README, SPEC.md, INSTALL.md | T19, T20 | none |

Gate: `python scripts/check.py --release`, fresh-clone Docker run, Kevin signs in as each demo
user. Merge to `main`. Tag `phase-4` and `release-1`.

## Phase 5: hardening

| Task | Title | Depends on |
|---|---|---|
| T22 | Self-audit: three reviewers per area, judge confirms, bug cards for each confirmed bug | phase 4 |

Then every confirmed bug becomes `Bxx` via `/bugfix`. Gate: no open confirmed bugs. Tag `phase-5`.

## Special cards

| Card | When | Runs |
|---|---|---|
| T-BRIEF | as soon as `docs/BRIEF.md` is filled | alone, docs only |
| CCxx | contract change request | alone |
| Bxx | bug fix | normal, by ownership |
| TEMPLATE | copy to make a new card | never |
