"""T03 · shared layout and landing page."""

from app.db import transaction


def test_landing_page_has_account_links_and_no_inline_code(client):
    response = client.get("/")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Create account" in body
    assert 'style="' not in body
    assert "<script" not in body.lower()


def test_candidate_visiting_landing_page_is_redirected(client, conn):
    with transaction(conn):
        cursor = conn.execute(
            "INSERT INTO users (email, password_hash, role, display_name, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            ("candidate@example.com", "x", "candidate", "Candidate", "2030-01-01T00:00:00Z"),
        )
    with client.session_transaction() as session:
        session["user_id"] = cursor.lastrowid
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/candidate/"


def test_404_uses_shared_layout_and_keeps_status(client):
    response = client.get("/missing-page")
    body = response.get_data(as_text=True)
    assert response.status_code == 404
    assert 'class="layout"' in body


def test_csrf_field_renders_session_token(app):
    with app.test_request_context("/"):
        from flask import session

        csrf_template = app.jinja_env.from_string(
            '{% from "components/forms.html" import csrf_field %}{{ csrf_field() }}'
        )
        rendered = csrf_template.render()
        assert session["csrf"] in rendered
