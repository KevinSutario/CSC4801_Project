"""Interview booking service (FP-SCHED-2). Owned by T16, then T17.

A candidate may book a slot if and only if: they own the application; the slot
belongs to the employer who owns the application's job (slots are employer-owned,
D13, so any future unbooked slot of that employer qualifies); the application
status is interviewing; the slot is in the future and unbooked; and the
application has no booking yet. Any failure raises before the transaction and
writes nothing. T17 adds the concurrent-conflict hardening (Conflict from
inside BEGIN IMMEDIATE and from IntegrityError, booking.conflict audit).
"""

import sqlite3

from app import audit
from app.applications.service import get_own_application
from app.db import now_iso, transaction
from app.errors import Conflict, Forbidden, NotFound


def is_eligible(conn: sqlite3.Connection, candidate_id: int, application_id: int) -> bool:
    """True only if the application is the candidate's, interviewing and unbooked.

    get_own_application raises NotFound if the application is missing and
    Forbidden if it belongs to another candidate.
    """
    application = get_own_application(conn, candidate_id, application_id)
    return application["status"] == "interviewing" and application["booking"] is None


def list_bookable_slots(conn: sqlite3.Connection, candidate_id: int,
                        application_id: int) -> list[dict]:
    """Future, unbooked slots of the employer owning the application's job,
    start ascending. Same ownership errors as is_eligible."""
    application = get_own_application(conn, candidate_id, application_id)
    employer = conn.execute(
        "SELECT c.owner_id FROM jobs AS j JOIN companies AS c ON c.id = j.company_id"
        " WHERE j.id = ?",
        (application["job_id"],),
    ).fetchone()
    rows = conn.execute(
        "SELECT s.id, s.starts_at, s.ends_at, s.created_tz"
        " FROM interview_slots AS s"
        " LEFT JOIN bookings AS b ON b.slot_id = s.id"
        " WHERE s.employer_id = ? AND b.id IS NULL AND s.starts_at > ?"
        " ORDER BY s.starts_at ASC, s.id ASC",
        (employer["owner_id"], now_iso()),
    ).fetchall()
    return [dict(row) for row in rows]


def book_slot(conn: sqlite3.Connection, candidate_id: int, application_id: int,
              slot_id: int) -> int:
    """Book a slot for the application. Returns the booking id.

    NotFound if the application or slot is missing. Forbidden if the application
    is another candidate's, or the status is not interviewing, or the application
    already has a booking, or the slot belongs to another employer, or the slot
    is in the past. Conflict if the slot is already booked (the simple check
    here; T17 re-checks inside BEGIN IMMEDIATE and from IntegrityError). No
    booking row is written on any failure.
    """
    # get_own_application: NotFound if missing, Forbidden if another candidate's.
    application = get_own_application(conn, candidate_id, application_id)

    slot = conn.execute(
        "SELECT id, employer_id, starts_at FROM interview_slots WHERE id = ?",
        (slot_id,),
    ).fetchone()
    if slot is None:
        raise NotFound()

    # The employer who owns the application's job (slots are employer-owned, D13).
    employer = conn.execute(
        "SELECT c.owner_id FROM jobs AS j JOIN companies AS c ON c.id = j.company_id"
        " WHERE j.id = ?",
        (application["job_id"],),
    ).fetchone()

    if application["status"] != "interviewing":
        raise Forbidden()
    if application["booking"] is not None:
        raise Forbidden()
    if employer is None or slot["employer_id"] != employer["owner_id"]:
        raise Forbidden()
    if slot["starts_at"] <= now_iso():
        raise Forbidden()

    # Simple pre-check; T17 hardens this inside BEGIN IMMEDIATE (D14).
    booked = conn.execute(
        "SELECT 1 FROM bookings WHERE slot_id = ?", (slot_id,)
    ).fetchone()
    if booked is not None:
        raise Conflict("Slot already booked")

    with transaction(conn, immediate=True):
        cursor = conn.execute(
            "INSERT INTO bookings (slot_id, application_id, booked_at) VALUES (?, ?, ?)",
            (slot_id, application_id, now_iso()),
        )
        booking_id = cursor.lastrowid
        audit.log_event(conn, candidate_id, "booking.create", "booking", booking_id,
                        f"slot {slot_id}")
    return booking_id
