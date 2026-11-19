"""Shared pytest fixtures. Owned by T01; T04 adds the factory and login fixtures.

Signatures follow docs/plan/07-CONTRACTS.md, section ``tests/conftest.py``.
Factories insert with plain SQL inside ``transaction(conn)`` — they never call a
service module, so lanes stay independent.
"""

import secrets

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.db import get_db, now_iso, transaction
from app.skills import get_or_create_skill_ids

_UNIQUE = {}  # default email -> next suffix; two factory calls never clash


def _unique_email(email: str) -> str:
    """Append a counter to the local part from the second call on."""
    _UNIQUE[email] = _UNIQUE.get(email, 0) + 1
    n = _UNIQUE[email]
    if n == 1:
        return email
    local, _, domain = email.partition("@")
    return f"{local}{n}@{domain}"


def _insert_user(conn, email: str, password: str, role: str, display_name: str) -> int:
    with transaction(conn):
        cursor = conn.execute(
            "INSERT INTO users (email, password_hash, role, display_name, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (email, generate_password_hash(password), role, display_name, now_iso()),
        )
        return cursor.lastrowid


@pytest.fixture()
def app(tmp_path):
    """A fresh app with its own database and upload dir under tmp_path."""
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "UPLOAD_DIR": str(tmp_path / "uploads"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def conn(app):
    with app.app_context():
        yield get_db()


@pytest.fixture()
def make_candidate(conn):
    """Return a factory inserting a candidate user + profile + skills. -> user id."""

    def _make(email="cand@example.com", password="Passw0rd!", name="Mei Lin Tan",
              skills=("python", "sql")) -> int:
        user_id = _insert_user(conn, _unique_email(email), password, "candidate", name)
        with transaction(conn):
            conn.execute(
                "INSERT INTO candidate_profiles (user_id, timezone, updated_at)"
                " VALUES (?, 'UTC', ?)",
                (user_id, now_iso()),
            )
            if skills:
                for skill_id in get_or_create_skill_ids(conn, list(skills)):
                    conn.execute(
                        "INSERT INTO candidate_skills (candidate_id, skill_id)"
                        " VALUES (?, ?)",
                        (user_id, skill_id),
                    )
        return user_id

    return _make


@pytest.fixture()
def make_employer(conn):
    """Return a factory inserting an employer user. -> user id."""

    def _make(email="emp@example.com", password="Passw0rd!", name="Daniel Wong") -> int:
        return _insert_user(conn, _unique_email(email), password, "employer", name)

    return _make


@pytest.fixture()
def make_company(conn):
    """Return a factory inserting a company owned by an employer. -> company id."""

    def _make(employer_id: int, name="Harbourline Logistics") -> int:
        with transaction(conn):
            cursor = conn.execute(
                "INSERT INTO companies (owner_id, name, updated_at) VALUES (?, ?, ?)",
                (employer_id, name, now_iso()),
            )
            return cursor.lastrowid

    return _make


@pytest.fixture()
def make_job(conn):
    """Return a factory inserting a job (auto-creating a company for the employer
    if the employer has none). -> job id"""

    def _make(employer_id: int, title="Data Analyst", skills=("python",), **cols) -> int:
        with transaction(conn):
            company_row = conn.execute(
                "SELECT id FROM companies WHERE owner_id = ?", (employer_id,)
            ).fetchone()
            if company_row is None:
                company_id = conn.execute(
                    "INSERT INTO companies (owner_id, name, updated_at)"
                    " VALUES (?, ?, ?)",
                    (employer_id, "Harbourline Logistics", now_iso()),
                ).lastrowid
            else:
                company_id = company_row["id"]
            cursor = conn.execute(
                "INSERT INTO jobs (company_id, title, description, location,"
                " employment_type, salary_min, salary_max, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    company_id,
                    title,
                    cols.get("description", ""),
                    cols.get("location", ""),
                    cols.get("employment_type", ""),
                    cols.get("salary_min"),
                    cols.get("salary_max"),
                    now_iso(),
                    now_iso(),
                ),
            )
            job_id = cursor.lastrowid
            if skills:
                for skill_id in get_or_create_skill_ids(conn, list(skills)):
                    conn.execute(
                        "INSERT INTO job_skills (job_id, skill_id) VALUES (?, ?)",
                        (job_id, skill_id),
                    )
        return job_id

    return _make


@pytest.fixture()
def make_application(conn):
    """Return a factory inserting an application. -> application id"""

    def _make(candidate_id: int, job_id: int, status="pending") -> int:
        with transaction(conn):
            cursor = conn.execute(
                "INSERT INTO applications (job_id, candidate_id, status, created_at,"
                " updated_at) VALUES (?, ?, ?, ?, ?)",
                (job_id, candidate_id, status, now_iso(), now_iso()),
            )
            return cursor.lastrowid

    return _make


@pytest.fixture()
def make_slot(conn):
    """Return a factory inserting an employer-owned slot (no job_id). -> slot id"""

    def _make(employer_id: int, starts_at="2030-01-07T02:00:00Z",
              ends_at="2030-01-07T02:30:00Z", created_tz="UTC") -> int:
        with transaction(conn):
            cursor = conn.execute(
                "INSERT INTO interview_slots (employer_id, starts_at, ends_at,"
                " created_tz, created_at) VALUES (?, ?, ?, ?, ?)",
                (employer_id, starts_at, ends_at, created_tz, now_iso()),
            )
            return cursor.lastrowid

    return _make


@pytest.fixture()
def make_booking(conn):
    """Return a factory inserting a booking. -> booking id"""

    def _make(application_id: int, slot_id: int) -> int:
        with transaction(conn):
            cursor = conn.execute(
                "INSERT INTO bookings (slot_id, application_id, booked_at)"
                " VALUES (?, ?, ?)",
                (slot_id, application_id, now_iso()),
            )
            return cursor.lastrowid

    return _make


def _session_csrf(client) -> str:
    """The client's session CSRF token; create one with a GET to / if missing.

    The anonymous landing page has no csrf field, so a GET to / may not create
    a token; in that case create one directly, as security.csrf_token() would.
    """
    with client.session_transaction() as sess:
        token = sess.get("csrf")
    if token is None:
        client.get("/")
        with client.session_transaction() as sess:
            token = sess.get("csrf") or secrets.token_urlsafe(32)
            sess["csrf"] = token
    return token


def _csrf_post(client, url: str, data: dict, **kwargs):
    data = dict(data)
    data["csrf_token"] = _session_csrf(client)
    return client.post(url, data=data, **kwargs)


def _login_as(client, user_id: int, role: str) -> None:
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["role"] = role
        sess["csrf"] = secrets.token_urlsafe(32)


@pytest.fixture()
def login_as():
    """Sign a test client in by setting the session directly, plus a csrf token."""
    return _login_as


@pytest.fixture()
def csrf_post():
    """POST with the session CSRF token added to the form data."""
    return _csrf_post


@pytest.fixture()
def login():
    """Sign in through /auth/login (works after T05)."""

    def _login(client, email: str, password: str):
        return _csrf_post(client, "/auth/login", {"email": email, "password": password})

    return _login
