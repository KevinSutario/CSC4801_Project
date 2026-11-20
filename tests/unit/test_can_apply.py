"""T14 · candidate applications and duplicate protection."""

import pytest

from app.applications import service
from app.db import now_iso, transaction
from app.errors import Conflict, Forbidden, NotFound, ValidationError


def test_fp_can_3_pending_duplicate_and_application_owner(
    conn, make_candidate, make_employer, make_job, make_slot, make_booking
):
    candidate_a = make_candidate(skills=("python",))
    candidate_b = make_candidate(email="candidate-b@example.com", skills=())
    employer_id = make_employer()
    job_id = make_job(employer_id, title="Analyst", skills=("python",))

    with pytest.raises(ValidationError):
        service.apply(conn, candidate_a, job_id, "x" * 2001)
    assert conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 0

    application_id = service.apply(conn, candidate_a, job_id, "Cover note")
    app_row = conn.execute(
        "SELECT status, cover_note FROM applications WHERE id = ?", (application_id,)
    ).fetchone()
    assert tuple(app_row) == ("pending", "Cover note")
    with pytest.raises(Conflict):
        service.apply(conn, candidate_a, job_id, "Another note")
    assert conn.execute(
        "SELECT COUNT(*) FROM applications WHERE candidate_id = ? AND job_id = ?",
        (candidate_a, job_id),
    ).fetchone()[0] == 1

    with transaction(conn):
        conn.execute(
            "UPDATE applications SET status = 'rejected', updated_at = ? WHERE id = ?",
            (now_iso(), application_id),
        )
    with pytest.raises(Conflict):
        service.apply(conn, candidate_a, job_id, "Retry")
    with pytest.raises(Forbidden):
        service.get_own_application(conn, candidate_b, application_id)
    with pytest.raises(NotFound):
        service.get_own_application(conn, candidate_a, 99999)

    slot_id = make_slot(employer_id)
    make_booking(application_id, slot_id)
    application = service.get_own_application(conn, candidate_a, application_id)
    assert application["booking"]["slot_id"] == slot_id
    assert application["booking"]["starts_at"] == "2030-01-07T02:00:00Z"

    listed = service.list_for_candidate(conn, candidate_a)
    assert listed[0]["id"] == application_id
    assert listed[0]["job_title"] == "Analyst"
    assert listed[0]["company_name"] == "Harbourline Logistics"


def test_apply_routes_confirm_submit_and_missing_job(
    client, make_candidate, make_employer, make_job, login_as, csrf_post
):
    candidate_id = make_candidate(name="Mei Lin Tan", skills=("python",))
    employer_id = make_employer()
    job_id = make_job(employer_id, title="Analyst", skills=("python",))

    login_as(client, candidate_id, "candidate")
    response = client.get(f"/jobs/{job_id}/apply")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Harbourline Logistics" in body
    assert "your name, your skills, your cover note" in body
    assert "Not shared: your resume, your email address, your other applications" in body
    assert "<textarea" in body

    response = csrf_post(client, f"/jobs/{job_id}/apply", {"cover_note": "I am interested."})
    assert response.status_code == 302
    assert response.headers["Location"] == "/candidate/applications"
    applications_page = client.get(response.headers["Location"]).get_data(as_text=True)
    assert "Application sent to Harbourline Logistics" in applications_page

    duplicate = csrf_post(client, f"/jobs/{job_id}/apply", {"cover_note": "Again"})
    assert duplicate.status_code == 409
    assert "already applied" in duplicate.get_data(as_text=True)
    assert client.get("/jobs/99999/apply").status_code == 404

    with client.session_transaction() as session:
        session["user_id"] = employer_id
    assert csrf_post(client, f"/jobs/{job_id}/apply", {}).status_code == 403


def test_my_applications_empty_state_and_owner_data(
    client, make_candidate, make_employer, make_job, login_as, csrf_post
):
    candidate_id = make_candidate(skills=())
    login_as(client, candidate_id, "candidate")
    response = client.get("/candidate/applications")
    assert "You have not applied to any jobs yet." in response.get_data(as_text=True)

    employer_id = make_employer()
    job_id = make_job(employer_id, title="Data Analyst")
    csrf_post(client, f"/jobs/{job_id}/apply", {"cover_note": ""})
    response = client.get("/candidate/applications")
    body = response.get_data(as_text=True)
    assert "Data Analyst" in body
    assert "Harbourline Logistics" in body
    assert "Pending" in body
    assert "/candidate/applications/" in body
