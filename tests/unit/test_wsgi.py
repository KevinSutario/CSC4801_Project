"""wsgi entry-point tests (T20).

Importing wsgi must build the app, create the database when missing, and seed the
demo data on a brand-new database, so `docker run` on a fresh clone gives data at
once. The app's Config reads DATABASE/UPLOAD_DIR from the environment at import
time (frozen T01 behaviour), exactly as Docker sets them before the process
starts; so these tests run wsgi in a FRESH subprocess with the env set, which
mirrors the real container start instead of a same-process importlib.reload.
"""

import os
import sqlite3
import subprocess
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _run_wsgi_import(tmp_path):
    """Import wsgi in a fresh interpreter with env set; return the db path."""
    db_path = tmp_path / "keystone.sqlite3"
    env = dict(os.environ)
    env["DATABASE"] = str(db_path)
    env["UPLOAD_DIR"] = str(tmp_path / "uploads")
    env["SECRET_KEY"] = "test"
    # Import wsgi (runs create_app + first-start seed) then exit cleanly.
    result = subprocess.run(
        [sys.executable, "-c", "import wsgi; assert wsgi.app is not None"],
        cwd=_ROOT, env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"wsgi import failed:\n{result.stderr}"
    return db_path


def _counts(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    finally:
        conn.close()
    return users, jobs


def test_import_wsgi_creates_a_seeded_database(tmp_path):
    db_path = _run_wsgi_import(tmp_path)
    assert db_path.exists()
    users, jobs = _counts(db_path)
    assert users == 5  # the five demo accounts
    assert jobs == 3


def test_reimport_does_not_duplicate_seed(tmp_path):
    db_path = _run_wsgi_import(tmp_path)
    _run_wsgi_import(tmp_path)  # second start on an existing database must not re-seed
    users, _ = _counts(db_path)
    assert users == 5
