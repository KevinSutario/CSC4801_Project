# 10 · Review protocol: one peer reads it

> Slimmed 2026-11-19. Was "three reviewers + a judge" (made for unreliable flash agents). With three
> real people, one careful peer reviewer is enough. The old multi-reviewer text is in git history if
> you ever need it.

## The rule

**Before P2 merges a task into `dev`, one other person (not the author) reads it.** The author never
reviews their own card. Who reviews whom: pick anyone free; usually P2 reviews, except on P2's own
cards, which P1 or P3 reviews.

## How deep

| Card type | Review depth |
|---|---|
| Plain CRUD + templates (T03, T07, T08, T09, T21, docs) | **Light**: read the diff, run `python scripts/check.py`, spot-check one edge case. 5–10 min. |
| High-risk logic (T11 matching, T12/T16/T17 scheduling, T06 authz sweep, T02 security, any CCxx) | **Careful**: the full checklist below, and try to break it with one adversarial test. |
| Bug fix (Bxx) | Confirm the new test fails without the fix and passes with it. |

## Careful-review checklist

1. **Requirement**: does the code do what the card and the brief rule say? Every acceptance item?
2. **Contract**: names, signatures, routes and templates exactly as in `07-CONTRACTS.md`?
3. **Invented things**: every function, method, column, config key and Flask API used actually exists.
4. **Security**: the checklist in `04-AUTH-SECURITY.md` (CSRF, auth/role, ownership, safe redirects).
5. **Edge cases**: empty, whitespace-only, too long, zero, negative, None, wrong type, duplicate,
   someone else's id, missing id, already deleted, timezone and DST.
6. **Transactions**: every write inside `transaction()`? Booking uses `immediate=True`?
7. **Tests**: template test names present? Tests check failure paths? Would a test catch the bug if a
   line were wrong? Any test weakened, skipped or deleted?
8. **Scope**: any change outside the Owns list? `python scripts/check_scope.py Txx` is OK?

## Review note format (save to `reviews/<id>.md`, keep it short)

```
REVIEW: T07   reviewer: P2   depth: light | careful
CHECK: PASSED (paste last line of check.py)
RESULT: PASS | FIX

FINDINGS (only if FIX):
F1  where: app/jobs/service.py:42
    problem: <one sentence>
    proof:   <quoted line, or a failing input>
```

On `FIX`: author fixes the listed findings (failing test first for any logic bug), re-runs
`python scripts/check.py`, and the same reviewer re-checks only those findings. Two rounds max, then
raise it with the team.

## When it joins two lanes (Phase 3)

For cards that connect features (apply→applicants, booking), the reviewer writes **one** test that
walks both features together, e.g. employer posts a job → candidate applies → employer sees the
applicant. That single end-to-end check replaces the old separate "merge review".

## Phase gate (P2)

Before tagging a phase done: all its tasks merged, `python scripts/check.py` passes,
`python scripts/check_contracts.py` passes, and for the phase's requirements confirm each FP-* in
`01-REQUIREMENTS.md` is built and has a test. No separate phase-review packet needed.

## Bugs found later (Week 12 audit, phase 5)

Each confirmed issue becomes a card `docs/tasks/B<n>.md` from `TEMPLATE.md`: failing test first, fix,
then a light re-review by someone other than the fixer.
