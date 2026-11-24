"""T08 · candidate resume persistence and privacy."""

import io
from pathlib import Path

import pytest
from werkzeug.datastructures import FileStorage

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


def test_fp_can_1_cv_file_upload_and_private_download(
    app, client, conn, make_candidate, make_employer, login_as, csrf_post
):
    owner_id = make_candidate(name="CV Owner", skills=())
    other_candidate_id = make_candidate(email="cv-other@example.com", skills=())
    employer_id = make_employer()
    valid_pdf = b"%PDF-1.4\nfirst demo CV\n%%EOF\n"
    upload_dir = Path(app.config["UPLOAD_DIR"])
    resume_service.save_resume(conn, owner_id, "Existing raw-text resume")

    login_as(client, owner_id, "candidate")
    response = csrf_post(
        client,
        "/candidate/resume/file",
        {"file": (io.BytesIO(valid_pdf), "../../candidate-cv.pdf", "application/pdf")},
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/candidate/resume")

    first = resume_service.get_resume_file(conn, owner_id)
    assert first["original_name"] == "../../candidate-cv.pdf"
    assert first["content_type"] == "application/pdf"
    assert first["size_bytes"] == len(valid_pdf)
    assert first["stored_name"] != first["original_name"]
    first_path = upload_dir / first["stored_name"]
    assert first_path.resolve().parent == upload_dir.resolve()
    assert first_path.read_bytes() == valid_pdf
    assert resume_service.get_resume(conn, owner_id)["body"] == "Existing raw-text resume"
    resolved = resume_service.resolve_resume_file(conn, owner_id)
    assert resolved["path"] == str(first_path.resolve())

    replacement_pdf = b"%PDF-1.7\nreplacement demo CV\n%%EOF\n"
    response = csrf_post(
        client,
        "/candidate/resume/file",
        {"file": (io.BytesIO(replacement_pdf), "replacement.pdf", "application/pdf")},
    )
    assert response.status_code == 302
    replacement = resume_service.get_resume_file(conn, owner_id)
    replacement_path = upload_dir / replacement["stored_name"]
    assert replacement["original_name"] == "replacement.pdf"
    assert replacement_path.read_bytes() == replacement_pdf
    assert not first_path.exists()
    assert resume_service.get_resume(conn, owner_id)["body"] == "Existing raw-text resume"
    assert conn.execute(
        "SELECT COUNT(*) FROM resume_files WHERE owner_id = ?", (owner_id,)
    ).fetchone()[0] == 1
    resume_page = client.get("/candidate/resume").get_data(as_text=True)
    assert "CV file (PDF, optional)" in resume_page
    assert "replacement.pdf" in resume_page
    assert "Download your CV" in resume_page
    assert 'enctype="multipart/form-data"' in resume_page

    max_bytes = app.config["MAX_UPLOAD_MB"] * 1024 * 1024
    invalid_uploads = (
        FileStorage(
            stream=io.BytesIO(valid_pdf),
            filename="resume.txt",
            content_type="application/pdf",
        ),
        FileStorage(
            stream=io.BytesIO(valid_pdf),
            filename="resume.pdf",
            content_type="application/octet-stream",
        ),
        FileStorage(
            stream=io.BytesIO(b"not a PDF"),
            filename="resume.pdf",
            content_type="application/pdf",
        ),
        FileStorage(
            stream=io.BytesIO(b"%PDF-" + b"x" * max_bytes),
            filename="oversized.pdf",
            content_type="application/pdf",
        ),
        FileStorage(
            stream=io.BytesIO(b""),
            filename="empty.pdf",
            content_type="application/pdf",
        ),
        FileStorage(
            stream=io.BytesIO(valid_pdf), filename="", content_type="application/pdf"
        ),
    )
    for uploaded in invalid_uploads:
        with pytest.raises(ValidationError) as exc_info:
            resume_service.save_resume_file(conn, owner_id, uploaded)
        assert "file" in exc_info.value.errors
        assert resume_service.get_resume_file(conn, owner_id) == replacement
        assert replacement_path.read_bytes() == replacement_pdf

    owner_download = client.get(f"/candidates/{owner_id}/resume/file")
    assert owner_download.status_code == 200
    assert owner_download.mimetype == "application/pdf"
    assert owner_download.data == replacement_pdf
    owner_download.close()

    login_as(client, other_candidate_id, "candidate")
    assert client.get(f"/candidates/{owner_id}/resume/file").status_code == 403

    login_as(client, employer_id, "employer")
    assert client.get(f"/candidates/{owner_id}/resume/file").status_code == 403

    login_as(client, owner_id, "candidate")
    assert client.get("/candidates/999999/resume/file").status_code == 403

    empty_owner_id = make_candidate(email="cv-empty@example.com", skills=())
    login_as(client, empty_owner_id, "candidate")
    assert client.get(f"/candidates/{empty_owner_id}/resume/file").status_code == 404

    login_as(client, owner_id, "candidate")
    response = csrf_post(client, "/candidate/resume/file/delete", {})
    assert response.status_code == 302
    assert resume_service.get_resume_file(conn, owner_id) is None
    assert not replacement_path.exists()
    login_as(client, owner_id, "candidate")
    assert client.get(f"/candidates/{owner_id}/resume/file").status_code == 404
