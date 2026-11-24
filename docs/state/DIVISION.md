# Division of labour — three people

Three owners, each building their own lane (by hand or with any AI assistant — Claude, Cursor,
Copilot). One of them (**P2**) is also the **integration lead**: the only one who merges to `dev` and
writes shared state. Business rules still come only from `docs/BRIEF.md`; the file-ownership and
workflow rules in `AGENTS.md` and `docs/plan/09-AGENT-WORKFLOW.md` still apply unchanged.

## The three people

| Person | Lane (theme) | Owns, across the whole project |
|---|---|---|
| **P1 — Candidate experience & docs** | everything a candidate sees + final docs | profile, resume, recommendations, apply, README/SPEC/INSTALL |
| **P2 — Employer, auth/security & integration lead** | employer side + the security spine + merging | security module, auth, company, jobs, applicants, authz sweep, Docker; also owns `dev`, STATUS/JOURNAL/DECISIONS, phase gates and the current contract fix |
| **P3 — Platform core, matching & scheduling** | the shared skeleton + the pure logic | app skeleton/schema, test harness, matching engine, time/slots, booking + conflict, seed data |

Why this cut: it follows the lanes already in `08-TASKS.md` (CAN / EMP / MATCH+SCHED), keeps each
file with one owner so the "Owns lists never overlap" rule is never broken when tasks run in
parallel, and puts the three shared-but-sequential Phase-1 tasks on whoever owns that spine.

## Who owns which task card

| Task | Title | Owner | Phase |
|---|---|---|---|
| CC01 | contract-change fix (in progress) | **P2** | pre-2 |
| T01 | app skeleton, config, db, schema, errors, stubs | **P3** | 1 |
| T02 | security module + audit log | **P2** | 1 |
| T03 | design tokens, layout, components, landing | **P1** | 1 |
| T04 | test harness: fixtures, factories, placeholders | **P3** | 1 |
| T05 | register, sign in, sign out, safe redirects | **P2** | 1 |
| T07 | candidate profile & skills, candidate home | **P1** | 2 |
| T08 | resume upload/list/delete/download | **P1** | 2 |
| T09 | company profile, employer home | **P2** | 2 |
| T10 | jobs: create/edit/close/delete/detail | **P2** | 2 |
| T11 | matching engine + skill normalisation | **P3** | 2 |
| T12 | time-zone helpers + interview slots | **P3** | 2 |
| T13 | recommendations page | **P1** | 3 |
| T14 | apply + confirm screen, my applications | **P1** | 3 |
| T15 | employer applicants list + status changes | **P2** | 3 |
| T16 | booking: eligibility, slots, confirm, book | **P3** | 3 |
| T17 | booking conflict + concurrency | **P3** | 3 |
| T06 | authorization sweep (FP-AUTH-3) | **P2** | 3 |
| T19 | seed demo data + reset command | **P3** | 4 |
| T20 | Dockerfile, wsgi, start-up | **P2** | 4 |
| T21 | README, SPEC.md, INSTALL.md | **P1** | 4 |
| T22 | self-audit (review agents only) | all three | 5 |
| CC02 | resume_files schema + CV-file contracts | **P2** | 6 |
| T23 | candidate CV file upload (alongside text) | **P1** | 6 |
| T24 | employer views own applicant's CV (ungraded) | **P2** | 6 |
| T25 | seed a demo CV file | **P3** | 6 |

Totals: P1 = 8 cards, P2 = 8 cards + CC01 + CC02, P3 = 8 cards. Balanced.

## Phase 6 — CV file + employer resume view (added 2026-11-24, D23)
New post-submission requirements (CV file input; a place for employers to see submissions). The
chain is strictly ordered because of the schema freeze and the service dependency:

