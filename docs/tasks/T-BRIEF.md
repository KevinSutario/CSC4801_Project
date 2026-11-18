# T-BRIEF · Fill rules from the course brief

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| any | docs | `docs/BRIEF.md` filled by Kevin | no | BLOCKED until docs/BRIEF.md has the brief |

## Goal
Copy every business rule the app needs from the brief into the plan, word for word, so no later
agent has to guess. Docs only. No code.

## Requirement
All FP-* ids.

## Owns
- `docs/plan/01-REQUIREMENTS.md`
- `docs/tasks/T05.md`
- `docs/tasks/T06.md`
- `docs/tasks/T07.md`
- `docs/tasks/T08.md`
- `docs/tasks/T09.md`
- `docs/tasks/T10.md`
- `docs/tasks/T11.md`
- `docs/tasks/T12.md`
- `docs/tasks/T13.md`
- `docs/tasks/T14.md`
- `docs/tasks/T15.md`
- `docs/tasks/T16.md`
- `docs/tasks/T17.md`

## May read
- `CLAUDE.md`
- `docs/BRIEF.md`
- every file listed under Owns

## Steps
1. Read `docs/BRIEF.md` fully. List every requirement id it defines.
2. In `01-REQUIREMENTS.md`, for each FP-* row: add a "Rule text" block under the table section,
   quoting the brief exactly, with the brief's section name. Answer each "Open questions" item with a
   quote, or write `NOT IN BRIEF`.
3. For FP-MATCH-1 and FP-SCHED-1 to 3: copy every worked example from the brief exactly (inputs and
   expected outputs) into the matching task card under `## Requirement`.
4. In each task card listed under Owns: replace every "(from the brief)" placeholder with the quoted
   rule. If a rule is `NOT IN BRIEF`, write the default already in the card and mark it
   `DEFAULT (not in brief)`.
5. If the brief has a requirement that no card covers: do not invent a card. List it under
   OPEN QUESTIONS in your reply.
6. Set Status to READY on every card whose rules are now complete. Leave BLOCKED where a rule the
   card needs is still missing, with the reason.

## Done when
- Every FP-* row has rule text or `NOT IN BRIEF`.
- No card still says "(from the brief)" without a quote or a DEFAULT mark.
- `python scripts/check_scope.py T-BRIEF` passes.

## Pitfalls
- Never paraphrase a rule. Quote it. A paraphrase is how a requirement gets silently changed.
- Do not change any card's Owns, Contract or test names.
