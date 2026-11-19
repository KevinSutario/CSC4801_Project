"""Database, schema, and skills tests. Owned by T01."""

import sqlite3

from app import create_app
from app.db import now_iso, transaction
from app.skills import parse_skill_list

EXPECTED_TABLES = {
    "users",
    "candidate_profiles",
    "skills",
    "candidate_skills",
    "resumes",
    "companies",
    "jobs",
    "job_skills",
    "applications",
    "interview_slots",
    "bookings",
    "audit_log",
}


def test_all_tables_exist(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    tables = {row["name"] for row in rows}
    assert EXPECTED_TABLES <= tables


def test_foreign_keys_on(conn):
    value = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert value == 1


def test_transaction_rolls_back_on_error(app, conn):
    with app.app_context():
        with transaction(conn):
            conn.execute("INSERT INTO users (email, password_hash, role, display_name,"
                         " created_at) VALUES (?, ?, ?, ?, ?)",
                         ("rb@example.com", "x", "candidate", "Roll Back", now_iso()))
        before = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        try:
            with transaction(conn):
                conn.execute("INSERT INTO users (email, password_hash, role, display_name,"
                             " created_at) VALUES (?, ?, ?, ?, ?)",
                             ("boom@example.com", "x", "candidate", "Boom", now_iso()))
                raise RuntimeError("force rollback")
        except RuntimeError:
            pass
        after = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    assert before == after == 1


def test_uq_application(conn):
    def _mk(prefix):
        conn.execute("INSERT INTO users (email, password_hash, role, display_name, created_at)"
                     " VALUES (?, 'x', 'candidate', ?, ?)", (f"{prefix}@example.com", prefix,
                                                             now_iso()))
        user_id = conn.execute("SELECT id FROM users WHERE email = ?",
                               (f"{prefix}@example.com",)).fetchone()["id"]
        conn.execute("INSERT INTO companies (owner_id, name, updated_at) VALUES (?, ?, ?)",
                     (user_id, f"{prefix} Co", now_iso()))
        company_id = conn.execute("SELECT id FROM companies WHERE owner_id = ?",
                                  (user_id,)).fetchone()["id"]
        conn.execute("INSERT INTO jobs (company_id, title, description, created_at, updated_at)"
                     " VALUES (?, 'Dev', 'x', ?, ?)", (company_id, now_iso(), now_iso()))
        job_id = conn.execute("SELECT id FROM jobs ORDER BY id DESC").fetchone()["id"]
        return user_id, job_id

    cand_id, job_id = _mk("cand")
    with transaction(conn):
        conn.execute("INSERT INTO applications (job_id, candidate_id, created_at, updated_at)"
                     " VALUES (?, ?, ?, ?)", (job_id, cand_id, now_iso(), now_iso()))
    try:
        with transaction(conn):
            conn.execute("INSERT INTO applications (job_id, candidate_id, created_at, updated_at)"
                         " VALUES (?, ?, ?, ?)", (job_id, cand_id, now_iso(), now_iso()))
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised


def test_unique_slot_booking(conn):
    def _mk(prefix):
        conn.execute("INSERT INTO users (email, password_hash, role, display_name, created_at)"
                     " VALUES (?, 'x', 'employer', ?, ?)", (f"{prefix}@example.com", prefix,
                                                            now_iso()))
        return conn.execute("SELECT id FROM users WHERE email = ?",
                            (f"{prefix}@example.com",)).fetchone()["id"]

    emp_id = _mk("emp")
    cand1 = _mk("cand1")
    cand2 = _mk("cand2")
    conn.execute("INSERT INTO companies (owner_id, name, updated_at) VALUES (?, ?, ?)",
                 (emp_id, "Co", now_iso()))
    company_id = conn.execute("SELECT id FROM companies WHERE owner_id = ?",
                              (emp_id,)).fetchone()["id"]
    conn.execute("INSERT INTO jobs (company_id, title, description, created_at, updated_at)"
                 " VALUES (?, 'Dev', 'x', ?, ?)", (company_id, now_iso(), now_iso()))
    job_id = conn.execute("SELECT id FROM jobs ORDER BY id DESC").fetchone()["id"]
    conn.execute("INSERT INTO interview_slots (employer_id, starts_at, ends_at, created_tz,"
                 " created_at) VALUES (?, ?, ?, 'UTC', ?)",
                 (emp_id, "2030-01-07T02:00:00Z", "2030-01-07T02:30:00Z", now_iso()))
    slot_id = conn.execute("SELECT id FROM interview_slots").fetchone()["id"]

    def _apply(cand_id):
        with transaction(conn):
            conn.execute("INSERT INTO applications (job_id, candidate_id, created_at, updated_at)"
                         " VALUES (?, ?, ?, ?)", (job_id, cand_id, now_iso(), now_iso()))
            return conn.execute("SELECT id FROM applications ORDER BY id DESC").fetchone()["id"]

    app1 = _apply(cand1)
    app2 = _apply(cand2)
    with transaction(conn):
        conn.execute("INSERT INTO bookings (slot_id, application_id, booked_at)"
                     " VALUES (?, ?, ?)", (slot_id, app1, now_iso()))
    # same slot, another application
    try:
        with transaction(conn):
            conn.execute("INSERT INTO bookings (slot_id, application_id, booked_at)"
                         " VALUES (?, ?, ?)", (slot_id, app2, now_iso()))
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised


def test_uq_booking_application(conn):
    def _mk(role, prefix):
        conn.execute("INSERT INTO users (email, password_hash, role, display_name, created_at)"
                     " VALUES (?, 'x', ?, ?, ?)", (f"{prefix}@example.com", role, prefix,
                                                    now_iso()))
        return conn.execute("SELECT id FROM users WHERE email = ?",
                            (f"{prefix}@example.com",)).fetchone()["id"]

    emp_id = _mk("employer", "emp")
    cand_id = _mk("candidate", "cand")
    conn.execute("INSERT INTO companies (owner_id, name, updated_at) VALUES (?, ?, ?)",
                 (emp_id, "Co", now_iso()))
    company_id = conn.execute("SELECT id FROM companies WHERE owner_id = ?",
                              (emp_id,)).fetchone()["id"]
    conn.execute("INSERT INTO jobs (company_id, title, description, created_at, updated_at)"
                 " VALUES (?, 'Dev', 'x', ?, ?)", (company_id, now_iso(), now_iso()))
    job_id = conn.execute("SELECT id FROM jobs ORDER BY id DESC").fetchone()["id"]
    conn.execute("INSERT INTO applications (job_id, candidate_id, created_at, updated_at)"
                 " VALUES (?, ?, ?, ?)", (job_id, cand_id, now_iso(), now_iso()))
    application_id = conn.execute("SELECT id FROM applications ORDER BY id DESC").fetchone()["id"]
    for i in (1, 2):
        conn.execute("INSERT INTO interview_slots (employer_id, starts_at, ends_at, created_tz,"
                     " created_at) VALUES (?, ?, ?, 'UTC', ?)",
                     (emp_id, f"2030-01-0{i}T02:00:00Z", f"2030-01-0{i}T02:30:00Z", now_iso()))
    slot1, slot2 = [row["id"] for row in
                    conn.execute("SELECT id FROM interview_slots ORDER BY id").fetchall()]
    with transaction(conn):
        conn.execute("INSERT INTO bookings (slot_id, application_id, booked_at)"
                     " VALUES (?, ?, ?)", (slot1, application_id, now_iso()))
    try:
        with transaction(conn):
            conn.execute("INSERT INTO bookings (slot_id, application_id, booked_at)"
                         " VALUES (?, ?, ?)", (slot2, application_id, now_iso()))
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised


def test_now_iso_format():
    import re

    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", now_iso())


def test_parse_skill_list():
    assert parse_skill_list(" Python, sql,PYTHON ,, ") == ["python", "sql"]


def test_unknown_route_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404


_SEEN_DATABASES: set[str] = set()


def test_fp_sec_4_tests_use_isolated_database(app, tmp_path):
    database = str(app.config["DATABASE"])
    assert str(tmp_path) in database
    # each test gets its own database: this path was never seen in an earlier test
    assert database not in _SEEN_DATABASES
    _SEEN_DATABASES.add(database)


def test_init_db_fresh_and_repeat(tmp_path):
    """A brand-new database initialises, and running init-db again still succeeds."""
    db_path = str(tmp_path / "fresh.sqlite3")
    app1 = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path,
                       "UPLOAD_DIR": str(tmp_path / "uploads")})
    # create_app just auto-initialised the missing database file; the CLI must
    # therefore succeed on the already-initialised database, not raise
    # "table users already exists".
    result = app1.test_cli_runner().invoke(args=["init-db"])
    assert result.exit_code == 0
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert EXPECTED_TABLES <= tables


