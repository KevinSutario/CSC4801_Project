JUDGE: CC01
RESULT: FIX

| Group | Found by | Category | Severity | Verdict | Proof |
|---|---|---|---|---|---|
| G1 (r1.F1, r2.F1, r3.F3) 02 folder layout stale | 3 | contract | minor | CONFIRMED | 02-ARCHITECTURE.md:28 `candidates/  routes.py service.py`; :33 `applications/ routes.py service.py`; :34 `scheduling/  routes.py service.py` vs 07-CONTRACTS.md:157, :170, :261, :294, :306. Same file's own flows (02:93, :125, :134, :136) use the new names. |
| G2 (r1.F2, r2.F2, r3.F4) jobs columns marked (brief) | 3 | contract | minor | CONFIRMED | 03-DATA-MODEL.md:74, :77, :78 `(brief) ...`; :6 defines (brief) as from docs/BRIEF.md vs 01-REQUIREMENTS.md:142 "Length limits: NOT IN BRIEF" and T10.md:31 DEFAULT. |
| G3 (r1.F3) local_to_utc placed before create_slot | 1 | contract | minor | CONFIRMED | 02:133-134 vs 07:297-299 and T12.md:83. Flow diagram puts conversion in the route; contract and card put it in the service. |
| G4 (r2.F3, r1-p3.F1) book_slot contract silent on past slot | 2 | contract | minor | CONFIRMED | 07:313-316 no outcome for a past slot. T16.md:39, :84 and 11-TESTING.md:60 say Forbidden. Source: CC01.md:201-204. |
| G5 (r3.F1, r1-p2.F1, r1-p4.F3) T06 missing-id 404 vs Forbidden-first resume view | 3 | test-gap | major | CONFIRMED | T06.md:55-56 "right role, missing id (999999): 404" with exemptions only for wrong-role. 07:175-176 and T08.md:64-67 Forbidden first. 04-AUTH-SECURITY.md:32, :38 blanket rule names get_resume_for_viewer. |
| G6 (r3.F2, r1-p4.F2) T06 ownership case on jobs.detail / applications.confirm / applications.submit | 2 | test-gap | major | CONFIRMED | T06.md:49-51, :55-56 vs 07:212 get_job NotFound only; T10.md:71, :111 any user 200; 07:251-254 apply NotFound/Conflict only. |
| G7 (r3.F5) step-7 grep not clean | 1 | scope | minor | CONFIRMED | Three SQL `ON CONFLICT(...) DO UPDATE` hits (T07:59, T08:61, T09:47); CC01.md:334 Done-when not literally met. |
| G8 (r1-p2.F2) 04 error-handler code list omits 405, 409 | 1 | contract | minor | CONFIRMED | 04-AUTH-SECURITY.md:52 vs 05-UX-FLOWS.md:77 and 07:63-64. |
| G9 (r1-p2.F3) Applicants table says "matched skills" | 1 | contract | minor | CONFIRMED | 05:86 vs 05:47-48, BRIEF.md:72, T15.md:63. |
| G10 (r1-p3.F2, r1-p8.F2) is_eligible bool vs raises | 2 | contract | minor | CONFIRMED | 07:308-309 and T16.md:60-61 `-> bool ... owns it` vs T16.md:76-77 get_own_application raises; T16.md:81. Source CC01.md:196-197. |
| G11 (r1-p3.F3) FP-SEC-4 test is order-dependent | 1 | test-gap | minor | CONFIRMED | T01.md:113-116 module-level variable compared in the next test. |
| G12 (r1-p3.F4) seed has one job with non-empty skills | 1 | functional | minor | UNCLEAR | 12-DEPLOY.md:33-34 quotes "two jobs with required skills"; :42-43 Data Analyst (Python, SQL) and Graduate Trainee (none). D17 as decided; BRIEF.md:66 allows an empty list. Kevin's call. |
| G13 (r1-p4.F1) FP-SEC-2 test email fails the card's own email regex | 1 | test-gap | major | CONFIRMED | T05.md:19 regex `^[^@\s]+@[^@\s]+\.[^@\s]+$`; T05.md:79-80 email `x'); DROP TABLE users; --@example.com` has spaces; re.match returns None. Same text CC01.md:300-303. |
| G14 (r1-p4.F4) "remove the skip on these four" with five named tests | 1 | test-gap | minor | CONFIRMED | T05.md:70 vs five bullets; T04.md:72-73 placeholders for every name in the 07 table incl. the "plus" FP-SEC name (07:349). |
| G15 (r1-p5.F1) T10 GET edit / confirm_delete ownership not stated | 1 | security | minor | CONFIRMED | T10.md:82, :84 only for update/delete; Step 9 (:91-97) silent; no employer-B GET test. Mitigated by T10.md:26 and the T06 sweep. |
| G16 (r1-p5.F2) no strip rule / whitespace-only title | 1 | test-gap | minor | CONFIRMED | T10.md:75-76 no strip; :100-101 invalid list lacks whitespace-only; T09.md:47 says strip. BRIEF.md:66 non-empty. |
| G17 (r1-p5.F3) FP-SEC-3 test wants description on /employer/ | 1 | test-gap | minor | CONFIRMED | T09.md:60-63 vs Step 4 (:50-52) home shows name only. |
| G18 (r1-p6.F1) "no skills" empty state hides the job list | 1 | functional | major | CONFIRMED | T13.md:54 "Empty states ... (no skills; no jobs)"; 05:108; 05:15 an empty state replaces a list; T13.md:62 test asserts only the text. BRIEF.md:50 MUST list all jobs; T13.md:26 no-skills job scores 100. |
| G19 (r1-p6.F2) T12 told to edit T09's template | 1 | scope | minor | CONFIRMED | T12.md:71-72 vs T09.md:50-52, T09 Owns employers/*, T12 Owns none; check_scope would fail. 05:50 requires the link. |
| G20 (r1-p6.F3) format_local cannot produce the range label | 1 | contract | minor | CONFIRMED | T12.md:93-94 range label vs 07:287 one time with year. Source CC01.md:217. |
| G21 (r1-p6.F4) DST fold unspecified | 1 | test-gap | minor | REJECTED | T12.md:79-81 fully specifies a deterministic algorithm (zoneinfo fold=0); the brief's "unambiguous, documented timezone" is about the zone. A fold test would be an extra. |
| G22 (r1-p7.F1) csrf_field not mentioned for new POST forms | 1 | security | minor | CONFIRMED | grep csrf in T10, T12, T14, T15, T16 returns nothing; 04-AUTH-SECURITY.md:44; 04 not in T14/T15 May read; tests post via csrf_post. Pre-dates CC01. |
| G23 (r1-p7.F2) T14 May read lacks timeutil / profile_service | 1 | contract | minor | CONFIRMED | T14.md:90-91 uses format_local and profile timezone; May read (:46-52) lacks both files. |
| G24 (r1-p7.F3) applied date: UTC vs employer's timezone | 1 | contract | minor | CONFIRMED | T15.md:41, :87 UTC vs 05:86-87 "employer's timezone"; no employer timezone column exists. |
| G25 (r1-p7.F4) cover-note validation untested, not in contract | 1 | test-gap | minor | CONFIRMED | T14.md:36, :76 vs contract comment :62-64 and tests :94-108. |
| G26 (r1-p7.F5) confirm_status GET with missing / bad `to` | 1 | test-gap | minor | CONFIRMED | T15.md:72-74, :89-90, tests silent; 07:66 has no form to re-render on a GET. |
| G27 (r1-p7.F6) no non-UTC render test in T14/T15 | 1 | test-gap | minor | CONFIRMED | T14.md:104, T15.md:106 with UTC-only fixtures; partly covered by T16.md:99 and T12 timeutil tests. |
| G28 (r1-p8.F1) "Nothing is written on any failure" vs booking.conflict audit | 1 | contract | minor | CONFIRMED | 07:316, T16.md:68, T17.md:53 vs T17.md:62-63, :71-72 and D14. Source CC01.md:204. |

FIX LIST (CONFIRMED only, worst first):
1. G13: T05.md Tests (:79-82) and CC01.md:300-303: change the FP-SEC-2 email to one with no whitespace that still carries metacharacters (e.g. `x');drop--table@example.com`, or put `'); DROP TABLE users; --` only in the display name and use a benign email).
2. G5: T06.md Step 2 (:55-60): add "for candidates.resume_view the missing-id case is 403 (Forbidden is checked before existence, 07/T08)"; 04-AUTH-SECURITY.md:32-38: carve out get_resume_for_viewer from the blanket "NotFound when the row does not exist" sentence.
3. G6: T06.md Step 2: exempt jobs.detail, applications.confirm, applications.submit from the "user B with A's id: 403" case (expected 200 / 200 / 302).
4. G18: T13.md Step 4 (:54) and test bullet (:62): the "no skills" hint is shown in addition to the full ranked list, never instead of it; the test asserts both. 05-UX-FLOWS.md:108: reword the row so it is a hint, not an empty state.
5. G1: 02-ARCHITECTURE.md:28, :33, :34 (plus missing skills.py, activity/): list the module files as 07-CONTRACTS.md names them.
6. G2: 03-DATA-MODEL.md:74, :77, :78: change (brief) to DEFAULT (not in brief).
7. G19: T09.md Step 4 (:50-52): add a link to /employer/slots ("Interview slots"); T12.md:71-72: drop the "add the link there only if T09 has not" clause.
8. G22: add one sentence to T10, T12, T14, T15, T16 Steps (or one line in 07-CONTRACTS.md next to :66): "every POST form includes csrf_field() (04-AUTH-SECURITY.md:44)"; optionally one test bullet per card asserting the hidden csrf_token input is in the rendered form.
9. G4: 07-CONTRACTS.md:313-316, T16.md:65-68, T17.md:52-53 (and CC01.md:201-204): add "or the slot is in the past" to the Forbidden list of book_slot.
10. G28: 07-CONTRACTS.md:316, T16.md:68, T17.md:53 (and CC01.md:204): "Nothing is written on any failure" becomes "No booking row is written on any failure; on Conflict a booking.conflict audit row is written in a separate transaction (D14)".
11. G10: 07-CONTRACTS.md:308-309, T16.md:60-61, :76-78 (and CC01.md:196-197): decide one behaviour for is_eligible on a missing or another candidate's application (recommend: raises NotFound/Forbidden via get_own_application; bool only for status and booking conditions).
12. G3: 02-ARCHITECTURE.md:133-135: move timeutil.local_to_utc inside the create_slot step.
13. G9: 05-UX-FLOWS.md:86: "matched skills" becomes "skills (with matched and missing as the score explanation)".
14. G24: 05-UX-FLOWS.md:87: "(shown in the employer's timezone)" becomes "(shown in UTC, DEFAULT (not in brief))".
15. G17: T09.md Step 4 or test bullet (:60-63): either home shows name and description, or the test asserts the description only on /employer/company.
16. G20: T12.md Step 6 (:93-94): say the range label is composed from two utc_to_local calls.
17. G8: 04-AUTH-SECURITY.md:52: list "400, 403, 404, 405, 409, 413, 500".
18. G14: T05.md:70: "remove the skip on these five"; T04.md Step 6: state that the "plus" FP-SEC names in the 07 table also get placeholders, except test_db.py which T01 writes directly.
19. G15: T10.md Step 9: "jobs.edit GET and jobs.confirm_delete GET load the job with get_owned_job"; add test bullet "employer B GET of A's edit and confirm-delete pages gives 403".
20. G16: T10.md Step 2: "strip title, description, location before validation"; add "whitespace-only title" (and negative / over-max salary) to the parametrised invalid list.
21. G23: T14.md May read: add app/timeutil.py, app/candidates/profile_service.py and 07 section "candidates: profile".
22. G25: T14.md contract comment: add ValidationError({"cover_note": ...}) if over 2000 chars; add a test bullet for a 2001-char note (400 via the route, no row).
23. G26: T15.md Step 5: define the confirm GET for a missing, unknown or current `to` (recommend 400 via errors/400.html) and add a test bullet.
24. G11: T01.md:113-116: make the FP-SEC-4 test self-contained (two apps from tmp_path / "a" and tmp_path / "b", or tmp_path_factory).
25. G7: CC01.md:328 step-7 pattern: exclude SQL upserts (grep -v "ON CONFLICT"), or record the three hits as accepted.
26. G27 (optional): add one bullet to T14 (mine page) with an Asia/Hong_Kong profile asserting "10:00 (Asia/Hong_Kong)" is rendered for the 02:00Z default slot.

QUESTIONS FOR KEVIN (UNCLEAR only):
1. G12: FP-DOC-3 requires "two jobs with required skills"; D17's mandatory minimum seeds "Data Analyst" (Python, SQL) and "Graduate Trainee" (no skills). Is one job with a non-empty skills list enough under your reading, or should 12-DEPLOY.md:48 and T19.md Step 2 mandate a third seeded job with a non-empty skills list?

Orchestrator note: G12 resolved by amending D17 to add a third mandatory job with a non-empty skills list ("Logistics Coordinator" at Tidewater requiring SQL, Excel), which satisfies both readings; recorded in DECISIONS.md and flagged for Kevin in the run summary. Card-sourced sentences (G4, G5/G6, G10, G13, G20, G28, G12) corrected in docs/tasks/CC01.md before the fix round.
