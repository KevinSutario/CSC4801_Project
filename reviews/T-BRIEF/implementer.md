TASK: T-BRIEF
FILES CHANGED:
- docs/plan/01-REQUIREMENTS.md
- docs/tasks/T05.md through T17.md (all thirteen)
TESTS ADDED: none (docs-only card)
CHECK OUTPUT:
=== lint: ruff check .
All checks passed!
=== tests: pytest tests/unit -q -rs -p no:cacheprovider
41 passed in 14.61s
=== contracts: skipped (no app/ folder yet)
CHECK PASSED
SCOPE CHECK: SCOPE OK for T-BRIEF
COMMIT: 47701ca on task/T-BRIEF ("T-BRIEF: Fill rules from the course brief"), working tree clean.
STATUS: done

Card statuses set:
- READY: T05, T06 (after deps), T07, T09, T10, T11, T12, T13 (after T11), T16, T17
- BLOCKED (rule quoted but the card contradicts it): T08, T14, T15

OPEN QUESTIONS (brief-vs-card conflicts or gaps; Steps, Contracts, Owns and test names unchanged):
1. 403 vs 404 for another user's object. FP-AUTH-3 says 403. T06 default and Steps of T08, T10, T12, T14, T15, T16 raise NotFound (404).
2. Resume (T08). FP-CAN-1 requires a raw-text resume, owner-only, others 403. T08 builds PDF upload with employer download.
3. Application statuses (T14, T15). FP-EMP-3: exactly Pending, Interviewing, Rejected, Accepted. T14 default has five lower-case values.
4. Re-apply (T14). FP-CAN-3: apply once; duplicate rejected without a row, no exception by status. T14 allows re-apply when none pending; unique index may be pending-only.
5. Transitions. NOT IN BRIEF; T14/T15 TRANSITIONS table forbids moves the brief does not.
6. Job delete (T10). FP-EMP-2: with dependants, 409 and nothing changed. T10 cascades.
7. Job skills may be empty (T10). T10 default said 1 to 30.
8. Slot duration (T12). 30-minute slots; T12 default 15 to 240. Brief ties slots to the employer, cards to jobs.
9. Applicant order and fields (T15). Brief ties: case-insensitive display name then candidate id; rows show identity, skills, score, status, booking.
10. Display name edit (T07 GAP). FP-CAN-1 profile includes a display name; no card lets a candidate edit it.
11. T16 needs the uq_booking_application index (application has no existing booking).
12. Role spelling: brief Candidate/Employer; contracts store lowercase.
13. Requirements with no card: FP-SEC-1 to 4 each demand a named unit test; FP-SEC-2 and FP-SEC-3 have no owning test. FP-ARCH-1, FP-PROC-1, FP-DOC-1/2/3, FP-TEST-1, FP-SUB-1 quoted under non-functional with suggested tasks. FP-DOC-3 seed list matters for T19.
14. Closed jobs do not exist in the brief; excluding closed jobs from recommendations is DEFAULT (not in brief).
15. 01-REQUIREMENTS asks for a DECISIONS.md entry when statuses change; orchestrator's file.

JOURNAL:
- Quoted every FP-* rule verbatim with its brief section into 01-REQUIREMENTS.md and into the Requirement section of T05 to T17; answered every open-question bullet with a quote or NOT IN BRIEF; copied the FP-MATCH-1 example table verbatim into T11; added FP-SEC-1..4, FP-DOC-3 and FP-TEST-1 quotes because they mandate tests no card owns.
- Decision not in the card: added a NEEDS DECISION status in 01-REQUIREMENTS and marked T08, T14, T15 BLOCKED, because the brief contradicts their defaults rather than leaving a gap; where a brief rule overrides a default I wrote SUPERSEDED on the card instead of editing Steps/Tests.
- Surprising: the brief disagrees with the plan on six substantive points (403 vs 404, raw-text resume, four title-case statuses, no re-apply, no cascade delete, 30-minute slots); several cards would fail grading as written.
- Out of scope noticed: no card owns the FP-SEC-2 SQL-injection test or the FP-SEC-3 XSS test; README mapping (FP-DOC-2) must cover every requirement id including FP-SEC and FP-DOC ones.
- Files were written with LF; git warns it will convert to CRLF on checkout (autocrlf), diff is content-only.

--- FIX ROUND 1 (verdict items 1 to 10) ---
Commit: b1aa462 "T-BRIEF: Fill rules from the course brief (fix verdict items 1-10)" on task/T-BRIEF.
CHECK PASSED (41 passed); SCOPE OK for T-BRIEF. 10 files changed, 86 insertions, 36 deletions.
Fixes: T10, T16, T13, T07, T06, T17 set BLOCKED (NEEDS DECISION) with quoted reasons; T12 quotes the
FP-SCHED-2 "belongs to the employer" bullet; T15 carries one definitive key list; resume_id and the
/resumes/<id> link relabelled CONFLICT; FP-MATCH-2 quoted in full; T11 collapse-spaces note added.
Also (not in fix list): FP-SCHED-3 row and T13 status set NEEDS DECISION/BLOCKED for consistency.
READY after this round: T05, T09, T11, T12. Everything else waits on CC01.
JOURNAL (fix round):
- Applied verdict items 1-10 by editing 10 Owns files; every status change points at the matching 01-REQUIREMENTS.md row and quotes the brief sentence that causes it.
- Did not open 07-CONTRACTS.md or 03-DATA-MODEL.md (outside May read); the Forbidden proposal for same-candidate-twice is recorded in T17 as a proposal.
- Noted: scripts/check.py runs under Python 3.11 on this machine while CLAUDE.md says 3.12; gate passes.