def test_init_db_empty_existing_file(tmp_path):
    """An existing but empty database file (no users table) initialises."""
    db_path = str(tmp_path / "empty.sqlite3")
    open(db_path, "w").close()  # exists, but zero tables
    app1 = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path,
                       "UPLOAD_DIR": str(tmp_path / "uploads")})
    result = app1.test_cli_runner().invoke(args=["init-db"])
    assert result.exit_code == 0
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert EXPECTED_TABLES <= tables


def test_init_db_partial_schema_is_rejected(tmp_path):
    """A half-built database (users only) must fail loudly, list the missing
    tables, and leave the database untouched."""
    db_path = str(tmp_path / "partial.sqlite3")
    conn = sqlite3.connect(db_path)
    conn.executescript("CREATE TABLE users (\n"
                       "  id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE COLLATE NOCASE,\n"
                       "  password_hash TEXT NOT NULL,\n"
                       "  role TEXT NOT NULL CHECK (role IN ('candidate', 'employer')),\n"
                       "  display_name TEXT NOT NULL, created_at TEXT NOT NULL\n"
                       ");")
    conn.commit()
    conn.close()

    app1 = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path,
                       "UPLOAD_DIR": str(tmp_path / "uploads")})
    result = app1.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code != 0
    missing = EXPECTED_TABLES - {"users"}
    for table in sorted(missing):
        assert table in result.output
    # the database was not modified: still exactly one table (users)
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert tables == {"users"}


