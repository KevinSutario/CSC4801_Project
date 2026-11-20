"""Employer applicant review requirement tests (FP-EMP-3). Owned by T15."""

import pytest

from app.applications import review_service
from app.applications.statuses import STATUSES
from app.errors import Forbidden, ValidationError
from app.jobs import service as jobs_service

_EXPECTED_KEYS = {
    "application_id", "candidate_id", "candidate_name", "headline", "skills",
    "score", "matched", "missing", "status", "applied_at", "booking",
}


def _job_with_skills(conn, make_employer, make_company, skills=("python", "sql")):
    emp = make_employer()
    make_company(emp)
    jid = jobs_service.create_job(
        conn, emp, "Data Analyst", "Do data.", "", "full-time", "", "",
        ",".join(skills),
    )
    return emp, jid


def test_fp_emp_3_applicant_fields_order_status_and_role(
    conn, client, make_employer, make_company, make_candidate, make_application,
    make_slot, make_booking, login_as,
):
    emp, jid = _job_with_skills(conn, make_employer, make_company)  # job needs python, sql

    # three candidates: full match, partial, and a name-tie with the partial one
    full = make_candidate(email="full@example.com", name="Zoe Adams", skills=("python", "sql"))
    partial_b = make_candidate(email="b@example.com", name="Bob Lee", skills=("python",))
    partial_a = make_candidate(email="a@example.com", name="amy ng", skills=("python",))
    for cid in (full, partial_b, partial_a):
        make_application(cid, jid)

    rows = review_service.list_applicants(conn, emp, jid)
    assert len(rows) == 3
    # keys exactly as contract, no resume_id
    for r in rows:
        assert set(r.keys()) == _EXPECTED_KEYS
        assert "resume_id" not in r
    # order: score desc, then case-insensitive name, then id. full(100) first; then the two 50s
    # tie broken by name: "amy ng" < "Bob Lee" (case-insensitive)
    assert [r["candidate_id"] for r in rows] == [full, partial_a, partial_b]
    assert rows[0]["score"] == 100
    assert rows[1]["score"] == rows[2]["score"] == 50
    assert rows[1]["matched"] == ["python"] and rows[1]["missing"] == ["sql"]


def test_set_status_transitions_audit_and_current_rejected(
    conn, make_employer, make_company, make_candidate, make_application
):
    emp, jid = _job_with_skills(conn, make_employer, make_company)
    cid = make_candidate(skills=("python", "sql"))
    app_id = make_application(cid, jid)  # starts 'pending'

    review_service.set_status(conn, emp, app_id, "interviewing")
    assert conn.execute("SELECT status FROM applications WHERE id = ?",
                        (app_id,)).fetchone()["status"] == "interviewing"
    # audited application.status with "<old> -> <new>"
    ev = conn.execute(
        "SELECT detail FROM audit_log WHERE action = 'application.status'"
        " ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert "pending" in ev["detail"] and "interviewing" in ev["detail"]

    # setting the current status is rejected
    with pytest.raises(ValidationError):
        review_service.set_status(conn, emp, app_id, "interviewing")
    # an unknown status is rejected
    with pytest.raises(ValidationError):
        review_service.set_status(conn, emp, app_id, "archived")
    assert "interviewing" in STATUSES


def test_status_change_keeps_booking(
    conn, make_employer, make_company, make_candidate, make_application, make_slot, make_booking
):
    emp, jid = _job_with_skills(conn, make_employer, make_company)
    cid = make_candidate(skills=("python",))
    app_id = make_application(cid, jid)
    slot = make_slot(emp)
    make_booking(app_id, slot)
    review_service.set_status(conn, emp, app_id, "interviewing")
    review_service.set_status(conn, emp, app_id, "rejected")  # leaves interviewing
    # booking still associated; slot still unavailable (FP-SCHED-2)
    row = conn.execute("SELECT slot_id FROM bookings WHERE application_id = ?",
                       (app_id,)).fetchone()
    assert row is not None and row["slot_id"] == slot
    rows = review_service.list_applicants(conn, emp, jid)
    assert rows[0]["booking"]["slot_id"] == slot


def test_other_employer_and_candidate_are_blocked(
    conn, client, make_employer, make_company, make_candidate, make_application, login_as, csrf_post
):
    emp, jid = _job_with_skills(conn, make_employer, make_company)
    cid = make_candidate(skills=("python",))
    app_id = make_application(cid, jid)

    other = make_employer(email="other@example.com")
    make_company(other)
    with pytest.raises(Forbidden):
        review_service.list_applicants(conn, other, jid)
    with pytest.raises(Forbidden):
        review_service.set_status(conn, other, app_id, "interviewing")

    # candidate GET the applicants page -> 403
    login_as(client, cid, "candidate")
    assert client.get(f"/employer/jobs/{jid}/applicants").status_code == 403


def test_list_applicants_fixed_query_count(
    conn, make_employer, make_company, make_candidate, make_application
):
    emp, jid = _job_with_skills(conn, make_employer, make_company)
    for i in range(30):
        cid = make_candidate(email=f"c{i}@example.com", name=f"Cand {i}", skills=("python",))
        make_application(cid, jid)
    seen = []
    conn.set_trace_callback(lambda stmt: seen.append(stmt))
    try:
        rows = review_service.list_applicants(conn, emp, jid)
    finally:
        conn.set_trace_callback(None)
    assert len(rows) == 30
    selects = [s for s in seen if s.lstrip().upper().startswith("SELECT")]
    # Fixed regardless of applicant count: get_owned_job, job_skills, applications,
    # candidate_skills, bookings.
    assert len(selects) <= 5
