"""T02 · security module: CSRF, headers, safe-redirect, rate limit, load_user.

No throwaway blueprint is registered (card rule). Hooks are exercised through the
real before/after_request handlers using the test client and app.test_request_context.
"""

import pytest

from app import security
from app.db import get_db, transaction


def test_post_without_csrf_token_is_403(client):
    # csrf_protect runs in before_request, before routing, so any POST without a
    # token is rejected even though no POST route exists.
    resp = client.post("/", data={})
    assert resp.status_code == 403


def test_post_with_correct_csrf_token_is_not_403(client):
    with client.session_transaction() as sess:
        sess["csrf"] = "known-token"
    resp = client.post("/", data={"csrf_token": "known-token"})
    # Passes CSRF; no POST route for "/", so routing gives 404 (not 403).
    assert resp.status_code != 403


def test_post_with_wrong_csrf_token_is_403(client):
    with client.session_transaction() as sess:
        sess["csrf"] = "right"
    resp = client.post("/", data={"csrf_token": "wrong"})
    assert resp.status_code == 403


def test_security_headers_present_on_404(client):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert "frame-ancestors 'none'" in resp.headers["Content-Security-Policy"]
    assert resp.headers["Referrer-Policy"] == "same-origin"


@pytest.mark.parametrize(
    "target,expected",
    [
        ("/candidate/", True),
        ("/", True),
        ("//evil.com", False),
        ("http://evil.com", False),
        ("https://evil.com", False),
        ("\\\\evil", False),
        ("/path\\with-backslash", False),
        ("", False),
        (None, False),
        ("relative/path", False),
    ],
)
def test_is_safe_next(target, expected):
    assert security.is_safe_next(target) is expected


def test_rate_limit_blocks_after_five_failures(app):
    key = security.login_key("Cand@Example.com ", "1.2.3.4")
    with app.app_context():
        assert security.is_login_blocked(key) is False
        for _ in range(5):
            security.record_failed_login(key)
        assert security.is_login_blocked(key) is True
        # A different key is unaffected.
        assert security.is_login_blocked(security.login_key("other@x.com", "9.9.9.9")) is False
        security.reset_login_failures(key)
        assert security.is_login_blocked(key) is False


def test_login_key_normalises_email():
    assert security.login_key("  User@Example.COM ", "1.1.1.1") == "user@example.com|1.1.1.1"


def test_load_user_clears_session_when_user_missing(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 99999  # no such user
    client.get("/does-not-exist")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_load_user_sets_g_user_for_real_user(app):
    with app.app_context():
        db = get_db()
        with transaction(db):
            db.execute(
                "INSERT INTO users (email, password_hash, role, display_name, created_at)"
                " VALUES (?, ?, ?, ?, ?)",
                ("me@example.com", "x", "candidate", "Me", "2030-01-01T00:00:00Z"),
            )
        uid = db.execute(
            "SELECT id FROM users WHERE email = ?", ("me@example.com",)
        ).fetchone()["id"]

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = uid
    # Drive one request through load_user, then read g.user inside a request context.
    with app.test_request_context("/"):
        from flask import session as flask_session

        flask_session["user_id"] = uid
        security.load_user()
        from flask import g

        assert g.user is not None
        assert g.user["id"] == uid
        assert g.user["email"] == "me@example.com"
        assert g.user["role"] == "candidate"
        assert g.user["display_name"] == "Me"


def test_csrf_token_is_stable_within_session_and_rotates(app):
    with app.test_request_context("/"):
        from flask import session as flask_session

        t1 = security.csrf_token()
        t2 = security.csrf_token()
        assert t1 == t2  # stable once created
        assert flask_session["csrf"] == t1
        security.rotate_csrf()
        t3 = security.csrf_token()
        assert t3 != t1  # rotated
