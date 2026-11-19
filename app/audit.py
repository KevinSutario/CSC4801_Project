"""Audit log. Owned by T02 (frozen afterwards).

Services call ``log_event`` inside their own transaction; it never opens one.
The fixed action list and the table live in docs/plan/03-DATA-MODEL.md.
"""

import sqlite3

from .db import now_iso

# The fixed list of audit actions (docs/plan/03-DATA-MODEL.md, "Audit actions").
ACTIONS: frozenset[str] = frozenset(
    {
        "user.register",
        "user.login",
        "user.login_failed",
        "profile.update",
        "resume.update",
        "company.update",
        "job.create",
        "job.update",
        "job.delete",
        "application.submit",
        "application.status",
        "slot.create",
        "slot.delete",
        "booking.create",
        "booking.conflict",
    }
)

_DETAIL_MAX = 500


def log_event(
    conn: sqlite3.Connection,
    actor_id: int | None,
    action: str,
    object_type: str,
    object_id: int | None,
    detail: str = "",
) -> None:
    """Insert one audit row. Call inside the caller's transaction.

    Raises ValueError for an action not in ACTIONS. ``detail`` is truncated to
    500 characters and must never carry passwords, tokens or file contents.
    """
    if action not in ACTIONS:
        raise ValueError(f"unknown audit action: {action!r}")
    conn.execute(
        "INSERT INTO audit_log (actor_id, action, object_type, object_id, detail, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (actor_id, action, object_type, object_id, (detail or "")[:_DETAIL_MAX], now_iso()),
    )


def list_events(conn: sqlite3.Connection, actor_id: int, limit: int = 100) -> list[dict]:
    """Return this actor's audit rows as dicts, newest first (ties broken by id)."""
    rows = conn.execute(
        "SELECT id, actor_id, action, object_type, object_id, detail, created_at"
        " FROM audit_log WHERE actor_id = ?"
        " ORDER BY created_at DESC, id DESC LIMIT ?",
        (actor_id, limit),
    ).fetchall()
    return [dict(row) for row in rows]
