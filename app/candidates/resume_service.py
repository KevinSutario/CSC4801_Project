"""Private, plain-text candidate resume persistence."""

import sqlite3

from app import audit
from app.db import now_iso, transaction
from app.errors import Forbidden, NotFound, ValidationError

RESUME_MAX_CHARS = 20000


def get_resume(conn: sqlite3.Connection, owner_id: int) -> dict | None:
    """Return the owner's resume row, or None when no resume has been saved."""
    row = conn.execute(
        "SELECT owner_id, body, updated_at FROM resumes WHERE owner_id = ?",
        (owner_id,),
    ).fetchone()
    return dict(row) if row else None


def save_resume(conn: sqlite3.Connection, owner_id: int, body: str) -> None:
    """Replace the owner's raw-text resume and record the update atomically."""
    body = body.strip()
    if not body or len(body) > RESUME_MAX_CHARS:
        raise ValidationError({"body": f"Enter a resume of 1 to {RESUME_MAX_CHARS} characters."})
    with transaction(conn):
        conn.execute(
            "INSERT INTO resumes (owner_id, body, updated_at) VALUES (?, ?, ?)"
            " ON CONFLICT(owner_id) DO UPDATE SET body = excluded.body,"
            " updated_at = excluded.updated_at",
            (owner_id, body, now_iso()),
        )
        audit.log_event(conn, owner_id, "resume.update", "resume", owner_id)


def get_resume_for_viewer(
    conn: sqlite3.Connection, viewer_id: int, candidate_id: int
) -> dict:
    """Return a resume only to its owner, distinguishing private and missing cases."""
    if viewer_id != candidate_id:
        raise Forbidden()
    resume = get_resume(conn, candidate_id)
    if resume is None:
        raise NotFound()
    return resume
