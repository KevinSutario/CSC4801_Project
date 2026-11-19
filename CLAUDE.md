# CLAUDE.md

The project rules live in **[AGENTS.md](AGENTS.md)** — one canonical, tool-neutral file for everyone
(people and any AI assistant). Read that at the start of every task.

This file exists only so Claude Code picks the rules up automatically. Do not duplicate rules here;
edit `AGENTS.md` instead.

Claude Code users also have optional helpers in `.claude/` (slash commands like `/dispatch`,
`/review-task`, `/merge`, and the implementer/reviewer agents). They are a convenience, not a
requirement — the workflow in `AGENTS.md` and `docs/plan/09-AGENT-WORKFLOW.md` works with any tool or
none.
