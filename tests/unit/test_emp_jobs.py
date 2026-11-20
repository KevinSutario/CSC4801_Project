"""Employer jobs requirement tests (FP-EMP-2). Owned by T10."""

import pytest

from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.jobs import service


def _count_jobs(conn) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()["n"]


def _mk_employer_with_company(conn, make_employer, make_company, email="e@example.com"):
    emp = make_employer(email=email)
    make_company(emp)
    return emp


@pytest.mark.parametrize(
    "field,kwargs",
    [
        ("title", {"title": ""}),
        ("title", {"title": "   "}),
        ("title", {"title": "x" * 121}),
        ("description", {"description": ""}),
        ("description", {"description": "x" * 5001}),
        ("employment_type", {"employment_type": "freelance"}),
        ("salary_min", {"salary_min": "notnum"}),
        ("salary_max", {"salary_max": "-5"}),
        ("salary_max", {"salary_min": "100", "salary_max": "50"}),
    ],
)
def test_fp_emp_2_invalid_inputs(conn, make_employer, make_company, field, kwargs):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    base = dict(title="Data Analyst", description="Do data.", location="Remote",
                employment_type="full-time", salary_min="", salary_max="", skills_text="python")
    base.update(kwargs)
    before = _count_jobs(conn)
    with pytest.raises(ValidationError) as exc:
        service.create_job(conn, emp, **base)
    assert field in exc.value.errors
    assert _count_jobs(conn) == before


def test_create_requires_company(conn, make_employer):
    emp = make_employer()  # no company
    with pytest.raises(ValidationError) as exc:
        service.create_job(conn, emp, "T", "D", "", "full-time", "", "", "python")
    assert "company" in exc.value.errors


