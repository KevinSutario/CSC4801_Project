# GitHub Copilot instructions

The project rules live in **[AGENTS.md](../AGENTS.md)** at the repo root — one canonical, tool-neutral
file for everyone. Read it before suggesting or editing code.

Key points Copilot must respect (full detail in AGENTS.md):

- Only change files in the current task card's "Owns" list (`docs/tasks/`). Scope is enforced by
  `python scripts/check_scope.py <task-id>`.
- Stack is fixed: Python 3.12, Flask 3.1, Jinja2, stdlib `sqlite3`, pytest. No ORM, no JS framework,
  no new dependencies beyond `requirements.lock` / `requirements-dev.txt`.
- Never invent functions, routes, columns or Flask APIs; names are frozen in
  `docs/plan/07-CONTRACTS.md`. Business rules come only from `docs/BRIEF.md`.
- Logic (matching, scheduling, auth) is test-first. Never weaken, skip or delete a test.
- The gate is `python scripts/check.py`; it must pass before anything is called done.

Do not duplicate rules here — edit `AGENTS.md`.