**CC02 (P2)** first — unfreezes `schema.sql`/contracts just long enough to add the `resume_files`
table and register the T23/T24 names, then re-freezes. **T23 (P1)** builds the candidate upload,
owner-only download and replace/remove on `resume_service.py` + its routes/template. Then two can run
in parallel: **T24 (P2)** adds the employer "View CV" link scoped to its own applicants (ungraded),
and **T25 (P3)** seeds a demo CV through the real `save_resume_file`. Grading note: the direct
resume URL stays owner-only/403 (graded); the employer view is encouraged but ungraded and not a
valid audit finding. Owns lists do not overlap (P1 = candidates/*, P2 = applications/* + the CC
files, P3 = seed).

## Phase by phase

**Phase 1 — foundation (one card at a time, no parallel work).** The order is fixed by dependencies:
T01 (P3) → T02 (P2) → T03 (P1) → T04 (P3) → T05 (P2). Everyone waits on this spine. After it merges,
the shared files (`app/__init__.py`, `app/db.py`, `app/schema.sql`, `app/errors.py`,
`app/security.py`, `app/audit.py`, `base.html`, `components/*`, `tests/conftest.py`) are **frozen** —
only a contract-change card (a CCxx, run by P2) may touch them again.

**Blocker right now:** CC01 (P2) is FIXING. Per STATUS.md nothing else runs until it merges. So the
first real parallel work can't start until P2 lands CC01 and Phase 1 finishes.

**Phase 2 — three lanes at once (the max is 3 agents).** Run in two batches, confirming scope first
with `python scripts/check_scope.py --overlap <ids>`:

- Batch 1: **T07 (P1)**, **T09 (P2)**, **T12 (P3)** — no shared files.
- Batch 2: **T08 (P1)**, **T10 (P2)**, **T11 (P3)** — no shared files.

Each person builds their own card on their own `task/Txx` branch and runs the gate before handing off.

**Phase 3 — joining the lanes (max 2 at once).** These cards cross lanes, so coordinate ordering:

- **T14 (P1)** and **T15 (P2)** depend on apply/jobs landing; T15 also needs T11.
- **T13 (P1)** needs T07+T10+T11. **T16 (P3)** needs T12+T14. **T17 (P3)** hardens T16.
- **T06 (P2)** is the authz sweep and goes last (needs T10, T15, T16).

Safe parallel pairs (non-overlapping files): T15 (P2) ∥ T16 (P3); T13 (P1) ∥ T16/T17 (P3).
T13 and T14 are both P1, so P1 runs them back to back. T06 writes only tests; any hole it finds
becomes a `Bxx` bug card fixed by the owner of that file. (T18 was descoped, D22.)

**Phase 4 — delivery.** T19 (P3) and T20 (P2) run together, then T21 (P1, the docs) after both.

**Phase 5 — hardening.** T22. All three act as reviewers across each other's areas; P2 (integration
lead) confirms each finding and opens a `Bxx` card for every confirmed bug.

## Integration lead (P2) — the shared duties

Everyone owns their own lane, but `dev` and shared state must have **one** writer, so P2 holds these:

- Owns `dev`. Merges each reviewed task branch straight onto `dev` with `git merge --no-ff` and runs
  `python scripts/check.py` after every merge. No `int/` branch, no separate merge review.
- Sole writer of `docs/state/*` (STATUS, DECISIONS) and `reviews/*`.
- Runs the phase gates and tags (`phase-1` … `release-1`).
- Handles contract-change cards (CCxx), including the current CC01.

P1 and P3 build on their own `task/Txx` branches off `dev`, run the gate and `check_scope.py`
themselves, then hand the branch to P2 for review + merge. They never write `docs/state/*`.

## Hand-off checklist (every person, every card)

1. `git switch -c task/Txx dev` and work on that branch (a worktree is optional).
2. Change only files in the card's **Owns** list. `python scripts/check_scope.py Txx` must print OK.
3. Write the failing test first for any logic, then the code (AGENTS.md rule 9).
4. `python scripts/check.py` must print CHECK PASSED — paste the output in the hand-off.
5. Hand the branch + the AGENTS.md reply block to a reviewer, then P2 merges. Do not merge yourself.

## Open coordination notes

- D16 (display name editable) and D18 (no closed job state) are still awaiting Kevin's confirm per
  STATUS.md — resolve before T10/T13 reach their closed-job branches.
- T06, T10, T13, T15, T16, T17 carry BLOCKED/decision notes in their cards; P2 clears each decision
  against `07-CONTRACTS.md` / the brief before that card is dispatched.