def test_create_valid_job_normalises_skills(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    jid = service.create_job(conn, emp, "Data Analyst", "Do data.", "Remote",
                             "full-time", "50000", "90000", " Python , SQL ,python ")
    job = service.get_job(conn, jid)
    assert job["title"] == "Data Analyst"
    assert job["company_name"]
    assert set(job["skills"]) == {"python", "sql"}  # normalised + deduped


def test_empty_skills_list_allowed(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    jid = service.create_job(conn, emp, "No Skills Job", "Desc", "", "contract", "", "", "")
    assert service.get_job(conn, jid)["skills"] == []


def test_delete_job_with_no_applications(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    jid = service.create_job(conn, emp, "Gone", "Desc", "", "full-time", "", "", "")
    service.delete_job(conn, emp, jid)
    with pytest.raises(NotFound):
        service.get_job(conn, jid)


def test_delete_job_with_application_is_409_and_changes_nothing(
    conn, make_employer, make_company, make_candidate, make_application
):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    jid = service.create_job(conn, emp, "Busy", "Desc", "", "full-time", "", "", "python")
    cand = make_candidate()
    make_application(cand, jid)
    with pytest.raises(Conflict):
        service.delete_job(conn, emp, jid)
    # job and its application unchanged
    assert service.get_job(conn, jid)["title"] == "Busy"
    assert conn.execute("SELECT COUNT(*) AS n FROM applications WHERE job_id = ?",
                        (jid,)).fetchone()["n"] == 1


def test_employer_b_cannot_delete_employer_a_job(conn, make_employer, make_company):
    emp_a = _mk_employer_with_company(conn, make_employer, make_company, email="a@example.com")
    jid = service.create_job(conn, emp_a, "A's job", "Desc", "", "full-time", "", "", "")
    emp_b = _mk_employer_with_company(conn, make_employer, make_company, email="b@example.com")
    with pytest.raises(Forbidden):
        service.delete_job(conn, emp_b, jid)
    assert service.get_job(conn, jid)["title"] == "A's job"  # not deleted


def test_get_owned_job_missing_is_404(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    with pytest.raises(NotFound):
        service.get_owned_job(conn, emp, 999999)


def test_list_jobs_includes_every_job_and_skills(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    service.create_job(conn, emp, "J1", "D", "", "full-time", "", "", "python,sql")
    service.create_job(conn, emp, "J2", "D", "", "part-time", "", "", "")
    jobs = service.list_jobs(conn)
    assert len(jobs) == 2
    by_title = {j["title"]: j for j in jobs}
    assert set(by_title["J1"]["skills"]) == {"python", "sql"}
    assert by_title["J2"]["skills"] == []


def test_list_jobs_uses_fixed_query_count(conn, make_employer, make_company):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    for i in range(50):
        service.create_job(conn, emp, f"Job {i}", "D", "", "full-time", "", "", "python")
    seen = []
    conn.set_trace_callback(lambda stmt: seen.append(stmt))
    try:
        jobs = service.list_jobs(conn)
    finally:
        conn.set_trace_callback(None)
    assert len(jobs) == 50
    selects = [s for s in seen if s.lstrip().upper().startswith("SELECT")]
    assert len(selects) <= 3  # no query-per-job


def test_detail_route_any_signed_in_user_and_404(client, conn, make_employer, make_company,
                                                 make_candidate, login_as):
    emp = _mk_employer_with_company(conn, make_employer, make_company)
    jid = service.create_job(conn, emp, "Visible", "Desc", "", "full-time", "", "", "python")
    cand = make_candidate()
    login_as(client, cand, "candidate")
    assert client.get(f"/jobs/{jid}").status_code == 200
    assert client.get("/jobs/999999").status_code == 404


def test_candidate_cannot_post_new_job(client, make_candidate, login_as, csrf_post):
    cand = make_candidate()
    login_as(client, cand, "candidate")
    resp = csrf_post(client, "/employer/jobs/new", {
        "title": "x", "description": "y", "location": "", "employment_type": "full-time",
        "salary_min": "", "salary_max": "", "skills": "",
    })
    assert resp.status_code == 403


def test_fp_emp_2_job_validation_and_deletion(
    conn, make_employer, make_company, make_candidate, make_application
):
    """Template-named FP-EMP-2 test: validation, empty skills, delete rules, ownership.

    The behaviours are also covered in finer-grained tests above; this function carries the
    exact name the course requirement mapping (01-REQUIREMENTS.md) expects.
    """
    emp = make_employer()
    make_company(emp)

    # invalid: whitespace-only title and bad employment type each raise, nothing written
    before = _count_jobs(conn)
    with pytest.raises(ValidationError) as exc:
        service.create_job(conn, emp, "   ", "Desc", "", "full-time", "", "", "python")
    assert "title" in exc.value.errors
    with pytest.raises(ValidationError) as exc:
        service.create_job(conn, emp, "Ok", "Desc", "", "freelance", "", "", "python")
    assert "employment_type" in exc.value.errors
    assert _count_jobs(conn) == before

    # valid job with normalised skills; empty skills list allowed
    jid = service.create_job(conn, emp, "Data Analyst", "Do data.", "Remote",
                             "full-time", "50000", "90000", " Python , SQL ,python ")
    assert set(service.get_job(conn, jid)["skills"]) == {"python", "sql"}
    jid_empty = service.create_job(conn, emp, "No Skills", "Desc", "", "contract", "", "", "")
    assert service.get_job(conn, jid_empty)["skills"] == []

    # a job with no applications deletes
    service.delete_job(conn, emp, jid_empty)
    with pytest.raises(NotFound):
        service.get_job(conn, jid_empty)

    # a job with an application: delete refused with Conflict (409), nothing changed
    make_application(make_candidate(), jid)
    with pytest.raises(Conflict):
        service.delete_job(conn, emp, jid)
    assert service.get_job(conn, jid)["title"] == "Data Analyst"
    assert conn.execute("SELECT COUNT(*) AS n FROM applications WHERE job_id = ?",
                        (jid,)).fetchone()["n"] == 1

    # another employer deleting this job: Forbidden (403), nothing deleted
    other = make_employer(email="other@example.com")
    make_company(other)
    with pytest.raises(Forbidden):
        service.delete_job(conn, other, jid)
    assert service.get_job(conn, jid)["title"] == "Data Analyst"
