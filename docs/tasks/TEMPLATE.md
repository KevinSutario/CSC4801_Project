# Txx · <title>

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| n | <lane> | <task ids> | no | READY |

## Goal
<Two or three sentences. What is true when this is done.>

## Requirement
<FP-* ids. Rule text copied from docs/BRIEF.md with its section name. If any rule is missing:
Status is BLOCKED and the agent stops.>

## Owns
- `<path the agent may create or change>`

## May read
- `CLAUDE.md`
- `docs/plan/07-CONTRACTS.md` (section: <name>)
- `<other files>`

## Contract
<Copy the exact signatures, routes and templates this task builds, from 07-CONTRACTS.md.>

## Steps
1. <small, checkable step>

## Tests
- `<file>::<test name>`: <what it proves>

## Done when
- `python scripts/check.py` passes
- `python scripts/check_scope.py Txx` passes
- <task-specific checks>

## Pitfalls
- <known traps>
