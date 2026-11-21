"""Auth requirement tests (FP-AUTH-1, FP-AUTH-2, FP-SEC-2). Owned by T05.

test_fp_auth_3_authorization_and_missing_object stays a T06 placeholder.
"""

import pytest
from werkzeug.security import check_password_hash

from app.auth import service


def _count_users(conn) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]


def _register_form(client, email="new@example.com", password="Passw0rd!",
                   role="candidate", name="New Person"):
    return client.post(
        "/auth/register",
        data={
            "email": email,
            "password": password,
            "role": role,
            "display_name": name,
            "csrf_token": _token(client),
        },
    )


def _token(client) -> str:
    with client.session_transaction() as sess:
        tok = sess.get("csrf")
        if tok is None:
            tok = "test-token"
            sess["csrf"] = tok
    return tok


def test_fp_auth_1_registration_and_session_lifecycle(client, conn):
    resp = _register_form(client, role="candidate")
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("user_id") is not None

    # logout empties the session
    resp = client.post("/auth/logout", data={"csrf_token": _token(client)})
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert "user_id" not in sess

    # login again, then GET / redirects by role
    resp = client.post(
        "/auth/login",
        data={"email": "new@example.com", "password": "Passw0rd!", "csrf_token": _token(client)},
    )
    assert resp.status_code == 302
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/candidate/")


@pytest.mark.parametrize(
    "email,password,role,name,bad_field",
    [
        ("not-an-email", "Passw0rd!", "candidate", "A Name", "email"),
        ("", "Passw0rd!", "candidate", "A Name", "email"),
        ("ok@example.com", "short", "candidate", "A Name", "password"),
        ("ok@example.com", "x" * 200, "candidate", "A Name", "password"),
        ("ok@example.com", "Passw0rd!", "candidate", "   ", "display_name"),
        ("ok@example.com", "Passw0rd!", "admin", "A Name", "role"),
    ],
)
def test_fp_auth_1_invalid_registration(client, conn, email, password, role, name, bad_field):
    before = _count_users(conn)
    resp = client.post(
        "/auth/register",
        data={"email": email, "password": password, "role": role,
              "display_name": name, "csrf_token": _token(client)},
    )
    assert resp.status_code == 400
    assert _count_users(conn) == before  # no row added


def test_fp_auth_1_invalid_registration_duplicate_email(client, conn):
    _register_form(client, email="dupe@example.com")
    client.post("/auth/logout", data={"csrf_token": _token(client)})  # become a visitor again
    before = _count_users(conn)
    # same email, different case -> still rejected, no new row
    resp = client.post(
        "/auth/register",
        data={"email": "DUPE@example.com", "password": "Passw0rd!", "role": "employer",
              "display_name": "Other", "csrf_token": _token(client)},
    )
    assert resp.status_code == 400
    assert _count_users(conn) == before


def test_fp_auth_2_salted_hash_and_password_verification(conn):
    uid = service.register(conn, "h1@example.com", "Passw0rd!", "candidate", "H One")
    row = conn.execute("SELECT password_hash FROM users WHERE id = ?", (uid,)).fetchone()
    stored = row["password_hash"]
    assert stored != "Passw0rd!"
    assert stored.startswith("scrypt:") or stored.startswith("pbkdf2:")
    assert check_password_hash(stored, "Passw0rd!")

    # same password, different salt -> different hash
    uid2 = service.register(conn, "h2@example.com", "Passw0rd!", "candidate", "H Two")
    row2 = conn.execute("SELECT password_hash FROM users WHERE id = ?", (uid2,)).fetchone()
    assert row2["password_hash"] != stored

    assert service.authenticate(conn, "h1@example.com", "Passw0rd!") is not None
    assert service.authenticate(conn, "h1@example.com", "wrong") is None
    assert service.authenticate(conn, "nobody@example.com", "Passw0rd!") is None
    # the returned dict never carries the hash
    user = service.authenticate(conn, "h1@example.com", "Passw0rd!")
    assert "password_hash" not in user


def test_fp_auth_3_authorization_and_missing_object(
    client, conn, make_candidate, make_employer, make_company, make_job,
    make_application, login_as, csrf_post,
):
    """Readable FP-AUTH-3 summary (full route-by-route sweep is in test_authz_sweep.py)."""
    from app.jobs import service as jobs_service

    emp_a = make_employer(email="a@example.com")
    make_company(emp_a, name="A Co")
    emp_b = make_employer(email="b@example.com")
    make_company(emp_b, name="B Co")
    job_a = jobs_service.create_job(conn, emp_a, "Job A", "Desc", "", "full-time", "", "", "python")
    cand_a = make_candidate(email="ca@example.com")
    cand_b = make_candidate(email="cb@example.com")
    app_a = make_application(cand_a, job_a)

    # employer B editing A's job -> 403 (wrong owner)
    login_as(client, emp_b, "employer")
    r = csrf_post(client, f"/employer/jobs/{job_a}/edit", {
        "title": "x", "description": "y", "location": "", "employment_type": "full-time",
        "salary_min": "", "salary_max": "", "skills": "",
    })
    assert r.status_code == 403

    # candidate B reading A's application -> 403 (wrong owner)
    login_as(client, cand_b, "candidate")
    assert client.get(f"/candidate/applications/{app_a}").status_code == 403

    # candidate opening an employer-only page -> 403 (wrong role)
    assert client.get("/employer/company").status_code == 403

    # employer A, missing job -> 404
    login_as(client, emp_a, "employer")
    assert client.get("/employer/jobs/999999/edit").status_code == 404

    # signed out -> redirect to login (not the content)
    with client.session_transaction() as s:
        s.clear()
    resp = client.get("/candidate/applications")
    assert resp.status_code in (301, 302)


