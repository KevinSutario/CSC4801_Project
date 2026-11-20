"""T08 · candidate resume persistence and privacy."""

import pytest

from app.candidates import profile_service, resume_service
from app.errors import ValidationError


def test_fp_can_1_profile_and_private_resume_rules(
    app, client, conn, make_candidate, make_employer, login_as
):
    owner_id = make_candidate(name="Resume Owner", skills=())
    other_candidate_id = make_candidate(email="other@example.com", skills=())
    employer_id = make_employer()

    profile_service.save_profile(
        conn, owner_id, "Resume Owner", "Analyst", "Hong Kong", "Asia/Hong_Kong", "", "Python"
    )
    resume_service.save_resume(conn, owner_id, "  Plain text resume  ")
    assert resume_service.get_resume(conn, owner_id)["body"] == "Plain text resume"
    resume_service.save_resume(conn, owner_id, "Replacement resume")
    assert resume_service.get_resume(conn, owner_id)["body"] == "Replacement resume"
    row_count = conn.execute(
        "SELECT COUNT(*) FROM resumes WHERE owner_id = ?", (owner_id,)
    ).fetchone()[0]
    assert row_count == 1

    with pytest.raises(ValidationError):
        resume_service.save_resume(conn, owner_id, "   ")
    with pytest.raises(ValidationError):
        resume_service.save_resume(conn, owner_id, "x" * (resume_service.RESUME_MAX_CHARS + 1))

    with client.session_transaction() as session:
        session["user_id"] = owner_id
    response = client.get(f"/candidates/{owner_id}/resume")
    assert response.status_code == 200
    assert "Replacement resume" in response.get_data(as_text=True)

    with client.session_transaction() as session:
        session["user_id"] = other_candidate_id
    assert client.get(f"/candidates/{owner_id}/resume").status_code == 403

    with client.session_transaction() as session:
        session["user_id"] = employer_id
    assert client.get(f"/candidates/{owner_id}/resume").status_code == 403

    missing_id = make_candidate(email="empty@example.com", skills=())
    with client.session_transaction() as session:
        session["user_id"] = missing_id
    assert client.get(f"/candidates/{missing_id}/resume").status_code == 404

    resume_service.save_resume(conn, owner_id, "<script>alert(1)</script>")
    with client.session_transaction() as session:
        session["user_id"] = owner_id
    response = client.get(f"/candidates/{owner_id}/resume")
    body = response.get_data(as_text=True)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body
    assert "<script>alert(1)</script>" not in body


def test_resume_form_saves_and_replaces_with_csrf(client, make_candidate, login_as, csrf_post):
    owner_id = make_candidate(skills=())
    login_as(client, owner_id, "candidate")
    response = client.get("/candidate/resume")
    assert response.status_code == 200
    assert "Only you can read your resume." in response.get_data(as_text=True)
    response = csrf_post(client, "/candidate/resume", {"body": "First resume"})
    assert response.status_code == 302
    response = csrf_post(client, "/candidate/resume", {"body": "Updated resume"})
    assert response.status_code == 302
    assert "Updated resume" in client.get("/candidate/resume").get_data(as_text=True)
