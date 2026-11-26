"""Database helpers. Owned by T01 (frozen afterwards).

Connections are in autocommit mode (isolation_level=None): every write must
happen inside ``with transaction(conn):`` or it commits immediately.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone

from flask import current_app, g

# Every table in docs/plan/03-DATA-MODEL.md, in schema.sql order.
REQUIRED_TABLES: tuple[str, ...] = (
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
)


def get_db() -> sqlite3.Connection:
    """One connection per request, stored on flask.g."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], isolation_level=None, detect_types=0
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e: BaseException | None = None) -> None:
    """Close the connection if it is open (registered as a teardown)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Run schema.sql on the configured database, exactly as written."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


def missing_tables(db: sqlite3.Connection) -> list[str]:
    """Return the REQUIRED_TABLES that do not exist in this database, in order."""
    present = {
        row[0]
        for row in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    return [table for table in REQUIRED_TABLES if table not in present]


def user_tables(db: sqlite3.Connection) -> list[str]:
    """Return every user-created table (SQLite-internal sqlite_* tables excluded)."""
    return [
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
            " AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def upgrade_interview_slot_notes() -> None:
    """Add notes to initialized databases without changing existing bookings."""
    conn = get_db()
    columns = "SELECT name FROM pragma_table_info('interview_slots')"
    existing = {row["name"] for row in conn.execute(columns)}
    if not existing or "interview_note" in existing or missing_tables(conn):
        return
    with transaction(conn, immediate=True):
        # Another process may have applied the upgrade while we waited for the lock.
        if "interview_note" not in {row["name"] for row in conn.execute(columns)}:
            conn.execute(
                "ALTER TABLE interview_slots ADD COLUMN interview_note TEXT NOT NULL DEFAULT ''"
            )


@contextmanager
def transaction(conn: sqlite3.Connection, immediate: bool = False) -> Iterator[sqlite3.Connection]:
    """BEGIN (or BEGIN IMMEDIATE); COMMIT on success, ROLLBACK and re-raise on error."""
    conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")


def now_iso() -> str:
    """UTC now as "YYYY-MM-DDTHH:MM:SSZ"."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
