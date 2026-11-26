# Locked decisions

An agent may not change these. If one looks wrong, stop and report.

## D1: Stack is Flask + SQLite + Jinja + pytest
- Chosen: the course template stack, server-rendered forms, no ORM, no JavaScript framework.
- Rejected: Next.js + Postgres (Kevin's usual stack). Would replace the template, Dockerfile and test
  layout, and gives a flash model more APIs to invent.
- Consequence: no new dependencies beyond `requirements.lock` and `requirements-dev.txt`.

## D2: Business rules come only from docs/BRIEF.md
- Chosen: rules are quoted from the brief. Tasks needing a missing rule are BLOCKED.
- Consequence: matching (T11), booking (T16, T17) cannot start until the brief is pasted.

## D3: Missing and not-yours objects both return 404
- Chosen: 404 for both, so ids cannot be probed, unless the brief says 403.

## D4: Shared files frozen after Phase 1
- Files: `app/__init__.py`, `app/db.py`, `app/schema.sql`, `app/errors.py`, `app/security.py`,
  `app/audit.py`, `app/templates/base.html`, `app/templates/components/*`, `tests/conftest.py`.
- Changed only through a contract change request card (CCxx).

## D5: Tests split per task file, template test names kept
- Template files `tests/unit/test_workflows.py` and `test_scheduling.py` are replaced by per-task
  files (T04), so parallel lanes never edit the same file. Every template test name is kept exactly.

## D6: Web-only scope
- Phone screens, extension, email, team chat, Keystone console, Handshake, mock interviews, offers and
  negotiation are out of scope.

## D7: FP-AUTH-3 tested as a Phase 3 sweep (T06)
- It needs real objects from every feature, so it is tested after they exist, across every route.

## D8: Matching engine (T11) is pure; its database service is T13's
- So T11 can run in Phase 2 in parallel with jobs (T10) without depending on it.

## D9: Another user's object is 403, a missing object is 404 (replaces D3)
- Source: brief FP-AUTH-3 ("authenticated user with the wrong role or owner: `403 Forbidden`"; "missing
  object that the caller would otherwise be allowed to access: `404 Not Found`"), repeated in FP-CAN-1
  and FP-EMP-2. Decided by Kevin 2026-11-10.
- Consequence: every ownership helper raises `Forbidden` for someone else's row and `NotFound` for a
  missing row. Applied by CC01 to the plan and cards T06, T08, T10, T12, T14, T15, T16.

## D10: The resume is raw text, one per candidate, owner-only
- Source: brief FP-CAN-1 (raw-text resume the owner can view and replace; PDF optional; any other
  candidate or employer gets 403). Decided by Kevin 2026-11-10.
- Consequence: `resumes(owner_id PK, body, updated_at)`; no file upload; no employer access; T08
  rewritten; `applications.resume_id` removed. `UPLOAD_DIR` and `MAX_UPLOAD_MB` stay in config, unused.
  Resume length limit 20000 chars is DEFAULT (not in brief).

## D11: Four statuses, any change allowed, apply once ever
- Source: brief FP-EMP-3 (exactly `Pending`, `Interviewing`, `Rejected`, `Accepted`), FP-CAN-3 (apply
  once; duplicate rejected without a row). Decided by Kevin 2026-11-10.
- Stored lower-case (`pending`, `interviewing`, `rejected`, `accepted`), labels in the brief's
  spelling. No transition rules (not in brief): the owner may set any status other than the current
  one. Unique index `uq_application (job_id, candidate_id)` with no WHERE clause. Re-applying after a
  rejection is refused.

## D12: Job delete with dependants is 409 and changes nothing; empty skills list allowed
- Source: brief FP-EMP-2. Decided by Kevin 2026-11-10.
- Consequence: `applications.job_id ON DELETE RESTRICT`; `delete_job` raises `Conflict` when the job
  has any application. Slots are employer-owned (D13), so applications and their bookings are a job's
  only dependants. Skills 0 to 30 (30 is DEFAULT).

## D13: Slots belong to the employer, last exactly 30 minutes, lie in the future; one booking per application
- Source: brief FP-SCHED-1 ("future, 30-minute availability slots"; "one owner"), FP-SCHED-2 ("the
  slot belongs to the employer for the candidate's application"; "the application has no existing
  booking"). Decided by Kevin 2026-11-10.
- Consequence: `interview_slots` loses `job_id`; slots page at `/employer/slots`; `create_slot` has no
  `job_id`; duration must be exactly 30 minutes ("exactly" is the decided reading of the brief's
  "30-minute"); `uq_booking_application` added. Overlap ban for one employer's own slots and 409 for
  deleting a booked slot are DEFAULT (not in brief).

## D14: Booking conflict contract
- Source: brief FP-SCHED-3. `Conflict("Slot already booked")`, HTTP 409, exactly one booking row,
  enforced by `BEGIN IMMEDIATE` plus `bookings.slot_id UNIQUE`. Losing user sees the booking page
  re-rendered with the message (DEFAULT). Same candidate booking twice is refused as ineligible
  (`Forbidden`) by the no-existing-booking condition.

## D15: Matching score and tie-breakers exactly as the brief
- Source: brief FP-MATCH-1. `score = 100` when the job has no required skills, else
  `floor(100 * |C ∩ R| / |R|)` as an int; dashboard ties by case-insensitive title then job id;
  applicant ties by case-insensitive display name then candidate id. The four worked examples are
  unit tests and seed data.

## D16: Candidate display name is editable in the profile
- Source: brief FP-CAN-1 ("edit only their own profile, including a display name"). Gap found by
  T-BRIEF. `save_profile` gains `display_name`; 1 to 80 chars is DEFAULT.

## D17: Seed data satisfies FP-DOC-3 with five accounts
- Three candidates (Python+SQL, Python, Rust) and two employers; "Data Analyst" requires Python and
  SQL, "Logistics Coordinator" requires SQL and Excel, "Graduate Trainee" requires nothing, so the four
  FP-MATCH-1 examples appear and "two jobs with required skills" holds on a literal reading (added
  2026-11-13 after the CC01 judge marked it UNCLEAR; Kevin to confirm); applications in all four
  statuses; two `interviewing` candidates eligible for the same unbooked slot.

## D18: Things kept as DEFAULT (not in brief)
- Password rules, email format, session lifetime, field length limits, slot overlap policy, display
  timezone, HTTP code for deleting a booked slot. Roles stored `candidate`/`employer`, shown
  `Candidate`/`Employer`.
- No open/closed or accepting state for jobs. The brief's FP-EMP-2 has create, view, edit and
  delete only, and FP-CAN-2 lists "all current (not deleted) jobs", so jobs carry no status flag:
  `jobs.is_open` and `jobs.accepting_applications` are both absent from the schema, contracts,
  factories and cards. Every job that exists is current, listable and applyable.
- History: a "stop/resume accepting applications" toggle (`accepting_applications` + a confirm
  action, apply → 409 when stopped) was briefly decided on 2026-11-19 then **deferred** the same day
  (Kevin): it is outside the brief, so ungraded and not audited, and with one week left the T10/T14
  effort goes to graded requirements instead. Revisit post-submission if the real workflow wants it.
- `normalise_skill` implements the brief's rule from T01 onward (strip, lower-case, nothing else; no
  collapsing of inner spaces), so no row ever needs re-normalising.
- Also noted: the FP-SEC-1 to FP-SEC-4 unit tests are assigned by CC01 to T06, T05, T09 and T01.

## D19: Process: T-BRIEF merged with four minor doc leftovers carried into CC01
- The T-BRIEF re-check verdict (reviews/T-BRIEF/verdict-2.md) confirmed four minor label
  inconsistencies on T12, T13, T15 and T17, each of which CC01 rewrites in full, and recommended
  merging. A second T-BRIEF fix round would edit sentences CC01 replaces hours later. Orchestrator
  decision 2026-11-12: merge b1aa462, run CC01 immediately, dispatch no phase-2 card before CC01 merges.
- Also: dev moved under T-BRIEF only by orchestrator state commits (docs/state, reviews, CC01 card),
  not by another agent's work, so no merge review (trigger B) was run for it. The same rule applies
  to later tasks whose only dev drift is orchestrator state commits.

## D20: Process slimmed for a 3-person team (2026-11-19)
- Chosen by Kevin: the engineering process was too heavy for three real people. Kept the cheap,
  high-value guards; dropped the swarm-era ceremony.
- **Kept**: one branch per task, non-overlapping Owns + `check_scope.py`, `check.py` gate, Phase 1
  serial + shared-file freeze (D4), contracts frozen, test-first for logic (matching/scheduling/auth).
- **Dropped/changed**: three-reviewers-plus-judge → one non-author peer review, light or careful by
  card type (`10-REVIEW-PROTOCOL.md`); `int/Txx` branch and separate merge review → merge straight
  onto `dev`; six-state machine → TODO/DOING/MERGED/BLOCKED; JOURNAL.md and BUGS.md retired (git log +
  STATUS cover them; a bug is a new Bxx card); worktrees now optional.
- **Roles**: three lane owners (P1/P2/P3 in `docs/state/DIVISION.md`); P2 is integration lead (sole
  merger of `dev`, sole writer of `docs/state/*`). Agents are optional helpers, not teammates.
- **Files changed**: `CLAUDE.md`, `docs/plan/09-AGENT-WORKFLOW.md`, `docs/plan/10-REVIEW-PROTOCOL.md`,
  `docs/state/STATUS.md`. Old versions remain in git history.
- Reversible: revert this commit to restore the full protocol.

## D21: Scope confirmed to the brief only (2026-11-19, 1-week timeline)
- Timeline dropped from ~2 months to 1 week. Kevin reviewed the plan against the brief and confirmed
  the scope is exactly the brief's graded requirements — no extra features.
- Confirmed to KEEP (all brief MUSTs): accounts/auth (FP-AUTH-1/2/3), candidate profile + skills +
  raw-text resume (FP-CAN-1), recommendations + match score (FP-CAN-2, FP-MATCH-1), apply + tracker
  (FP-CAN-3), company profile (FP-EMP-1), job posting (FP-EMP-2), applicants + accept/reject
  (FP-EMP-3), interview slots + booking + atomic conflict (FP-SCHED-1/2/3), docs/Docker/seed
  (FP-DOC-1/2/3, FP-SUB-1). "Role fit" = the match score. Booking kept at minimal (not polished).
- Confirmed to DROP: job search (never in brief, ungraded — not built); the stop/resume toggle
  (D18, deferred); the activity log + Today dashboard (D22).
- Rationale: grading is requirements (10) + cross-team audit (30); a non-brief feature earns nothing
  and still costs build + audit-surface time. Spend the week on brief MUSTs.

## D22: Activity log + Today dashboard descoped (2026-11-19)
- T18 (activity-log viewer page + Today-page dashboard widgets) is cut for this submission. Neither
  is in the brief, so both are ungraded and not audited.
- The `audit_log` table and `audit.log_event` STAY — features still write audit rows (FP-SEC-ish,
  and it is cheap); only the *viewer page* and the dashboard widgets are removed.
- The candidate home (`/candidate/`, `candidates.today`) stays as a plain landing page (welcome +
  links), built by T07. `core.index` still redirects signed-in candidates there.
- Effects: T18 card marked DESCOPED (kept for history); `app/activity/*` dropped from T01's
  blueprints; `activity.list` + `tests/unit/test_activity.py` removed from contracts and T04; T18
  removed from the Phase-3 map and the P1 lane; T17 and T06 no longer list T18 as a parallel peer.
- Reversible: T18.md retains the full spec; re-add the blueprint and route to restore it.

## D23: CV file upload + employer resume view (2026-11-24, Phase 6)
- New requirements from Kevin + the 2026-11-24 course clarification: candidates get a real CV **file**
  input, and employers get a place to see submissions. This **adds** to, and does not replace, the
  D10 raw-text resume.
- Graded vs ungraded (from the clarification): the **direct** resume URL/API stays owner-only, 403 for
  everyone else — graded (FP-CAN-1). Employers viewing an applicant's resume is **encouraged but
  ungraded** and is not a valid peer-audit finding. The FP-EMP-3 fields (identity, skills, score,
  status, booking) are graded and already shipped in T15 — unchanged.
- Decisions: (a) CV file is **additive** alongside the text resume; (b) **one PDF per candidate**,
  stored **on disk** under the already-wired `UPLOAD_DIR`, metadata in a new `resume_files` table,
  size ≤ `MAX_UPLOAD_MB` (2); (c) reuse the existing **`resume.update`** audit action so the frozen
  `audit.py` is untouched; (d) the candidate's direct download route is owner-only (403 before
  existence, like `resume_view`); the employer view is a **separate** `/employer/...` route scoped to
  the employer's own job's applicants (T24).
- Cards: **CC02** (P2) adds the table + contracts (schema is frozen, so it must be a CC card);
  **T23** (P1) builds the candidate upload/download; **T24** (P2) adds the employer view link;
  **T25** (P3) seeds a demo CV. Order: CC02 → T23 → {T24, T25}.
- Reversible: the text resume and all graded behaviour are untouched; dropping T23/T24 leaves the
  brief MUSTs intact.

## D24 · Interview notes and meeting links (2026-11-26, Phase 6)

- CC03 adds one optional plain-text note per employer-owned slot. Its startup upgrade adds the
  column in place so existing slots and bookings keep their IDs, times, and relationships.
- T27 shows the candidate the note after booking and makes it available in the owning employer's
  booking views. Standalone HTTPS URLs with a valid host and no embedded credentials render as
  Join interview links. Other note lines render as escaped text.
- P2 authorized merging CC03 before T27 without waiting for a non-author peer review. Both scope
  checks passed, and the combined changes passed the release gate.
