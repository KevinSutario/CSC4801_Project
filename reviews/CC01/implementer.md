TASK: CC01
FILES CHANGED: docs/plan/01-REQUIREMENTS.md, 02-ARCHITECTURE.md, 03-DATA-MODEL.md, 04-AUTH-SECURITY.md, 05-UX-FLOWS.md, 07-CONTRACTS.md, 11-TESTING.md, 12-DEPLOY.md; scripts/contracts.json; docs/tasks/T01, T04, T05, T06, T07, T08 (rewritten), T09, T10 (rewritten), T11, T12 (rewritten), T13, T14 (rewritten), T15 (rewritten), T16 (rewritten), T17 (rewritten), T19 (rewritten), T21.
Commit 7e800bd on task/CC01.
TESTS ADDED: none (docs-only). Test names assigned: test_db.py::test_fp_sec_4_tests_use_isolated_database (T01), test_auth.py::test_fp_sec_2_sql_metacharacters_stay_bound (T05), test_emp_company.py::test_fp_sec_3_script_tag_is_escaped (T09), test_authz_sweep.py::test_fp_sec_1_object_access_boundaries (T06).
CHECK OUTPUT: lint All checks passed; 41 passed; contracts skipped (no app/); CHECK PASSED
SCOPE CHECK: SCOPE OK for CC01
Step 2: 03-DATA-MODEL SQL block executes cleanly in sqlite3 :memory: (12 tables; indexes uq_application, uq_booking_application, ix_jobs_company, ix_applications_job, ix_applications_candidate, ix_slots_employer, ix_audit_actor).
Step 3: contracts.json parses; T08/T10/T12 names and endpoints updated; every task key kept.
Step 7 grep: only SQLite `ON CONFLICT(...) DO UPDATE` hits remain (T07, T08, T09); no card says BLOCKED.
STATUS: done
OPEN QUESTIONS:
1. T14 "Depends on" still lists T08; that dependency existed only for the resume select. Could be dropped.
2. Empty-state text "No open jobs right now. Check back soon." became "No jobs right now. Check back soon." (D18).
3. T12's slots page is reached from the employer home (T09's template). T09 Step 4 needs a one-line link to /employer/slots; orchestrator's call.
JOURNAL:
- Applied D9 to D18 across 8 plan files, contracts.json and 17 cards: 403/404 split, raw-text owner-only resume, four lower-case statuses with apply-once-ever, 409 job delete with count_dependants, employer-owned 30-minute slots with uq_booking_application and make_booking, exact "Slot already booked" contract, integer-arithmetic score and tie-breakers, editable display name, D17 seed minimum with five accounts, no closed job state (is_open and list_open_jobs gone), FP-SEC tests assigned.
- Decisions not in the card: a Conflict message for delete_job; Forbidden-before-NotFound ordering in T08's get_resume_for_viewer; UPLOAD_DIR/MAX_UPLOAD_MB marked "unused since CC01" in three places; T19 computes seed slot dates relative to today so they stay future.
- Surprising: the step 7 grep for CONFLICT also matches SQLite's ON CONFLICT keyword; left as code.
- Out of scope noticed: T14 still depends on T08 for a reason that no longer exists; T09's employer home needs a link to /employer/slots.

--- FIX ROUND 1 (verdict items 1 to 26) ---
Commit 96b0fcf on task/CC01. CHECK PASSED (41 passed); SCOPE OK for CC01. 6 plan files and 13 cards changed (158 insertions, 72 deletions).
Decisions not spelled out: cover-note rule added to 07-CONTRACTS too; csrf_field rule in 07 under errors.py plus per-card sentence and test bullet; confirm_status GET with bad `to` is 400 via errors/400.html (DEFAULT); 03-DATA-MODEL legend reworded for the DEFAULT marker.
D17 third job "Logistics Coordinator" (SQL, Excel) added to 12-DEPLOY and T19.
JOURNAL (fix round): applied all actionable verdict items; T15 bad-status example changed from `hired` to `bogus` to keep the step-7 grep clean; 01-REQUIREMENTS and 11-TESTING needed no change.
