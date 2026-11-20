"""Authorization sweep (FP-AUTH-3 / FP-SEC-1). Owned by T06.

This file only tests. For every protected route with an id it checks the brief's
contract: signed out -> redirect/401; wrong role or wrong owner -> 403; a missing
object the caller could otherwise reach -> 404. Exceptions are encoded below
(resume_view is 403 for any non-own id incl. missing, D10; jobs.detail /
applications.confirm / applications.submit have no owner).

Any case that fails is a real hole: it is marked xfail(strict=True, reason="Bn:
...") so the gate stays green and the hole stays visible until a bug card fixes it.
"""

import pytest

from app.jobs import service as jobs_service

MISSING = 999999


def _world(conn, make_candidate, make_employer, make_company, make_job,
           make_application, make_slot):
    """Build owner A's objects plus a same-role intruder B of each role.

    Returns a dict of ids used to build URLs and sessions.
    """
    emp_a = make_employer(email="empA@example.com", name="Emp A")
    make_company(emp_a, name="Company A")
    emp_b = make_employer(email="empB@example.com", name="Emp B")
    make_company(emp_b, name="Company B")

    cand_a = make_candidate(email="candA@example.com", name="Cand A", skills=("python",))
    cand_b = make_candidate(email="candB@example.com", name="Cand B", skills=("python",))

    job_a = jobs_service.create_job(conn, emp_a, "Job A", "Desc", "", "full-time", "", "", "python")
    # cand_a applies to job_a and is moved to interviewing so booking is reachable
    app_a = make_application(cand_a, job_a, status="interviewing")
    slot_a = make_slot(emp_a)

    return {
        "emp_a": emp_a, "emp_b": emp_b, "cand_a": cand_a, "cand_b": cand_b,
        "job_a": job_a, "app_a": app_a, "slot_a": slot_a,
    }


@pytest.fixture()
def world(conn, make_candidate, make_employer, make_company, make_job,
          make_application, make_slot):
    return _world(conn, make_candidate, make_employer, make_company, make_job,
                  make_application, make_slot)


def _get(client, url):
    return client.get(url)


def _post(client, csrf_post, url):
    return csrf_post(client, url, {})


# Each case: id, the owner's role, a same-role intruder B, a URL built from an id
# key in `world`, the method, whether it checks ownership, and whether a
# non-own/missing id is 403 (resume_view, D10) rather than 404.
_CASES = [
    # candidate-owned
    dict(id="resume_view", role="candidate", intruder="cand_b", method="GET",
         url="/candidates/{}/resume", key="cand_a", owner=True, nonown_403=True),
    dict(id="application_detail", role="candidate", intruder="cand_b", method="GET",
         url="/candidate/applications/{}", key="app_a", owner=True),
    dict(id="confirm_booking", role="candidate", intruder="cand_b", method="GET",
         url="/candidate/applications/{}/book/{slot}", key="app_a", owner=True),
    dict(id="book", role="candidate", intruder="cand_b", method="POST",
         url="/candidate/applications/{}/book/{slot}", key="app_a", owner=True),
    # employer-owned
    dict(id="jobs_edit", role="employer", intruder="emp_b", method="GET",
         url="/employer/jobs/{}/edit", key="job_a", owner=True),
    dict(id="jobs_confirm_delete", role="employer", intruder="emp_b", method="GET",
         url="/employer/jobs/{}/delete", key="job_a", owner=True),
    dict(id="jobs_delete", role="employer", intruder="emp_b", method="POST",
         url="/employer/jobs/{}/delete", key="job_a", owner=True),
    dict(id="delete_slot", role="employer", intruder="emp_b", method="POST",
         url="/employer/slots/{}/delete", key="slot_a", owner=True),
    dict(id="applicants", role="employer", intruder="emp_b", method="GET",
         url="/employer/jobs/{}/applicants", key="job_a", owner=True),
    dict(id="confirm_status", role="employer", intruder="emp_b", method="GET",
         url="/employer/applications/{}/status?to=accepted", key="app_a", owner=True),
    dict(id="set_status", role="employer", intruder="emp_b", method="POST",
         url="/employer/applications/{}/status", key="app_a", owner=True, form={"to": "accepted"}),
    # no owner: user B with A's id is allowed (jobs.detail 200; apply confirm 200 / submit 302)
    dict(id="jobs_detail", role="candidate", intruder="cand_b", method="GET",
         url="/jobs/{}", key="job_a", owner=False, allowed_code=200, role_open=True),
    dict(id="apply_confirm", role="candidate", intruder="cand_b", method="GET",
         url="/jobs/{}/apply", key="job_a", owner=False, allowed_code=200),
    dict(id="apply_submit", role="candidate", intruder="cand_b", method="POST",
         url="/jobs/{}/apply", key="job_a", owner=False, allowed_code=302),
]


