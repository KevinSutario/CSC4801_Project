# 11 · Testing

## Rules

1. **Test first for logic.** Write the test, run it, show it failing, then write the code.
2. **Services are tested directly** with the `conn` fixture. Routes are tested with `client` only
   for: status codes, redirects, CSRF, login and role checks, and that the page shows the right text.
3. **Every requirement test name from the template is kept exactly** (`07-CONTRACTS.md`). A task may
   add more tests. It never renames a template test.
4. **Test the failure paths**, not only the happy path: missing fields, too long, wrong type, someone
   else's object, missing object, duplicate, conflict.
5. **No sleeping, no network, no real clock in assertions.** Use fixed UTC strings far in the future
   (2030 and later), so tests never break as time passes.
6. **No skipped tests at release.** Placeholders are `@pytest.mark.skip(reason="TODO Txx")` until
   their task replaces them. `python scripts/check.py --release` fails if any test is skipped.
7. **Brief examples are copied verbatim.** If the brief gives worked examples (matching, booking),
   each one becomes a parametrised test case with the brief's exact inputs and outputs, and a
   comment `# brief: <section>`.

## Fixtures (`tests/conftest.py`: T01 writes app, client, conn; T04 adds the rest; then frozen)

```python
@pytest.fixture
def app(tmp_path):         # create_app with TESTING, temp DATABASE and UPLOAD_DIR, SECRET_KEY="test"
                           # runs init_db(); resets the login rate limiter
@pytest.fixture
def client(app): ...       # app.test_client()
@pytest.fixture
def conn(app): ...         # yields get_db() inside app.app_context()
```
Factory fixtures return functions (see `07-CONTRACTS.md` for signatures).
`csrf_post(client, url, data)` reads the token from the session and adds `csrf_token` to `data`.

Example:
```python
def test_fp_emp_2_job_validation_and_deletion(conn, make_employer, make_company):
    emp = make_employer()
    make_company(emp)
    with pytest.raises(ValidationError) as e:
        jobs_service.create_job(conn, emp, title="", description="x", location="",
                                employment_type="", salary_min="", salary_max="", skills_text="")
    assert "title" in e.value.errors
```

## What a good requirement test checks

| Requirement | Must check at least |
|---|---|
| FP-AUTH-1 | register, then login works, session has user; logout clears it; protected page redirects after logout; invalid email, short password, duplicate email, bad role all rejected with field errors |
| FP-AUTH-2 | stored hash is not the password; two users with the same password get different hashes; correct password verifies; wrong password does not |
| FP-AUTH-3 | candidate cannot open employer pages (403); employer A cannot see or edit employer B's job (agreed code); missing id gives 404 |
| FP-CAN-1 | profile saves and reloads; skills normalised and deduped; resume: wrong type and too-large rejected; owner can download; another candidate cannot; rules from brief for employers |
| FP-CAN-2 | every open job is returned (count equals open jobs); each keeps all its original fields; order follows the brief; closed jobs excluded if the brief says so |
| FP-CAN-3 | second pending application to the same job is refused with the brief's result; a candidate cannot read another's application |
| FP-EMP-1 | create, read back, update company; validation errors; one company per employer |
| FP-EMP-2 | every invalid field rejected; valid job saved with skills; delete removes it and follows the brief for linked rows; cannot delete another employer's job |
| FP-EMP-3 | applicant rows have exactly the brief's fields, in the brief's order; status change follows allowed transitions; only the job's owner (employer role) can see or change |
| FP-MATCH-1 | every brief example exactly; normalisation cases; the floor; each tie-breaker on its own, and both together |
| FP-SCHED-1 | slot entered in Asia/Hong_Kong stored as correct UTC; shown back correctly in another zone; end before start rejected; nonexistent DST time rejected; delete works; deleting a booked slot follows the brief |
| FP-SCHED-2 | eligible applicant books; ineligible (wrong status, another job, someone else's application) refused |
| FP-SCHED-3 | second booking of the same slot gets exactly the brief's conflict result; the database still holds one booking |

## Extra test layers (cheap, find the bugs reviewers miss)

- **Property tests without new dependencies**: loop over 200 generated inputs with
  `random.Random(1234)` (fixed seed). Use for: `rank` never drops or duplicates jobs, never mutates
  input, is deterministic; `local_to_utc` then `utc_to_local` gives back the same local time.
- **Mutation check** (phase gates): the judge agent breaks the code on purpose in a scratch copy
  (flip a comparison, remove a tie-breaker, drop an ownership check) and confirms a test fails.
  Survivors become new tests. See `10-REVIEW-PROTOCOL.md`.
- **Performance smoke test** (T22): seed 200 jobs and 200 candidates; recommendations and
  applicants pages each answer in under 1 second with the test client.

## Requirement-test mapping (for the README, written by T21)

T21 builds the README table from this file plus `07-CONTRACTS.md`: one row per FP-* ID, with the
implementation files and the exact `file::test_name`. Run
`python -m pytest --collect-only -q` and check every named test exists.
