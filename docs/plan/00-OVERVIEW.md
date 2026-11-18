# 00 · Overview: read this first

## What we are building

**Keystone** is a job platform with two kinds of users:

- **Candidates** build a profile with skills and a private resume, see jobs ranked by how well they
  match, apply, and book an interview slot.
- **Employers** build a company profile, post jobs, see applicants, and offer interview slots.

It is the web-only cut of the Keystone design canvas. Its look (navy and blue, IBM Plex, clean
cards) comes from that canvas. Its required behaviour comes from the course brief.

**Keystone's core idea, kept in this build:** the system proposes, a person decides. Nothing
consequential happens without a clear confirm screen, and important actions are written to an
audit log.

## What is graded (from the repo template)

| Area | Requirement IDs | Plan file |
|---|---|---|
| Accounts and sessions | FP-AUTH-1, FP-AUTH-2, FP-AUTH-3 | `04-AUTH-SECURITY.md` |
| Candidate workflows | FP-CAN-1, FP-CAN-2, FP-CAN-3 | `05-UX-FLOWS.md` |
| Employer workflows | FP-EMP-1, FP-EMP-2, FP-EMP-3 | `05-UX-FLOWS.md` |
| Matching | FP-MATCH-1 | `02-ARCHITECTURE.md`, task T11 |
| Scheduling | FP-SCHED-1, FP-SCHED-2, FP-SCHED-3 | `03-DATA-MODEL.md`, tasks T12, T16, T17 |
| Docs and delivery | README mapping, SPEC.md, INSTALL.md, Dockerfile | tasks T19 to T21 |
| Cross-team audit (Week 12) | security, functional, performance bugs found by other teams | `10-REVIEW-PROTOCOL.md`, phase 5 |

`01-REQUIREMENTS.md` has the full list and which ones are still **BLOCKED** on the brief.

## Not in this build

Phone screens, browser extension, email, team chat, Keystone staff console, agent-to-agent
Handshake, mock interviews, offers and negotiation. These were cut from the canvas. Do not build
them, even partly.

## How to read the plan

| File | What it holds | Who reads it |
|---|---|---|
| `00-OVERVIEW.md` | this page | everyone, once |
| `01-REQUIREMENTS.md` | every FP-* requirement, its rule source, its tests | orchestrator, test writers |
| `02-ARCHITECTURE.md` | folders, modules, request and data flow | everyone, once |
| `03-DATA-MODEL.md` | the exact SQL schema | tasks that touch data |
| `04-AUTH-SECURITY.md` | auth design and the security checklist | auth tasks, every reviewer |
| `05-UX-FLOWS.md` | screens, routes and user journeys per role | UI tasks |
| `06-DESIGN-SYSTEM.md` | colors, type, spacing, components | UI tasks |
| `07-CONTRACTS.md` | **frozen** names: routes, functions, templates, tables | everyone, every task |
| `08-TASKS.md` | phases, task order, parallel lanes, dependencies | orchestrator |
| `09-AGENT-WORKFLOW.md` | how agents are dispatched, isolated and merged | orchestrator |
| `10-REVIEW-PROTOCOL.md` | 3 reviewers + 1 judge | orchestrator, reviewers |
| `11-TESTING.md` | test rules, fixtures, requirement-test mapping | everyone |
| `12-DEPLOY.md` | Docker, waitress, demo data | delivery tasks |

## Phases

| Phase | Goal | Runs | Gate |
|---|---|---|---|
| 0 | Tooling: the gate command works | 1 agent | `python scripts/check.py` passes on an empty app |
| 1 | Foundation: app, database, security, layout, auth | 1 agent at a time | Phase review clean, FP-AUTH-1 and 2 tests pass |
| 2 | Core features in 4 parallel lanes | up to 3 agents at once | Each task reviewed, phase review clean |
| 3 | Features that join lanes together | up to 2 at once | Merge reviews clean, all FP tests pass |
| 4 | Delivery: seed data, Docker, docs | 1 to 2 at once | Fresh clone builds and runs from README |
| 5 | Hardening: self-audit like Week 12 | review agents only | No confirmed bugs left open |

## The one rule that matters most

**One task, one agent, one worktree, one fresh context.** A flash model loses track in long
sessions. Small task cards and fresh sessions keep every agent working at its best.
