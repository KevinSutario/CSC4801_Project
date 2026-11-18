REVIEWER: 3
CHECKED: 1 (requirement and contract: every fix-list item 1 to 10 against the worktree files at b1aa462, each new quote against docs/BRIEF.md, each new contract claim against docs/plan/07-CONTRACTS.md and docs/plan/03-DATA-MODEL.md), 2 (security: docs-only change, no routes, SQL, templates or uploads touched; nothing to tick), 3 (tests and edges: no test files touched, no test names changed, `git grep "(from the brief)"` finds only the T-BRIEF card itself, `check_scope.py T-BRIEF` prints `SCOPE OK for T-BRIEF`, diff stat 47701ca..b1aa462 touches only Owns files)
FINDINGS: 2

Item-by-item result (verified by reading the worktree files, not the packet):
1. T10 BLOCKED with cascade/409, 404/403 and closed-jobs reasons: applied (T10.md:5, :21-25, :34-38). Steps 7 and the test bullet left as written, which the fix list allowed.
2. T16 BLOCKED with three reasons, Steps 3-4 and the "slot of a different job" case marked CONFLICT, T12 corrected to quote the brief, FP-SCHED-2 row NEEDS DECISION: applied (T16.md:5, :28-34, :71-76, :86-89; T12.md:28-35 quote "> - the slot belongs to the employer for the candidate's application;" is verbatim BRIEF.md:115; 01-REQUIREMENTS.md:201). 03-DATA-MODEL.md:127 confirms the index is still commented out; :112 confirms employer_id exists on interview_slots.
3. Closed jobs relabelled CONFLICT in T13, T10 and the plan; FP-CAN-2 NEEDS DECISION; T13 BLOCKED: applied (T13.md:5, :25-30; T10.md:34-38; 01-REQUIREMENTS.md:82, :108-111).
4. T15 definitive key list restored and marked DEFAULT: applied (T15.md:26-32). 07-CONTRACTS.md:243 gives only the signature, no key list, so nothing in the frozen contract contradicts it.
5. T07 BLOCKED, FP-CAN-1 NEEDS DECISION: applied (T07.md:5, :23-27; 01-REQUIREMENTS.md:81). 07-CONTRACTS.md:160-161 confirms save_profile has no name parameter.
6. T06 BLOCKED, T16 added to the card list: applied (T06.md:5, :34).
7. resume_id and the /resumes/<id> link relabelled CONFLICT: applied (T15.md:33-37, :83-84, status :5).
8. T17 BLOCKED with the same-candidate-twice reason: applied (T17.md:5, :24-31). See F1 for a wrong sentence inside the new text.
9. FP-MATCH-2 full paragraph: applied and verbatim against BRIEF.md:102 (01-REQUIREMENTS.md:193-194).
10. T11 "need no re-normalising" dropped, OPEN QUESTION on "collapse spaces" added: applied (T11.md:36-42); 07-CONTRACTS.md:94 confirms the provisional rule says "collapse spaces".

F1
severity: minor
category: contract
where: docs/tasks/T17.md:29-31
claim: The fix-round text added to T17 tells the T17 agent that 07-CONTRACTS.md is outside "this task's May read", but T17's own May read lists that file and the cited line is in the listed section.
trigger: Dispatch T17 after the decision; the agent reads Requirement line 30 ("that file is outside this task's May read") and then May read line 45.
expected: The card either says "outside T-BRIEF's May read" or simply cites 07-CONTRACTS.md:277 as a file the T17 agent may read, since the proposal (Forbidden for an ineligible booking) is exactly what the contract already states.
actual: The card contradicts itself. T17.md:29-31: "The T-BRIEF reviewer proposed `Forbidden` (the error T16 Step 4 raises for an ineligible booking) and cited `07-CONTRACTS.md`; that file is outside this task's May read, so it is recorded here as a proposal, not a DEFAULT." T17.md:45: "- `docs/plan/07-CONTRACTS.md` (section: scheduling)". 07-CONTRACTS.md:252 opens "### scheduling (T12 slots, T16 and T17 booking)" and :277 inside it reads "# Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief". An agent following house rule 2 may wrongly treat the contract file as off-limits, or treat the decided value as undecided when the contract already fixes it.
evidence: T17.md:30 "that file is outside this task's May read"; T17.md:45 "`docs/plan/07-CONTRACTS.md` (section: scheduling)"; 07-CONTRACTS.md:277 "# Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief"

F2
severity: minor
category: contract
where: docs/tasks/T12.md:5
claim: The fix round made the 404-vs-403 CONFLICT a stated BLOCKED reason on T10 and T06 but left T12 READY although T12 carries the identical unresolved conflict in its Step 3 and test bullet, so the same undecided rule now blocks one phase-2 card and not the other.
trigger: Orchestrator dispatches every READY phase-2 card. T12's agent, per T12.md:89-90, writes test_fp_sched_1_invalid_slots asserting NotFound for "someone else's job"; the brief (BRIEF.md:66, FP-EMP-2) says that employer "**MUST** receive `403`". If the orchestrator later decides 403 (the brief's text), the merged T12 test and create_slot must be rewritten, while T10, with the same conflict, was held back precisely to avoid that.
expected: Either T12 is BLOCKED on the same decision as T10 (T10.md:5 cites "Step 4 and the test bullet give `NotFound` (404) where the brief says the other employer MUST receive 403" as a blocking reason), or T10's status drops that reason and both cards treat 404-vs-403 as a flagged-not-blocking CONFLICT, consistently.
actual: T12.md:5 "READY (rules quoted from the brief; duration default SUPERSEDED; the rest DEFAULT (not in brief))" while T12.md:37-38 "CONFLICT (flagged, not changed): the brief (FP-EMP-2, FP-AUTH-3) gives `403` for another employer's posting; the invalid-slots test bullet says `NotFound` for "someone else's job"." and T12.md:90 "someone else's job (`NotFound`)". T10.md:5 lists the same conflict as a reason for BLOCKED. 01-REQUIREMENTS.md:200 keeps FP-SCHED-1 READY while :47 keeps FP-AUTH-3 NEEDS DECISION "cards use 404 where the brief says 403", and :74-75 says "Decision needed before those cards run", naming T12.
evidence: T12.md:5 "READY"; T12.md:70 "check job ownership (`NotFound`)"; T12.md:90 "someone else's job (`NotFound`)"; 01-REQUIREMENTS.md:74-75 "T06's default and the feature cards T08, T10, T12, T14, T15, T16 return 404 (`NotFound`) for another user's object. The brief says 403. Decision needed before those cards run."