def test_fp_sec_2_sql_metacharacters_stay_bound(conn):
    evil_email = "x');drop--table@example.com"
    evil_name = "Robert'); DELETE FROM users; --"
    uid = service.register(conn, evil_email, "Passw0rd!", "candidate", evil_name)
    # table still exists and holds the row with the literal strings
    row = conn.execute(
        "SELECT email, display_name FROM users WHERE id = ?", (uid,)
    ).fetchone()
    assert row["email"] == evil_email
    assert row["display_name"] == evil_name
    assert service.authenticate(conn, evil_email, "Passw0rd!") is not None


def test_login_open_redirect_is_blocked(client, conn):
    _register_form(client, email="r@example.com")
    client.post("/auth/logout", data={"csrf_token": _token(client)})
    resp = client.post(
        "/auth/login?next=//evil.com",
        data={"email": "r@example.com", "password": "Passw0rd!", "csrf_token": _token(client)},
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    assert "evil.com" not in resp.headers["Location"]


def test_login_safe_next_is_honoured(client, conn):
    _register_form(client, email="r2@example.com")
    client.post("/auth/logout", data={"csrf_token": _token(client)})
    resp = client.post(
        "/auth/login?next=/candidate/profile",
        data={"email": "r2@example.com", "password": "Passw0rd!", "csrf_token": _token(client)},
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/candidate/profile")


def test_sixth_bad_login_is_rate_limited(client, conn):
    _register_form(client, email="rl@example.com")
    client.post("/auth/logout", data={"csrf_token": _token(client)})
    for _ in range(5):
        resp = client.post(
            "/auth/login",
            data={"email": "rl@example.com", "password": "wrong", "csrf_token": _token(client)},
        )
        assert resp.status_code == 400
    resp = client.post(
        "/auth/login",
        data={"email": "rl@example.com", "password": "wrong", "csrf_token": _token(client)},
    )
    assert resp.status_code == 429


def test_logout_get_is_405(client):
    assert client.get("/auth/logout").status_code == 405


def test_logout_without_csrf_is_403(client, conn):
    _register_form(client, email="c@example.com")
    resp = client.post("/auth/logout", data={})  # no csrf_token
    assert resp.status_code == 403


def test_signed_in_user_opening_register_is_redirected(client, conn):
    _register_form(client, email="si@example.com")
    resp = client.get("/auth/register")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_distributed_brute_force_is_blocked_per_email(client, conn):
    """B5: 5 wrong attempts on one email from DIFFERENT IPs must lock it (per-email limit).

    Before the fix the limiter keyed on email|ip, so rotating the IP gave a fresh bucket and the
    6th attempt still returned 400. The per-email key must block it with 429.
    """
    _register_form(client, email="victim@example.com")
    client.post("/auth/logout", data={"csrf_token": _token(client)})
    # five wrong guesses, each from a different source IP
    for i in range(5):
        resp = client.post(
            "/auth/login",
            data={"email": "victim@example.com", "password": "wrong", "csrf_token": _token(client)},
            environ_base={"REMOTE_ADDR": f"10.0.0.{i}"},
        )
        assert resp.status_code == 400
    # a sixth attempt from yet another new IP must be blocked by the per-email limit
    resp = client.post(
        "/auth/login",
        data={"email": "victim@example.com", "password": "wrong", "csrf_token": _token(client)},
        environ_base={"REMOTE_ADDR": "10.0.0.99"},
    )
    assert resp.status_code == 429


def test_rate_limit_is_also_per_ip(client, conn):
    """B5: one IP hammering many different emails must also lock on the per-IP limit."""
    for i in range(5):
        resp = client.post(
            "/auth/login",
            data={"email": f"user{i}@example.com", "password": "wrong",
                  "csrf_token": _token(client)},
            environ_base={"REMOTE_ADDR": "203.0.113.7"},
        )
        assert resp.status_code == 400
    resp = client.post(
        "/auth/login",
        data={"email": "fresh@example.com", "password": "wrong", "csrf_token": _token(client)},
        environ_base={"REMOTE_ADDR": "203.0.113.7"},
    )
    assert resp.status_code == 429