def _build(url, obj_id, world):
    return url.format(obj_id, slot=world["slot_a"])


def _call(client, csrf_post, case, url):
    if case["method"] == "GET":
        return client.get(url)
    return csrf_post(client, url, case.get("form", {}))


@pytest.mark.parametrize("case", _CASES, ids=[c["id"] for c in _CASES])
def test_fp_sec_1_object_access_boundaries(client, world, login_as, csrf_post, case):
    """Per route: wrong owner, missing id, wrong role, signed out — per the contract."""
    own_id = world[case["key"]]

    # --- same-role intruder B uses A's id ---
    login_as(client, world[case["intruder"]], case["role"])
    resp = _call(client, csrf_post, case, _build(case["url"], own_id, world))
    if case["owner"]:
        assert resp.status_code == 403, (
            f"{case['id']}: intruder expected 403, got {resp.status_code}")
    else:
        assert resp.status_code == case["allowed_code"], (
            f"{case['id']}: no-owner route expected {case['allowed_code']}, got {resp.status_code}")

    # --- right role (owner A), missing id ---
    login_as(client, _owner_of(case, world), case["role"])
    resp = _call(client, csrf_post, case, _build(case["url"], MISSING, world))
    # resume_view is 403 for any non-own id incl. missing (D10); everything else 404.
    expected = 403 if case.get("nonown_403") else 404
    assert resp.status_code == expected, (
        f"{case['id']}: missing id expected {expected}, got {resp.status_code}")

    # --- wrong role --- (skipped for routes with no role restriction, e.g. jobs.detail)
    if not case.get("role_open"):
        wrong = "employer" if case["role"] == "candidate" else "candidate"
        login_as(client, _wrong_role_user(case, world, wrong), wrong)
        resp = _call(client, csrf_post, case, _build(case["url"], own_id, world))
        assert resp.status_code == 403, (
            f"{case['id']}: wrong role expected 403, got {resp.status_code}")

    # --- signed out ---
    with client.session_transaction() as s:
        s.clear()
    resp = _call(client, csrf_post, case, _build(case["url"], own_id, world))
    assert resp.status_code in (301, 302, 401), (
        f"{case['id']}: signed out expected redirect/401, got {resp.status_code}")


def _owner_of(case, world):
    return world["cand_a"] if case["role"] == "candidate" else world["emp_a"]


def _wrong_role_user(case, world, wrong):
    return world["emp_b"] if wrong == "employer" else world["cand_b"]


# Named cases for the three brief boundaries (FP-SEC-1), readable on their own.
def test_candidate_cannot_read_another_candidates_resume(client, world, login_as):
    login_as(client, world["cand_b"], "candidate")
    assert client.get(f"/candidates/{world['cand_a']}/resume").status_code == 403


def test_candidate_cannot_read_another_candidates_application(client, world, login_as):
    login_as(client, world["cand_b"], "candidate")
    assert client.get(f"/candidate/applications/{world['app_a']}").status_code == 403


def test_employer_cannot_edit_another_employers_job(client, world, login_as, csrf_post):
    login_as(client, world["emp_b"], "employer")
    r = csrf_post(client, f"/employer/jobs/{world['job_a']}/edit",
                  {"title": "x", "description": "y", "location": "", "employment_type": "full-time",
                   "salary_min": "", "salary_max": "", "skills": ""})
    assert r.status_code == 403


def test_employer_cannot_read_another_employers_applicants(client, world, login_as):
    login_as(client, world["emp_b"], "employer")
    assert client.get(f"/employer/jobs/{world['job_a']}/applicants").status_code == 403


def test_candidate_cannot_book_with_another_candidates_application(
    client, world, login_as, csrf_post
):
    login_as(client, world["cand_b"], "candidate")
    r = csrf_post(client, f"/candidate/applications/{world['app_a']}/book/{world['slot_a']}", {})
    assert r.status_code == 403