def test_init_db_jobs_only_without_users_is_rejected(tmp_path):
    """A database holding only a jobs table (no users) must also be refused:
    running schema.sql would crash on the existing jobs table. The CLI must
    report the missing tables and leave the database untouched."""
    db_path = str(tmp_path / "jobs_only.sqlite3")
    conn = sqlite3.connect(db_path)
    conn.executescript("CREATE TABLE jobs (\n"
                       "  id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL,\n"
                       "  title TEXT NOT NULL, description TEXT NOT NULL,\n"
                       "  created_at TEXT NOT NULL, updated_at TEXT NOT NULL\n"
                       ");")
    conn.commit()
    conn.close()

    app1 = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path,
                       "UPLOAD_DIR": str(tmp_path / "uploads")})
    result = app1.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code != 0
    missing = EXPECTED_TABLES - {"jobs"}
    for table in sorted(missing):
        assert table in result.output
    # the database was not modified: still exactly one table (jobs)
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert tables == {"jobs"}


def test_init_db_legacy_table_only_is_rejected(tmp_path):
    """A database holding only a non-schema table (legacy_data) must be refused:
    it is not an empty database, and running schema.sql would silently create
    the app tables alongside unknown data. The CLI must report the missing
    tables and leave the database untouched."""
    db_path = str(tmp_path / "legacy.sqlite3")
    conn = sqlite3.connect(db_path)
    conn.executescript("CREATE TABLE legacy_data (\n"
                       "  id INTEGER PRIMARY KEY, note TEXT NOT NULL\n"
                       ");")
    conn.commit()
    conn.close()

    app1 = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": db_path,
                       "UPLOAD_DIR": str(tmp_path / "uploads")})
    result = app1.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code != 0
    for table in sorted(EXPECTED_TABLES):
        assert table in result.output
    # the database was not modified: still exactly one table (legacy_data)
    conn = sqlite3.connect(db_path)
    tables = {row[0] for row in
              conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert tables == {"legacy_data"}
